import os
import gzip, bz2
import tarfile, zipfile, rarfile

import shutil


def _unzip_zip_file(file, unzip_dir="."):
    try:
        with zipfile.ZipFile(file) as zip_file:
            [zip_file.extract(name, unzip_dir) for name in zip_file.namelist()]
    except Exception as e:
        raise RuntimeError(f"解压.zip文件出错, 原因:{e}")


def _unzip_rar_file(file, unzip_dir="."):
    try:
        with rarfile.RarFile(file) as rar_file:
            [rar_file.extract(name, unzip_dir) for name in rar_file.namelist()]
    except Exception as e:
        raise RuntimeError(f"解压.rar文件出错, 原因:{e}")


def _unzip_gzip_file(file, unzip_dir="."):
    try:
        new_file = os.path.join(unzip_dir, os.path.splitext(os.path.basename(file))[0])
        if new_file.find(".") == -1:
            new_file += ".txt"
        with gzip.open(file, "rb") as gz_file:
            with open(new_file, "wb") as f:
                for data in iter(lambda: gz_file.read(1024), b''):
                    f.write(data)
    except Exception as e:
        raise RuntimeError(f"解压.gzip文件出错, 原因:{e}")


def _unzip_tar_file(file, unzip_dir="."):
    try:
        with tarfile.open(file) as tar_file:
            for name in tar_file.getnames():
                tar_file.extract(name, unzip_dir)
    except Exception as e:
        raise RuntimeError(f"解压.tar文件出错, 原因:{e}")


def _unzip_bz2_file(file, unzip_dir="."):
    try:
        new_file = os.path.join(unzip_dir, os.path.splitext(os.path.basename(file))[0])
        if new_file.find(".") == -1:
            new_file += ".txt"
        with bz2.open(file, "rb") as bz2_file:
            with open(new_file, "wb") as f:
                for data in iter(lambda: bz2_file.read(1024), b''):
                    f.write(data)
    except Exception as e:
        raise RuntimeError(f"解压.bz2文件出错, 原因:{e}")


def _unzip_tar_gz_file(file, unzip_dir="."):
    try:
        _unzip_gzip_file(file, unzip_dir)

        file = os.path.join(unzip_dir, os.path.splitext(file)[0])
        _unzip_tar_file(file, unzip_dir)

        os.remove(file)
    except Exception as e:
        raise RuntimeError(f"解压.tar.gz文件出错, 原因:{e}")


def _unzip_tar_bz2_file(file, unzip_dir="."):
    try:
        _unzip_bz2_file(file, unzip_dir)

        file = os.path.join(unzip_dir, os.path.splitext(file)[0])
        _unzip_tar_file(file, unzip_dir)

        os.remove(file)
    except Exception as e:
        raise RuntimeError(f"解压.tar.bz2文件出错, 原因:{e}")


def decompression(file, unzip_dir="."):
    if not os.path.exists(unzip_dir):
        os.makedirs(unzip_dir)

    if file.endswith(".zip"):
        _unzip_zip_file(file, unzip_dir)
    elif file.endswith(".rar"):
        _unzip_rar_file(file, unzip_dir)
    elif file.endswith(".tar.gz"):
        _unzip_tar_gz_file(file, unzip_dir)
    elif file.endswith(".tar.bz2"):
        _unzip_tar_bz2_file(file, unzip_dir)
    elif file.endswith(".gz"):
        _unzip_gzip_file(file, unzip_dir)
    elif file.endswith(".bz2"):
        _unzip_bz2_file(file, unzip_dir)
    elif file.endswith(".tar") or file.endswith(".tgz"):
        _unzip_tar_file(file, unzip_dir)
    else:
        print(f"不支持的解压类型!")


if __name__ == "__main__":
    decompression("foobar.tar.bz2")
