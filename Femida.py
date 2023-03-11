import os
import os.path
import socket
import time
import threading
import configparser
import pytermgui as ptg
from colorama import Fore
from loguru import logger
from cryptography.fernet import Fernet
from progress.bar import IncrementalBar

def clear():
    os.system('cls' if os.name=='nt' else 'clear')

def banner():
    print(Fore.CYAN + r"""
 ________ _______   _____ ______   ___  ________  ________     
|\  _____\\  ___ \ |\   _ \  _   \|\  \|\   ___ \|\   __  \    
\ \  \__/\ \   __/|\ \  \\\__\ \  \ \  \ \  \_|\ \ \  \|\  \   
 \ \   __\\ \  \_|/_\ \  \\|__| \  \ \  \ \  \ \\ \ \   __  \  
  \ \  \_| \ \  \_|\ \ \  \    \ \  \ \  \ \  \_\\ \ \  \ \  \ 
   \ \__\   \ \_______\ \__\    \ \__\ \__\ \_______\ \__\ \__\
    \|__|    \|_______|\|__|     \|__|\|__|\|_______|\|__|\|__|
    """)
    print(Fore.CYAN + "[ Автор ]:  " + Fore.LIGHTMAGENTA_EX +  "𝐓𝐫𝐚𝐠𝐢𝐜 𝐂𝐢𝐭𝐲#0001")
    print(Fore.CYAN + "* Проект для доступа к зашифрованной сети Femida *\n")

def return_data():
    return input(Fore.LIGHTBLACK_EX + '[' + Fore.CYAN + 'Femida' + Fore.LIGHTBLACK_EX + ']' + " >>> ")

def choice_create(title: str, choice_list):
    print(Fore.LIGHTBLACK_EX + '[' + Fore.CYAN + 'Femida' + Fore.LIGHTBLACK_EX + ']' + ' {0}'.format(title))
    for choice in choice_list:
        print(Fore.CYAN + '[{0}] - '.format(choice_list.index(str(choice))) + Fore.LIGHTBLACK_EX + str(choice))

def generate_key():
    key = Fernet.generate_key()
    with open('src/crypto.key', 'wb') as key_file:
        key_file.write(key)

def load_key():
    try:
        return open('src/crypto.key', 'rb').read()
    except:
        pass


