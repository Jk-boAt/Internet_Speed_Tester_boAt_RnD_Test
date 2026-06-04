import os
from datetime import datetime
from mail_sender import send_summary_email

# Jenkins Workspace Log File
#LOG_FILE = r"C:\ProgramData\Jenkins\.jenkins\workspace\Internet_Speed_Tester_boAtRnD_BangaloreOffice\internet_alerts.log"

LOG_FILE = r"C:\InternetMonitor\internet_alerts.log"


def read_log_file():

    if not os.path.exists(LOG_FILE):
        print("Log file not found.")
        return None

    with open(LOG_FILE, "r", encoding="utf-8") as file:
        content = file.read()

    if not content.strip():
        print("No incidents found.")
        return None

    return content


def clear_log_file():

    with open(LOG_FILE, "w", encoding="utf-8") as file:
        file.write("")


if __name__ == "__main__":

    print("\n===== Hourly Internet Summary =====\n")

    log_content = read_log_file()

    if log_content is None:
        print("Nothing to send.")
        exit(0)

    try:

        summary_header = f"""
Internet Monitoring Summary Report

Generated Time : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

========================================================
"""

        email_content = summary_header + "\n" + log_content

        send_summary_email(email_content)

        clear_log_file()

        print("Summary email sent successfully.")
        print("Log file cleared.")

    except Exception as e:

        print("Failed to send email.")
        print(str(e))
        
