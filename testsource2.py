#coding:utf-8
import pandas as pd

df =pd.DataFrame([["tokyo","haha",3,4,5],["osaka","chichi",13,14,15],["nagoya","oji",23,24,25],["tokyo","haha",33,34,35]])
print(df)
print(df.ix[:,[0]])

df =pd.get_dummies(df)
print(df)
print(df.ix[0,0])

an =pd.Series(["unchi"])
an.append(pd.Series(["unchicchi"]))
#print(an)