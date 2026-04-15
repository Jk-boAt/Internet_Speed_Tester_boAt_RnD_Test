import sys

try:
    sys.stdout.reconfigure(encoding='utf-8')
except:
    pass

import speedtest
import subprocess
from mail_sender import send_alert_email
import time

MIN_DOWNLOAD = 30
MIN_UPLOAD = 30
MAX_PING = 80

def get_wifi_name():
    try:
        output = subprocess.check_output("netsh wlan show interfaces", shell=True).decode()
        for line in output.split("\n"):
            if "SSID" in line and "BSSID" not in line:
                return line.split(":")[1].strip()
    except:
        return "Unknown"

def run_speed_test():
    for i in range(3):  # retry 3 times
        try:
            st = speedtest.Speedtest(secure=True)
            st.get_best_server()

            download = round(st.download() / 1000000, 2)
            upload = round(st.upload() / 1000000, 2)
            ping = round(st.results.ping, 2)

            return download, upload, ping

        except Exception as e:
            print(f"Retry {i+1} failed:", e)
            time.sleep(5)

    raise Exception("Speedtest failed after retries")


def check_alert(download, upload, ping):
       
    alerts = []

    if download < MIN_DOWNLOAD:
        alerts.append(f"Low Download Speed: {download} Mbps")

    if upload < MIN_UPLOAD:
        alerts.append(f"Low Upload Speed: {upload} Mbps")

    if ping > MAX_PING:
        alerts.append(f"High Ping: {ping} ms")

    return alerts

if __name__ == "__main__":
    print("\n===== Internet Speed Test Report =====\n")

    wifi = get_wifi_name()
    d, u, p = run_speed_test()
    alerts = check_alert(d, u, p)

    print(f"📶 WiFi Name       : {wifi}")
    print(f"⬇️ Download Speed : {d} Mbps")
    print(f"⬆️ Upload Speed   : {u} Mbps")
    print(f"📡 Ping (Latency) : {p} ms")

    print("\n-------------------------------------")
    
    #TARGET_WIFI = "Jk's iQOO"
    TARGET_WIFI = "IMAGINE"

    if alerts:
        print("ALERT DETECTED:")
        for alert in alerts:
            print(alert)

        if wifi == TARGET_WIFI:
            print("WiFi matched. Sending alert email...")
            send_alert_email(d, u, p, alerts, wifi,
                             MIN_DOWNLOAD, MIN_UPLOAD, MAX_PING)
        else:
            print(f"WiFi '{wifi}' is not target. Skipping email.")

#     if alerts:
#         print("🚨 ALERT DETECTED:")
#         for alert in alerts:
#             print(f"⚠️ {alert}")
#         send_alert_email(d, u, p, alerts, wifi,
#                  MIN_DOWNLOAD, MIN_UPLOAD, MAX_PING)
    else:
        print("✅ Internet Status: GOOD")

    print("\n=====================================\n")