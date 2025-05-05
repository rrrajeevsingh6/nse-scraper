import requests
import time
import schedule

# ✅ Telegram Bot credentials (embedded directly)
BOT_TOKEN = '7531795553:AAGi7B-cOGQflaKMEX6sBKEIECRFqhPGZ5M'
CHANNEL_ID = '@TradeMastermindTips'

def send_alert(message):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    payload = {
        'chat_id': CHANNEL_ID,
        'text': message
    }
    try:
        response = requests.post(url, data=payload)
        print(f"Telegram sent: {response.status_code}")
    except Exception as e:
        print(f"Telegram error: {e}")

def fetch_option_chain(symbol):
    url = f'https://www.nseindia.com/api/option-chain-indices?symbol={symbol}'
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://www.nseindia.com/option-chain'
    }
    session = requests.Session()
    session.get('https://www.nseindia.com', headers=headers)
    res = session.get(url, headers=headers)
    data = res.json()
    return data

def process():
    for symbol in ['NIFTY', 'BANKNIFTY']:
        try:
            data = fetch_option_chain(symbol)
            send_alert(f'✅ {symbol} Option Chain fetched successfully')
        except Exception as e:
            send_alert(f'❌ {symbol} fetch failed: {e}')

schedule.every(1).minutes.do(process)

while True:
    schedule.run_pending()
    time.sleep(1)
