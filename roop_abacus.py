# -*- coding: utf-8 -*-
"""
Created on Fri Mar  2 18:30:07 2018
#1
@author: 1500197
#2
@author: 1500570

(0.　ライブラリと関数の宣言)
1. パラメータの宣言とターゲットの格納
2. 基準形状の仮定
3. 仮定形状の荷重変形関係を算定
4. ターゲットと基準形状の差分ベクトル{r}の作成
5. 収束？
6. 各パラメータの増分形状解析を実施
7. 荷重増分ベクトル{f_inc}を算出
8. パラメータ荷重増分マトリクス[k_matrix]を作成
9. [k_matrix]の一般化逆行列の作成と次元圧縮
10. パラメータの増分ベクトルを[k_matrix+] *{r}で算出
11. 基準形状の更新
"""

import copy
import numpy as np
import subprocess
import os
import shutil
import math


#refから.inp(固有値解析、大変形解析)とcsv出力用ポスト処理実行ファイル(.py)を作成するクラス
##参照ファイルは.txtで拡張子なしの名前を入力

curd =os.getcwd()
lll =os.listdir(curd)
class Create_input:
    def __init__(self, ref_list):
        self.eg = open(ref_list[0]+'.txt', 'r',encoding='utf-8').readlines()
        self.df = open(ref_list[1]+'.txt', 'r',encoding='utf-8').readlines()
        self.qd = open(ref_list[2]+'.txt', 'r',encoding='utf-8').readlines()

    def create_input(self, shape, name):
        #eg(固有値解析)inputファイル
        eg2 = copy.deepcopy(self.eg)
        eg2[1] = eg2[1].replace('xxxxx', str(shape[0]))
        eg2[2] = eg2[2].replace('xxxxx', str(shape[1]))
        eg2[3] = eg2[3].replace('xxxxx', str(shape[2]))
        eg2[4] = eg2[4].replace('xxxxx', str(shape[3]))
        eg2[5] = eg2[5].replace('xxxxx', str(shape[4]))
        with open(name[0] + '.inp', 'w', encoding='utf-8') as file:
            file.writelines( eg2 )

        #df(固有値解析)inputファイル
        df2 = copy.deepcopy(self.df)
        df2[1] = df2[1].replace('xxxxx', str(shape[0]))
        df2[2] = df2[2].replace('xxxxx', str(shape[1]))
        df2[3] = df2[3].replace('xxxxx', str(shape[2]))
        df2[4] = df2[4].replace('xxxxx', str(shape[3]))
        df2[5] = df2[5].replace('xxxxx', str(shape[4]))
        df2[24] = df2[24].replace('xxxxx', name[0])
        with open(name[1] + '.inp', 'w', encoding='utf-8') as file:
            file.writelines( df2 )

        #ｃｓｖ出力用pytyonファイル
        qd2 = copy.deepcopy(self.qd)
        qd2[10] = qd2[10].replace('xxxxx', name[1]+'.odb')
        qd2[30] = qd2[30].replace('xxxxx', name[2]+'.csv')
        with open(name[2] + '.py', 'w', encoding='utf-8') as file:
            file.writelines( qd2 )

#荷重変形関係を成形する関数
##ファイル名, 材長, 変位の範囲, 分割数を指定
##ファイルは拡張子なしの名前を入力
def adjust_csv(name, L, dmax, rate):
    dat = np.loadtxt(name+'.csv',delimiter=',',dtype=float)
    dat[:,1] = dat[:,1]/L*1000

    def_range = dmax
    sampling_rate = rate

    sample_x = dat[:,1]
    sample_y = dat[:,0]

    vals_x = np.linspace(0,def_range,sampling_rate+1)
    vals_y = np.interp(vals_x,sample_x,sample_y)

    return vals_y

