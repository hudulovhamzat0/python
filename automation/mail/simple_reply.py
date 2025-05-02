import imaplib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
from email.header import decode_header
import re

IMAP_SERVER = "imap.gmail.com"
SMTP_SERVER = "smtp.gmail.com"
EMAIL_ACCOUNT = "your_email@gmail.com"
EMAIL_PASSWORD = "your_password"

def check_emails():
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
    mail.select('inbox')

    status, emails = mail.search(None, '(UNSEEN)')
    email_ids = emails[0].split()

    for email_id in email_ids:
        status, email_data = mail.fetch(email_id, "(RFC822)")
        raw_email = email_data[0][1].decode("utf-8")

        subject, sender = parse_email(raw_email)
        sender_name = extract_name(sender)
        send_reply(sender, sender_name)

def parse_email(raw_email):
    subject = re.search(r"Subject: (.*?)\r\n", raw_email)
    subject = decode_header(subject.group(1))[0][0].decode() if subject else "No Subject"
    sender = re.search(r"From: (.*?)\r\n", raw_email)
    sender = sender.group(1) if sender else "No Sender"
    return subject, sender

def extract_name(sender):
    match = re.search(r"([^@]+)", sender)
    return match.group(1).capitalize() if match else "Customer"

def send_reply(recipient_email, sender_name):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ACCOUNT
    msg['To'] = recipient_email
    msg['Subject'] = "Re: Your Inquiry"

    reply_text = f"Hello {sender_name},\n\nWe will answer your mail in a few days! Thanks for mailing us.\n\nBest regards,\nYour Support Team"
    msg.attach(MIMEText(reply_text, 'plain'))

    server = smtplib.SMTP(SMTP_SERVER, 587)
    server.starttls()
    server.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
    text = msg.as_string()
    server.sendmail(EMAIL_ACCOUNT, recipient_email, text)
    server.quit()

while True:
    check_emails()
    time.sleep(60)
