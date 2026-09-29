# CLI 工具参考

以 scripts/cli.py、scripts/crypto_data.py 和 scripts/technical_analysis.py 的当前实现为准。所有示例从技能目录运行。安装依赖用 `python -m pip install -r requirements.txt`；帮助用 `python scripts/cli.py --help` 或 `python scripts/cli.py <command> --help`。

## 输入与输出约定

- inst_id 为交易对，ccy 为资产代码；CLI 转成大写，不做公司别名解析。
- 公司名称由 agent 先解析为交易代码，再直接查询“交易代码-USDT-SWAP”，例如 Tesla / 特斯拉使用 `candles "TSLA-USDT-SWAP"`。不要使用公司全称拼接；映射不明确时按 [技能入口](../SKILL.md)先核实。这不是合约上市承诺。
- 成功输出使用 toon_format.encode，即 **TOON**，不能直接交给 JSON 解析器或 jq。函数虽名为 output_json，实际不输出 JSON。
- 显式错误通常为 JSON 的 error 字段；有些异常直接抛出，空结果也需检查。失败可能以退出码 0 结束，因此同时检查内容与退出码。
- 浮点数最多保留 8 位小数，NaN/Inf 转为 null。极低价格和极小比率可能损失精度，不据此给虚假精确的买点。
- datetime 由 Unix 毫秒生成，表示 UTC 时刻但通常不带时区后缀；不要当作本地时间。fear-greed 的 date 按 UTC 日期生成。K 线开盘时间与各 bar 的分桶边界是两件事，不擅自宣称所有日线均为 UTC 零点开盘。
- limit 是请求数量，不保证实际返回数量。当前没有历史翻页命令；不要声称支持无限历史。保守使用 100 并检查实际范围，接口约束不等于 argparse 强制上限。
- K 线原始 confirm 字段被代码丢弃，末根可能未收盘；不能由输出确认其收盘状态。
- 没有实时 ticker、公司代码搜索、基本面、估值、账户余额、下单或回测命令。Python 模块有些内部参数不在 CLI 暴露，不给 CLI 虚构参数。

## 11 个命令

下表参数列给出完整可用参数与默认值。inst_id / ccy 为位置参数，其余用表中选项名。

| 命令 | 位置参数 | 选项与默认值 | 用途 |
| --- | --- | --- | --- |
| candles | inst_id | --bar 1H; --limit 100 | OHLCV、波段与数据时间 |
| indicators | inst_id | --bar 1D; --limit 100; --last-n 10; --factor default | 多行指标与变化 |
| summary | inst_id | --bar 1D; --limit 100; --factor default | 最新一行的分类快照 |
| support-resistance | inst_id | --bar 1D; --limit 100; --window 5 | 局部极值与全样本比例位置 |
| funding-rate | inst_id | --limit 100 | 永续历史及当前/预测费率 |
| open-interest | inst_id | --period 1H; --limit 100 | 历史及实时 OI |
| long-short-ratio | ccy | --period 1H; --limit 100 | 账户多空比 |
| top-trader-ratio | inst_id | --period 5m; --limit 100 | 顶级交易员仓位比 |
| option-ratio | ccy | --period 8H; --limit 100 | 期权持仓量及成交量比值 |
| liquidation | inst_id | --state filled | 固定价格桶的强平汇总 |
| fear-greed | 无 | --days 7 | alternative.me 加密情绪历史 |

### 周期与参数

- bar 帮助列出 1m、5m、15m、30m、1H、4H、1D、1W；实际支持由接口决定，CLI 不验证全部周期。
- open-interest 与 long-short-ratio 的 period 帮助列出 5m、1H、1D。
- top-trader-ratio 默认 5m；CLI 未枚举有效周期，使用其他粒度时核实接口支持，不能照搬 bar。
- option-ratio 的 period 帮助列出 8H、1D；limit 在本地截取，未传入该接口。
- factor 仅接受 default（12,26,9）或 fast（5,13,8），仅 indicators 和 summary 暴露。
- last-n=0 返回所有已计算行；limit 决定计算样本，last-n 只裁剪输出。不把 last-n=5 理解为只拿 5 根计算。
- liquidation 只有 state 参数，没有 CLI --bar、--limit 或 --bucket-size。filled 是默认；其他 state 的有效性以接口响应为准，不把未成交状态称为已发生强平。

## 返回字段与实现细节

### candles

行字段：datetime、open、high、low、close、vol。按时间升序。close 为该根 K 线价格，不是独立 ticker。原始 volCcy、volCcyQuote、confirm 不在输出中。

### indicators

按时间升序，默认只返回末 10 行：

