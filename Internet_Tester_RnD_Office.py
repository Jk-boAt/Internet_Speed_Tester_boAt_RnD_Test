import sys
import os
import time
import speedtest
import subprocess
from datetime import datetime

try:
    sys.stdout.reconfigure(encoding='utf-8')
except:
    pass

MIN_DOWNLOAD = 30
MIN_UPLOAD = 30
MAX_PING = 80

TARGET_WIFI = "IMAGINE"

LOG_FILE = r"C:\InternetMonitor\internet_alerts.log"


def get_wifi_name():
    try:
        output = subprocess.check_output(
            "netsh wlan show interfaces",
            shell=True
        ).decode()

        for line in output.split("\n"):
            if "SSID" in line and "BSSID" not in line:
                return line.split(":")[1].strip()

    except:
        return "Unknown"

    return "Unknown"


def log_alert(message):

    os.makedirs(
        os.path.dirname(LOG_FILE),
        exist_ok=True
    )

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    with open(
        LOG_FILE,
        "a",
        encoding="utf-8"
    ) as f:

        f.write("\n")
        f.write("=" * 30)
        f.write("\n")
        f.write(f"[{timestamp}]\n")
        f.write(message)
        f.write("\n")


def run_speed_test():

    for i in range(3):

        try:

            st = speedtest.Speedtest(
                secure=True
            )

            st.get_best_server()

            download = round(
                st.download() / 1000000,
                2
            )

            upload = round(
                st.upload() / 1000000,
                2
            )

            ping = round(
                st.results.ping,
                2
            )

            return (
                download,
                upload,
                ping
            )

        except Exception as e:

            print(
                f"Retry {i+1} failed: {e}"
            )

            time.sleep(5)

    raise Exception(
        "Speed test failed after 3 retries"
    )


def check_alert(download, upload, ping):

    alerts = []

    if download < MIN_DOWNLOAD:
        alerts.append(
            f"Low Download Speed: {download} Mbps"
        )

    if upload < MIN_UPLOAD:
        alerts.append(
            f"Low Upload Speed: {upload} Mbps"
        )

    if ping > MAX_PING:
        alerts.append(
            f"High Ping: {ping} ms"
        )

    return alerts


if __name__ == "__main__":

    print("===== Internet Speed Monitor =====")

    wifi = get_wifi_name()

    print("WiFi:", wifi)

    if wifi != TARGET_WIFI:

        print(
            f"WiFi '{wifi}' is not target WiFi."
        )

        sys.exit(0)

    try:

        d, u, p = run_speed_test()

        print("Download:", d, "Mbps")
        print("Upload:", u, "Mbps")
        print("Ping:", p, "ms")

        alerts = check_alert(
            d,
            u,
            p
        )

        if alerts:

            message = (
                f"WiFi      : {wifi}\n"
                f"Download  : {d} Mbps\n"
                f"Upload    : {u} Mbps\n"
                f"Ping      : {p} ms\n\n"
                f"Thresholds:\n"
                f"Download < {MIN_DOWNLOAD} Mbps\n"
                f"Upload < {MIN_UPLOAD} Mbps\n"
                f"Ping > {MAX_PING} ms\n\n"
                f"Alerts:\n"
            )

            for alert in alerts:
                message += (
                    f"- {alert}\n"
                )

            log_alert(message)

            print(
                "Issue logged successfully."
            )

        else:

            print(
                "Internet status GOOD."
            )

    except Exception as e:

        log_alert(
            f"WiFi : {wifi}\n\n"
            f"NO INTERNET / SPEED TEST FAILED\n\n"
            f"Error:\n{str(e)}"
        )

        print(
            "Internet failure logged."
        )