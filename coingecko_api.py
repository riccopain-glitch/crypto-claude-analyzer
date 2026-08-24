import requests
import time
from typing import Dict, List, Optional

class CoinGeckoAPI:
    """Free CoinGecko API wrapper - no auth key needed"""
    
    BASE_URL = "https://api.coingecko.com/api/v3"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'CryptoClaude-Bot/1.0'
        })
    
    def get_coin_data(self, coin_id: str) -> Optional[Dict]:
        """Get current data for a coin (free endpoint)"""
        try:
            url = f"{self.BASE_URL}/coins/{coin_id}"
            params = {
                'localization': False,
                'tickers': False,
                'market_data': True,
                'community_data': False,
                'developer_data': False,
                'sparkline': True
            }
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching {coin_id}: {e}")
            return None
    
    def get_trending_coins(self) -> Optional[List[Dict]]:
        """Get trending coins (great for early calls)"""
        try:
            url = f"{self.BASE_URL}/search/trending"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.json().get('coins', [])
        except Exception as e:
            print(f"Error fetching trending: {e}")
            return None
    
    def get_new_coins(self) -> Optional[List[Dict]]:
        """Get recently added coins (for sniping)"""
        try:
            url = f"{self.BASE_URL}/coins/markets"
            params = {
                'vs_currency': 'usd',
                'order': 'last_added',
                'per_page': 50,
                'page': 1,
                'sparkline': False
            }
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching new coins: {e}")
            return None
    
    def get_market_data(self, coin_ids: List[str]) -> Optional[Dict]:
        """Get market data for multiple coins"""
        try:
            url = f"{self.BASE_URL}/simple/price"
            params = {
                'ids': ','.join(coin_ids),
                'vs_currencies': 'usd',
                'include_market_cap': True,
                'include_24hr_vol': True,
                'include_24hr_change': True,
                'include_last_updated_at': True
            }
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching market data: {e}")
            return None
    
    def search_coin(self, query: str) -> Optional[List[Dict]]:
        """Search for a coin by name"""
        try:
            url = f"{self.BASE_URL}/search"
            params = {'query': query}
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json().get('coins', [])
        except Exception as e:
            print(f"Error searching coin: {e}")
            return None
