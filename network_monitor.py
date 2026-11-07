import subprocess
import datetime
import time
import platform
from concurrent.futures import ThreadPoolExecutor

previous_states = {}

def send_webhook_alert(host,is_up):
    status_text = "DOWN" if not is_up else "UP"
    print(f" [ALERT] Target {host} status changed. New state: {status_text}")

def ping(host):

    param = "-n" if platform.system().lower() ==  "windows" else "-c"
    command = ["ping" , param , "1" , host]

    try:
        result = subprocess.run(command,
                                 stdout=subprocess.DEVNULL , 
                                 stderr=subprocess.DEVNULL, 
                                 timeout=3)
        is_up = (result.returncode == 0)
    except subprocess.TimeoutExpired:
        is_up = False
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "UP" if is_up else "DOWN"
    print(f"{timestamp} Target={host} is {status}")

    if host not in previous_states:
        previous_states[host] = is_up
        print(f"Intialized {host} -> State is {status}")
    else:
        if previous_states[host] != is_up:
            send_webhook_alert(host, is_up)
            previous_states[host] = is_up
        else:
            status_str = "UP" if is_up else "DOWN "
            print(f"[{timestamp}] {host} stable ({status_str})")

    return is_up

if __name__ == "__main__":

    targets = ["1.1.1.1",
               "8.8.8.8",
               "192.168.1.1"]

    print(f"Starting network monitor for {len(targets)} targets...\n")

    try:
        while True:
            print(f"\n Starting check cycle at {datetime.datetime.now().strftime('%H:%M:%S')}")
            with ThreadPoolExecutor(max_workers=5) as executor:
                executor.map(ping, targets)
            time.sleep(10)
            
    except KeyboardInterrupt:
        print("\nNetwork monitor stopped by the user.")