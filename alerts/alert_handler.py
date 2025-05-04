import smtplib
from twilio.rest import Client
def send_email_alert(product):
    # Email configuration
    sender_email = "your_email@gmail.com"
    receiver_email = "receiver_email@gmail.com"
    password = "your_email_password"
    message = f"Alert! The product '{product['name']}' is out of stock or has a price drop."
    
    # Create the email
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
def send_sms_alert(product):
    # Twilio configuration
    account_sid = 'your_account_sid'
    auth_token = 'your_auth_token'
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=f"Alert! The product '{product['name']}' is out of stock or has a price drop.",
        from_='your_twilio_number',
        to='receiver_phone_number'
    )