def initialize():

    def updater_info():
        config = configparser.ConfigParser()
        config['INFO'] = {
            "version": '0.0.7',
            "updater": True,
        }
        config['UPDATER'] = {
            "ip": '217.151.231.247',
            "port": 6060,
        }
        with open("src/updater_info.ini", "w") as configfile:
                config.write(configfile)



    def config_creator():

        def config_writer():
            global OUTPUT

            OUTPUT = {}

            def generate_config(OUTPUT):
                try:
                    config = configparser.ConfigParser()
                    config['GLOBAL'] = {
                        'username': OUTPUT['Ваше имя: '],
                        'ip': OUTPUT['IP Сервера: '],
                        "port": OUTPUT['PORT Сервера: '],
                        "buffer_size": OUTPUT['Буфер обмена: '],
                        "timeout": OUTPUT['Время ожидания: '],
                        "connections": OUTPUT['Максимальное количество подключений: '],
                        "termuxUI": bool(True if OUTPUT['Использовать UI для Termux [y/n]: '] == 'y' else False),
                        }
                    with open("src/config.ini", "w") as configfile:
                        config.write(configfile)
                except:
                    pass

            def submit(manager: ptg.WindowManager, window: ptg.Window) -> None:
                global OUTPUT

                try:
                    for widget in window:
                        if isinstance(widget, ptg.InputField):
                            OUTPUT[widget.prompt] = widget.value
                            continue

                        if isinstance(widget, ptg.Container):
                            label, field = iter(widget)
                            OUTPUT[label.value] = field.value
                except:
                    pass

                finally:
                    try:
                        generate_config(OUTPUT)
                        manager.stop()
                        clear()
                        initialize()
                    except:
                        pass

            CONFIG = """
            config:
                InputField:
                    styles:
                        prompt: dim italic
                        cursor: '@72'
                Label:
                    styles:
                        value: dim bold

                Window:
                    styles:
                        border: '60'
                        corner: '60'

                Container:
                    styles:
                        border: '96'
                        corner: '96'
            """

            with ptg.YamlLoader() as loader:
                loader.load(CONFIG)

            with ptg.WindowManager() as manager:
                window = (
                    ptg.Window(
                        ptg.InputField("{0}".format(os.getlogin()), prompt="Ваше имя: "),
                        ptg.InputField("127.0.0.1", prompt="IP Сервера: "),
                        ptg.InputField("8080", prompt="PORT Сервера: "),
                        ptg.InputField("16000", prompt="Буфер обмена: "),
                        ptg.InputField("100", prompt="Время ожидания: "),
                        ptg.InputField("5", prompt="Максимальное количество подключений: "),
                        ptg.InputField("n", prompt="Использовать UI для Termux [y/n]: "),
                        "",
                        ["Создать", lambda *_: submit(manager, window)],
                        "",
                        ["Выйти", lambda *_: exit()],
                        width=60,
                        box="DOUBLE",
                    )
                    .set_title("[210 bold]Femida | Редактор конфигурации")
                    .center()
                )

                manager.add(window)

        def config_writer_low_ui():

            def clear_spec():
                clear()
                banner()

            def get_username():
                clear_spec()
                logger.info("Введите ваше имя: ")
                return str(return_data())

            def get_ip():
                clear_spec()
                logger.info("Введите IP сервера: ")
                return str(return_data())
            
            def get_port():
                clear_spec()
                logger.info("Введите порт сервера: ")
                return int(return_data())
            
            def get_buffer_size():
                clear_spec()
                logger.info("Введите количество буфера обмена: ")
                return int(return_data())
            
            def get_timeout():
                clear_spec()
                logger.info("Введите время ожидания: ")
                return int(return_data())
            
            def get_connections():
                clear_spec()
                logger.info("Введите максимальное количество подключений: ")
                return int(return_data())
            
            def get_termux_ui():
                clear_spec()
                logger.info("Использовать UI для Termux [True/False]: ")
                return bool(return_data())
            
            def create_config_local():
                Username = get_username()
                Ip = get_ip()
                Port = get_port()
                BufferSize = get_buffer_size()
                Timeout = get_timeout()
                Connections = get_connections()
                TermuxUI = get_termux_ui()

                clear_spec()

                config = configparser.ConfigParser()
                config['GLOBAL'] = {
                    'username': Username,
                    'ip': Ip,
                    "port": Port,
                    "buffer_size": BufferSize,
                    "timeout": Timeout,
                    "connections": Connections,
                    "termuxUI": TermuxUI,
                }
                with open("src/config.ini", "w") as configfile:
                    config.write(configfile)
                initialize()
            
            create_config_local()

        def config_femida():
            config = configparser.ConfigParser()
            config['GLOBAL'] = {
                'username': os.getlogin(),
                'ip': '217.151.231.247',
                "port": 8080,
                "buffer_size": 16000,
                "timeout": 100,
                "connections": 5,
                "termuxUI": False,
            }
            with open("src/config.ini", "w") as configfile:
                config.write(configfile)
            initialize()
            
        
        def config_manager():
            clear()
            banner()
            choice_create("Управление конфигурацией", ["Создать (TUI)", "Создать (Low UI)", "Использовать от Femida", 'Выход'])
            returned = int(return_data())
            if returned == 0:
                config_writer()
            elif returned == 1:
                config_writer_low_ui()
            elif returned == 2:
                config_femida()
            else:
                exit()
            
        config_manager()
        clear()

    def initialize_main():
        clear()
        banner()

        config = configparser.ConfigParser()
        config.read('src/config.ini')

        choice_create("Выберите вариант работы", ['Клиент', 'Сервер', 'Выход'])
        returned = int(return_data())
        if returned == 0:
            main_client(config)
        elif returned == 1:
            main_server(config)
        else:
            exit()


    def component_check():
        clear()
        banner()
        bar = IncrementalBar('Проверка компонентов', max = 5)

        if not os.path.exists('src'):
            os.mkdir('src')
        bar.next()

        time.sleep(0.5)

        if not os.path.exists('src/config.ini'):
            bar.finish()
            clear()
            config_creator()
        else:
            bar.next()

        time.sleep(0.5)
        
        if not os.path.exists('src/crypto.key'):
            generate_key()
        bar.next()

        time.sleep(0.5)

        if not os.path.exists('src/updater_info.ini'):
            updater_info()
        bar.next()

        if not os.path.exists('Updater.py'):
            updater = False
        bar.next()

        time.sleep(1)

        clear()
        banner()

        if updater == False:
            configUpdater = configparser.ConfigParser()
            configUpdater.read('src/updater_info.ini')

            if bool(configUpdater['INFO']['updater']) == True:
                logger.warning("Отсуствует файл автоматического обновления Updater.py, отключите updater что бы не получать данное сообщение.")
            logger.info("Остальные 4 компонента загружены успешно")
        else:
            logger.info("Все компоненты загружены")

        time.sleep(3)
        initialize_main()


    component_check()


