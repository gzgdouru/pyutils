import os


class MyFileDeal:
    def __init__(self, dealDir):
        self.dealDir = os.path.normcase(os.path.normpath(dealDir))
        if self.dealDir[-1] != "/": self.dealDir += "/"

    def batch_file_rename(self, srcStr, dstStr, isTree=True, isPrint=True):
        if isTree:
            for root, dirs, files in os.walk(self.dealDir):
                [self.single_file_rename(os.path.join(root, file), srcStr, dstStr, isPrint) for file in files]
        else:
            [self.single_file_rename(os.path.join(self.dealDir, file), srcStr, dstStr, isPrint) for file in
             os.listdir(self.dealDir)
             if os.path.isfile(os.path.join(self.dealDir, file))]

    def single_file_rename(self, file, srcStr, dstStr, isPrint=True):
        if file.find(srcStr) != -1:
            newFile = file.replace(srcStr, dstStr, 1)
            os.rename(file, newFile)
            if isPrint: print("[{}] -> [{}]".format(file, newFile))


if __name__ == "__main__":
    fileDeal = MyFileDeal("f:/public")
    fileDeal.batch_file_rename(".pyc", ".txt", isTree=True)
    # fileDeal.batch_file_rename(".txt", ".pyc")
