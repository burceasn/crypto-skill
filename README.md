# Crypto Technical Analysis Skill

> MCP-powered cryptocurrency market data and technical analysis toolkit

An AI-ready skill that provides real-time crypto market data from OKX exchange and comprehensive technical indicator calculations. Designed for seamless integration with MCP (Model Context Protocol) clients like Claude, OpenCode, and other AI agents.

## Features

### Market Data Tools (MCP)

| Tool | Description |
|------|-------------|
| `get_candles` | K-line/OHLCV data (1m to 1W timeframes) |
| `get_funding_rate` | Perpetual contract funding rates |
| `get_open_interest` | Open interest with USD valuation |
| `get_long_short_ratio` | Elite trader positioning data |
| `get_top_trader_position_ratio` | Top 5% traders' long/short position ratio |
| `get_option_oi_volume_ratio` | Option call/put OI and volume ratio |
| `get_fear_greed_index` | Fear and Greed Index from alternative.me |
| `get_liquidation` | Historical liquidation records |

### Technical Indicators

| Category | Indicators |
|----------|------------|
| **Trend** | MA (5/10/20/50), EMA (12/26), DMI/ADX |
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

## Installation

### Prerequisites

- Python 3.11+
- Network access to OKX (proxy may be required in some regions)

### Setup

```bash
# Clone the repository
git clone https://github.com/burceasn/crypto-skill.git
cd crypto-skill

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Option 1: MCP Integration (Recommended for AI Agents)

Add to your MCP client configuration:

```json
{
  "mcpServers": {
    "crypto": {
      "command": "python",
      "args": ["/path/to/crypto-skill/scripts/crypto_mcp_server.py"],
      "env": {
        "PYTHONIOENCODING": "utf-8"
      }
    }
  }
}
```

Then your AI agent can call tools:

```python
# Get BTC 1-hour candles
skill_mcp(
  mcp_name="crypto",
  tool_name="get_candles",
  arguments={"inst_id": "BTC-USDT", "bar": "1H", "limit": 100}
)

# Get funding rate
skill_mcp(
  mcp_name="crypto",
  tool_name="get_funding_rate",
  arguments={"inst_id": "ETH-USDT-SWAP", "limit": 50}
)

# Get fear and greed index
skill_mcp(
  mcp_name="crypto",
  tool_name="get_fear_greed_index",
  arguments={"days": 30}
)
```

### Option 2: Direct Python API

```python
from scripts.technical_analysis import TechnicalAnalysis

# Fetch data and calculate all indicators
ta = TechnicalAnalysis.from_api("BTC-USDT", bar="1H", limit=100)
indicators = ta.get_all_indicators()

# Get latest values
latest = indicators.iloc[-1]
print(f"Price: {latest['close']:.2f}")
print(f"RSI(14): {latest['rsi14']:.2f}")
print(f"MACD DIF: {latest['macd_dif']:.4f}")
print(f"ADX: {latest['dmi_adx']:.2f}")
```

### Option 3: Batch Analysis

```python
from scripts.technical_analysis import analyze_all_assets

# Analyze multiple assets at once
results = analyze_all_assets(
    inst_ids=['BTC-USDT', 'ETH-USDT', 'SOL-USDT'],
    bar='1D',
    limit=100
)
# Results saved to result/ folder with timestamp
```

### Option 4: Derivatives Data

```python
from scripts.technical_analysis import TechnicalAnalysis

# Funding rate
funding = TechnicalAnalysis.fetch_funding_rate("BTC-USDT-SWAP", limit=10)

# Open interest
oi = TechnicalAnalysis.fetch_open_interest("BTC-USDT-SWAP", period='1H', limit=10)

# Long/Short ratio
ls = TechnicalAnalysis.fetch_long_short_ratio("BTC", period='1H', limit=10)

# Top trader position ratio
top = TechnicalAnalysis.fetch_top_trader_position_ratio("BTC-USDT-SWAP", period='1H', limit=10)

# Option call/put ratio
opt = TechnicalAnalysis.fetch_option_oi_volume_ratio("BTC", period='8H')
```

## Project Structure

```
crypto-skill/
├── README.md                       # This file
├── requirements.txt                # Python dependencies
├── SKILL.md                        # Skill documentation
│
├── scripts/
│   ├── crypto_data.py              # OKX API wrapper
│   ├── crypto_mcp_server.py        # MCP protocol server
│   └── technical_analysis.py       # TA indicator engine
│
└── references/
    └── indicators.md               # Technical indicator guide
```

## Technical Analysis Module

### Available Methods

#### Trend Indicators

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `calculate_ma(period)` | period: int | pd.Series | Simple Moving Average |
| `calculate_ema(period)` | period: int | pd.Series | Exponential Moving Average |
| `calculate_dmi(period=14)` | period: int | (+DI, -DI, ADX) | Directional Movement Index |

#### Momentum Indicators

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `calculate_rsi(period=14)` | period: int | pd.Series | Relative Strength Index |
| `calculate_macd(fast=12, slow=26, signal=9)` | fast, slow, signal: int | (DIF, DEA, Histogram) | MACD |
| `calculate_kdj(n=9, m1=3, m2=3)` | n, m1, m2: int | (K, D, J) | KDJ Stochastic |

#### Volatility Indicators

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `calculate_bollinger_bands(period=20, std_dev=2)` | period, std_dev: int | (Upper, Middle, Lower) | Bollinger Bands |
| `calculate_atr(period=14)` | period: int | pd.Series | Average True Range |

#### Volume Indicators

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `calculate_obv()` | - | pd.Series | On-Balance Volume |

#### Price Structure

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `calculate_fibonacci_retracement(high, low)` | high, low: float | Dict[str, float] | Fibonacci levels |
| `find_support_resistance(window=5)` | window: int | (supports[], resistances[]) | Key price levels |

### get_all_indicators() Output

Returns a DataFrame with all calculated indicators:

| Category | Columns |
|----------|---------|
| Price | open, high, low, close, volume |
| Moving Averages | ma5, ma10, ma20, ma50, ema12, ema26 |
| RSI | rsi6, rsi14 |
| MACD | macd_dif, macd_dea, macd_hist |
| KDJ | kdj_k, kdj_d, kdj_j |
| DMI | dmi_plus_di, dmi_minus_di, dmi_adx |
| Bollinger | bb_upper, bb_middle, bb_lower, bb_width |
| ATR | atr14 |
| OBV | obv |
| Price Change | price_change_1, price_change_5, price_change_20 |
| Volume Change | volume_change, volume_sma20 |

## Configuration

### Proxy Settings

The project defaults to using a local proxy at `127.0.0.1:7890`. To change this, edit `scripts/crypto_data.py`:

```python
DEFAULT_PROXY = {
    "http": "http://127.0.0.1:7890",
    "https": "http://127.0.0.1:7890"
}
```

Or disable proxy entirely when calling functions:

```python
df = get_okx_candles("BTC-USDT", use_proxy=False)
```

## Requirements

```
pandas>=2.0.0
numpy>=1.24.0
requests>=2.31.0
urllib3>=2.0.0
```

## Disclaimer

This project is for educational and research purposes only. **Not financial advice.**

Trade at your own risk. The market can stay irrational longer than you can stay solvent.

## Acknowledgments

- **[Oh My OpenCode](https://github.com/code-yeongyu/oh-my-opencode.git)** - The AI agent framework
- **[OpenCode](https://github.com/anomalyco/opencode.git)** - The foundation for AI coding

## License

MIT License - Use it, fork it, learn from it.