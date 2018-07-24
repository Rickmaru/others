#author;R.Kunimoto, TAKENAKA co.
#coding:utf-8

import random
from sklearn import preprocessing
from sklearn import ensemble
from sklearn import svm
from sklearn import linear_model
from sklearn import neural_network
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# データ無作為抽出時の重複抽出を防ぐチェッカー関数
# listにはインデクスのリスト、idにはチェック対象インデクスint
def checker(list,id):
    for ai in list:
        if ai == id:
            return True
        else:
            continue
    return False

# データセットおよび予実表出力先ディレクトリ
path = 'C:\\Users\\1500570\\Documents\\R\\WS\\kosugi\\'
# データセットは事前に目的変数としてt=Tの行にt=T+24[h]の実績値が含まれるという前提
data = pd.read_csv(path+"data_normal.csv")
# data = data.sample(3000)

y = data["y"]
# 天気情報あり/なしをコメントアウトで切替
# x = data[["week_sin","week_cos","time_sin","time_cos","sunlight","temp","moist","y1"]]
x = data[["week_sin","week_cos","time_sin","time_cos","y1"]]

# RMSE計算結果格納用リスト
score = []
# 各学習アルゴリズムforループ用変数
n_ml = 0
# 無作為抽出するデータ数
n_ext = 1000

# メインループ（試す学習アルゴリズム数分）
while n_ml < 4:
    n_term = 0
    score2 = []
    # サブループ（試す学習データ期間セクション数分）
    while n_term < 3:
        # ファイル出力用の実測値/予測値格納用リスト
        aarray = []
        parray = []
        # 無作為抽出時重複チェック用リスト
        i_list=[]
        j = 0
        rmse = 0
        t = 14*(n_term+1)
        # インデクス用、tにはデータの期間（日）が入るため、データ行数は一日で48（∵30分ごとのデータ）
        term = t*48 -1
        # 無作為抽出を行うたびモデルを学習・予測してaarray/parrayに実績/予測結果を格納していくループ
        while j < n_ext:
            flag = False
            # 無作為抽出を行い、インデクスは既選択リストi_listへappend
            while flag == False:
                i = random.randint(1,len(data)-term-2)
                if checker(i_list,i) == True:
                    continue
                else:
                    flag = True
                    i_list.append(i)
            # n_mlの値によって学習アルゴリズムを選択
            if n_ml == 0:
                namae = "rfr"
                rf = ensemble.RandomForestRegressor(n_estimators=10)
            elif n_ml == 1:
                namae = "svr"
                rf = svm.SVR()
            elif n_ml == 2:
                namae = "lmr"
                rf = linear_model.LinearRegression()
            elif n_ml == 3:
                namae = "nnr"
                rf = neural_network.MLPRegressor(hidden_layer_sizes=(10,1))
            # iは予測対象ではなく学習期間データの開始インデクス
            x_train = x.iloc[i:i+term,:]
            y_train = y.iloc[i:i+term]
            x_test = x.iloc[i+term,:]
            y_test = y.iloc[i+term]
            rf.fit(x_train,y_train)
            py = rf.predict(x_test)
            aarray.append(y_test)
            parray.append(float(py))
            rmse += (y_test-float(py))**2
            j += 1
            # 進捗表示用
            if(j%100 == 0):
                print("j = "+str(j)+" / "+str(n_ext))
        p = np.vstack((aarray,parray)).swapaxes(0,1)
        np.savetxt(path+"written_"+namae+"_"+str((n_term+1)*14)+".csv",p,delimiter=",")
        n_term += 1
        score2.append(float(rmse/float(n_ext)))
        print(score2)
        print(namae+str(n_term)+" is end")
    score.append(score2)
    n_ml += 1

print(score)
print("end")
