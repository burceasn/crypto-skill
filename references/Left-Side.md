# Left-Side Investing Reference (左侧投资)

## Core Concept

Left-side investing (左侧投资 / 左侧交易) means **accumulating an asset while its price is still falling**, before a bottom is confirmed. The "left side" refers to the descending segment of a price cycle — the part of the chart that sits to the *left* of the eventual trough.

| Term              | Position on Chart          | Timing                             |
| ----------------- | -------------------------- | ---------------------------------- |
| **Left-Side (左侧)** | On the way *down* to a bottom | Before reversal is confirmed        |
| **Right-Side (右侧)** | On the way *up* from a bottom | After reversal is confirmed         |

The core trade-off: **left-side entries give lower average cost but accept higher uncertainty and temporary drawdown**; right-side entries give higher certainty but a worse price.

---

## Core Philosophy

1. **Buy fear, not greed** — Enter when sentiment is at an extreme, not when everyone is already bullish.
2. **Time over timing** — Precision is impossible. Accept being early; profit comes from the eventual cycle, not from calling the exact bottom.
3. **Position management over prediction** — No one catches the bottom. Success comes from *how* you buy (staging), not *whether* you guessed the low.
4. **Discount anchoring** — Every tranche is justified by value/discount, not by hope of a bounce.
5. **Survival first** — A left-side position must be structured to survive a deeper drop without forced exit.

## Market Conditions Favoring Left-Side Entry

Enter left-side only when **multiple capitulation signals converge**. Use `indicators.md` for signal interpretation.

### Sentiment Capitulation

| Signal (from skill data)            | Left-Side Trigger                             |
| ----------------------------------- | --------------------------------------------- |
| Fear & Greed Index                  | Extreme Fear (< 20), sustained                 |
| Funding Rate                        | Deeply negative and persistent (shorts pay longs) |
| Long/Short Ratio                    | Extreme low long ratio (crowd is short)        |
| Liquidation Data                    | Heavy long liquidations (capitulation flush)   |

### Technical Oversold

| Signal (from indicators.md)     | Left-Side Trigger                                   |
| ------------------------------- | --------------------------------------------------- |
| RSI (14)                        | < 30 oversold; < 20 extreme (bullish divergence ideal) |
| KDJ                             | K, D < 20, J < 0 (extreme oversold)                 |
| Bollinger %B                    | < 0 (price below lower band)                         |
| MACD Histogram                  | Bearish bars shrinking (momentum exhaustion)         |

### Price Structure Support

| Signal                          | Left-Side Trigger                                    |
| ------------------------------- | ---------------------------------------------------- |
| Fibonacci Retracement           | 0.618 – 0.786 retracement zone of the prior up-leg    |
| Horizontal Support              | Major swing low / historical support, multiple tests  |
| Long MA                         | Weekly MA50 / MA200 as institutional floor            |

**Convergence rule**: a valid left-side setup requires **≥ 1 sentiment signal + ≥ 1 technical signal + ≥ 1 structural level** simultaneously. A single oversold reading alone is *not* sufficient.

---

## Entry Methods

### 1. Fixed-Interval DCA (定投)

Buy a fixed amount at fixed time intervals regardless of price.

$$ \text{Shares}_t = \dfrac{C}{P_t} $$

where $C$ = fixed fiat allocation per period, $P_t$ = price at time $t$.

- **Pros**: No timing skill needed, lowest psychological load.
- **Cons**: Highest average cost if market only moves down then sharply up.
- **Best for**: Long-term position building, no leverage.

### 2. Price-Level Ladder (网格建仓 / 阶梯建仓)

Place buy orders at predefined descending price levels.

| Level | Price Drop from Start | Allocation |
| ----- | --------------------- | ---------- |
| 1     | 0% (start)            | 10%        |
| 2     | -10%                  | 20%        |
| 3     | -20%                  | 30%        |
| 4     | -30%                  | 40%        |

- **Pros**: Systematic, lower average cost than DCA in trending-down markets.
- **Cons**: Gaps may not fill; requires price to drop to accumulate.

### 3. Fibonacci-Level Accumulation

Allocate tranches at Fibonacci retracement levels (0.382, 0.5, 0.618, 0.786) of the prior impulse leg.

$$ \text{Tranche}_i \text{ at } \text{Price} = \text{High} - (\text{High} - \text{Low}) \times F_i $$

where $F_i \in \{0.382, 0.5, 0.618, 0.786\}$.

- **Pros**: Anchored to structural levels where reversals are statistically frequent.
- **Cons**: Assumes a prior leg is correctly identified.

### 4. Pyramiding Down (倒金字塔 / 越跌越买)

Increase size as price falls, weighted toward the lower levels.

$$ \text{Size}_i = \text{Base} \times (1 + i \times k) $$

