import socket

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # 不实际发送数据包，只是为了获取IP地址
        s.connect(('8.8.8.8', 80))
        ip_address = s.getsockname()[0]
    except socket.error:
        ip_address = '127.0.0.1'
    finally:
        s.close()
    return ip_address

print(get_ip_address())
