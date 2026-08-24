from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from analyzer import CryptoAnalyzer
import os
import threading
import time
import requests
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'crypto-dashboard-secret'
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize analyzer
API_KEY = os.getenv("ANTHROPIC_API_KEY")
analyzer = CryptoAnalyzer(API_KEY)

# Store coin data
coin_data_store = {}
analysis_store = {}

def get_trending_coins():
    """Fetch trending coins from CoinGecko"""
    try:
        url = "https://api.coingecko.com/api/v3/search/trending"
        response = requests.get(url, timeout=5)
        data = response.json()
        coins = []
        for item in data.get('coins', [])[:5]:  # Get top 5
            coin_info = item['item']
            coins.append({
                'id': coin_info['id'],
                'name': coin_info['name'],
                'symbol': coin_info['symbol'].upper(),
                'image': coin_info['image'],
                'market_cap_rank': coin_info.get('market_cap_rank'),
                'data': coin_info['data']
            })
        return coins
    except Exception as e:
        print(f"Error fetching trending coins: {e}")
        return []

def get_coin_details(coin_id):
    """Get detailed price and market data for a coin"""
    try:
        url = f"https://api.coingecko.com/api/v3/coins/{coin_id}?localization=false&market_data=true&community_data=false&developer_data=false&sparkline=true"
        response = requests.get(url, timeout=5)
        data = response.json()
        
        return {
            'name': data.get('name'),
            'symbol': data.get('symbol', '').upper(),
            'image': data.get('image', {}).get('large'),
            'price': data.get('market_data', {}).get('current_price', {}).get('usd', 0),
            'market_cap': data.get('market_data', {}).get('market_cap', {}).get('usd', 0),
            'volume_24h': data.get('market_data', {}).get('total_volume', {}).get('usd', 0),
            'price_change_24h': data.get('market_data', {}).get('price_change_percentage_24h', 0),
            'price_change_7d': data.get('market_data', {}).get('price_change_percentage_7d', 0),
            'sparkline': data.get('market_data', {}).get('sparkline_7d', {}).get('price', []),
            'all_time_high': data.get('market_data', {}).get('ath', {}).get('usd', 0),
            'all_time_low': data.get('market_data', {}).get('atl', {}).get('usd', 0),
        }
    except Exception as e:
        print(f"Error fetching coin details for {coin_id}: {e}")
        return None

def analyze_coin_worker(coin_id, coin_symbol, coin_data):
    """Analyze coin with Claude in background"""
    try:
        analysis = analyzer.analyze_bullish_signals({
            'symbol': coin_symbol,
            'price': coin_data.get('price'),
            'market_cap': coin_data.get('market_cap'),
            'volume_24h': coin_data.get('volume_24h'),
            'price_change_24h': coin_data.get('price_change_24h'),
            'price_change_7d': coin_data.get('price_change_7d'),
        })
        
        analysis_store[coin_id] = {
            'status': 'ready',
            'analysis': analysis
        }
        
        socketio.emit('analysis_update', {
            'coin_id': coin_id,
            'analysis': analysis
        })
    except Exception as e:
        print(f"Error analyzing {coin_symbol}: {e}")
        analysis_store[coin_id] = {
            'status': 'error',
            'analysis': f"Error analyzing coin: {str(e)}"
        }

def update_dashboard():
    """Update dashboard with trending coins"""
    while True:
        try:
            coins = get_trending_coins()
            
            for coin in coins:
                coin_id = coin['id']
                
                # Get detailed data
                details = get_coin_details(coin_id)
                if details:
                    coin_data_store[coin_id] = {
                        **coin,
                        **details
                    }
                    
                    # Emit update to frontend
                    socketio.emit('coin_update', coin_data_store[coin_id])
                    
                    # Analyze if not already analyzing
                    if coin_id not in analysis_store:
                        analysis_store[coin_id] = {'status': 'analyzing', 'analysis': '...'}
                        thread = threading.Thread(
                            target=analyze_coin_worker,
                            args=(coin_id, coin['symbol'], details)
                        )
                        thread.daemon = True
                        thread.start()
            
            time.sleep(30)  # Update every 30 seconds
        except Exception as e:
            print(f"Dashboard update error: {e}")
            time.sleep(30)

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/api/coins')
def api_coins():
    return json.dumps(coin_data_store)

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    # Send current data
    for coin_id, coin_data in coin_data_store.items():
        emit('coin_update', coin_data)
        if coin_id in analysis_store:
            emit('analysis_update', {
                'coin_id': coin_id,
                'analysis': analysis_store[coin_id]['analysis']
            })

if __name__ == '__main__':
    # Start dashboard update thread
    thread = threading.Thread(target=update_dashboard)
    thread.daemon = True
    thread.start()
    
    print("🌐 Dashboard starting at http://localhost:5000")
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
