# trade-skill

[English](README.md) · [技能入口](SKILL.md) · [CLI 参考](references/CLI.md)

基于现有 Python CLI 获取 OKX 行情、衍生品数据及技术指标，并以左侧交易框架评估下跌中的分批建仓机会。支持查询加密货币、贵金属和公司关联交易对；具体产品与数据覆盖以接口响应为准。

## 默认分析风格

趋势描述与买入决策分开：上涨不自动推荐追买，下跌不自动否决承接。普通回撤、深度调整和恐慌出清均可评估；极端恐慌或确认反转不是统一入场前提。

具体行动由价格依据、持有逻辑、预算、已有仓位和失效条件决定。左侧不等于无条件越跌越买。用户明确指定其他策略时，以用户要求为准。工具只查询和分析，不下单。

## 安装与运行

使用 Python 3.11+，在项目目录安装依赖：

```bash
python -m pip install -r requirements.txt
python scripts/cli.py --help
python scripts/cli.py indicators BTC-USDT --bar 1D --limit 100 --last-n 20
python scripts/cli.py support-resistance BTC-USDT --bar 1D
```

技能名称已经是 trade-skill。安装为技能时，将包含 SKILL.md、scripts、references 和 requirements.txt 的目录命名为 trade-skill。源码工作目录可以保留原名；修改仓库不会自动更新已安装的旧副本。

## 公司名称查询

收到公司名称，先解析为交易代码，再通过 CLI 直接按“交易代码-USDT-SWAP”查询。例如 Tesla / 特斯拉解析为 TSLA：

```bash
python scripts/cli.py candles "TSLA-USDT-SWAP" --bar 1D --limit 100
```

不使用公司全称拼接交易对。映射不明确时先核实，并披露实际查询标识。示例不保证合约存在，查询失败不代表看空。公司合约不是股票，也不提供公司基本面。

## 工具与文档

全部 11 个命令的参数、字段和限制集中在 [CLI.md](references/CLI.md)，避免多处说明不一致。

| 命令 | 功能 |
| --- | --- |
| candles | K 线与成交量 |
| indicators | 多行完整指标 |
| summary | 最新指标分类快照 |
| support-resistance | 局部极值与区间比例 |
| funding-rate | 历史及当前/预测费率 |
| open-interest | 历史与实时未平仓量 |
| long-short-ratio | 账户多空比 |
| top-trader-ratio | 顶级交易员仓位比 |
| option-ratio | 期权比值原始字段 |
| liquidation | 固定价格桶强平汇总 |
| fear-greed | alternative.me 情绪历史 |

- [SKILL.md](SKILL.md)：技能发现、标的解析、文档路由和策略优先级。
- [Left-Side.md](references/Left-Side.md)：入场资格、分批资金、失效和产品边界。
- [STRATEGY.md](references/STRATEGY.md)：取数、证据组织、输出及行为验收场景。
- [indicators.md](references/indicators.md)：指标的左侧用途与误读边界。
- scripts/cli.py：命令入口；crypto_data.py：数据访问；technical_analysis.py：指标计算。

成功输出为 **TOON，而不是 JSON**；错误可能为 JSON 或异常。需检查空值、时间及末根 K 线状态。当前没有 MA200、公司估值、账户或下单功能。支撑和斐波那契输出的实现限制见 CLI 参考，不将其直接当作买卖信号。
