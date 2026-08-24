# 🤖 Crypto Claude Analyzer Bot

A free crypto trading analysis bot that gives you:
- ✅ Early bullish coin signals
- ✅ New coin info for sniping
- ✅ Coin information lookup
- ✅ Portfolio analysis & multiplication feedback
- ✅ Buy/Sell price alerts

**100% Free** - Uses only free APIs (CoinGecko) + Claude AI

## Setup

### 1. Get Claude API Key
- Go to https://console.anthropic.com/
- Create account or login
- Get your API key
- Copy it to `.env` file (see below)

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Bot

**Create `.env` file:**
```
CLAUDE_API_KEY=your_key_here
```

**Create `portfolio.json` (optional):**
```bash
cp portfolio.json.example portfolio.json
# Edit with your actual holdings
```

**Create `tracked_coins.json` (optional):**
```bash
cp tracked_coins.json.example tracked_coins.json
# Edit with your buy/sell prices
```

### 4. Run Bot
```bash
python bot.py
```

The bot will:
- Check trending coins for early bullish signals
- Monitor new coin listings for sniping opportunities
- Track your custom coins and alert on buy/sell prices
- Analyze your portfolio every cycle
- Save alerts to `alerts.json`

## How It Works

### Bullish Signals
Bot checks top 5 trending coins and uses Claude to analyze:
- Technical indicators
- Volume patterns
- Price momentum
- Entry/target prices

### New Coin Sniping
Monitors newly listed coins and evaluates:
- Liquidity
- Market cap
- Sniping viability
- Quick exit prices

### Price Alerts
Set buy/sell prices in `tracked_coins.json`:
- Get alerts when prices hit targets
- Formatted ready-to-copy for trading

### Portfolio Analysis
Claud AI analyzes your portfolio and recommends:
- Best coins to increase allocation
- Coins to reduce/exit
- Multiplication strategies
- Risk assessment

## API Limits

**CoinGecko Free:**
- 10-50 calls/minute (no auth needed)
- Perfect for hourly/5-minute checks

**Claude API:**
- Pay-per-token (very cheap)
- ~$0.03 per analysis call

## Customization

Edit `config.py` to change:
- Check interval (currently 5 minutes)
- Number of coins to track
- Price alert thresholds
- Analysis parameters

## Alerts

All alerts saved to `alerts.json` with timestamps. Use this to:
- Review past signals
- Track bot performance
- Export to Discord/Telegram webhook

## Limitations

- No actual trade execution (informational only)
- Depends on free CoinGecko API (may have rate limits)
- Portfolio analysis requires manual setup

## Next Steps

1. Add Discord webhook for real-time notifications
2. Add wallet tracking via Etherscan
3. Add technical indicators (RSI, MACD)
4. Add exchange order book analysis
5. Integrate with actual exchange APIs for execution

## Support

This bot is completely free and uses only free APIs.

Claude API costs:
- Input: ~$3 per 1M tokens
- Output: ~$15 per 1M tokens
- Realistic monthly cost: $5-20 depending on usage
