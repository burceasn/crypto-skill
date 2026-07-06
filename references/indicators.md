# Technical Indicators Reference

> Knowledge base for signal interpretation. Agent policy (`AGENTS.md`) references this document for analysis.

---

## Trend Indicators

### MA (Moving Average)

**Purpose**: Smooth price fluctuations, reveal trend direction.

**Formula**: $MA(N) = \dfrac{C_1 + C_2 + \cdots + C_N}{N}$

| Period | Meaning | Application |
|--------|---------|-------------|
| MA5 | Weekly average (ultra-short) | Immediate trend, frequent crossovers |
| MA10 | 2-week average (short) | Short-term support/resistance |
| MA20 | Monthly average (medium-short) | Swing trading core reference |
| MA50 | 2-month average (medium) | Medium-term trend boundary |
| MA200 | Long-term average | Bull/Bear divider, institutional focus |

**Signals**:

| Pattern | Signal | Meaning |
|---------|--------|---------|
| Golden Cross (short MA crosses above long MA) | Buy | Short-term momentum > long-term |
| Death Cross (short MA crosses below long MA) | Sell | Short-term momentum < long-term |
| Bullish Alignment (MA5 > MA10 > MA20 > MA50) | Strong Uptrend | All timeframes agree |
| Bearish Alignment (MA5 < MA10 < MA20 < MA50) | Strong Downtrend | All timeframes agree |
| MA Convergence | Pending Breakout | Wait for direction confirmation |

---

### EMA (Exponential Moving Average)

**Purpose**: More weight on recent prices, faster response than MA.

**Formula**: $EMA(t) = \alpha \cdot Price(t) + (1 - \alpha) \cdot EMA(t-1)$, where $\alpha = \dfrac{2}{N+1}$

**Key Periods**:

- **EMA12**: Short-term momentum, MACD fast line basis
- **EMA26**: Medium-term momentum, MACD slow line basis

**vs MA**: EMA reacts faster to sudden moves, better for volatile crypto markets.

---

### DMI (Directional Movement Index)

**Purpose**: Measure trend strength AND direction.

**Components**:
- **+DI**: Upward momentum strength
- **-DI**: Downward momentum strength
- **ADX**: Trend strength (direction-agnostic)

**Parameter**: Period = 14

**ADX Interpretation**:

| ADX Value | Market State | Trading Strategy |
|-----------|--------------|------------------|
| < 20 | No trend / Ranging | Range trade, avoid trend strategies |
| 20-25 | Trend forming | Prepare entry, await confirmation |
| 25-40 | Trend confirmed | Trade with trend, hold position |
| 40-50 | Strong trend | Add to position, watch for extremes |
| > 50 | Extreme trend | Prepare exit, reversal possible |

**Direction**: $\text{Signal} = 
\begin{cases}
\text{Long}, & \text{if } +DI > -DI \text{ and } ADX > 25 \\
\text{Short}, & \text{if } -DI > +DI \text{ and } ADX > 25 \\
\text{None}, & \text{otherwise}
\end{cases}$

---

## Momentum Indicators

### RSI (Relative Strength Index) 

**Purpose**: Measure overbought/oversold conditions and momentum.

**Formula**: $RSI = 100 - \frac{100}{1 + RS}$, where $RS = \frac{\text{Avg Gain}}{\text{Avg Loss}}$

**Parameter**: Period = 14

**Zone Analysis**:

| RSI Range | State | Action |
|-----------|-------|--------|
| > 80 | Extreme Overbought | Strong short signal, high reversal probability |
| 70-80 | Overbought | Watch for short, await confirmation |
| 50-70 | Bullish Zone | Uptrend, hold longs |
| 30-50 | Bearish Zone | Downtrend, hold shorts |
| 20-30 | Oversold | Watch for long, await confirmation |
| < 20 | Extreme Oversold | Strong long signal, high bounce probability |

**Divergence (Most Important Reversal Signal)**:
| Type | Pattern | Meaning |
|------|---------|---------|
| Bearish Divergence | Price new high, RSI no new high | Upward momentum exhausted, prepare short |
| Bullish Divergence | Price new low, RSI no new low | Downward momentum exhausted, prepare long |
| Hidden Divergence | Price pullback but RSI holds | Trend continuation signal |

**Trend Context**:

- **Uptrend**: RSI 40-50 = support zone (add to longs)
- **Downtrend**: RSI 50-60 = resistance zone (add to shorts)

---

### MACD (Moving Average Convergence Divergence)

**Purpose**: Track momentum changes via EMA differential.

