#import geopandas as gpd
import test2 as t2 
import csv
import sys
import numpy as np
import matplotlib.pyplot as plt

#fp = r"/Users/onoderanaoki/Dropbox/農地プロジェクト/ポリゴンデータ（農水省より入手）/03201盛岡市2017/japan_ver81/japan_ver81.shp"
#data = gpd.read_file(fp)
#data.plot();

#out = r"/Users/onoderanaoki/Dropbox/農地プロジェクト/ポリゴンデータ（農水省より入手）/03201盛岡市2017/03201盛岡市2017_5_2.shp" 
#selection = data[0:5]
#selection.to_file(out)

#fp_50 = r"/Users/onoderanaoki/Dropbox/農地プロジェクト/ポリゴンデータ（農水省より入手）/03201盛岡市2017/03201盛岡市2017_5_2.shp"

#data_50 = gpd.read_file(fp_50)
#data_50.plot();
#data = gpd.read_file(fp)

#data.plot();
#print(data.crs)

def mapplotfarmer():
	#farmer = ("5c51d9e57c7133dcc0310c7121ff3d09",)
	farmer = ("d13345046225a821c12782c4632f88cb",)
	rows = t2.retrievefromdb(farmer)
	#上記耕作者が耕作している地域の農地を取得
	applicablearea = t2.searchfarmland(rows)
	print(applicablearea)
	rows2 = t2.farmersretrievefromdb(applicablearea)
	#print(rows2)
	#print(applicablearea)
	#t2.mapplot(rows,applicablearea)
	#t2.mapplotfarmers(rows,applicablearea)
	t2.mapplotfarmers(rows,rows2,farmer)

def mapplotfarmer2():
	farmer = ("d13345046225a821c12782c4632f88cb",)
	#farmer = ("7e2047b697ce0f5778f6d8e43d68dd2e",)
	rows = t2.retrievefromdb(farmer)
	#print(rows)
	#上記farmerが耕作する農地農地、もっとも遠い農地の距離を求める
	#print(rows[0][7])
	#上記耕作者が耕作している周りの農地情報を取得
	rows2 = t2.searchsurroundfarmland(rows)		
	#print(applicablearea)
	#rows2 = t2.farmersretrievefromdb(applicablearea)
	#print(rows2)
	#print(applicablearea)
	#t2.mapplot(rows,applicablearea)
	#t2.mapplotfarmers(rows,applicablearea)
	print(t2.measuredistancebetweenfarmland(rows))
	t2.mapplotfarmers(rows,rows2,farmer)


def mapplotinarea(area):
	rows = t2.farmersretrievefromdb2(area)
	#t2.mapplotfarmers2(rows)
	t2.mapplot(rows)
	
def farmlandredistribution(area):
	#areaのfarmland情報を取得
	rows = t2.farmersretrievefromdb(area)
	#地図にプロット
	t2.mapplotfarmers(rows)
	#再配分
	t2.redistribution(rows)


def cityscul():
	city = ("遠野市","一関市","陸前高田市","釜石市","二戸市","八幡平市","奥州市","滝沢市","雫石町","葛巻町","岩手町","志和町","矢巾町","西和賀町","金ケ崎町","平泉町","住田町","大槌町","山田町","岩泉町","田野畑村","普代村","軽米町","野田村","九戸村","洋野町","一戸町")
	for i in city:
		print(i)
		t2.main(i)

def histplot():
	x = list(t2.farmlandsdistance())
	print(np.amax(x))
	y = np.array(x).flatten()
	plt.hist(y,bins=10)
	plt.show()

#histplot()
#mapplotfarmer("57e53ce9389d91eaf8c0e0c02160a093")
#mapplotfarmer()


#mapplotfarmer2()
area = ("花巻市上根子字谷地","花巻市上根子字米倉")
mapplotinarea(area)
#t2.main("北上市")

#重心の計算
#t2.calculatecenterofgravity()

#rows = t2.addresslist("札幌市")
#print(rows)
#t2.mapplot(rows)

#指定した市町村の田の合計面積と件数
#t2.conditionalareatotal("盛岡市")