#ファイル名を受け取ってABAQUS固有値解析、大変形解析、解析結果の格納を実行する関数
##ファイルは拡張子なしの名前を入力
def abaqus_run(name):
    abaqus_pass = '/appls/ABAQUS/Ver6101/Commands/abaqus'

    eg_cmd = abaqus_pass + ' job=' + name[0] + ' cpus=1 interactive'
    df_cmd = abaqus_pass + ' job=' + name[1] + ' cpus=1 interactive'
    qd_cmd = abaqus_pass + ' python ' + name[2] + '.py'

    subprocess.run(eg_cmd, shell = True, check = True)
    subprocess.run(df_cmd, shell = True, check = True)
    subprocess.run(qd_cmd, shell = True, check = True)


"""
1. パラメータの宣言とターゲットの格納
"""

#解析前提条件変数の宣言
dmax = 100 #同定する変形の範囲の最大値（部材角dmax/1000[rad]まで)
rate = 100 #指定範囲の分割数
inc = 0.1 #パラメータの増分値
error_0 = 1 #誤差ベクトルの収束判定値
divv =10 #選択した特異値ランクで何回回すか
itr_max = 5 *divv #イテレーション回数の最大値
itr_max =100
mode_0 = 1 #行列を縮退するための判定値


#ターゲット荷重変形関係を成形して格納
f_tar = adjust_csv('tar_qd',1000, dmax, rate) #1000で元と同じ

#初期形状の宣言
H = float(1000)
B = float(300)
tw = float(16)
tf = float(22)
l = float(6000)
keta =[int(math.log10(H)), int(math.log10(B)), int(math.log10(tw)), int(math.log10(tf)), int(math.log10(l))]

#参照ファイル名（拡張子なし）を指定してクラスを呼び出し
ref = ['ref_eg','ref_df', 'ref_qd'] #拡張子なし
inp = Create_input(ref)

"""
2. 基準形状の仮定
"""
shape_0 = np.array([H,B,tw,tf,l]) #初期形状の配列
itr_f = np.zeros([rate+1, itr_max]) #各イテレーションの基準荷重ベクトル格納配列
itr_shape = np.zeros([itr_max, len(shape_0)]) #各イテレーションの基準形状格納配列

