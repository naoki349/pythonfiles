import test2 as t2 
import test7 as t7
import MySQLdb
import numpy as np
import pandas as pd
import folium
import sys
import random
from tqdm import tqdm

def farmlandoptimization2():
	#if __name__ == '__main__':
	distancepre = {}
	distancepost = {}
	arr = []
	temp = ""
	#該当する農家の農地情報を取得
	#areaname = ("花巻市上根子","花巻市中北万","花巻市上北万","花巻市南万")
	areaname = ("花巻市上北万")
	farmersinfo = np.array(t2.farmersretrievefromdb4(areaname))
	#0:id		1:farmer		2:zyuusinnLatitude		3:zyuusinnlongitude		4:checkfarmer		5:maximumdistancefarmland		6:distance
	#print(farmersinfo)
	farmersuniq = sorted(set(farmersinfo[:,4]))	
	#print(farmersuniq)
	#farmersの農家について、該当農家とそれ以外として交換する
	for naoki,farmer in enumerate(tqdm(farmersuniq)):
		#print(farmer)
		#最も重心から遠い農地を引数として渡し、この農地を半径とした場合の円内にある農地情報を取得
		#rows = t2.retrievefromdb5(farmer) 	#重心からの距離で降順
		hohoho = np.where(farmer == farmersinfo[:1])		#?farmersinfo[1]のみ検索し、distanceで降順に並べる
		#hohoho = np.array(rows)
		#print(hohoho)
		#print(str(hohoho[0][26]) +  " " + str(hohoho[0][27]))
		#farmarの農地が一つしかない場合、次の農家に移す
		if farmersinfo[hohoho[0]][6] == 0.0: #or hohoho[0][28] == None:			#農地が一つの場合、dbに聞きにいく前に次の農家に行くようにした方が良い
			#print("continueします")
			continue
		#farmer以外の農家に関して、farmerの周りにある農地情報を取得
		#rows2 = t2.surroundfarmlandinformation3(hohoho[0][2],hohoho[0][1],hohoho[0][9],hohoho[0][27])		#[2]:Latitude,[1]:longitude,[9]:farmer,[27]:distance
		#print(hohoho[0][27])
		#rows2 = t2.surroundfarmlandinformation3(hohoho[0][26],hohoho[0][25],hohoho[0][9],hohoho[0][28])		#[2]:Latitude,[1]:longitude,[9]:farmer,[27]:distance,[25]:zyuusinnlongitude,[26]:zyuusinnLatitude
		nothohoho = np.where(farmer == farmersinfo[:4] and farmer != farmersinfo[:1])		#distanceで降順に並べる
		#print(rows2)
		#nothohoho = np.array(rows2)
		#print(nothohoho)
		#hohohoho,hohohohoho = np.where(farmer == farmersinfo)
		#農地の交換
		for i,hoho in enumerate(tqdm(hohoho)):
			#print(hoho[0])
			#if hoho[27] == 0.0 or hoho[27] == None or nothoho[27] == 0.0 :
					#continue
			for j,nothoho in enumerate(nothohoho):
				#農地が一つしかない場合、対象農家の場合は、交換の対象としない
				if nothoho[29] == None:
					continue
				if (t2.dist_on_sphere((float(hoho[26]),float(hoho[25])),(float(nothoho[2]),float(nothoho[1]))) < float(hoho[28])) and (t2.dist_on_sphere((float(hoho[2]),float(hoho[1])),(float(nothoho[26]),float(nothoho[25]))) < float(nothoho[29])):
					#print("farmer(hohoho):" + str(hohoho[i][9]) + " 交換前:" + str(hohoho[i][0]) + " farmer(nothohoho):" + str(nothohoho[j][9]) + " 交換前:" + str(nothohoho[j][0]) )
					#全ての農地情報を交換
					temp = hoho.copy()
					hoho = nothoho.copy()
					hohoho[i] = hoho.copy()
					nothoho = temp	#いらない
					nothohoho[j] = temp
					#farmer情報を交換
					ho = hohoho[i][9]
					hohoho[i][9] = nothohoho[j][9]
					hoho[9] = hohoho[i][9]
					nothohoho[j][9] = ho
					nothoho[9] = ho	#いらない
					#zyuusinnLatitude,zyuusinnlongitudeを交換を交換
					hogehogehogehoge,hogehogehogehogehoge = hohoho[i][26],hohoho[i][25]
					hohoho[i][26],hohoho[i][25] = nothohoho[j][26],nothohoho[j][25]
					hoho[26],hoho[25] = hohoho[i][26],hohoho[i][25]
					nothohoho[j][26],nothohoho[j][25] = hogehogehogehoge,hogehogehogehogehoge
					nothoho[26],nothoho[25] = hogehogehogehoge,hogehogehogehogehoge		#いらない
					#対象耕作者の重心までの距離を更新
					hohoho[i][28] = t2.dist_on_sphere((float(hohoho[i][2]),float(hohoho[i][1])),(float(hohoho[i][26]),float(hohoho[i][25])))
					hoho[28] = hohoho[i][28]
					nothohoho[j][28] = t2.dist_on_sphere((float(nothohoho[j][2]),float(nothohoho[j][1])),(float(hohoho[i][26]),float(hohoho[i][25])))
					nothoho[28] = nothohoho[j][27]	#いらない
					#自身の重心までの距離を更新
					hohoho[i][29] =  ""
					hoho[29] = ""
					nothohoho[j][29] = t2.dist_on_sphere((float(nothohoho[j][2]),float(nothohoho[j][1])),(float(nothohoho[j][26]),float(nothohoho[j][25])))
					nothoho[29] = nothohoho[j][29]	#いらない
					#交換フラグを変更
					hohoho[i][30] = 1
					hoho[30] = 1
					nothohoho[j][30] = 1
					nothoho[30] = 1	#いらない
					#交換情報を記録
					car = ""
					if hoho[27] is None:
						car = str(nothoho[9]) + "→" + str(hoho[9]) + "→"
						#car = str(nothoho[0]) + "," + str(hoho[0]) + ","
						hoho[27] = car
						hohoho[i][27] = car
					else:
						car = str(hoho[27]) + hoho[9] + "→"
						hoho[27] = car
						hohoho[i][27] = car
						#hohoho[i][27] == ""
						#print("noneでした")
					#hohoho[i][27].append(str(nothohoho[j][0]) + "→") 
					#hoho[27] = hohoho[i][27]
					#print(hoho[27])
					car2 = ""
					if nothoho[27] is None:
						#car2 = str(hoho[0]) + "," +  str(nothoho[0]) + ","
						car2 =  str(hoho[9]) + "→" +  str(nothoho[9]) + "→"
						nothoho[27] = car2
						nothohoho[j][27] = car2
					else:
						#car2 = nothoho[27] + str(nothoho[0]) + ","
						car2 = str(nothoho[27]) + str(nothoho[9])+ "→"
						nothoho[27] = car2
						nothohoho[j][27] = car2
					#print(nothoho[27])
					#print("farmer(hohoho):" + str(hohoho[i][9]) + " 交換後:" + str(hohoho[i][0]) + " farmer(nothohoho):" + str(nothohoho[j][9]) + " 交換後:" + str(nothohoho[j][0]) )
					break
		#mysqlを更新(farmerが変わるタイミング)				交換するタイミングについては、例えば5000個以上溜まったら実行する、というのも手か
		#print("sqlの操作")
		sys.exit()
		updateid = ""
		updatefarmer = ""
		updatezyuusinnLatitude = ""
		updatezyuusinnlongitude = ""
		updateexchangerecord = ""
		for i,fish in enumerate(hohoho):
			if fish[30] == 1:
				updateid += str(fish[0]) + ","								#id
				updatefarmer += "'" + str(fish[9]) + "',"				#farmer
				updatezyuusinnLatitude += str(fish[26]) + ","	#zyuusinnLatitude
				updatezyuusinnlongitude += str(fish[25]) + ","	#zyuusinnlongitude
				#updateexchangerecord = join(fish[27])
				#print(fish[27])
				updateexchangerecord += "'" + str(fish[27]) + "',"	#exchangerecord
				hohoho[i][30] = 0
				#hoho[29] = 0
		for j,melon in enumerate(nothohoho):
			if melon[30] == 1:
				updateid += str(melon[0]) + ","								#id
				updatefarmer += "'" + str(melon[9]) + "',"				#farmer
				updatezyuusinnLatitude += str(melon[26]) + ","	#zyuusinnLatitude
				updatezyuusinnlongitude += str(melon[25]) + ","	#zyuusinnlongitude
				#updateexchangerecord = join(melon[27])
				updateexchangerecord += "'" + str(melon[27]) + "',"	#exhangerecord
				nothohoho[j][30] = 0
				#nothoho[29] = 0
		#文字列の最後の「,」を削除し、dbを更新する
		#print("ID:" + str(updateid))
		if updateid != "":
			updateid = updateid[:-1]
			updatefarmer = updatefarmer[:-1]
			updatezyuusinnLatitude = updatezyuusinnLatitude[:-1]
			updatezyuusinnlongitude = updatezyuusinnlongitude[:-1]
			updateexchangerecord = updateexchangerecord[:-1]
			t7.massinputsql2(updateid,updatefarmer,updatezyuusinnLatitude,updatezyuusinnlongitude,updateexchangerecord)
	print(str(areaname) + "の処理が終わりました。")

