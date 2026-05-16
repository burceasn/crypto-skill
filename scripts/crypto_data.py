"""
Crypto Data API Module

Provides a collection of functions for fetching cryptocurrency market data from OKX and CoinMarketCap.

1) get_okx_candles(inst_id, bar="1H", limit=100) -> DataFrame
2) get_fear_greed_index(days=7) -> DataFrame
3) get_okx_funding_rate(inst_id, limit=100) -> DataFrame
4) get_okx_open_interest(inst_id, period="1H", limit=100) -> DataFrame
5) get_long_short_ratio(ccy, period="1H", limit=100) -> DataFrame
6) get_okx_liquidation(inst_id, state="filled", limit=100) -> DataFrame
7) get_top_trader_long_short_position_ratio(inst_id, period="5m", begin=None, end=None, limit=100) -> DataFrame
8) get_option_open_interest_volume_ratio(ccy, period="8H") -> DataFrame
"""

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import pandas as pd
import time
import logging
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

# ==============================================================================
# Constants & Session
# ==============================================================================
DEFAULT_HEADERS = {"User-Agent": "Mozilla/5.0"}
DEFAULT_TIMEOUT = 10

_retry_strategy = Retry(
    total=3,
    backoff_factor=0.5,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET"],
)
_adapter = HTTPAdapter(max_retries=_retry_strategy)

_session = requests.Session()
_session.headers.update(DEFAULT_HEADERS)
_session.mount("https://", _adapter)
_session.mount("http://", _adapter)


def _handle_request_error(error: Exception) -> None:
    """Handle request exceptions uniformly and print error messages."""
    if isinstance(error, requests.exceptions.ReadTimeout):
        logger.info(
            "Error: Read timeout. Network congestion or server blocking possible."
        )
    elif isinstance(error, requests.exceptions.SSLError):
        logger.info("Error: SSL handshake failed.")
    else:
        logger.info(f"Error occurred: {error}")


def _okx_get(
    url: str,
    params: dict,
    columns: Optional[list] = None,
    timeout: int = DEFAULT_TIMEOUT,
    headers: Optional[dict] = None,
) -> Optional[list]:
    """
    Common OKX API GET request pattern using shared session with retry.

    Returns the raw data list on success, or None on failure.
    Handles: request → raise_for_status → check code=="0" → extract data.
    """
    try:
        resp = _session.get(url, params=params, headers=headers, timeout=timeout)
        resp.raise_for_status()
        body = resp.json()
        if body.get("code") != "0":
            logger.info("OKX API %s returned non-zero code: %s", url, body.get("code"))
            return None
        return body.get("data", [])
    except Exception as e:
        _handle_request_error(e)
        return None


def get_okx_candles(
    inst_id: str, bar: str = "1H", limit: int = 100
) -> Optional[pd.DataFrame]:
    """Get K-line data for OKX trading pairs."""
    logger.info("Fetching OKX candles: inst_id=%s bar=%s limit=%d", inst_id, bar, limit)
    candles = _okx_get(
        "https://www.okx.com/api/v5/market/candles",
        {"instId": inst_id, "bar": bar, "limit": limit},
    )
    if candles is None:
        return None
    df = pd.DataFrame(
        candles,
        columns=[
            "ts", "open", "high", "low", "close",
            "vol", "volCcy", "volCcyQuote", "confirm",
        ],
    )
    df["datetime"] = pd.to_datetime(pd.to_numeric(df["ts"]), unit="ms")
    df = df[["datetime", "open", "high", "low", "close", "vol"]]
    for col in ["open", "high", "low", "close", "vol"]:
        df[col] = pd.to_numeric(df[col])
    df = df.sort_values("datetime").reset_index(drop=True)
    return df


