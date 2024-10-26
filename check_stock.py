import requests
from bs4 import BeautifulSoup
import time

# URL of the product page and Discord webhook URL
url = "https://ninjutso.com/products/snappyfire-8k-receiver?_pos=1&_sid=e0128d0dd&_ss=r"
webhook_url = "https://discord.com/api/webhooks/1299602587619692595/EPdcJ3wBnrCYvH32wRTpdYuDwKCYp14BAtsROkYfoZDxtMea5Nf_mL7vBBAUGIscEVG1"

# Function to check if the item is in stock
def check_stock():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Find the stock button and check its text
    stock_button = soup.find("button", class_="button-class-name")  # Replace with actual class name if necessary
    if stock_button and "order now" in stock_button.text.lower():
        send_discord_notification()
    else:
        print("Still sold out, checking again...")

# Function to send a notification to Discord
def send_discord_notification():
    data = {
        "content": "🚨 SnappyFire 8K Receiver is now in stock! [Order Now]({})".format(url)
    }
    response = requests.post(webhook_url, json=data)
    if response.status_code == 204:
        print("Notification sent to Discord.")
    else:
        print("Failed to send notification.")

# Main loop to check stock every 60 seconds
while True:
    check_stock()
    time.sleep(60)
