import requests
from config import telegram_api , telegram_developer_id

TELEGRAM_BOT_TOKEN = telegram_api
TELEGRAM_DEVELOPER_ID = telegram_developer_id

#Chat id for channels or groups, you should add your bot to the channel or group and get the chat id
#check youtube for more information.
TELEGRAM_CHAT_ID = "----------------------------"  

# Telegram'a bildirim gönderen fonksiyon
def send_telegram_notification(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    response = requests.post(url, data=data)


def send_message_to_developer(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_DEVELOPER_ID,
        "text": message
    }
    response = requests.post(url, data=data)

send_message_to_developer("Trade bot starts")