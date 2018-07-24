#author:R.Kunimoto, Info Engineering Div @TAKENAKA co.
#coding:utf-8
import os
import csv
import datetime

if __name__ == "__main__":
    print ("元となるディレクトリのパスを入力 ※注意：デリミタは「\」※")
    path = str(input("input:"))
    path = path.replace("\\","\\\\")
    print("階層の深さを半角数字で指定(例えば3の場合、元ディレクトリ含めて3階層分以下の情報を出力)")
    dpt = int(input("input:"))

    dir_list = []
    file_list = []
    new_dir_list = []
    new_fil_list = []
    root_count = path.count("\\")

    for (root, dirs, files) in os.walk(path):
        for dir in dirs:
            dir_list.append(os.path.join(root,dir))
        for file in files:
            file_list.append(os.path.join(root,file))

    i = 0
    j = 0
    while i < len(dir_list):
        if dir_list[i].count("\\") -root_count -dpt <= -1:
            new_dir_list.append(dir_list[i])
        i += 1
    while j < len(file_list):
        if file_list[j].count("\\") -root_count -dpt <= -1:
            new_fil_list.append(file_list[j])
        j += 1

    def writer(path):
        tmpl = path.split("\\")
        tmpl2 = []
        ti = 0
        while ti < dpt:
            try:
                tmpl2.append(tmpl[root_count+ti])
            except:
                return tmpl2
            ti += 1
        return tmpl2

    dd = datetime.datetime.today().strftime("%y%m%d-%H%M%S-")
    f = open(path+"\\"+dd+"dirTREE_depthU="+str(dpt)+".csv", "w+", newline="")
    ff = csv.writer(f)
    for line in new_dir_list:
        ff.writerow(writer(line))
    f2 = open(path+"\\"+dd+"fileTREE_depthU="+str(dpt)+".csv", "w+", newline="")
    ff2 = csv.writer(f2)
    for line in new_fil_list:
        ff2.writerow(writer(line))

    print("Program finished")