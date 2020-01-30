import os
import requests

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_API_URL = os.getenv('TELEGRAM_API_URL')
API_URL = os.getenv('API_URL')
BASE_URL = f'{TELEGRAM_API_URL}/bot{TELEGRAM_TOKEN}'

def handle_message(message, chat_id):
    print(f'message >>\n{message}')
    url = f'{BASE_URL}/sendMessage'
    r = requests.post(url, data={'chat_id': chat_id, 'text': 'eu bot'}) 
    data = r.json() 
    return data
    
def set_webhook():
    url = f'{BASE_URL}/setWebhook'
    r = requests.post(url, data={'url': f'{API_URL}/{TELEGRAM_TOKEN}'}) 
    data = r.json() 
    print(f'Set Webhook >>\n{data}')
    return

def healthcheck():
    url = f'{BASE_URL}/getMe'
    r = requests.get(url) 
    data = r.json() 
    print(f'Healthcheck >>\n{data}')
    return data