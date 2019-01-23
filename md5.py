import string
import hashlib
import itertools
import time
import re


class CharsType:
    all = string.printable  # 所有字符
    digits = string.digits  # 数字
    lowercase = string.ascii_lowercase  # 小写字符
    uppercase = string.ascii_uppercase  # 大写字符
    digits_lowercase = string.digits + string.ascii_lowercase  # 数字加小写字符
    digits_uppercase = string.digits + string.ascii_uppercase  # 数字加大写字符
    letters = string.ascii_letters  # 大小写字符
    digits_letters = string.digits + string.ascii_letters  # 数字加大小写字符


def get_md5(value):
    m = hashlib.md5()
    m.update(str(value).encode("utf-8"))
    return m.hexdigest()


def generate_phone():
    phone_list = []
    phone_list.append(['1'])
    phone_list.append(map(str, range(3, 10)))
    [phone_list.append(map(str, range(10))) for i in range(9)]
    return phone_list


def phone_reverse(md5):
    phone_list = generate_phone()
    result = None
    mobile = re.compile(r'^(13[0-9]|14[579]|15[0-3,5-9]|16[6]|17[0135678]|18[0-9]|19[89])\d{8}$')
    count = 0
    time_start = time.time()
    for phone in itertools.product(*phone_list):
        count += 1
        print("\r已尝试记录数:{0}".format(count), end="")
        phone = "".join(phone)
        if not re.match(mobile, phone):
            continue
        else:
            if md5 == get_md5(phone):
                result = phone
                break
    print("\n")
    time_end = time.time()
    print("匹配完成, 号码:{0}, 耗时:{1}".format(result, time_end - time_start))
    return result


def md5_reverse(md5, mins=6, maxs=32, chars=None):
    chars = string.printable if not chars else chars
    result = None
    time_start = time.time()
    count = 0
    for i in range(mins, maxs + 1):
        chars_list = [chars for j in range(i)]
        for combine in itertools.product(*chars_list):
            count += 1
            print("\r试验{0}位匹配, 已尝试记录数:{1}".format(i, count), end="")
            strCombine = "".join(combine)
            if get_md5(strCombine) == md5:
                result = strCombine
                break
        print("\n")
        if result: break
    time_end = time.time()
    print("匹配完成, 字符:{0}, 耗时:{1}".format(result, time_end - time_start))


if __name__ == "__main__":
    md5_reverse("22924f252015d4c967c0454e0878a89b", mins=6, chars=CharsType.digits_lowercase)
    # phone_reverse("173f8c8e2286385f440f38472d27100d")
