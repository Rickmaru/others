#author;R.Kunimoto, TAKENAKA co.
#coding:utf-8
import csv
import os

path = "C:\\Users\\1500570\\Documents\\R\\WS\\dataset"
fn = "data04.csv"
r_filepath = path + "\\" + fn
fr = open(r_filepath, "r")
rem = csv.reader(fr)
fwtr = open(path+"\\"+"written3.csv", "w+", newline="")
wrmtr = csv.writer(fwtr)

term = 48
pred = 1

dataframe = []
new_frame = []

for line in rem:
    dataframe.append(line)

i = 1
lenlen = len(dataframe)
firstf = True

while i < lenlen - term:
    if i >= term+1:
        tmpf = []
        tmpi = 0
        while tmpi < 7:
            tmpf.append(dataframe[i][tmpi])
            tmpi += 1
        j = 0
        while j <= term:
            if j != term:
                tmpf.append(dataframe[i-term+j][7])
            else:
                tmpf.append(dataframe[i-term+j+pred][7])
            j += 1
        wrmtr.writerow(tmpf)
    i += 1

fr.close()
fwtr.close()

print("end")