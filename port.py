import telnetlib
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

logger = logging.getLogger("port_detection")
logger.setLevel(logging.INFO)
sHandle = logging.StreamHandler()
sHandle.setLevel(logging.INFO)
sHandle.setFormatter(logging.Formatter("[%(asctime)s] [%(name)s] [%(levelname)s] : %(message)s"))
logger.addHandler(sHandle)


def _port_check_thread(host, port, timeout=3):
    logger.info(f"尝试访问{host}主机的{port}端口!")
    tn = telnetlib.Telnet()
    try:
        tn.open(host, port, timeout=timeout)
        tn.write("exit\n".encode("utf-8"))
        return port
    except Exception as e:
        pass
    return None


def port_check(host, ports, timeout=3, workers=5):
    with ThreadPoolExecutor(max_workers=workers) as executor:
        tasks = [executor.submit(_port_check_thread, host, port, timeout) for port in ports]

        for task in as_completed(tasks):
            result = task.result()
            if result:
                yield result


if __name__ == "__main__":
    ports = range(9000, 9999)
    valid_port = port_check("172.16.34.16", ports)
    print(list(valid_port))
