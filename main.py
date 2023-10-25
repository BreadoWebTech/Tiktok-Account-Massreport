import ctypes, json, os, time, random, string, getpass, threading, re, sys

try:
    import pystyle
    import colorama
    import tls_client
    import httpx
    import user_agent
    import datetime
except ModuleNotFoundError:
    os.system("pip install pystyle")
    os.system("pip install colorama")
    os.system("pip install tls_client")
    os.system("pip install httpx")
    os.system("pip install user_agent")
    os.system("pip install datetime")

from pystyle import Write, System, Colorate, Colors
from colorama import Fore, Style, init

red = Fore.RED
yellow = Fore.YELLOW
green = Fore.GREEN
blue = Fore.BLUE
orange = Fore.RED + Fore.YELLOW
pretty = Fore.LIGHTMAGENTA_EX + Fore.LIGHTCYAN_EX
magenta = Fore.MAGENTA
lightblue = Fore.LIGHTBLUE_EX
cyan = Fore.CYAN
gray = Fore.LIGHTBLACK_EX + Fore.WHITE
reset = Fore.RESET
pink = Fore.LIGHTGREEN_EX + Fore.LIGHTMAGENTA_EX
dark_green = Fore.GREEN + Style.BRIGHT

success = 0
failed = 0
generated_agents = 0
total = 1
config_file = "config.json"
proxy_file = "proxies.txt"

acceptable_values = ["y", "yes", "true", "1"]

start = time.time()
ctypes.windll.kernel32.SetConsoleTitleW(f'[ Tiktok MassReport ] By H4cK3dR4Du & 452b')

def save_proxies(proxies):
    with open(proxy_file, "w") as file:
        file.write("\n".join(proxies))

def get_proxies():
    with open(proxy_file, 'r', encoding='utf-8') as f:
        proxies = f.read().splitlines()
    if not proxies:
        proxy_log = {}
    else:
        proxy = random.choice(proxies)
        proxy_log = {
            "http://": f"http://{proxy}", "https://": f"http://{proxy}"
        }
    try:
        url = "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all"
        response = httpx.get(url, proxies=proxy_log, timeout=60)

        if response.status_code == 200:
            proxies = response.text.splitlines()
            save_proxies(proxies)
        else:
            time.sleep(1)
            get_proxies()
    except httpx.ProxyError:
        get_proxies()
    except httpx.ReadError:
        get_proxies()
    except httpx.ConnectTimeout:
        get_proxies()
    except httpx.ReadTimeout:
        get_proxies()
    except httpx.ConnectError:
        get_proxies()
    except httpx.ProtocolError:
        get_proxies()

def check_proxies_file(proxy_file):
    if os.path.exists(proxy_file):
        if os.path.getsize(proxy_file) == 0:
            get_proxies()
    else:
        print(f"Proxy file '{proxy_file}' does not exist. Create a new proxy file.")
        get_proxies()

try:
     with open(config_file) as f:
        data = json.load(f)
        if data.get("proxy_scraper") in acceptable_values:
            check_proxies_file()
        else:
            pass
except FileNotFoundError:
        print("Config file not found.")
except json.JSONDecodeError:
        print("Invalid JSON in the config file.")

def update_console_title(success, failed, total):
    success_rate = round(success / total * 100, 2)
    title = f'[ Tiktok MassReport ] By H4cK3dR4Du & 452b | Reports Sent : {success} ~ Failed : {failed} ~ Success Rate : {success_rate}%'
    ctypes.windll.kernel32.SetConsoleTitleW(title)


def get_time_rn():
    timee = datetime.datetime.now().strftime("%H:%M:%S")
    return timee 

def check_ui():
    output_lock = threading.Lock()
    while True:
        success_rate = round(success/total*100,2)
        System.Clear()
        with output_lock:
            Write.Print(f"""
\t\t\t▄▄▄▄▄▪  ▄ •▄ ▄▄▄▄▄      ▄ •▄     ▄▄▄  ▄▄▄ . ▄▄▄·      ▄▄▄  ▄▄▄▄▄
\t\t\t•██  ██ █▌▄▌▪•██  ▪     █▌▄▌▪    ▀▄ █·▀▄.▀·▐█ ▄█▪     ▀▄ █·•██  
\t\t\t ▐█.▪▐█·▐▀▀▄· ▐█.▪ ▄█▀▄ ▐▀▀▄·    ▐▀▀▄ ▐▀▀▪▄ ██▀· ▄█▀▄ ▐▀▀▄  ▐█.▪
\t\t\t ▐█▌·▐█▌▐█.█▌ ▐█▌·▐█▌.▐▌▐█.█▌    ▐█•█▌▐█▄▄▌▐█▪·•▐█▌.▐▌▐█•█▌ ▐█▌·
\t\t\t ▀▀▀ ▀▀▀·▀  ▀ ▀▀▀  ▀█▄▀▪·▀  ▀    .▀  ▀ ▀▀▀ .▀    ▀█▄▀▪.▀  ▀ ▀▀▀ 

----------------------------------------------------------------------------------------------------------------------
\t\t\tSent Reports : [ {success} ] ~ Failed : [ {failed} ] ~ Success Rate : [ {success_rate}% ]
----------------------------------------------------------------------------------------------------------------------
""" , Colors.blue_to_red, interval=0.000)
            time.sleep(10)

