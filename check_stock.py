import requests
from bs4 import BeautifulSoup
import os

# URL of the product page
url = "https://ninjutso.com/products/snappyfire-8k-receiver?_pos=1&_sid=e0128d0dd&_ss=r"

# Get Discord webhook URL from environment variable
webhook_url = os.environ.get("DISCORD_WEBHOOK_URL")

# Function to check if the item is in stock
def check_stock():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    
    print(f"Fetched page with status code: {response.status_code}")
    if response.status_code != 200:
        print(f"Failed to retrieve the page, status code: {response.status_code}")
        return
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Find the stock button
    stock_button = soup.find("button", {"data-product-id": "7046239387712"})
    if stock_button:
        button_text = stock_button.text.strip().lower()
        print(f"Found stock button with text: '{button_text}'")
        print(f"Stock button HTML: {stock_button}")
        
        # Use the 'disabled' attribute to determine stock status
        if stock_button.get("disabled"):
            send_discord_notification(False)
        else:
            send_discord_notification(True)
    else:
        print("Could not find the stock button.")

# Function to send a notification to Discord
def send_discord_notification(is_in_stock):
    if not webhook_url:
        print("Discord webhook URL not provided.")
        return
    else:
        print(f"Webhook URL length: {len(webhook_url)} characters")

    if is_in_stock:
        message = f":rotating_light: SnappyFire 8K Receiver is now in stock! <@325536985454477322> [Order Now]({url})"
    else:
        message = ":rotating_light: Product not in stock"
    
    data = {
        "content": message
    }
    
    print(f"Sending message: {message}")
    
    response = requests.post(webhook_url, json=data)
    if response.status_code in [200, 204]:
        print("Notification sent to Discord.")
    else:
        print(f"Failed to send notification, status code: {response.status_code}")
        print(f"Response: {response.text}")

# Run the stock check once
if __name__ == "__main__":
    check_stock()
