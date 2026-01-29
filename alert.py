import smtplib
from email.message import EmailMessage

def send_alert():
    msg = EmailMessage()
    msg.set_content("Poaching detected! Immediate attention required.")
    msg['Subject'] = 'ALERT: Poaching Detected'
    msg['From'] = 'evevoiceassistant@gmail.com'
    msg['To'] = 'charumca2325@bpibs.in'

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login('evevoiceassistant@gmail.com', 'your_password')
        smtp.send_message(msg)
