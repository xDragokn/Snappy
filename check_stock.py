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
    
    # Find the button and check if it indicates "Sold out" or "Order Now"
    stock_button = soup.find("button", {"data-product-id": "7046239387712"})  # Adjust to match product ID
    if stock_button:
        if stock_button.get("disabled") is not None or "Sold out" in stock_button.text:
            send_discord_notification(False)  # Notify that it's not in stock
        elif "Order Now" in stock_button.text:
            send_discord_notification(True)  # Notify that it's in stock
    else:
        print("Could not find the stock button, checking again...")

# Function to send a notification to Discord
def send_discord_notification(is_in_stock):
    if is_in_stock:
        message = f"🚨 SnappyFire 8K Receiver is now in stock! <@325536985454477322> [Order Now]({url})"
    else:
        message = "🚨 Product not in stock"
    
    data = {
        "content": message
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
