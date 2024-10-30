import requests
from bs4 import BeautifulSoup
import os

# URL of the product page
url = "https://ninjutso.com/products/snappyfire-8k-receiver"

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
    
    # Check the product availability from the meta tag
    availability_tag = soup.find("meta", {"property": "product:availability"})
    if availability_tag:
        availability = availability_tag["content"]
        print(f"Product availability: {availability}")

        if availability == "instock":
            send_discord_notification()  # Notify that it's in stock
        else:
            print("Product is not in stock.")
    else:
        print("Could not find the product availability tag.")

# Function to send a notification to Discord
def send_discord_notification():
    if not webhook_url:
        print("Discord webhook URL not provided.")
        return

    message = f":rotating_light: SnappyFire 8K Receiver is now in stock! @everyone [Order Now]({url})"
    
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