for p in range(itr_max):
    print('ITARATION' + str(p+1))
    print(shape_0)
    itr_shape[p,:] = shape_0

    """
    3. 仮定形状の荷重変形関係を算定
    """
    #shape_0で定義される形状の.inpファイルを作成
    #eg, df, qdの順は変えないで
    name = ['dum_eg','dum_df', 'dum_qd']
    inp.create_input(shape_0, name)

    #shape_0の解析結果を成形してf_0に格納
    curd =os.getcwd()
    lll =os.listdir(curd)
    abaqus_run(name)
    f_0 = adjust_csv(name[2], shape_0[4], dmax, rate)
    lll2 =os.listdir(curd)
    lll3 =list(set(lll2) -set(lll))
    tmp =curd+"/"+str(p)+"_0_0"
    os.mkdir(tmp)
    for line in lll3:
        shutil.move(curd+"/"+str(line),tmp)
    itr_f[:,p] = f_0

    """
    4. ターゲットと基準形状の差分ベクトル{r}の作成
    """
    #ターゲットとの差分ベクトルを作成
    r_vector =f_tar -f_0
    print("rベクトル",r_vector)

    """
    5. 収束判定
    """
    if r_vector.max() < error_0:
        print('{r}max < ' + str(error_0))
        break
    else:

        """
        6. 各パラメータの増分形状解析を実施
        """
        #増分値incをもとに増分足し合わせ用のマトリクスを作成
        #inc_matrix =np.array([H/100.0,B/100.0,tw/100.0,tf/100.0,l/100.0])
        inc_matrix = np.eye(len(shape_0))
        incmn =0
        while incmn <len(shape_0):
            inc_matrix[incmn,incmn] =shape_0[incmn]/100.0
            incmn +=1
        #kijun =np.linalg.norm(np.array([0.1 for ihadame in range(len(shape_0))])) #特異値スイッチの基準ノルム計算
        kijun =np.linalg.norm(inc_matrix) #特異値スイッチの基準ノルム計算

        #荷重増分マトリクスを格納する配列k_matrixを初期化
        k_matrix = np.zeros([rate+1,len(shape_0)])

        for i in range(len(inc_matrix)):
            #作成ファイル名をi毎に変える場合は名称を宣言
            #name =['dum_eg'+str(i),'dum_df'+str(i), 'dum_qd'+str(i)]

            #i番目のパラメータに微小増分を加算
            shape_i=shape_0+inc_matrix[i]

            #shape_iの.inpファイルを作成
            inp.create_input(shape_i, name)

            #shape_iの解析を実行し解析結果を出力
            curd =os.getcwd()
            lll =os.listdir(curd)
            abaqus_run(name)
            #shape_iの解析結果を成形してf_iに格納
            #L=H*lam
            #print(adjust_csv(name[2], shape_i[4], dmax, rate))
            f_i = adjust_csv(name[2], shape_i[4], dmax, rate)
            lll2 =os.listdir(curd)
            lll3 =list(set(lll2) -set(lll))
            tmp =curd+"/"+str(p)+"_"+str(i)+"_5"
            os.mkdir(tmp)
            for line in lll3:
                shutil.move(curd+"/"+str(line),tmp)

            """
            7. 荷重増分ベクトル{f_inc}を算出
            """
            #i番目のパラメータによる増分ベクトルを作成
            f_inc = f_i-f_0

            """
            8. パラメータ荷重増分マトリクス[k_matrix]を作成
            """
            #荷重増分マトリクスのi列に増分ベクトルf_incを格納
            print("k_mat",k_matrix)
            print("f_incf",f_inc)
            print("inc_mat",inc_matrix)
            k_matrix[:,i] = f_inc/inc_matrix[i,i]

        #np.savetxt('k_matrix.csv',k_matrix,delimiter=',')
        #np.savetxt('r_vector.csv',r_vector,delimiter=',')


        """
        9. [k_matrix]の一般化逆行列を作成
        [k_matrix]+=[V][sigma]-1[U]T
        10. パラメータの増分ベクトルを[k_matrix+] *{r}で算出
        {d(shape0)}=[k_matrix]^+ {r_vector}
        """
        tempi =int(p/divv)
        if tempi >4:
            tempi =4
        while tempi < len(shape_0):
            #print("元行列", k_matrix)
            k_matg =np.linalg.pinv(k_matrix)
            u, s, v =np.linalg.svd(k_matg, full_matrices=False)
            print("u,s,v")
            print(u)
            print(s)
            print(v)
            ss =np.zeros([len(s)])
            un =0
            while un < tempi +1:
                ss[un] =copy.deepcopy(s[un])
                un +=1
            ss =np.diag(ss)
            print("ss",ss)
            k_matrixG =np.dot(np.dot(v.T,ss),u.T)
            print("k_matrixG", k_matrixG)
            #k_matrix =np.linalg.pinv(k_matrix)
            #print("疑似逆行列", k_matrix)
            d_shape_0 =np.dot(k_matrixG.T,r_vector)
            print("d_shape_0", d_shape_0)
            #d_shape_0の桁数が調整元のパラメータ以上のスケール(log10)だったら各値を0.1倍する
            ketan =0
            while ketan <len(d_shape_0):
                if int(math.log10(math.fabs(d_shape_0[ketan]))) >=keta[ketan]:
                    d_shape_0 =d_shape_0 *0.1
                    #調整してみたので、最初からチェック
                    ketan =0
                    continue
                else:
                    #一個めのパラメータが大丈夫そうなら、次のパラメータを見る
                    ketan +=1
            if np.linalg.norm(d_shape_0) >kijun:
                break
            else:
                tempi +=1

        """
        11. 基準形状の更新
        """
        shape_0 = shape_0 +d_shape_0
        if shape_0.any() <0:
            print("shape_0 < 0")
            break
    np.savetxt('itr_f_process.csv', itr_f, delimiter=',')
    np.savetxt('itr_shape_process.csv', itr_shape, delimiter=',')
np.savetxt('itr_f.csv', itr_f, delimiter=',')
np.savetxt('itr_shape.csv', itr_shape, delimiter=',')
print('COMPLETE')
