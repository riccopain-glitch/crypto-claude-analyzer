import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
CLAUDE_API_KEY = os.getenv('CLAUDE_API_KEY')
ETHERSCAN_API_KEY = os.getenv('ETHERSCAN_API_KEY', '')  # Optional, free tier available

# Bot Settings
CHECK_INTERVAL_MINUTES = 5  # Check every 5 minutes (not every minute to avoid rate limits)
MAX_COINS_TO_TRACK = 50

# Portfolio Settings
PORTFOLIO_FILE = 'portfolio.json'  # You'll create this
WALLET_ADDRESS = os.getenv('WALLET_ADDRESS', '')  # Ethereum wallet for tracking

# Price Alert Thresholds (you'll customize these)
ALERT_THRESHOLDS = {
    'bullish_rsi_threshold': 30,  # RSI below 30 = oversold/potential bullish
    'price_change_24h': 5,  # Alert if 24h change > 5%
    'volume_spike': 20,  # Alert if volume spike > 20%
}
