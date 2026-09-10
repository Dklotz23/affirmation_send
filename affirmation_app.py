import os
import sys
import smtplib
from email.mime.text import MIMEText
import logging
import requests


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger_file_handler = logging.handlers.RotatingFileHandler(
    "status.log",
    maxBytes=1024 * 1024,
    backupCount=1,
    encoding="utf8",
)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger_file_handler.setFormatter(formatter)
logger.addHandler(logger_file_handler)

try:
    DKLOTZ96182_GMAIL_APP_PW = os.environ["DKLOTZ96182_GMAIL_APP_PW"]
except KeyError:
    DKLOTZ96182_GMAIL_APP_PW = "Token not available!"

def send_sms_via_email(number, carrier_gateway, message_body):
    # Combine the number and gateway domain
    recipient_email = f"{number}@{carrier_gateway}"
    
    # Set up email server credentials
    sender_email = "dklotz96182@gmail.com"
    app_password = DKLOTZ96182_GMAIL_APP_PW
    app_password = "hwnd mtma gpja btzw" # Generated via Google Account security
    
    # Configure the message
    msg = MIMEText(message_body)
    msg['From'] = sender_email
    msg['To'] = recipient_email
    
    try:
        # Connect to Gmail's SMTP server
        server = smtplib.SMTP("://gmail.com", 587)
        server.starttls() # Secure the connection
        server.login(sender_email, app_password)
        
        # Send the message
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        print("Text message sent successfully!")
    except Exception as e:
        print(f"Failed to send text: {e}")

# Example usage: Sending a text to a Verizon phone number
#send_sms_via_email("1234567890", "vtext.com", "Hello! This is a free automated text.")

def fetch_affirmation():
    """
    Fetches a random positive affirmation from the free affirmations.dev API.
    Logs errors locally if the request fails.
    """
    url = "https://www.affirmations.dev"
    
    try:
        # Send a GET request to the API
        response = requests.get(url, timeout=10)
        
        # Raise an exception for HTTP errors (e.g., 404, 500)
        response.raise_for_status()
        
        # Parse the JSON response
        data = response.json()
        
        # Return the affirmation text
        return data.get("affirmation", "You are doing great!")
        
    except requests.exceptions.RequestException as e:
        # Automatically log the error to the local text file for background debugging
        logger.info(f"API Request failed: {e}")
        return None
    except ValueError as e:
        logger.info(f"Failed to parse JSON response: {e}")
        return None

if __name__ == "__main__":
    print("Fetching your daily affirmation...")
    affirmation = fetch_affirmation()
    
    if affirmation:
        msg = f"Todays Affirmation: {affirmation}"
        print(msg)
        send_sms_via_email(6097602333, "vtext.com", msg)
        logger.info(msg)
    else:
        logger.info(f"\n[Error] Could not fetch affirmation.")
