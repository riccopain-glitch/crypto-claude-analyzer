import json
import time
from datetime import datetime
from typing import Dict, List
from coingecko_api import CoinGeckoAPI
from analyzer import CryptoAnalyzer
from config import *

class CryptoBot:
    """Main bot that monitors and analyzes crypto"""
    
    def __init__(self, api_key: str):
        self.coingecko = CoinGeckoAPI()
        self.analyzer = CryptoAnalyzer(api_key)
        self.tracked_coins = self._load_tracked_coins()
        self.alerts = []
    
    def _load_tracked_coins(self) -> Dict:
        """Load coins to track from file"""
        try:
            with open('tracked_coins.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Default coins to track
            return {
                'bitcoin': {'symbol': 'BTC', 'buy_price': 40000, 'sell_price': 45000},
                'ethereum': {'symbol': 'ETH', 'buy_price': 2000, 'sell_price': 2500},
                'solana': {'symbol': 'SOL', 'buy_price': 100, 'sell_price': 150},
            }
    
    def _save_tracked_coins(self):
        """Save tracked coins to file"""
        with open('tracked_coins.json', 'w') as f:
            json.dump(self.tracked_coins, f, indent=2)
    
    def check_trending_coins(self):
        """Check trending coins for early bullish signals"""
        print(f"\n[{datetime.now()}] Checking trending coins...")
        trending = self.coingecko.get_trending_coins()
        
        if not trending:
            print("Failed to fetch trending coins")
            return
        
        for coin in trending[:5]:  # Top 5 trending
            coin_id = coin['item']['id']
            coin_name = coin['item']['name']
            symbol = coin['item']['symbol'].upper()
            
            print(f"\n🔥 Analyzing {coin_name} ({symbol})...")
            
            # Get detailed data
            coin_data = self.coingecko.get_coin_data(coin_id)
            if coin_data:
                analysis = self.analyzer.analyze_bullish_signals(coin_data)
                print(f"Analysis: {analysis}")
                
                self.alerts.append({
                    'type': 'bullish_signal',
                    'coin': coin_name,
                    'symbol': symbol,
                    'analysis': analysis,
                    'timestamp': datetime.now().isoformat()
                })
                
                time.sleep(1)  # Rate limit
    
    def check_new_coins(self):
        """Check for new coin listings for sniping"""
        print(f"\n[{datetime.now()}] Checking new coins...")
        new_coins = self.coingecko.get_new_coins()
        
        if not new_coins:
            print("Failed to fetch new coins")
            return
        
        for coin in new_coins[:5]:  # Top 5 newest
            coin_name = coin.get('name', 'Unknown')
            symbol = coin.get('symbol', '?').upper()
            price = coin.get('current_price', 0)
            
            print(f"\n🆕 Analyzing {coin_name} ({symbol}) - ${price}")
            
            analysis = self.analyzer.analyze_new_coin(coin)
            print(f"Analysis: {analysis}")
            
            self.alerts.append({
                'type': 'new_coin',
                'coin': coin_name,
                'symbol': symbol,
                'price': price,
                'analysis': analysis,
                'timestamp': datetime.now().isoformat()
            })
            
            time.sleep(1)
    
    def check_price_alerts(self):
        """Check if tracked coins hit buy/sell prices"""
        print(f"\n[{datetime.now()}] Checking price alerts...")
        
        coin_ids = list(self.tracked_coins.keys())
        market_data = self.coingecko.get_market_data(coin_ids)
        
        if not market_data:
            print("Failed to fetch market data")
            return
        
        for coin_id, config in self.tracked_coins.items():
            if coin_id not in market_data:
                continue
            
            data = market_data[coin_id]
            current_price = data['usd']
            symbol = config['symbol']
            buy_price = config['buy_price']
            sell_price = config['sell_price']
            
            print(f"\n{symbol}: ${current_price}")
            
            # Check buy signal
            if current_price <= buy_price:
                alert = self.analyzer.generate_buy_alert(
                    symbol, current_price, buy_price,
                    f"Price at buy threshold"
                )
                print(f"🟢 BUY ALERT: {alert}")
                self.alerts.append({
                    'type': 'buy_alert',
                    'coin': symbol,
                    'price': current_price,
                    'alert': alert,
                    'timestamp': datetime.now().isoformat()
                })
            
            # Check sell signal
            if current_price >= sell_price:
                alert = self.analyzer.generate_sell_alert(
                    symbol, current_price, sell_price,
                    f"Price at sell threshold"
                )
                print(f"🔴 SELL ALERT: {alert}")
                self.alerts.append({
                    'type': 'sell_alert',
                    'coin': symbol,
                    'price': current_price,
                    'alert': alert,
                    'timestamp': datetime.now().isoformat()
                })
    
    def analyze_portfolio(self):
        """Analyze your portfolio"""
        print(f"\n[{datetime.now()}] Analyzing portfolio...")
        
        try:
            with open(PORTFOLIO_FILE, 'r') as f:
                portfolio = json.load(f)
        except FileNotFoundError:
            print(f"Portfolio file not found. Create {PORTFOLIO_FILE} first.")
            return
        
        # Get current market data for portfolio coins
        coin_ids = list(portfolio.keys())
        market_data = self.coingecko.get_market_data(coin_ids)
        
        if not market_data:
            print("Failed to fetch market data for portfolio")
            return
        
        analysis = self.analyzer.analyze_portfolio(portfolio, market_data)
        print(f"\nPortfolio Analysis:\n{analysis}")
        
        self.alerts.append({
            'type': 'portfolio_analysis',
            'analysis': analysis,
            'timestamp': datetime.now().isoformat()
        })
    
    def get_coin_info(self, coin_name: str):
        """Get general coin information"""
        print(f"\nFetching info for {coin_name}...")
        
        search_results = self.coingecko.search_coin(coin_name)
        if not search_results:
            print(f"Coin '{coin_name}' not found")
            return
        
        coin_id = search_results[0]['id']
        coin_data = self.coingecko.get_coin_data(coin_id)
        
        if coin_data:
            # Extract key info
            info = {
                'name': coin_data.get('name'),
                'symbol': coin_data.get('symbol', '').upper(),
                'price': coin_data.get('market_data', {}).get('current_price', {}).get('usd', 'N/A'),
                'market_cap': coin_data.get('market_data', {}).get('market_cap', {}).get('usd', 'N/A'),
                'volume_24h': coin_data.get('market_data', {}).get('total_volume', {}).get('usd', 'N/A'),
                'change_24h': coin_data.get('market_data', {}).get('price_change_percentage_24h', 'N/A'),
                'description': coin_data.get('description', {}).get('en', 'N/A')[:200]
            }
            
            print(json.dumps(info, indent=2))
            return info
    
    def run_continuous(self):
        """Run bot continuously"""
        print(f"🤖 CryptoBot started at {datetime.now()}")
        print(f"Checking every {CHECK_INTERVAL_MINUTES} minutes...\n")
        
        try:
            while True:
                self.check_trending_coins()
                time.sleep(2)
                
                self.check_new_coins()
                time.sleep(2)
                
                self.check_price_alerts()
                time.sleep(2)
                
                self.analyze_portfolio()
                
                # Save alerts
                self._save_alerts()
                
                print(f"\n⏳ Sleeping for {CHECK_INTERVAL_MINUTES} minutes...")
                time.sleep(CHECK_INTERVAL_MINUTES * 60)
        
        except KeyboardInterrupt:
            print("\n🛑 Bot stopped")
    
    def _save_alerts(self):
        """Save alerts to file"""
        with open('alerts.json', 'w') as f:
            json.dump(self.alerts[-50:], f, indent=2)  # Keep last 50 alerts


if __name__ == "__main__":
    if not CLAUDE_API_KEY:
        print("Error: CLAUDE_API_KEY not set in .env")
        exit(1)
    
    bot = CryptoBot(CLAUDE_API_KEY)
    
    # Run continuous monitoring
    bot.run_continuous()
