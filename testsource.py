#coding:utf-8
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.spatial import distance
from scipy.spatial.distance import cityblock

a =np.array([[1.2,2.5,4,1,7],
             [1.1, 10,6,9,3],
             [2,    5,4,11,5],
             [1,2,3,4,5]])


u, s, v =np.linalg.svd(a, full_matrices=False)
print(u)
print(s)
print(v)
ss =np.diag(s)


#SVD戻す
print(np.dot(u,np.dot(ss,v)))

#疑似逆用にsを反転！
un =0
while un <3:
    s[un] =s[un]**-1
    un +=1

s =np.diag(s)

#疑似逆
t =np.dot(v.T,np.dot(s,u.T))
print("計算したの",t)
print("pinvのやつ",np.linalg.pinv(a))

print(np.dot(np.linalg.pinv(a),a))
print(np.dot(t,a))