def get_fear_greed_index(days: int = 7) -> Optional[pd.DataFrame]:
    """Get Fear & Greed Index historical data (alternative.me)."""
    url = "https://api.alternative.me/fng/"
    params = {"limit": days}
    try:
        logger.info("Fetching Fear & Greed index: days=%d", days)
        resp = _session.get(url, params=params, timeout=DEFAULT_TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
        if data.get("metadata", {}).get("error"):
            logger.info("Fear & Greed API error in response metadata")
            return None
        if data.get("data"):
            df = pd.DataFrame(data["data"])
            df["timestamp"] = pd.to_numeric(df["timestamp"], errors="coerce")
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s", utc=True)
            df["date"] = df["timestamp"].dt.strftime("%Y-%m-%d")
            df["value"] = pd.to_numeric(df["value"], errors="coerce")
            df = df[["date", "value", "value_classification"]]
            return df
        return None
    except Exception as e:
        _handle_request_error(e)
        return None


def get_okx_funding_rate(inst_id: str, limit: int = 100) -> Optional[pd.DataFrame]:
    """Get OKX perpetual contract funding rate history and current rate."""
    logger.info("Fetching OKX funding rate: inst_id=%s limit=%d", inst_id, limit)
    hist_data = _okx_get(
        "https://www.okx.com/api/v5/public/funding-rate-history",
        {"instId": inst_id, "limit": limit},
    )
    if hist_data is None:
        return None
    curr_data = _okx_get(
        "https://www.okx.com/api/v5/public/funding-rate",
        {"instId": inst_id},
    )
    if curr_data is None:
        return None
    df_hist = pd.DataFrame(hist_data)
    df_hist = df_hist[["fundingTime", "fundingRate", "realizedRate"]]
    df_hist["type"] = "Settled"
    curr_record = curr_data[0]
    row_0 = {
        "fundingTime": curr_record["fundingTime"],
        "fundingRate": curr_record["fundingRate"],
        "realizedRate": None,
        "type": "Current/Predicted",
    }
    df_curr = pd.DataFrame([row_0])
    df_final = pd.concat([df_curr, df_hist], axis=0, ignore_index=True)
    df_final["datetime"] = pd.to_datetime(
        pd.to_numeric(df_final["fundingTime"]), unit="ms"
    )
    df_final["fundingRate"] = pd.to_numeric(df_final["fundingRate"])
    df_final["realizedRate"] = pd.to_numeric(df_final["realizedRate"])
    df_final = df_final[["datetime", "fundingRate", "realizedRate", "type"]]
    return df_final


def get_okx_open_interest(
    inst_id: str, period: str = "1H", limit: int = 100
) -> Optional[pd.DataFrame]:
    """Get OKX Open Interest (including USD value)."""
    timeout_seconds = 30
    logger.info(
        "Fetching OKX open interest: inst_id=%s, period=%s, limit=%d",
        inst_id, period, limit,
    )
    hist_data = _okx_get(
        "https://www.okx.com/api/v5/rubik/stat/contracts/open-interest-history",
        {"instId": inst_id, "period": period, "limit": limit},
        headers=DEFAULT_HEADERS,
        timeout=timeout_seconds,
    )
    if hist_data is None:
        return None
    curr_data = _okx_get(
        "https://www.okx.com/api/v5/public/open-interest",
        {"instId": inst_id},
        headers=DEFAULT_HEADERS,
        timeout=timeout_seconds,
    )
    if curr_data is None:
        return None
    price_data = _okx_get(
        "https://www.okx.com/api/v5/public/mark-price",
        {"instId": inst_id},
        headers=DEFAULT_HEADERS,
        timeout=timeout_seconds,
    )
    if price_data is None:
        return None
    df_hist = pd.DataFrame(hist_data, columns=["ts", "oi", "oiCcy", "oiUsd"])
    df_hist = df_hist[["ts", "oiCcy", "oiUsd"]]
    df_hist["type"] = "History"
    current_oi_ccy = float(curr_data[0]["oiCcy"])
    current_price = float(price_data[0]["markPx"])
    current_oi_usd = current_oi_ccy * current_price
    row_0 = {
        "ts": curr_data[0]["ts"],
        "oiCcy": curr_data[0]["oiCcy"],
        "oiUsd": current_oi_usd,
        "type": "Current (Real-time)",
    }
    df_curr = pd.DataFrame([row_0])
    df_final = pd.concat([df_curr, df_hist], axis=0, ignore_index=True)
    df_final["datetime"] = pd.to_datetime(pd.to_numeric(df_final["ts"]), unit="ms")
    df_final["oiCcy"] = pd.to_numeric(df_final["oiCcy"])
    df_final["oiUsd"] = pd.to_numeric(df_final["oiUsd"])
    df_final = df_final[["datetime", "oiCcy", "oiUsd", "type"]]
    return df_final


def get_long_short_ratio(
    ccy: str, period: str = "1H", limit: int = 100
) -> Optional[pd.DataFrame]:
    """Get OKX elite trader long/short account ratio. Simplified implementation, single request max 100 records."""
    logger.info(
        "Fetching OKX long/short ratio: ccy=%s period=%s limit=%d", ccy, period, limit
    )
    records = _okx_get(
        "https://www.okx.com/api/v5/rubik/stat/contracts/long-short-account-ratio",
        {"ccy": ccy, "period": period, "limit": limit},
    )
    if not records:
        return None
    df = pd.DataFrame(records, columns=["ts", "longShortPosRatio"])
    df["datetime"] = pd.to_datetime(pd.to_numeric(df["ts"]), unit="ms")
    df["longShortPosRatio"] = pd.to_numeric(df["longShortPosRatio"])
    df = df[["datetime", "longShortPosRatio"]]
    df = df.sort_values("datetime", ascending=False).reset_index(drop=True)
    if len(df) > limit:
        df = df.head(limit)
    return df


def get_okx_liquidation(
    inst_id: str, state: str = "filled", limit: int = 100
) -> Optional[pd.DataFrame]:
    """Get OKX perpetual contract liquidation order data."""
    logger.info(
        "Fetching OKX liquidation: inst_id=%s, state=%s, limit=%d",
        inst_id, state, limit,
    )
    if inst_id.endswith("-SWAP"):
        inst_family = inst_id[:-5]
    else:
        inst_family = inst_id
    data_list = _okx_get(
        "https://www.okx.com/api/v5/public/liquidation-orders",
        {"instType": "SWAP", "instFamily": inst_family, "state": state, "limit": limit},
    )
    if not data_list:
        return None
    all_details = []
    for item in data_list:
        for detail in item.get("details", []):
            all_details.append(
                {
                    "ts": detail["ts"],
                    "side": detail["side"],
                    "bkPx": detail["bkPx"],
                    "sz": detail["sz"],
                }
            )
    if not all_details:
        return None
    df = pd.DataFrame(all_details)
    df["datetime"] = pd.to_datetime(pd.to_numeric(df["ts"]), unit="ms")
    df["bkPx"] = pd.to_numeric(df["bkPx"])
    df["sz"] = pd.to_numeric(df["sz"])
    df = df[["datetime", "side", "bkPx", "sz"]]
    df = df.sort_values("datetime", ascending=False).reset_index(drop=True)
    return df


def get_top_trader_long_short_position_ratio(
    inst_id: str,
    period: str = "5m",
    begin: Optional[str] = None,
    end: Optional[str] = None,
    limit: int = 100,
) -> Optional[pd.DataFrame]:
    """Get OKX elite trader long/short position ratio. Simplified implementation."""
    logger.info(
        "Fetching OKX top trader long/short ratio: inst_id=%s period=%s",
        inst_id, period,
    )
    params: dict = {"instId": inst_id, "period": period, "limit": limit}
    if begin:
        params["begin"] = begin
    if end:
        params["end"] = end
    records = _okx_get(
        "https://www.okx.com/api/v5/rubik/stat/contracts/long-short-position-ratio-contract-top-trader",
        params,
    )
    if not records:
        return None
    df = pd.DataFrame(records, columns=["ts", "longShortPosRatio"])
    df["datetime"] = pd.to_datetime(pd.to_numeric(df["ts"]), unit="ms")
    df["longShortPosRatio"] = pd.to_numeric(df["longShortPosRatio"])
    df = df[["datetime", "longShortPosRatio"]]
    df = df.sort_values("datetime", ascending=False).reset_index(drop=True)
    return df


def get_option_open_interest_volume_ratio(
    ccy: str, period: str = "8H", limit: int = 100
) -> Optional[pd.DataFrame]:
    """Get call/put option open interest ratio and volume ratio."""
    logger.info(
        "Fetching OKX option OI/volume ratio: ccy=%s period=%s limit=%d",
        ccy, period, limit,
    )
    records = _okx_get(
        "https://www.okx.com/api/v5/rubik/stat/option/open-interest-volume-ratio",
        {"ccy": ccy, "period": period},
    )
    if not records:
        return None
    df = pd.DataFrame(records, columns=["ts", "oiRatio", "volRatio"])
    df["datetime"] = pd.to_datetime(pd.to_numeric(df["ts"]), unit="ms")
    df["oiRatio"] = pd.to_numeric(df["oiRatio"])
    df["volRatio"] = pd.to_numeric(df["volRatio"])
    df = df[["datetime", "oiRatio", "volRatio"]]
    df = df.sort_values("datetime", ascending=False).reset_index(drop=True)
    if len(df) > limit:
        df = df.head(limit)
    return df


def save_to_csv(df: pd.DataFrame, filename: str) -> None:
    if df is not None:
        df.to_csv(filename, index=False)
        logger.info(f"Data saved to {filename}")
    else:
        logger.info("No data to save to CSV.")


if __name__ == "__main__":
    logger.info(
        "Crypto data module test run. You can import and call functions from other modules."
    )
