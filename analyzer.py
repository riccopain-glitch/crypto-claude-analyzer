from anthropic import Anthropic
from typing import Dict, List
import json

class CryptoAnalyzer:
    """Uses Claude to analyze crypto data"""
    
    def __init__(self, api_key: str):
        self.client = Anthropic(api_key=api_key)
        self.conversation_history = []
    
    def analyze_bullish_signals(self, coin_data: Dict) -> str:
        """Analyze if a coin shows bullish signals"""
        prompt = f"""
Analyze this coin for EARLY BULLISH SIGNALS. Be concise and actionable.

Coin Data:
{json.dumps(coin_data, indent=2)}

Provide:
1. Bullish signal strength (High/Medium/Low)
2. Key reasons
3. Entry price recommendation
4. Target price (short term: 1-7 days)
5. Risk level

Be brief and direct.
"""
        return self._get_response(prompt)
    
    def analyze_portfolio(self, portfolio: Dict, market_data: Dict) -> str:
        """Analyze portfolio and give feedback on multiplication strategy"""
        prompt = f"""
Analyze this crypto portfolio and give strategic feedback on how to MULTIPLY it.

Portfolio:
{json.dumps(portfolio, indent=2)}

Current Market Data:
{json.dumps(market_data, indent=2)}

Provide:
1. Portfolio health assessment
2. Top 3 coins to increase allocation in
3. Coins to reduce/exit
4. Best strategy for multiplication (hold/trade/DCA)
5. Risk assessment
6. Specific action items

Be practical and specific.
"""
        return self._get_response(prompt)
    
    def analyze_new_coin(self, coin_info: Dict) -> str:
        """Analyze a new coin for sniping opportunity"""
        prompt = f"""
Evaluate this NEW COIN for sniping potential. Be quick and decisive.

Coin Info:
{json.dumps(coin_info, indent=2)}

Provide:
1. Snipe potential (Yes/No/Maybe)
2. Why/why not
3. If yes - suggested entry price
4. Quick exit price (1-3 days)
5. Risk level (High/Med/Low)

Be direct. Assume high volatility.
"""
        return self._get_response(prompt)
    
    def generate_buy_alert(self, coin: str, current_price: float, target_price: float, reason: str) -> str:
        """Generate a buy alert"""
        prompt = f"""
Generate a SHORT BUY ALERT for trading:

Coin: {coin}
Current Price: ${current_price}
Target Buy Price: ${target_price}
Reason: {reason}

Format as a 1-line alert ready to copy-paste to trading chat.
"""
        return self._get_response(prompt)
    
    def generate_sell_alert(self, coin: str, current_price: float, target_price: float, reason: str) -> str:
        """Generate a sell alert"""
        prompt = f"""
Generate a SHORT SELL ALERT for trading:

Coin: {coin}
Current Price: ${current_price}
Target Sell Price: ${target_price}
Reason: {reason}

Format as a 1-line alert ready to copy-paste to trading chat.
"""
        return self._get_response(prompt)
    
    def _get_response(self, prompt: str) -> str:
        """Get response from Claude"""
        self.conversation_history.append({
            "role": "user",
            "content": prompt
        })
        
        response = self.client.messages.create(
            model="claude-sonnet-5",
            max_tokens=1024,
            messages=self.conversation_history
        )
        
        # Handle thinking blocks and text blocks
        assistant_message = ""
        for block in response.content:
            if hasattr(block, 'text'):
                assistant_message = block.text
                break
        if not assistant_message:
            assistant_message = "Unable to analyze at this time"

        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })
        
        return assistant_message
