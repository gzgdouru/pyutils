import socket

import redis


def get_host_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


if __name__ == "__main__":
    rconn = redis.Redis(host="47.107.162.149", port=6379)
    local_ip = get_host_ip()
    password = rconn.hget("rootpass", local_ip)
    print(password.decode("utf-8"))
