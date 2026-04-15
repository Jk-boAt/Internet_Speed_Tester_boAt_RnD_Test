import sys

try:
    sys.stdout.reconfigure(encoding='utf-8')
except:
    pass

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

EMAIL_SENDER = "boatqatest@gmail.com"
EMAIL_PASSWORD = "cdcjeeydsnaeslzo"
#EMAIL_RECEIVER = ["jayakumar.v@imaginemarketingindia.com", "naveen.m@imaginemarketingindia.com", "rasiq.khan@imaginemarketingindia.com"]
EMAIL_RECEIVER = ["jayakumar.v@imaginemarketingindia.com"]


def send_alert_email(download, upload, ping, alerts, wifi_name,
min_download, min_upload, max_ping):

    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    subject = "🚨 [ALERT] Internet Issue Detected at boAt R&D Office 🚨"

    message = f"""Hi Team,

Internet issue detected at Bangalore boAt R&D office.

📶 Network Details:
Time: {now}
WiFi: {wifi_name}

📊 Current Speed:
Download: {download} Mbps
Upload: {upload} Mbps
Ping: {ping} ms

⚙️ Configured Thresholds:
Min Download : {min_download} Mbps
Min Upload : {min_upload} Mbps
Max Ping : {max_ping} ms

Alerts:
"""
    for alert in alerts:
        message += f"- {alert}\n"

    message += """

Please check the network.

Regards,
boAt R&D - Internet Monitor Bot
"""

    msg = MIMEMultipart()
    msg["From"] = EMAIL_SENDER
    msg["To"] = ", ".join(EMAIL_RECEIVER)
    msg["Subject"] = subject
    msg.attach(MIMEText(message, "plain"))

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(EMAIL_SENDER, EMAIL_PASSWORD)
    server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
    server.quit()

    print("📧 Alert email sent!")