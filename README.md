# BlackSwanRadar
BlackSwanRadar is an intelligent stock anomaly detection bot that uses advanced Z-Score, Bollinger Bands, MACD, and RSI indicators to spot buy and sell signals before the market reacts.

🔹 Features:

✅ Automated stock data retrieval via Yahoo Finance

✅ Smart anomaly detection with multi-indicator analysis

✅ Real-time email alerts for buy/sell signals

✅ Python-powered financial insights

**Anomalies Detection Conditions in the Code. 
The script detects buy and sell anomalies based on four indicators:**

Z-Score (Statistical measure of deviation from the mean)

MACD & MACD Signal (Trend-following momentum indicator)

RSI (Relative Strength Index) (Momentum indicator for overbought/oversold levels)

Bollinger Bands (Measures price volatility)

🚀 Buy Signal (Oversold Condition)
A BUY signal is triggered when all the following conditions are met:

Z-Score < -2 (Stock price is significantly below its average, indicating it's undervalued)
RSI < 30 (Stock is oversold, indicating potential price reversal)
MACD > MACD Signal (Momentum shift towards an uptrend)
Close Price < Lower Bollinger Band (Stock is trading below its usual volatility range)
✅ If all these conditions are met, the script sends a Buy Alert email.

⚠️ Sell Signal (Overbought Condition)
A SELL signal is triggered when all the following conditions are met:

Z-Score > 2 (Stock price is significantly above its average, indicating it's overvalued)
RSI > 70 (Stock is overbought, indicating potential price drop)
MACD < MACD Signal (Momentum shift towards a downtrend)
Close Price > Upper Bollinger Band (Stock is trading above its usual volatility range)
✅ If all these conditions are met, the script sends a Sell Alert email.

🔍 Summary of Conditions
Condition	Buy Signal (📈)	Sell Signal (📉)
Z-Score	< -2 (Undervalued)	> 2 (Overvalued)
RSI	< 30 (Oversold)	> 70 (Overbought)
MACD vs Signal	MACD > MACD Signal	MACD < MACD Signal
Close Price	< Lower Bollinger Band	> Upper Bollinger Band
