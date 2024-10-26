import requests

webhook_url = "https://discord.com/api/webhooks/1299602587619692595/EPdcJ3wBnrCYvH32wRTpdYuDwKCYp14BAtsROkYfoZDxtMea5Nf_mL7vBBAUGIscEVG1"
data = {"content": "Test message from stock checker script"}
response = requests.post(webhook_url, json=data)

if response.status_code == 204:
    print("Test message sent successfully.")
else:
    print("Failed to send test message.")
