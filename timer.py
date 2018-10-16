import time
from functools import wraps

def timer(func):
    @wraps(func)
    def get_time(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print("{0}执行完毕, 耗时:{1}".format(func.__name__, str(end-start)))
        return result
    return get_time

@timer
def test_timer(name="一支穿云箭"):
    for i in range(10):
        print(name)
        time.sleep(0.2)
    return 1, 3

if __name__ == "__main__":
    num, num1 = test_timer()
    print(num, num1)


