# trade-skill

[中文](README_CN.md) · [Agent instructions](SKILL.md) · [CLI reference](references/CLI.md)

A Python CLI and agent skill for market data and left-side accumulation analysis. It queries OKX market and derivatives data, calculates technical indicators, and retrieves crypto sentiment from alternative.me. Crypto, precious-metal and company-linked instrument candidates are supported through the same interface; actual availability depends on the upstream service.

## Trading approach

The default is staged accumulation during declines, before a bottom is confirmed. Trend direction and entry suitability are separate decisions: a strong rally alone is not a reason to buy, and a downtrend alone does not veto an entry.

Evaluate price anchors, the holding thesis, available budget, existing exposure and invalidation conditions. Ordinary pullbacks can qualify without extreme fear, capitulation or a confirmed reversal. Left-side trading does not mean unlimited averaging down. Explicit user strategy choices take precedence. This toolkit does not place orders.

## Setup

Use Python 3.11+ and run from the project directory:

```bash
python -m pip install -r requirements.txt
python scripts/cli.py --help
python scripts/cli.py indicators BTC-USDT --bar 1D --limit 100 --last-n 20
python scripts/cli.py support-resistance BTC-USDT --bar 1D
```

The skill name is trade-skill. When installing it, name the containing skill directory trade-skill and include SKILL.md, scripts, references and requirements.txt. The source checkout may retain its existing directory name. Updating the repository does not automatically update an installed copy.

## Company instruments

Resolve the company name to its trading symbol, then query **symbol-USDT-SWAP** directly. For Tesla, resolve to TSLA:

```bash
python scripts/cli.py candles "TSLA-USDT-SWAP" --bar 1D --limit 100
```

Do not construct instrument identifiers from literal company names. Verify ambiguous symbol mappings before querying and disclose the actual identifier. Examples do not assert a listing. A failed request is not bearish evidence, and a company-linked perpetual is not the company's stock.

## Commands and documentation

[CLI.md](references/CLI.md) is the single reference for all 11 commands, their options, fields, examples and implementation limits.

| Command | Purpose |
| --- | --- |
| candles | OHLCV data |
| indicators | Indicator history |
| summary | Latest categorized indicator snapshot |
| support-resistance | Local extrema and range ratios |
| funding-rate | Historical and current/predicted funding |
| open-interest | Historical and current open interest |
| long-short-ratio | Account ratio |
| top-trader-ratio | Top-trader position ratio |
| option-ratio | Raw option ratio fields |
| liquidation | Fixed price-bucket liquidation summary |
| fear-greed | Crypto sentiment history |

- [SKILL.md](SKILL.md): discovery, instrument resolution, routing and policy precedence.
- [Left-Side.md](references/Left-Side.md): entry eligibility, staging, budgets and invalidation.
- [STRATEGY.md](references/STRATEGY.md): data workflow, reporting and behavioral review cases.
- [indicators.md](references/indicators.md): evidence interpretation and limitations.
- scripts/cli.py: command entrypoint; crypto_data.py: data access; technical_analysis.py: calculations.

Successful output is **TOON, not JSON**. Explicit errors may be JSON; empty results and exceptions also require inspection. Check timestamps, missing values and potentially unfinished candles. The CLI does not provide MA200, company fundamentals, account balances or order execution. Review the documented support/resistance and Fibonacci implementation before using their results.
