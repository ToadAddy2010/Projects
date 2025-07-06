import pandas as pd
from datetime import datetime
import random
import os
import smtplib
from email.mime.text import MIMEText

# Your email credentials and SMTP server info
MY_EMAIL = 'pythonsmtplibaddy@gmail.com'
MY_PASSWORD = os.environ.get("EMAIL_PASSWORD")
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587  # or 465 for SSL

# Load the CSV with birthdays and emails
df = pd.read_csv('birthdays.csv')

# Get today's month and day
today = datetime.today()
today_month = today.month
today_day = today.day

# Filter people whose birthday is today
matches = df[(df['month'] == today_month) & (df['day'] == today_day)]

if matches.empty:
    print("No birthdays today.")
else:
    template_dir = 'letter_templates'
    templates = [file for file in os.listdir(template_dir) if file.endswith('.txt')]

    for _, row in matches.iterrows():
        recipient_name = row['name']
        recipient_email = row['email']

        # Choose a random template
        chosen_template = random.choice(templates)
        template_path = os.path.join(template_dir, chosen_template)

        # Read and personalize the template
        with open(template_path, 'r', encoding='utf-8') as file:
            content = file.read()
        personalized_message = content.replace('[NAME]', recipient_name)

        # Create the email
        msg = MIMEText(personalized_message)
        msg['Subject'] = 'Happy Birthday!'
        msg['From'] = MY_EMAIL
        msg['To'] = recipient_email

        # Send the email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Secure the connection
            server.login(MY_EMAIL, MY_PASSWORD)
            server.sendmail(MY_EMAIL, recipient_email, msg.as_string())
            print(f"Sent birthday email to {recipient_name} at {recipient_email}")


