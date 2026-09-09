# Crypto Technical Analysis Skill

[![English](https://img.shields.io/badge/lang-English-blue.svg)](README.md) [![中文](https://img.shields.io/badge/lang-中文-red.svg)](README_CN.md)

> Python-based cryptocurrency market data and technical analysis toolkit

An AI-ready skill that provides real-time crypto market data from OKX exchange and comprehensive technical indicator calculations. Designed for seamless command-line usage.

## Features

### Market Data Commands

| Command | Description |
|---------|-------------|
| `candles` | K-line/OHLCV data (1m to 1W timeframes) |
| `funding-rate` | Perpetual contract funding rates |
| `open-interest` | Open interest with USD valuation |
| `long-short-ratio` | Account long/short ratio |
| `top-trader-ratio` | Top 5% traders' long/short position ratio |
| `option-ratio` | Option call/put OI and volume ratio |
| `fear-greed` | Fear and Greed Index from alternative.me |
| `liquidation` | Price-bucket liquidation summary (aggregated by $500 price intervals) |

### Technical Analysis Commands

| Command | Description |
|---------|-------------|
| `indicators` | Complete technical indicators (MA, RSI, MACD, KDJ, etc.) with MACD presets |
| `summary` | Structured summary: price plus trend/momentum/volatility categories |
| `support-resistance` | Support/resistance levels and Fibonacci retracement |

### Technical Indicators

| Category | Indicators |
|----------|------------|
| **Trend** | MA (5/10/20/50/100), EMA (12/26), DMI/ADX |
| **Momentum** | RSI (6/14), MACD (DIF/DEA/Histogram), KDJ |
| **Volatility** | Bollinger Bands, ATR |
| **Volume** | OBV (On-Balance Volume) |
| **Structure** | Fibonacci Retracement, Support/Resistance |

### Supported Assets

| Code | Name | Spot | Perpetual |
|------|------|------|-----------|
| BTC | Bitcoin | BTC-USDT | BTC-USDT-SWAP |
| ETH | Ethereum | ETH-USDT | ETH-USDT-SWAP |
| BNB | BNB | BNB-USDT | BNB-USDT-SWAP |
| SOL | Solana | SOL-USDT | SOL-USDT-SWAP |
| ZEC | Zcash | ZEC-USDT | ZEC-USDT-SWAP |
| XAU | Gold | - | XAU-USDT-SWAP |

### Supported RWA Assets

RWA refers to on-chain real-world assets, which typically only have derivative trading pairs. When querying these assets, use the format "ticker-USDT-swap".

| Company | Stock Ticker | Trading Pair |
|---------|--------------|--------------|
| Tesla | TSLA | TSLA-USDT-swap |
| SpaceX | SPCX | SPCX-USDT-swap |
| Micron | MU | MU-USDT-swap |

## Installation

### Prerequisites

- Python 3.11+
- Network access to OKX API

### Setup

```bash
# Clone the repository
git clone https://github.com/burceasn/crypto-skill.git
cd crypto-skill

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Python CLI

```bash
# Get K-line data
python scripts/cli.py candles BTC-USDT --bar 1H --limit 100

# Get funding rate
python scripts/cli.py funding-rate BTC-USDT-SWAP --limit 50

# Get technical indicators
python scripts/cli.py indicators ETH-USDT --bar 4H --last-n 5

# Get technical indicators with fast MACD preset (5, 13, 8)
python scripts/cli.py indicators BTC-USDT --bar 4H --last-n 5 --factor fast

# Get liquidation price-bucket summary
python scripts/cli.py liquidation BTC-USDT-SWAP

# Get Fear and Greed Index
python scripts/cli.py fear-greed --days 30

# Get support and resistance levels
python scripts/cli.py support-resistance BTC-USDT --bar 1D
```

### Command Reference

#### candles - K-Line Data
```bash
python scripts/cli.py candles <inst_id> [--bar BAR] [--limit LIMIT]
# Example: python scripts/cli.py candles BTC-USDT --bar 1H --limit 100
```

#### funding-rate - Funding Rate
```bash
python scripts/cli.py funding-rate <inst_id> [--limit LIMIT]
# Example: python scripts/cli.py funding-rate BTC-USDT-SWAP --limit 50
```

#### open-interest - Open Interest
```bash
python scripts/cli.py open-interest <inst_id> [--period PERIOD] [--limit LIMIT]
# Example: python scripts/cli.py open-interest BTC-USDT-SWAP --period 1H --limit 50
```

#### indicators - Technical Indicators
```bash
python scripts/cli.py indicators <inst_id> [--bar BAR] [--limit LIMIT] [--last-n N] [--factor FACTOR]
# Example: python scripts/cli.py indicators ETH-USDT --bar 4H --last-n 10
# MACD presets via --factor: default (12,26,9) or fast (5,13,8)
```

#### fear-greed - Fear and Greed Index
```bash
python scripts/cli.py fear-greed [--days DAYS]
# Example: python scripts/cli.py fear-greed --days 30
```

#### long-short-ratio - Long/Short Ratio
```bash
python scripts/cli.py long-short-ratio <ccy> [--period PERIOD] [--limit LIMIT]
# Example: python scripts/cli.py long-short-ratio BTC --period 1H --limit 50
```

#### option-ratio - Option Call/Put Ratio
```bash
python scripts/cli.py option-ratio <ccy> [--period PERIOD] [--limit LIMIT]
# Example: python scripts/cli.py option-ratio BTC --period 8H --limit 20
```

#### top-trader-ratio - Top Trader Position Ratio
```bash
python scripts/cli.py top-trader-ratio <inst_id> [--period PERIOD] [--limit LIMIT]
# Example: python scripts/cli.py top-trader-ratio BTC-USDT-SWAP --period 1H --limit 24
```

#### liquidation - Price-Bucket Liquidation Summary
```bash
python scripts/cli.py liquidation <inst_id> [--state STATE]
# Example: python scripts/cli.py liquidation BTC-USDT-SWAP
```

Returns liquidation records aggregated into $500 price buckets, sorted by total size descending. `side = sell` means a long position was liquidated; `side = buy` means a short position was liquidated.

#### summary - Technical Analysis Summary
```bash
python scripts/cli.py summary <inst_id> [--bar BAR] [--limit LIMIT] [--factor FACTOR]
# Example: python scripts/cli.py summary BTC-USDT --bar 1D
```

#### support-resistance - Support and Resistance Levels
```bash
python scripts/cli.py support-resistance <inst_id> [--bar BAR] [--limit LIMIT] [--window N]
# Example: python scripts/cli.py support-resistance ETH-USDT --bar 1D
```

## Project Structure

```
crypto-skill/
├── README.md                   # This file (English)
├── README_CN.md                # Chinese documentation
├── SKILL.md                    # Skill documentation
├── requirements.txt            # Python dependencies
│
├── scripts/
│   ├── cli.py                  # CLI implementation
│   ├── crypto_data.py          # OKX API wrapper
│   └── technical_analysis.py   # TA indicator engine
│
└── references/
    ├── INDICATORS.md           # Technical indicator guide
    ├── STRATEGY.md             # Trading strategy guidelines
    └── Left-Side.md            # Left-side investing (contrarian accumulation) guide
```

## Python API (Advanced)

For programmatic access, you can import the modules directly:

```python
from scripts.crypto_data import get_okx_candles, get_fear_greed_index
from scripts.technical_analysis import TechnicalAnalysis

# Fetch K-line data
df = get_okx_candles("BTC-USDT", bar="1H", limit=100)

# Calculate indicators
kline_data = df.to_dict(orient="records")
ta = TechnicalAnalysis(kline_data=kline_data, inst_id="BTC-USDT", bar="1H")
indicators = ta.get_all_indicators()
print(indicators.tail(5))
```

## Output Format

All commands output JSON to stdout, making it easy to:

- Pipe to other tools: `python scripts/cli.py candles BTC-USDT | jq '.[0]'`
- Save to files: `python scripts/cli.py indicators BTC-USDT > analysis.json`
- Process in scripts: `result=$(python scripts/cli.py fear-greed --days 7)`

## Requirements

```
pandas>=2.0.0
numpy>=1.24.0
requests>=2.31.0
urllib3>=2.0.0
toon-format==0.9.0b1
```

## Disclaimer

**⚠️ Important Notice:** This skill only provides technical analysis and position recommendations, and does **not** support direct trading. For the sake of ==cybersecurity== and ==being responsible for your own funds==, it is **strongly discouraged** to entrust your cryptocurrency to an AI agent entirely, no matter how powerful the agent is.

## License

MIT License - Use it, fork it, learn from it.