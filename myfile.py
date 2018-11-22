import os


def read_big_file(file, size=10240, delimiter="\n"):
    '''大文件读取'''
    buf = ""
    with open(file) as f:
        while True:
            while delimiter in buf:
                pos = buf.index(delimiter)
                yield buf[:pos]
                buf = buf[pos + len(delimiter):]
            chunk = f.read(size)
            if not chunk:
                yield buf
                break
            buf += chunk


def single_file_rename(file, srcStr, dstStr, isPrint=True):
    '''单个文件重命名'''
    # if file.endswith(srcStr):
    if srcStr in file:
        newFile = file.replace(srcStr, dstStr, 1)
        os.rename(file, newFile)
        if isPrint:
            print("[{0}] -> [{1}]".format(file, newFile))


def batch_file_rename(dirpath, srcStr, dstStr, isTree=True, isPrint=True):
    '''批量文件重命名'''
    dirpath = os.path.normcase(os.path.normpath(dirpath))
    if isTree:
        [single_file_rename(os.path.join(root, file), srcStr, dstStr, isPrint) for root, dirs, files in os.walk(dirpath)
         for file in files]
    else:
        for file in os.listdir(dirpath):
            file = os.path.join(dirpath, file)
            if os.path.isfile(file):
                single_file_rename(file, srcStr, dstStr, isPrint)


if __name__ == "__main__":
    # for lineno, line in enumerate(read_big_file("input.txt")):
    #     print("{0}:{1}".format(lineno + 1, line))

    # single_file_rename(r'F:\test\marrow_bk\attr_desc.py', ".py", ".txt")

    batch_file_rename(r'F:\git_python_bk', ".txt", ".py")
