# CRT Trading Strategy - ZForex Methodology

## Core Principles

This strategy is based on **Candle Range Theory (CRT)** as taught by the ZForex channel.

### Reference
- YouTube Channel: https://www.youtube.com/@zforeex
- Methodology: CRT (Candle Range Theory)

## Strategy Overview

### Primary Concept
CRT is a price action methodology focused on:
- Liquidity manipulation
- Range identification
- Structural alignment
- Multi-timeframe confirmation

### Key Components

1. **Structure Analysis (H4)**
   - Primary trend direction
   - Major support/resistance levels
   - Liquidity pools (PDH/PDL)
   
2. **Pattern Recognition**
   - R-Pattern identification
   - Manipulation detection
   - Consolidation zones
   
3. **Execution Criteria**
   - H4 structure aligned
   - M15 displacement confirmed
   - M5 retest validated
   - Liquidity swept
   
## Entry Rules

### Prerequisites (ALL must be met)
1. H4 structure clearly bullish or bearish
2. Multi-asset correlation aligned
3. M15 shows clear displacement
4. M5 confirms retest of swept liquidity
5. Risk/Reward >= 2.0

### Entry Checklist
- [ ] H4 trend identified
- [ ] Liquidity levels marked
- [ ] Sweep confirmed
- [ ] M15 displacement validated
- [ ] M5 retest complete
- [ ] RR ratio calculated
- [ ] Risk percentage within limits

## Exit Rules

### Take Profit
- Minimum RR: 2.0
- Target: Opposite liquidity level
- Partial profit: 50% at 1.5 RR

### Stop Loss
- Below/above swept liquidity
- Maximum risk: 2% per trade

### Trade Management
- Move to breakeven at 1% profit
- Trail stop at 50% of current profit

## Risk Management

### Position Sizing
- Max risk per trade: 2%
- Max daily drawdown: 5%
- Max total drawdown: 10%
- Max concurrent positions: 3

### Defensive Rules
- Stop trading after 3 consecutive losses
- Reduce size by 50% in high volatility
- No trading during major news events
- No revenge trading

## Timeframe Structure

### Multi-Timeframe Analysis
- **H4**: Primary structure and trend
- **H1**: Secondary confirmation
- **M15**: Entry displacement
- **M5**: Precise entry timing

### Layout Configuration
- Layout 1: H4 + H1 (macro structure)
- Layout 2: M15 (operational)
- Layout 3: M5 (execution)

## Trading Sessions

### Preferred Sessions
- London: 08:00-12:00 UTC
- New York: 13:00-17:00 UTC
- Overlap: 13:00-16:00 UTC (best)

### Avoid Trading
- Low liquidity hours
- Major news releases
- Market open/close volatility

## Performance Metrics

### Target Metrics
- Win rate: >= 60%
- Profit factor: >= 2.0
- Max drawdown: <= 10%
- Risk/Reward: >= 2.0

### Monthly Goals
- Minimum trades: 20
- Maximum drawdown: 8%
- Consistency: > 80% of days profitable

## Continuous Improvement

### After Each Trade
- Log trade context
- Review decision process
- Identify improvements
- Update pattern library

### Weekly Review
- Calculate performance metrics
- Identify recurring mistakes
- Adjust parameters if needed
- Review correlation patterns

## Integration with AntiGravity System

This strategy is enforced through:

1. **DecisionEngine**: Validates H4 structure and multi-timeframe alignment
2. **RiskEngine**: Enforces risk limits and drawdown controls
3. **DrawdownGuard**: Manages active positions with trailing stops
4. **TradeJournal**: Records all trades for analysis
5. **PerformanceTracker**: Monitors adherence to strategy rules

---

**Remember**: The system follows ZForex CRT methodology strictly. When in doubt, consult the ZForex YouTube channel for clarification.
