import requests
import json
from datetime import datetime, timedelta
import time
from colorama import Fore, Style, init


init(autoreset=True)

BASE_API_URL = "https://api.miniapp.dropstab.com/api"
BASE_HEADERS = {
    "accept": "application/json",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/json",
    "priority": "u=1, i",
    "sec-ch-ua": "\"Microsoft Edge\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\", \"Microsoft Edge WebView2\";v=\"129\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "Referer": "https://mdkefjwsfepf.dropstab.com/",
    "Referrer-Policy": "strict-origin-when-cross-origin"
}

def get_headers(token=None):
    headers = BASE_HEADERS.copy()
    if token:
        headers["authorization"] = f"Bearer {token}"
    return headers

def get_token_and_login(payload):
    headers = get_headers()
    body = json.dumps({"webAppData": payload})
    print(Fore.CYAN + "Logging in...")
    
    response = requests.post(f"{BASE_API_URL}/auth/login", headers=headers, data=body)
    if response.status_code == 200:
        try:
            token = response.json()["jwt"]["access"]["token"]
            print(Fore.GREEN + "Login successful.")
            return token
        except KeyError:
            print(Fore.RED + "Login failed: Incorrect response structure.")
            raise Exception("Login failed: Incorrect response structure.")
    else:
        print(Fore.RED + f"Login failed: {response.status_code} - {response.text}")
        raise Exception(f"Login failed: {response.status_code} - {response.text}")

def get_user_info(token):
    headers = get_headers(token)
    print(Fore.CYAN + "Fetching user information...")
    
    response = requests.get(f"{BASE_API_URL}/user/current", headers=headers)
    if response.status_code == 200:
        data = response.json()
        print(Fore.GREEN + f"Account: {data['tgUsername']}, Balance: {data['balance']}")
        return data
    else:
        print(Fore.RED + f"Failed to fetch user information: {response.status_code} - {response.text}")
        raise Exception(f"Failed to fetch user information: {response.status_code} - {response.text}")

def daily_bonus(token):
    headers = get_headers(token)
    print(Fore.CYAN + "Claiming daily bonus...")
    
    response = requests.post(f"{BASE_API_URL}/bonus/dailyBonus", headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data["result"]:
            print(Fore.GREEN + f"Daily bonus claimed. Streaks: {data['streaks']}")
    else:
        print(Fore.RED + f"Failed to claim daily bonus: {response.status_code} - {response.text}")
        raise Exception(f"Failed to claim daily bonus: {response.status_code} - {response.text}")

def check_tasks(token):
    headers = get_headers(token)
    print(Fore.CYAN + "Checking available tasks...")
    
    response = requests.get(f"{BASE_API_URL}/quest", headers=headers)
    if response.status_code == 200:
        tasks = response.json()
        any_claimed = False


def dynamic_countdown(sleep_time):
    while sleep_time > 0:
        hours, remainder = divmod(sleep_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        print(f"\rWaiting until 00:01 UTC to restart... {int(hours):02}:{int(minutes):02}:{int(seconds):02}", end="")
        time.sleep(1)
        sleep_time -= 1
    print()

from datetime import datetime, timedelta, timezone

def wait_until_midnight():
    now = datetime.now(timezone.utc)  # Gunakan timezone-aware UTC datetime
    next_run = now.replace(hour=0, minute=1, second=0, microsecond=0)
    if now >= next_run:
        next_run += timedelta(days=1)
    sleep_time = (next_run - now).total_seconds()
    dynamic_countdown(int(sleep_time))


def process_queries():
    while True:
        with open('sesi.txt', 'r') as file:
            queries = [query.strip() for query in file.readlines()]

        for query in queries:
            try:
                print(Fore.CYAN + "Processing account...")
                token = get_token_and_login(query)
                get_user_info(token)
                daily_bonus(token)
 
            except Exception as e:
                print(Fore.RED + f"Error occurred: {e}")
                
        wait_until_midnight()

process_queries()
