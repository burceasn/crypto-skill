# 加密货币技术分析技能

[![English](https://img.shields.io/badge/lang-English-blue.svg)](README.md) [![中文](https://img.shields.io/badge/lang-中文-red.svg)](readme_cn.md)

> 基于 Shell 脚本的加密货币市场数据与技术分析工具包

一个 AI 就绪的技能，提供来自 OKX 交易所的实时加密货币市场数据和全面的技术指标计算。专为命令行使用而设计。

## 功能特性

### 市场数据命令

| 命令 | 描述 |
|---------|-------------|
| `candles` | K线/OHLCV 数据（1分钟到1周时间周期） |
| `funding-rate` | 永续合约资金费率 |
| `open-interest` | 持仓量（含美元估值） |
| `long-short-ratio` | 精英交易员持仓人数比 |
| `top-trader-ratio` | 前5%交易员多空仓位比 |
| `option-ratio` | 期权看涨/看跌持仓量和交易量比 |
| `fear-greed` | 恐惧贪婪指数（alternative.me） |
| `liquidation` | 历史爆仓记录 |

### 技术分析命令

| 命令 | 描述 |
|---------|-------------|
| `indicators` | 完整技术指标（MA, RSI, MACD 等） |
| `summary` | 快速技术分析摘要 |
| `support-resistance` | 支撑/阻力位和斐波那契回撤 |

### 技术指标

| 类别 | 指标 |
|----------|------------|
| **趋势** | MA (5/10/20/50), EMA (12/26), DMI/ADX |
| **动量** | RSI (6/14), MACD (DIF/DEA/柱状图), KDJ |
| **波动率** | 布林带, ATR |
| **成交量** | OBV (能量潮指标) |
| **结构** | 斐波那契回撤, 支撑/阻力位 |

### 支持的资产

| 代码 | 名称 | 现货 | 永续合约 |
|------|------|------|-----------|
| BTC | 比特币 | BTC-USDT | BTC-USDT-SWAP |
| ETH | 以太坊 | ETH-USDT | ETH-USDT-SWAP |
| BNB | BNB | BNB-USDT | BNB-USDT-SWAP |
| SOL | Solana | SOL-USDT | SOL-USDT-SWAP |
| ZEC | 大零币 | ZEC-USDT | ZEC-USDT-SWAP |
| XAU | 黄金 | - | XAU-USDT-SWAP |

## 安装

### 前置条件

- Python 3.11+
- 可访问 OKX API 的网络

### 设置

```bash
# 克隆仓库
git clone https://github.com/burceasn/crypto-skill.git
cd crypto-skill

# 安装依赖
pip install -r requirements.txt

# 添加执行权限 (Linux/macOS)
chmod +x crypto.sh
```

## 使用方法

### Shell 脚本（推荐）

```bash
# 获取 K 线数据
./crypto.sh candles BTC-USDT --bar 1H --limit 100

# 获取资金费率
./crypto.sh funding-rate BTC-USDT-SWAP --limit 50

# 获取技术指标
./crypto.sh indicators ETH-USDT --bar 4H --last-n 5

# 获取恐惧贪婪指数
./crypto.sh fear-greed --days 30

# 获取支撑阻力位
./crypto.sh support-resistance BTC-USDT --bar 1D
```

### 直接使用 Python CLI

```bash
python scripts/cli.py candles BTC-USDT --bar 1H --limit 100
python scripts/cli.py funding-rate ETH-USDT-SWAP --limit 50
python scripts/cli.py indicators BTC-USDT --bar 1D --last-n 10
```

### 命令参考

#### candles - K线数据
```bash
./crypto.sh candles <inst_id> [--bar BAR] [--limit LIMIT]
# 示例: ./crypto.sh candles BTC-USDT --bar 1H --limit 100
```

#### funding-rate - 资金费率
```bash
./crypto.sh funding-rate <inst_id> [--limit LIMIT]
# 示例: ./crypto.sh funding-rate BTC-USDT-SWAP --limit 50
```

#### indicators - 技术指标
```bash
./crypto.sh indicators <inst_id> [--bar BAR] [--limit LIMIT] [--last-n N]
# 示例: ./crypto.sh indicators ETH-USDT --bar 4H --last-n 10
```

#### fear-greed - 恐惧贪婪指数
```bash
./crypto.sh fear-greed [--days DAYS]
# 示例: ./crypto.sh fear-greed --days 30
```

## 项目结构

```
crypto-skill/
├── crypto.sh                   # Shell 入口
├── README.md                   # 英文文档
├── README_CN.md                # 中文文档（本文件）
├── requirements.txt            # Python 依赖
├── SKILL.md                    # 技能文档
│
├── scripts/
│   ├── cli.py                  # CLI 实现
│   ├── crypto_data.py          # OKX API 封装
│   └── technical_analysis.py   # 技术分析引擎
│
└── references/
    └── indicators.md           # 技术指标指南
```

## Python API（高级用法）

对于程序化访问，可以直接导入模块：

```python
from scripts.crypto_data import get_okx_candles, get_fear_greed_index
from scripts.technical_analysis import TechnicalAnalysis

# 获取 K 线数据
df = get_okx_candles("BTC-USDT", bar="1H", limit=100)

# 计算指标
kline_data = df.to_dict(orient="records")
ta = TechnicalAnalysis(kline_data=kline_data, inst_id="BTC-USDT", bar="1H")
indicators = ta.get_all_indicators()
print(indicators.tail(5))
```

## 输出格式

所有命令输出 JSON 到标准输出，便于：

- 管道处理：`./crypto.sh candles BTC-USDT | jq '.[0]'`
- 保存文件：`./crypto.sh indicators BTC-USDT > analysis.json`
- 脚本处理：`result=$(./crypto.sh fear-greed --days 7)`

## 依赖要求

```
pandas>=2.0.0
numpy>=1.24.0
requests>=2.31.0
urllib3>=2.0.0
```

## 免责声明

**⚠️ 重要提示：** 本技能仅提供技术分析和持仓建议，不支持直接进行交易。出于对网络安全以及对自己资金负责的态度，**强烈不建议**将自己的加密货币完全交给 AI 代理负责，无论该代理有多强大。

## 许可证

MIT 许可证 - 随意使用、分支、学习。