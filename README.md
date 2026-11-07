# network-monitor
 
A small Python script I built to monitor the status of websites or network devices.

## What it does:
* **Pings targets:** Checks if target IP addresses (like Google or a router) are online using standard system pings.
* **Runs concurrently:** Uses multi-threading (`ThreadPoolExecutor`) to check multiple addresses at the exact same time instead of one-by-one.
* **Tracks changes:** Remembers the past state of each target so it only prints an alert when something actually changes .
* **Runs continuously:** Loops forever in the background checking every 10 seconds until you stop it (`Ctrl + C`).