def checkforchange():
	distancepre = {}
	distancepost = {}
	dispre = 0
	dispost = 0
	areaname = ("花巻市上根子")
	#指定地域の農地情報を取得
	row1,row2 = runtwosql(areaname)
	row1 = np.array(row1)
	row2 = np.array(row2)
	farmersuniq = sorted(set(row1[:,9]))	
	#print(row1)
	#print(row2)
	for farmer in tqdm(farmersuniq):
		gaitourow1 = []
		gaitourow2 = []
		#交換前の農地間の距離を求める（最小全域木問題）
		ho,hoo = np.where(farmer == row1)
		for hoge in ho:
			gaitourow1.append(row1[hoge])
		gaitourow1 = np.array(gaitourow1)
		hoho,hoohoo = np.where(farmer == row2)
		for hogehoge in hoho:
			gaitourow2.append(row2[hogehoge])
		gaitourow2 = np.array(gaitourow2)
		#farmerごとに距離を計測
		#if farmer == '32e03320f345f7aefd82a1c37ee2a1d2':
			#print(str(gaitourow1[gaitourow1[:,2].argsort(),:]) + " " + str(gaitourow2[gaitourow2[:,2].argsort(),:]))
		if len(gaitourow1) == 1:
			distancepre[farmer] = 0
		else:
			distancepre[farmer] = t2.measuredistancebetweenfarmland2(gaitourow1[gaitourow1[:,2].argsort(),:])		#noutinavi_addzyuusinnのfarmerの全ての農地の距離
		if len(gaitourow2) != 0:
			distancepost[farmer] = t2.measuredistancebetweenfarmland2(gaitourow2[gaitourow2[:,2].argsort(),:])		#noutinavi_addzyuusinn2のfarmerの全ての農地の距離
		else:
			distancepost[farmer] = 0
		#print(distancepre)
		#print(distancepost)
		dispre += distancepre[farmer]
		dispost += distancepost[farmer]
	for farmer in tqdm(farmersuniq):	
		if distancepre[farmer] != 0:
			rate = (distancepost[farmer] - distancepre[farmer]) /distancepre[farmer]
		else:
			rate = 0
		print("farmer: " + farmer + " 交換前:" + str(distancepre[farmer]) + " 交換後:" + str(distancepost[farmer]) + " 増加率:" + str(rate) + " 寄与度:" + str((distancepost[farmer] - distancepre[farmer]) / (dispost - dispre)))
	print("総距離の増加率:" + str((dispost-dispre)/dispre))
	print("総距離(pre):" + str(dispre))
	print("総距離(post):" + str(dispost))

def runtwosql(areaname):
	conn = MySQLdb.connect(
	user='root',
	passwd='',
	host='localhost',
	db='db',
	charset='utf8')
	# カーソルを取得する
	cur = conn.cursor()	
	
	sql1 = "select * from noutinavi_addzyuusinn where farmer = any (select distinct(farmer) from noutinavi_addzyuusinn where address like '%" +str(areaname) +"%')  and classification_of_land_code_name = '田';"
	cur.execute(sql1)
	row1 = cur.fetchall()
	
	sql2 = "select * from noutinavi_addzyuusinn2 where farmer = any (select distinct(farmer) from noutinavi_addzyuusinn where address like '%" +str(areaname) +"%')  and classification_of_land_code_name = '田';"
	cur.execute(sql2)
	row2 = cur.fetchall()
	
	return row1,row2
#iconinfo = farmlandoptimizationbefore()
#farmlandoptimization2(iconinfo)
farmlandoptimization2()
#checkforchange()