**Formula**:
$$
\begin{align}
\text{DIF (Fast Line)} &= EMA_{12} - EMA_{26} \\
\text{DEA (Signal Line)} &= EMA_9(\text{DIF}) \\
\text{Histogram} &= (\text{DIF} - \text{DEA}) \times 2
\end{align}
$$


**Signal Categories**:

**1. Crossovers**:

| Pattern | Location | Meaning |
|---------|----------|---------|
| Golden Cross (DIF above DEA) | Above zero | Strong trend continuation |
| Golden Cross (DIF above DEA) | Below zero | Possible reversal start |
| Death Cross (DIF below DEA) | Below zero | Weak trend continuation |
| Death Cross (DIF below DEA) | Above zero | Possible pullback start |

**2. Zero Line**:
- DIF/DEA above zero = Bull market, prioritize longs
- DIF/DEA below zero = Bear market, prioritize shorts
- Zero line cross = Major trend transition

**3. Histogram**:

| Pattern | Meaning |
|---------|---------|
| Red bars expanding | Bullish momentum increasing |
| Red bars shrinking | Bullish momentum weakening, watch for reversal |
| Green bars expanding | Bearish momentum increasing |
| Green bars shrinking | Bearish momentum weakening, watch for bounce |

---

### KDJ (Stochastic Oscillator)

**Purpose**: Measure price position relative to range, fast overbought/oversold detection.

**Formula**:
$$
\begin{align}
RSV &= \frac{Close - Low_N}{High_N - Low_N} \times 100 \\
K &= \frac{2}{3} \times K_{prev} + \frac{1}{3} \times RSV \\
D &= \frac{2}{3} \times D_{prev} + \frac{1}{3} \times K \\
J &= 3K - 2D
\end{align}
$$


**Parameters**: N=9, M1=3, M2=3

**Signals**:
| Condition | State | Action |
|-----------|-------|--------|
| K, D > 80 | Overbought | Watch for short, J > 100 = extreme |
| K, D < 20 | Oversold | Watch for long, J < 0 = extreme |
| K crosses above D | Golden Cross | Buy signal (more valid at low levels) |
| K crosses below D | Death Cross | Sell signal (more valid at high levels) |

**J-line Extremes**: $J > 100$ or $J < 0$ = Short-term extreme, high reversal probability.

---

## Volatility Indicators

### Bollinger Bands

**Purpose**: Dynamic support/resistance based on standard deviation.

**Formula**:
$$
\begin{align}
\text{Middle} &= MA_{20} \\
\text{Upper} &= MA_{20} + 2 \times \sigma \\
\text{Lower} &= MA_{20} - 2 \times \sigma \\
\%B &= \frac{\text{Price} - \text{Lower}}{\text{Upper} - \text{Lower}}
\end{align}
$$


**Price Position**:

| Position | State | Action |
|----------|-------|--------|
| Touch upper band | Overbought | Watch for pullback |
| Touch lower band | Oversold | Watch for bounce |
| Walking upper band | Strong uptrend | Don't rush to short |
| Walking lower band | Strong downtrend | Don't rush to long |

**Bandwidth**:
| Pattern | Meaning | Action |
|---------|---------|--------|
| Squeeze (narrow bands) | Low volatility, pending breakout | Wait for direction |
| Expansion (wide bands) | Trend started | Trade with trend |

**%B Values**:
- %B > 1 = Price above upper band, extreme overbought
- %B < 0 = Price below lower band, extreme oversold
- %B = 0.5 = Price at middle band

---

### ATR (Average True Range)

**Purpose**: Measure volatility for stop-loss/take-profit distance.

**Formula**:
$$
\begin{align}
TR &= \max(High - Low,\; \lvert High - PrevClose \rvert,\; \lvert Low - PrevClose \rvert) \\
ATR &= MA_{14}(TR)
\end{align}
$$


**Applications**:

| Use Case | Formula | Notes |
|----------|---------|-------|
| Stop Loss | Entry ± 1.5-2 × ATR | Avoid normal volatility stop-outs |
| Take Profit | Entry ± 2-3 × ATR | Reasonable risk/reward |
| Position Size | Risk Amount / ATR | Reduce size when volatility high |

**Volatility Assessment**:
- ATR% = ATR / Price × 100
- ATR% < 3% = Low volatility, can increase leverage
- ATR% > 5% = High volatility, reduce leverage and size

---

## Volume Indicators

### OBV (On-Balance Volume)

**Purpose**: Track money flow via cumulative volume weighted by price direction.

**Rules**:
- Close > Previous Close: OBV += Today's Volume
- Close < Previous Close: OBV -= Today's Volume
- Close = Previous Close: OBV unchanged