- **Pros**: Lowest possible average cost.
- **Cons**: Highest risk — amplifies loss if the asset never recovers. **Must be capped.**

> **CRITICAL**: Pyramiding down must always be bounded by a hard total-allocation cap and a thesis-invalidation level. Unbounded "越跌越买" is the classic path to ruin.

---

## Position Sizing Rules

| Rule                      | Limit                                   |
| ------------------------- | --------------------------------------- |
| Total allocation to asset | ≤ 30% of portfolio (per `STRATEGY.md`)  |
| Number of tranches        | 3 – 5 (never fewer than 3)              |
| Max tranche size          | ≤ 50% of remaining budget               |
| Reserve requirement       | Always keep ≥ 30% cash reserve          |
| Leverage                  | **None** (left-side + leverage = forced liquidation risk) |

**Tranche-size progression** (choose one, never mix ad-hoc):

- **Equal**: each tranche = total / N (safest)
- **Decreasing**: larger early, smaller late (front-loads conviction)
- **Increasing (pyramid)**: smaller early, larger late (lowest avg cost, highest risk)

---

## Risk Management

### Thesis Invalidation (the real stop-loss)

Left-side investing does **not** use tight ATR stops (they'd be hit by normal volatility on the way down). Instead, define a **structural invalidation level**:

| Invalidation Trigger                             | Action                         |
| ------------------------------------------------ | ------------------------------ |
| Price closes below the major structural support  | Exit / stop adding             |
| Fibonacci 0.786 level decisively broken          | Reassess — trend likely dead    |
| **Fundamental** breakdown (not just price)       | Exit fully                     |
| Funding/sentiment *stays* negative with no recovery after prolonged period | Reassess thesis |

### Hard Rules

1. **Never average down into a fundamentally broken asset** — only into a fundamentally sound asset in a sentiment-driven decline.
2. **Never use leverage** on a left-side position.
3. **Never deploy the full budget at once** — staging is the entire edge.
4. **Never add below invalidation** — if the level breaks, you stop, you do not "get a better price."
5. **Max tolerable drawdown** — pre-commit a portfolio-level drawdown limit (e.g., -20%) and honor it.

### Distinguishing "Dip" from "Death"

| Question                       | Dip (buyable)                    | Death (avoid)                    |
| ------------------------------ | -------------------------------- | -------------------------------- |
| Is the decline sentiment-driven? | Yes — panic, liquidation flush  | No — fundamental deterioration  |
| Is the asset structurally sound? | Yes (network/usage intact)      | No (broken model, insolvency)   |
| Are capitulation signals present? | Yes (extreme fear, flush)      | No (slow bleed, no flush)       |
| Is this a major support level?   | Yes (historical support, fib)  | No (free-fall, no floor)        |

---

## Standard Left-Side Workflow (MANDATORY)

### Step 1: Qualify the Asset

- Confirm the asset is fundamentally sound (this is a *value* decline, not a *death* decline).
- If fundamentals are broken → **do not left-side invest**, regardless of oversold signals.

### Step 2: Identify Structural Levels

- Fetch K-line data (`candles`) and mark: major swing low, horizontal support, Fibonacci 0.618–0.786 zone, weekly MA50/MA200.

### Step 3: Confirm Capitulation

- Fetch sentiment data: Fear & Greed index, funding rate, long/short ratio, liquidation records.
- Require ≥ 1 sentiment capitulation signal.

### Step 4: Build the Tranche Plan

- Decide entry method (DCA / ladder / Fibonacci / pyramid).
- Define: total allocation, number of tranches, size per tranche, price level per tranche, reserve %, invalidation level.

### Step 5: Execute with Discipline

- Place limit orders at predefined levels (no market-chasing).
- Execute exactly per plan — no improvising larger sizes "because it dropped more."

### Step 6: Monitor & Honor Invalidation

- Re-evaluate at each tranche fill and at the invalidation level.
- If invalidation breaks → stop adding, reassess exit.

---

## Common Mistakes (FORBIDDEN)

- **All-in at the first dip** — violates staging; the price can always go lower.
- **Leveraged bottom-fishing** — a deeper dip liquidates you before the recovery.
- **Averaging into a dead asset** — conflating "cheap" with "value."
- **No invalidation level** — turning a losing trade into a permanent bag-holder.
- **Ignoring time** — left-side positions can stay underwater for months; exit logic must account for this.
- **Treating left-side as a fast trade** — it is a *position* strategy, not a scalp.

---

## Integration Notes

- Pair with `indicators.md` for exact interpretation of RSI, KDJ, Bollinger, Fibonacci, funding, and liquidation signals.
- Pair with `STRATEGY.md` for the overall analysis workflow, multi-timeframe verification, and portfolio risk limits.
- Left-side entries still respect higher-timeframe context: a valid left-side long should not fight a structurally intact higher-timeframe downtrend without capitulation evidence.
