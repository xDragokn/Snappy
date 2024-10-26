import requests
from bs4 import BeautifulSoup
import os

# URL of the product page and Discord webhook URL
url = "https://ninjutso.com/products/snappyfire-8k-receiver?_pos=1&_sid=e0128d0dd&_ss=r"
webhook_url = os.environ.get("DISCORD_WEBHOOK_URL")

# Function to check if the item is in stock
def check_stock():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    
    # Ensure the request was successful
    print(f"Fetched page with status code: {response.status_code}")
    if response.status_code != 200:
        print(f"Failed to retrieve the page, status code: {response.status_code}")
        return
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Find the button and check if it indicates "Sold out" or "Order Now"
    stock_button = soup.find("button", {"data-product-id": "7046239387712"})
    if stock_button:
        print(f"Found stock button with text: {stock_button.text.strip()}")
        if stock_button.get("disabled") is not None or "Sold out" in stock_button.text:
            send_discord_notification(False)  # Notify that it's not in stock
        elif "Order Now" in stock_button.text:
            send_discord_notification(True)  # Notify that it's in stock
        else:
            print("Stock status unknown.")
    else:
        print("Could not find the stock button.")

# Function to send a notification to Discord
def send_discord_notification(is_in_stock):
    if not webhook_url:
        print("Discord webhook URL not provided.")
        return

    if is_in_stock:
        message = f":rotating_light: SnappyFire 8K Receiver is now in stock! @dragokn [Order Now]({url})"
    else:
        message = ":rotating_light: Product not in stock"
    
    data = {
        "content": message
    }
    
    # Debugging output to see what is being sent
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