def mass_report():
    global success, total, failed, generated_agents
    proxy = random.choice(open("proxies.txt", "r").readlines()).strip() if len(open("proxies.txt", "r").readlines()) != 0 else None

    session = tls_client.Session(
        client_identifier="chrome_113",
        random_tls_extension_order=True
    )

    if "@" in proxy:
        user_pass, ip_port = proxy.split("@")
        user, password = user_pass.split(":")
        ip, port = ip_port.split(":")
        proxy_string = f"http://{user}:{password}@{ip}:{port}"
    else:
        ip, port = proxy.split(":")
        proxy_string = f"http://{ip}:{port}"

    session.proxies = {
        "http": proxy_string,
        "https": proxy_string
    }


#    create a dictionary to map report types to report type codes so we get rid of those ugly elif statements
    report_type_mapping = {
    "Violence": 90013,
    "Sexual Abuse": 90014,
    "Animal Abuse": 90016,
    "Criminal Activities": 90017,
    "Hate": 9020,
    "Bullying": 9007,
    "Suicide Or Self-Harm": 90061,
    "Dangerous Content": 90064,
    "Sexual Content": 90084,
    "Porn": 90085,
    "Drugs": 90037,
    "Firearms Or Weapons": 90038,
    "Sharing Personal Info": 9018,
    "Human Exploitation": 90015,
    "Under Age": 91015
    }


    try:
        with open(config_file) as f:
            data = json.load(f)
            url = data.get('report_url', '')
            report_types = data.get('report_types', {})
    except FileNotFoundError:
        print("config.json not found")

#   put report_type to a default value
    report_type = None

# go through all the report types and set report_type if a match is found
    for report_type_name, report_type_code in report_type_mapping.items():
        if report_types.get(report_type_name, "").lower() in acceptable_values:
            report_type = report_type_code
            break  # stop searching when report typ got matched 

#   Check if report_type was set and use it
    if report_type is not None:
        output_lock = threading.Lock() 
        headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.62"
    }

    try:
        match_reason = re.search(r'reason=(\d+)', url)
        match_nickname = re.search(r'nickname=([^&]+)', url)
        match_owner_id = re.search(r'owner_id=([^&]+)', url)
        if match_nickname:
            username = match_nickname.group(1)
        if match_owner_id:
            iduser = match_owner_id.group(1)
        if match_reason:
            reason_number = match_reason.group(1)
            new_url = url.replace(f"reason={reason_number}", f"reason={report_type}")
            report = session.get(new_url)
            if "Thanks for your feedback" in report.text or report.status_code == 200:
                with output_lock:
                    time_rn = get_time_rn()
                    print(f"[ {magenta}{time_rn}{reset} ] | ( {green}+{reset} ) {blue}Reported with success to ", end='')
                    sys.stdout.flush()
                    Write.Print(f"{username} ~ {iduser}\n", Colors.purple_to_red, interval=0.000)
                    success += 1
                    total += 1
                    failed += 0
                    update_console_title(success, failed, total)
                    mass_report()
            else:
                with output_lock:
                    time_rn = get_time_rn()
                    print(f"[ {magenta}{time_rn}{reset} ] | ( {red}-{reset} ) {yellow}Cannot report to ", end='')
                    sys.stdout.flush()
                    Write.Print(f"{username} ~ {iduser}\n", Colors.purple_to_red, interval=0.000)
                    failed += 1
                    total += 1
                    success += 0
                    update_console_title(success, failed, total)
                    mass_report()
        else:
            mass_report()  
    except Exception as e:
        failed += 1
        total += 1
        sucess += 0
        update_console_title(success, failed, total)
        mass_report()

def mass_report_thread():
    mass_report()

def check_ui_thread():
    check_ui()

try:
    with open(config_file) as f:
        data = json.load(f)
        num_threads = data.get('threads', 1)  # Set a default value (1 thread) if 'threads' is not defined in the config
except FileNotFoundError:
    print("config.json not found")
except json.JSONDecodeError:
    print("Invalid JSON in the config file.")

threads = []

with threading.Lock():
    for _ in range(num_threads - 1):
        thread = threading.Thread(target=mass_report_thread)
        thread.start()
        threads.append(thread)

    check_ui_thread = threading.Thread(target=check_ui_thread)
    check_ui_thread.start()
    threads.append(check_ui_thread)

    for thread in threads:
        thread.join()