- 价格：datetime、open、high、low、close、volume（来自原始 vol）。
- 均线：ma5、ma10、ma20、ma50、ma100。
- 动量：rsi14、macd_dif、macd_dea、macd_hist、kdj_k、kdj_d、kdj_j。
- 方向与强度：plus_di、minus_di、adx。
- 波动：atr14、atr14_pct、bb_upper、bb_mid、bb_lower、bb_pctb、bb_bandwidth。
- 成交量：obv。

没有 RSI6、MA200 或独立 EMA 输出。滚动均线与布林带需足够样本，指数平滑指标也有初始化影响；null 不代表零。公式与解读见 [indicators.md](indicators.md)。

### summary

对象含 asset、indicators、data_summary。indicators 中价格、datetime 和 obv 位于该层，trend / momentum / volatility 是其子对象；data_summary.total_candles 为样本数。只有最新行，没有买卖评级、背离识别、涨跌幅或建仓资格。

### support-resistance

对象含 inst_id、bar、current_price、support_levels、resistance_levels、fibonacci_retracement、price_range.high/low。

两个极值数组均按价格降序，没有去重或相对现价筛选。默认极值左右各需 5 根；数组可能为空。比例按全样本 low+(high-low)×r 计算，不是自动识别的上升波段回撤。具体转换见指标参考。

### funding-rate

行字段：datetime、fundingRate、realizedRate、type。当前行放前，type 为 Current/Predicted，realizedRate 为 null；历史为 Settled。历史返回顺序应检查，按时间对齐后再判断持续变化。原始小数需乘 100 才是百分比。

### open-interest

行字段：datetime、oiCcy、oiUsd、type。首行为 Current (Real-time)，其 oiUsd 由当前 oiCcy × markPx 计算；历史行为 History。时间与其他命令不保证完全同步，不能混用实时点与历史点推断同一时刻变化。

### long-short-ratio / top-trader-ratio

均返回 datetime、longShortPosRatio，按时间降序。相同字段名不代表相同统计口径：

- long-short-ratio 调用 long-short-account-ratio，查询参数是 ccy。代码注释称 elite，但不能据此声称它一定是顶级 5% 的仓位比。
- top-trader-ratio 调用 long-short-position-ratio-contract-top-trader，查询参数是 inst_id。

不把账户比当仓位比，不把样本比当全市场资金流。begin/end 虽存在于 Python 函数，但 CLI 未暴露。

### option-ratio

返回 datetime、oiRatio、volRatio，按时间降序并本地截取 limit。实现没有验证分子分母方向，不能仅凭旧文档称其为 call/put 并据此判断看多；需要核实上游口径后解释。没有覆盖时标注不可用。

### liquidation

对象字段：inst_id、state、start_time、end_time、total_records、bucket_size、price_buckets。每桶含 price、buy_sz、sell_sz、total_sz，按 total_sz 降序。

固定 bucket_size=500，price 为向下取整后的桶下界。sz 为原始数量，没有名义美元转换。覆盖时间取返回样本，不能称为固定 24 小时或全市场数据。对低价资产过粗时，不用桶边界推导精确支撑或未来清算价。

### fear-greed

行字段：date、value、value_classification；来自 alternative.me。检查时间顺序与覆盖范围，不声称来自 CoinMarketCap。仅提供市场情绪背景。

## 调用示例

按任务选用，无需每次全部运行：

```bash
python scripts/cli.py candles BTC-USDT --bar 1W --limit 100
python scripts/cli.py indicators BTC-USDT --bar 1D --limit 100 --last-n 20
python scripts/cli.py indicators BTC-USDT --bar 4H --limit 100 --last-n 10 --factor fast
python scripts/cli.py summary BTC-USDT --bar 1D --factor default
python scripts/cli.py support-resistance BTC-USDT --bar 1D --window 5
python scripts/cli.py funding-rate BTC-USDT-SWAP --limit 50
python scripts/cli.py open-interest BTC-USDT-SWAP --period 1H --limit 50
python scripts/cli.py long-short-ratio BTC --period 1H --limit 50
python scripts/cli.py top-trader-ratio BTC-USDT-SWAP --period 5m --limit 50
python scripts/cli.py option-ratio BTC --period 8H --limit 20
python scripts/cli.py liquidation BTC-USDT-SWAP --state filled
python scripts/cli.py fear-greed --days 30
python scripts/cli.py candles "TSLA-USDT-SWAP" --bar 1D --limit 100
```

## 失败处理

先检查命令、身份映射和参数，再区分空样本、网络故障及产品不支持。只做有限的针对性重试；单次失败不能证明没有该合约。仍失败则披露已尝试标识和缺失数据，继续独立可完成的分析。

基本面、公司映射或接口口径需外部核实时使用可用的可靠来源，注明来源和日期；没有外部访问能力就保留未知，不制造结论。