def main_client(config: configparser.ConfigParser) -> None:
    try:
        cryptkey = Fernet(load_key())
    except:
        pass

    clear()
    banner()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = (config['GLOBAL']['ip'], int(config['GLOBAL']['port']))
    sock.connect(server_address)
    logger.warning('Подключено | IP: {0} | PORT: {1}'.format(config['GLOBAL']['ip'], config['GLOBAL']['port']) if config['GLOBAL']['ip'] != '217.151.231.247' else 'Подключено к Femida')
    logger.info("/exit - выход из программы")
     
    def outdatas():
        while True:
            outdata = str(input())
            if outdata == '/exit':
                exit()
                break
            try:
                outdata_for_crypt = f"{config['GLOBAL']['username']}: {outdata}".encode('utf-8')
                cryptmessage = cryptkey.encrypt(outdata_for_crypt)
                sock.send(cryptmessage)
            except:
                pass
 
 
    def indatas():
        while True:
            try:
                indata = sock.recv(int(config['GLOBAL']['buffer_size']))
                decryptmessage = cryptkey.decrypt(indata.decode('utf-8'))
                recvdata = decryptmessage.decode('utf-8').replace("b", "").replace("'", "").split(':')
            except:
                pass
            print(Fore.LIGHTBLACK_EX + '[' + Fore.LIGHTMAGENTA_EX + '{0}'.format(str(recvdata[0])) + Fore.LIGHTBLACK_EX + "] :" + Fore.LIGHTBLACK_EX + str(recvdata[1]))

    try:
        t1 = threading.Thread(target=indatas, name='input')
        t2 = threading.Thread(target=outdatas, name='out')
        t1.start()
        t2.start()
        t2.join()
    except:
        pass




def main_server(config: configparser.ConfigParser) -> None:
    global clients
    global end

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (config['GLOBAL']['ip'], int(config['GLOBAL']['port']))
    sock.bind(server_address)
    sock.listen(int(config['GLOBAL']['connections']))

    clear()
    banner()
    logger.info('Запуск сервера. | IP: {0} | PORT: {1}'.format(config['GLOBAL']['ip'], config['GLOBAL']['port']))
    logger.info('Количество соединений задано: {0}'. format(config['GLOBAL']['connections']))
    
    clients = []
    end = []

    def accept():
        while True:
            client, addr = sock.accept()
            clients.append(client)

     
    def recv_data(client):
        while True:
            try:
                indata = client.recv(int(config['GLOBAL']['buffer_size']))
            except Exception as e:
                clients.remove(client)
                end.remove(client)
                logger.info("\ r" + '-' * 5 + f'Сервер отключен: текущее количество подключений: ----- {len (clients)}' + '-' * 5, end = '')
                break
            print(indata.decode('utf-8'))
            for clien in clients:
                if clien != client:
                    clien.send(indata)

    def indatas():
        while True:
            for clien in clients:
                if clien in end:
                    continue
                index = threading.Thread(target = recv_data,args = (clien,))
                index.start()
                end.append(clien)

    t1 = threading.Thread(target = indatas,name = 'input')
    t1.start()
    t3 = threading.Thread(target = accept(),name = 'accept')
    t3.start()
    t2.join()
    for client in clients:
        client.close()
    logger.warning('Сервер отключен')

if __name__ == "__main__":
    initialize()
