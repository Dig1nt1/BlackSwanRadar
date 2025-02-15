import yfinance as yf
import pandas as pd
import numpy as np
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# -------------------- EMAIL CONFIG --------------------
EMAIL_ADDRESS = "your-email@gmail.com"
EMAIL_PASSWORD = "your-app-password"
RECIPIENT_EMAIL = "your-email@gmail.com"

def send_email(subject, message):
    """Send an email alert for buy/sell signals."""
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = RECIPIENT_EMAIL
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, RECIPIENT_EMAIL, msg.as_string())
        server.quit()
        print(f"📩 Email Sent: {subject}")

    except Exception as e:
        print(f"❌ Email Failed: {e}")

# -------------------- STOCK ANALYSIS FUNCTIONS --------------------
def get_stock_data(ticker):
    """Fetch historical stock data."""
    stock = yf.Ticker(ticker)
    data = stock.history(period="3mo")
    return data

def calculate_indicators(data):
    """Calculate Z-Score, Bollinger Bands, MACD, and RSI."""
    data['Mean'] = data['Close'].rolling(window=20).mean()
    data['StdDev'] = data['Close'].rolling(window=20).std()
    data['Z-Score'] = (data['Close'] - data['Mean']) / data['StdDev']
    
    # Bollinger Bands
    data['BB_Upper'] = data['Mean'] + (2 * data['StdDev'])
    data['BB_Lower'] = data['Mean'] - (2 * data['StdDev'])

    # MACD Calculation
    short_ema = data['Close'].ewm(span=12, adjust=False).mean()
    long_ema = data['Close'].ewm(span=26, adjust=False).mean()
    data['MACD'] = short_ema - long_ema
    data['MACD_Signal'] = data['MACD'].ewm(span=9, adjust=False).mean()

    # RSI Calculation
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))

    return data

def detect_anomalies(data, ticker):
    """Detect anomalies using multiple indicators and send email alerts."""
    last_row = data.iloc[-1]

    zscore = last_row['Z-Score']
    macd = last_row['MACD']
    macd_signal = last_row['MACD_Signal']
    rsi = last_row['RSI']
    close_price = last_row['Close']

    print(f"\n🔍 Checking {ticker} for {data.index[-1]}")
    print(f"   📌 Z-Score: {zscore:.2f}")
    print(f"   📌 MACD: {macd:.2f}, MACD Signal: {macd_signal:.2f}")
    print(f"   📌 RSI: {rsi:.2f}")
    print(f"   📌 Close Price: {close_price:.2f}")

    # Buy Signal Conditions
    if zscore < -2 and rsi < 30 and macd > macd_signal and close_price < last_row['BB_Lower']:
        print(f"📈 BUY SIGNAL: {close_price:.2f}")
        subject = f"🚀 Buy Alert: {ticker} - {data.index[-1]}"
        message = f"Stock {ticker} is oversold! 📈\n\n- Z-Score: {zscore:.2f}\n- RSI: {rsi:.2f}\n- MACD: {macd:.2f}\n- Close Price: {close_price:.2f}"
        send_email(subject, message)

    # Sell Signal Conditions
    if zscore > 2 and rsi > 70 and macd < macd_signal and close_price > last_row['BB_Upper']:
        print(f"📉 SELL SIGNAL: {close_price:.2f}")
        subject = f"⚠️ Sell Alert: {ticker} - {data.index[-1]}"
        message = f"Stock {ticker} is overbought! 📉\n\n- Z-Score: {zscore:.2f}\n- RSI: {rsi:.2f}\n- MACD: {macd:.2f}\n- Close Price: {close_price:.2f}"
        send_email(subject, message)

# -------------------- MAIN FUNCTION --------------------
def run_bot(ticker):
    """Run the full stock anomaly detection bot."""
    print(f"🚀 Running Anomaly Detection for {ticker}")
    data = get_stock_data(ticker)
    data = calculate_indicators(data)
    detect_anomalies(data, ticker)

# -------------------- RUN SCRIPT --------------------
if __name__ == "__main__":
    # Test email functionality
    send_email("Test Email", "This is a test message to check if email alerts are working.")

    # Run stock anomaly detection
    ticker = "ITC.NS"  # Change to any stock ticker
    run_bot(ticker)
