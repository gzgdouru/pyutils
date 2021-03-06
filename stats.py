import sys, os, time
import chardet


class CodeStats:
    def __init__(self, dirPath:str=".", fileSuffix:list=None, ignoreDirs:list=None, ignoreFiles:list=None, ignoreNullLine:bool=True)->None:
        self.dirPath = os.path.normcase(dirPath)
        self.fileSuffix = fileSuffix if fileSuffix else []
        self.ignoreDirs = ignoreDirs if ignoreDirs else []
        self.ignoreFiles = ignoreFiles if ignoreFiles else []
        self.ignoreNullLine = ignoreNullLine
        self.totalCount = 0
        self.statsFileNums = 0

    def get_file_for_path(self):
        for root, dirs, files in os.walk(self.dirPath):
            if self.get_dirname(root) in self.ignoreDirs:
                del dirs[:]
                continue

            for name in files:
                if name in self.ignoreFiles:
                    continue
                _, suffix = os.path.splitext(name)
                if not self.fileSuffix or suffix in self.fileSuffix:
                    yield os.path.join(root, name)

    @staticmethod
    def get_dirname(filePath):
        return filePath.split(os.sep)[-1]

    def stats_line_count(self):
        timeStart = time.time()
        for file in self.get_file_for_path():
            self.statsFileNums += 1
            count = self.stats_file(file)
            print("stats file({0})-->{1}".format(file, count))
            self.totalCount += count
        timeEnd = time.time()
        print("文件数:{0} 代码行数:{1} 耗时:{2}".format(self.statsFileNums, self.totalCount, timeEnd - timeStart))

    def stats_file(self, file, encoidng="utf-8"):
        count = 0
        for line in open(file, "r", encoding=encoidng, errors="replace"):
            if not self.ignoreNullLine:
                count += 1
            elif line[:-1]:
                count += 1
            else:
                pass
        return count


if __name__ == "__main__":
    dirPath = r"F:\git_python\dice"  # 根目录
    ignoreDirs = [".git", "migrations"]  # 忽略的目录
    fileSuffix = [".py", ".html"]  # 统计的文件后缀
    ignoreFiles = []  # 忽略的文件

    codeStat = CodeStats(dirPath=dirPath, fileSuffix=fileSuffix, ignoreDirs=ignoreDirs, ignoreFiles=ignoreFiles,
                         ignoreNullLine=True)
    codeStat.stats_line_count()
