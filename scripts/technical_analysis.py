#!/usr/bin/env python3
"""
Technical analysis module - pure computation, no network access.

Data must be provided externally (e.g., from cli.py or other callers).
This module does NOT fetch data from any API.
"""

import logging
from typing import Dict, List, Optional
import pandas as pd
import numpy as np

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


class TechnicalAnalysis:
    # MACD preset parameter sets
    MACD_PRESETS = {
        "default": (12, 26, 9),
        "fast": (5, 13, 8),
    }

    def __init__(
        self,
        kline_data: List[Dict],
        inst_id: Optional[str] = None,
        bar: Optional[str] = None,
        macd_fast: int = 12,
        macd_slow: int = 26,
        macd_signal: int = 9,
    ):
        """
        Initialize with pre-fetched kline data.

        Args:
            kline_data:  List of candle dicts, must contain keys:
                         datetime, open, high, low, close, vol
            inst_id:     Optional label for reference (no network use)
            bar:         Optional label for reference (no network use)
            macd_fast:   MACD fast EMA period (default: 12)
            macd_slow:   MACD slow EMA period (default: 26)
            macd_signal: MACD signal EMA period (default: 9)
        """
        self.inst_id = inst_id
        self.bar = bar
        self.macd_fast = macd_fast
        self.macd_slow = macd_slow
        self.macd_signal = macd_signal
        self.data = pd.DataFrame(kline_data)
        if not self.data.empty:
            self._process_dataframe()

    def _process_dataframe(self):
        if self.data is not None and not self.data.empty:
            if "datetime" in self.data.columns:
                self.data["datetime"] = pd.to_datetime(self.data["datetime"])
            self.data = (
                self.data.sort_values("datetime").reset_index(drop=True)
                if "datetime" in self.data.columns
                else self.data
            )
            for col in ["open", "high", "low", "close", "vol"]:
                if col in self.data.columns:
                    self.data[col] = pd.to_numeric(self.data[col], errors="coerce")

    def get_all_indicators(self) -> pd.DataFrame:
        if self.data is None or self.data.empty:
            return pd.DataFrame()
        df = self.data.copy()
        close = df["close"] if "close" in df else pd.Series(dtype=float)
        indicators = pd.DataFrame(index=df.index)
        indicators["datetime"] = df.get("datetime")
        indicators["open"] = df.get("open")
        indicators["high"] = df.get("high")
        indicators["low"] = df.get("low")
        indicators["close"] = close
        vol = df.get("vol")
        indicators["volume"] = vol
        # Simple indicators
        indicators["ma5"] = close.rolling(window=5).mean()
        indicators["ma10"] = close.rolling(window=10).mean()
        delta = close.diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.ewm(alpha=1 / 14, adjust=False).mean()
        avg_loss = loss.ewm(alpha=1 / 14, adjust=False).mean()
        rs = avg_gain / avg_loss
        indicators["rsi14"] = 100 - (100 / (1 + rs))
        ema_fast = close.ewm(span=self.macd_fast, adjust=False).mean()
        ema_slow = close.ewm(span=self.macd_slow, adjust=False).mean()
        dif = ema_fast - ema_slow
        dea = dif.ewm(span=self.macd_signal, adjust=False).mean()
        indicators["macd_dif"] = dif
        indicators["macd_dea"] = dea
        indicators["macd_hist"] = (dif - dea) * 2

        high = df["high"] if "high" in df else pd.Series(dtype=float)
        low = df["low"] if "low" in df else pd.Series(dtype=float)

        # --- ATR (14) + ATR% ---
        tr1 = high - low
        tr2 = (high - close.shift(1)).abs()
        tr3 = (low - close.shift(1)).abs()
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        atr14 = tr.ewm(alpha=1 / 14, adjust=False).mean()
        indicators["atr14"] = atr14
        indicators["atr14_pct"] = atr14 / close * 100

        # --- ADX / +DI / -DI (14) ---
        up_move = high - high.shift(1)
        down_move = low.shift(1) - low
        plus_dm = pd.Series(np.where((up_move > down_move) & (up_move > 0), up_move, 0.0), index=df.index)
        minus_dm = pd.Series(np.where((down_move > up_move) & (down_move > 0), down_move, 0.0), index=df.index)
        smooth_plus_dm = plus_dm.ewm(alpha=1 / 14, adjust=False).mean()
        smooth_minus_dm = minus_dm.ewm(alpha=1 / 14, adjust=False).mean()
        plus_di = 100 * smooth_plus_dm / atr14
        minus_di = 100 * smooth_minus_dm / atr14
        dx = 100 * (plus_di - minus_di).abs() / (plus_di + minus_di)
        adx = dx.ewm(alpha=1 / 14, adjust=False).mean()
        indicators["plus_di"] = plus_di
        indicators["minus_di"] = minus_di
        indicators["adx"] = adx

        # --- Bollinger Bands (20, 2) ---
        bb_mid = close.rolling(window=20).mean()
        bb_std = close.rolling(window=20).std()
        bb_upper = bb_mid + 2 * bb_std
        bb_lower = bb_mid - 2 * bb_std
        indicators["bb_upper"] = bb_upper
        indicators["bb_mid"] = bb_mid
        indicators["bb_lower"] = bb_lower
        indicators["bb_pctb"] = (close - bb_lower) / (bb_upper - bb_lower)
        indicators["bb_bandwidth"] = (bb_upper - bb_lower) / bb_mid * 100

        # --- KDJ (9, 3, 3) ---
        low_9 = low.rolling(window=9).min()
        high_9 = high.rolling(window=9).max()
        rsv = (close - low_9) / (high_9 - low_9) * 100
        k = rsv.ewm(com=2, adjust=False).mean()
        d = k.ewm(com=2, adjust=False).mean()
        j = 3 * k - 2 * d
        indicators["kdj_k"] = k
        indicators["kdj_d"] = d
        indicators["kdj_j"] = j

        # --- OBV ---
        vol_series = vol if vol is not None else pd.Series(0, index=df.index)
        direction = pd.Series(np.where(close > close.shift(1), 1, np.where(close < close.shift(1), -1, 0)), index=df.index)
        indicators["obv"] = (vol_series * direction).cumsum()

        return indicators

    def calculate_fibonacci_retracement(
        self, high: float, low: float
    ) -> Dict[str, float]:
        """Calculate Fibonacci retracement levels."""
        diff = high - low
        levels = {
            "0.0": low,
            "0.236": low + diff * 0.236,
            "0.382": low + diff * 0.382,
            "0.5": low + diff * 0.5,
            "0.618": low + diff * 0.618,
            "0.786": low + diff * 0.786,
            "1.0": high,
        }
        return levels

    def find_support_resistance(
        self, window: int = 5
    ) -> tuple[list[float], list[float]]:
        """Find support and resistance levels using local extrema."""
        if self.data is None or self.data.empty:
            return [], []

        highs = self.data["high"].values
        lows = self.data["low"].values

        supports = []
        resistances = []

        for i in range(window, len(highs) - window):
            # Check for local high (resistance)
            is_high = True
            for j in range(-window, window + 1):
                if j != 0 and highs[i] < highs[i + j]:
                    is_high = False
                    break
            if is_high:
                resistances.append(float(highs[i]))

            # Check for local low (support)
            is_low = True
            for j in range(-window, window + 1):
                if j != 0 and lows[i] > lows[i + j]:
                    is_low = False
                    break
            if is_low:
                supports.append(float(lows[i]))

        return supports, resistances


def _analyze_single_asset(ta: TechnicalAnalysis, asset: str) -> Optional[Dict]:
    """Analyze a single asset and return summary (indicators + metadata)."""
    if ta.data is None or ta.data.empty:
        return None
    indicators = ta.get_all_indicators().iloc[-1].to_dict()
    data_summary = {"total_candles": len(ta.data)}
    return {"asset": asset, "indicators": indicators, "data_summary": data_summary}