**Signals**:

| Pattern | Meaning |
|---------|---------|
| Price up + OBV up | Healthy uptrend, sustainable |
| Price up + OBV down (divergence) | Weak uptrend, reversal warning |
| Price down + OBV down | Normal pullback, not panic |
| Price down + OBV up (divergence) | Possible bottom accumulation |

---

## Price Structure Indicators

### Fibonacci Retracement

**Purpose**: Identify potential support/resistance based on Fibonacci ratios.

**Key Levels**:
| Ratio | Meaning | Significance |
|-------|---------|--------------|
| 0.236 | Shallow retracement | Strong trends often stop here |
| 0.382 | Golden retracement | Common support/resistance ★ |
| 0.500 | Mid retracement | Psychological level |
| 0.618 | Deep retracement | Most important level ★★★ |
| 0.786 | Extreme retracement | Trend may be invalidated |

**Extension Levels (for take-profit)**:
- 1.272: First target
- 1.618: Second target (golden extension)
- 2.618: Extreme target

**Application Rules**:
1. Uptrend pullback to 0.382-0.618 zone = High probability long entry
2. Downtrend bounce to 0.382-0.618 zone = High probability short entry
3. Retracement beyond 0.786 = Original trend likely ended

---

### Support/Resistance

**Pivot Points Calculation**:
$$
\begin{align}
P &= \frac{High + Low + Close}{3} \\
R_1 &= 2P - Low, \quad S_1 = 2P - High \\
R_2 &= P + (High - Low), \quad S_2 = P - (High - Low) \\
R_3 &= High + 2(P - Low), \quad S_3 = Low - 2(High - P)
\end{align}
$$
**Swing High/Low Identification**:

- Swing High: Highest point with 3-5 lower bars on each side
- Swing Low: Lowest point with 3-5 higher bars on each side
- Multiple tests without break = Strong level

---

## Derivatives Data Interpretation

### Funding Rate

| Dimension           | Observation                      | Meaning                                       |
| ------------------- | -------------------------------- | --------------------------------------------- |
| Positive / Negative | funding > 0 / < 0                | Direction of payment between longs and shorts |
| Absolute value      | High funding                     | Leveraged crowding + rising trading costs     |
| Persistence         | Long-term positive / negative    | Structural bullish / bearish market           |
| Relation to price   | funding ↑ + price ↑              | Healthy trend                                 |
|                     | funding ↑ + price ↓              | Squeezing / forced positioning structure      |
|                     | extreme funding + sideways price | Risk accumulation phase                       |

### Open Interest

| Pattern | Meaning | Implication |
|---------|---------|-------------|
| OI rising + Price rising | New longs entering | Uptrend confirmed |
| OI rising + Price falling | New shorts entering | Downtrend confirmed |
| OI falling + Price rising | Shorts covering | Uptrend may be weak |
| OI falling + Price falling | Longs liquidating | Downtrend may be weak |

### Liquidation Data

| Pattern | Meaning | Implication |
|---------|---------|-------------|
| Heavy long liquidations (side='sell') | Market crashed longs | Possible bottom forming |
| Heavy short liquidations (side='buy') | Market squeezed shorts | Possible top forming |
| Dense liquidations | Extreme move | Trend may reverse or accelerate |
| Sparse liquidations | Normal volatility | Trend likely continues |

### Judgement Based on Derivatives Data

| Price    | OI (Open Interest) | Funding Rate                          | Liquidation Tendency                          | Interpretation & Action                               |
| -------- | ------------------ | ------------------------------------- | --------------------------------------------- | ----------------------------------------------------- |
| Rising   | Rising             | Positive, moderately increasing       | Small short liquidations (scattered)          | Strong bullish trend, go long / hold longs            |
| Rising   | Falling            | Positive, declining from high         | Dense short liquidations (short covering bid) | Short squeeze-driven rebound, reduce longs            |
| Falling  | Rising             | Negative, steadily decreasing         | Small long liquidations (scattered)           | Strong bearish trend, short / hold shorts             |
| Falling  | Falling            | Negative, rebounding from extreme low | Dense long liquidations (long capitulation)   | Late-stage long flush, take profit on shorts          |
| Sideways | Flat or rising     | Extremely positive and not reverting  | Emerging long liquidation pressure            | Risk accumulation, reduce longs / consider short      |
| Sideways | Flat or rising     | Extremely negative and not recovering | Emerging short liquidation pressure           | Risk accumulation, reduce shorts / consider long      |
| Sideways | Sharp decline      | Returning toward neutral              | Dual liquidation already occurred             | Market reset, wait for OI recovery before positioning |
