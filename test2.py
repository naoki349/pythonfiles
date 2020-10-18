import networkx as nx
import matplotlib.pyplot as plt
import MySQLdb
from tqdm import tqdm
import csv
import sys
import numpy as np
from scipy.sparse.csgraph import shortest_path, floyd_warshall, dijkstra, bellman_ford, johnson
from scipy.sparse import csr_matrix
#import test10_newalgorithm as t10

def init():
    global cnx #接続オブジェクトをグローバル変数で定義する。
    cnx = MySQLdb.connect(host='localhost', user='root', password='',  db='db',charset='utf8')

def initareaname(areaname):
	global glbareaname
	glbareaname = areaname

def rowsreceiver(hoge):
	global glbrows
	glbrows = hoge

def rowssubmit():
	print(glbrows)
	#return glbrows

def retrievefromdb(farmer):
	#if __name__ == '__main__':
		# 接続する
		conn = MySQLdb.connect(
		user='root',
		passwd='',
		host='localhost',
		db='db')
		# カーソルを取得する
		cur = conn.cursor()		
		# SQL（データベースを操作するコマンド）を実行する
		sql = "select distinct id,latitude,longitude,farmer,zyuusinnLatitude,zyuusinnlongitude,address,(6371 * acos(cos(radians(zyuusinnLatitude))* cos(radians(latitude))* cos(radians(longitude) - radians(zyuusinnlongitude))+ sin(radians(zyuusinnLatitude))* sin(radians(latitude)))) AS distance,null,selectedfarm_disp_area_on_registry from noutinavi_addzyuusinn where farmer = '" + str(farmer[0]) + "' and classification_of_land_code_name = '田' ORDER BY distance desc;"
		#print(sql)
		cur.execute(sql)
		# 実行結果を取得する
		rows = cur.fetchall()
		# 接続を閉じる
		cur.close
		conn.close
		return rows

def retrievefromdb2(farmer):
	#if __name__ == '__main__':
		# 接続する
		conn = MySQLdb.connect(
		user='root',
		passwd='',
		host='localhost',
		db='db')
		# カーソルを取得する
		cur = conn.cursor()		
		# SQL（データベースを操作するコマンド）を実行する
		sql = "select distinct *,(6378.137 * acos(cos(radians(zyuusinnLatitude))* cos(radians(latitude))* cos(radians(longitude) - radians(zyuusinnlongitude))+ sin(radians(zyuusinnLatitude))* sin(radians(latitude)))) AS distance ,null ,null from noutinavi_addzyuusinn where farmer = '" + str(farmer) + "' and classification_of_land_code_name = '田' ORDER BY distance desc;"
		#print(sql)
		cur.execute(sql)
		# 実行結果を取得する
		rows = cur.fetchall()
		# 接続を閉じる
		cur.close
		conn.close
		return rows

def retrievefromdb3(farmers):		#noutinavi_addzyuusinn2からデータを入手
	#if __name__ == '__main__':
		# 接続する
		conn = MySQLdb.connect(
		user='root',
		passwd='',
		host='localhost',
		db='db',
		charset='utf8')
		# カーソルを取得する
		cur = conn.cursor()		
		# SQL（データベースを操作するコマンド）を実行する
		sql = "select distinct id,longitude,Latitude,address,classification_of_land_code_name,selectedfarm_disp_area_on_registry,section_of_noushinhou_code_name,section_of_toshikeikakuhou_code_name,owner_farm_intention_code_name,farmer,kind_of_right_code_name,commencement_and_end_stages_from_to,right_setting_contents_code_name,usage_situation_investigation_result_code_name,disp_usage_situation_investigation_date,owner_ascertainment_status_code_name,disp_public_date_by_nouchihou_no_323,owner_statement_intent_survey_results_code_name,disp_useIntention_investigation_date,disp_recommendation_conten_date,disp_notice_date_by_nouchihou_no_43,disp_order_date_nouchihou_no_441,disp_notice_date_by_nouchihou_no_443,farm_committee_name,processed_time,zyuusinnlongitude,zyuusinnLatitude,(6378.137 * acos(cos(radians(zyuusinnLatitude))* cos(radians(latitude))* cos(radians(longitude) - radians(zyuusinnlongitude))+ sin(radians(zyuusinnLatitude))* sin(radians(latitude)))) AS distance ,null ,null from noutinavi_addzyuusinn2 where ( " + str(farmers) + ") and classification_of_land_code_name = '田' ORDER BY farmer;"
		#print(sql)
		cur.execute(sql)
		# 実行結果を取得する
		rows = cur.fetchall()
		# 接続を閉じる
		cur.close
		conn.close
		return rows

def retrievefromdb4(farmers):			#noutinavi_addzyuusinnからデータを入手
	#if __name__ == '__main__':
		# 接続する
		conn = MySQLdb.connect(
		user='root',
		passwd='',
		host='localhost',
		db='db')
		# カーソルを取得する
		cur = conn.cursor()		
		# SQL（データベースを操作するコマンド）を実行する
		sql = "select distinct id,longitude,Latitude,address,classification_of_land_code_name,selectedfarm_disp_area_on_registry,section_of_noushinhou_code_name,section_of_toshikeikakuhou_code_name,owner_farm_intention_code_name,farmer,kind_of_right_code_name,commencement_and_end_stages_from_to,right_setting_contents_code_name,usage_situation_investigation_result_code_name,disp_usage_situation_investigation_date,owner_ascertainment_status_code_name,disp_public_date_by_nouchihou_no_323,owner_statement_intent_survey_results_code_name,disp_useIntention_investigation_date,disp_recommendation_conten_date,disp_notice_date_by_nouchihou_no_43,disp_order_date_nouchihou_no_441,disp_notice_date_by_nouchihou_no_443,farm_committee_name,processed_time,zyuusinnlongitude,zyuusinnLatitude,(6378.137 * acos(cos(radians(zyuusinnLatitude))* cos(radians(latitude))* cos(radians(longitude) - radians(zyuusinnlongitude))+ sin(radians(zyuusinnLatitude))* sin(radians(latitude)))) AS distance ,null ,null from noutinavi_addzyuusinn where ( " + str(farmers) + ") and classification_of_land_code_name = '田' ORDER BY farmer;"
		#print(sql)
		cur.execute(sql)
		# 実行結果を取得する
		rows = cur.fetchall()
		# 接続を閉じる
		cur.close
		conn.close
		return rows

def retrievefromdb5(farmer):
	#if __name__ == '__main__':
		# 接続する
		conn = MySQLdb.connect(
		user='root',
		passwd='',
		host='localhost',
		db='db',
		charset='utf8')
		# カーソルを取得する
		cur = conn.cursor()		
		# SQL（データベースを操作するコマンド）を実行する
		sql = "select distinct *,(6378.137 * acos(cos(radians(zyuusinnLatitude))* cos(radians(latitude))* cos(radians(longitude) - radians(zyuusinnlongitude))+ sin(radians(zyuusinnLatitude))* sin(radians(latitude)))) AS distance ,null ,null,null from noutinavi_addzyuusinn2 where farmer = '" + str(farmer) + "' and classification_of_land_code_name = '田' ORDER BY distance desc;"
		#print(sql)
		cur.execute(sql)
		# 実行結果を取得する
		rows = cur.fetchall()
		# 接続を閉じる
		cur.close
		conn.close
		return rows

def retrievefromdb6(farmer):
	#if __name__ == '__main__':
		# 接続する
		conn = MySQLdb.connect(
		user='root',
		passwd='',
		host='localhost',
		db='db',
		charset='utf8')
		# カーソルを取得する
		cur = conn.cursor()		
		# SQL（データベースを操作するコマンド）を実行する
		sql = "select  id,longitude,Latitude,selectedfarm_disp_area_on_registry,farmer,zyuusinnlongitude,zyuusinnLatitude,exchangerecord,(6378.137 * acos(cos(radians(zyuusinnLatitude))* cos(radians(latitude))* cos(radians(longitude) - radians(zyuusinnlongitude))+ sin(radians(zyuusinnLatitude))* sin(radians(latitude)))) AS distance ,null ,null  from noutinavi_addzyuusinn2 where farmer = '" + str(farmer) + "' and classification_of_land_code_name = '田' ORDER BY distance desc;"
		#print(sql)
		cur.execute(sql)
		# 実行結果を取得する
		rows = cur.fetchall()
		# 接続を閉じる
		cur.close
		conn.close
		return rows

def retrievefromdb7(farmer):
	#if __name__ == '__main__':
		# 接続する
		#conn = MySQLdb.connect(
		#user='root',
		#passwd='',
		#host='localhost',
		#db='db',
		#charset='utf8')
		
		# カーソルを取得する
		cur = cnx.cursor()		
		# SQL（データベースを操作するコマンド）を実行する
		sql = "select  farmer,zyuusinnLatitude,zyuusinnlongitude,max((6378.137 * acos(cos(radians(zyuusinnLatitude))* cos(radians(latitude))* cos(radians(longitude) - radians(zyuusinnlongitude))+ sin(radians(zyuusinnLatitude))* sin(radians(latitude))))) from noutinavi_addzyuusinn2 where farmer = '" + str(farmer[0]) + "' and classification_of_land_code_name = '田' group by farmer,zyuusinnLatitude,zyuusinnlongitude;"
		#print(sql)
		cur.execute(sql)
		# 実行結果を取得する
		#print(farmer[0])
		rows =  list(cur.fetchall())
		#print(rows)
		# 接続を閉じる
		#cur.close
		#conn.close
		return rows

def retrievefromdb8(farmers):		#noutinavi_addzyuusinn2からデータを入手
	#if __name__ == '__main__':
		# 接続する
		conn = MySQLdb.connect(
		user='root',
		passwd='',
		host='localhost',
		db='db',
		charset='utf8')
		# カーソルを取得する
		cur = conn.cursor()
		# SQL（データベースを操作するコマンド）を実行する
		sql = "select distinct id,longitude,Latitude,address,classification_of_land_code_name,selectedfarm_disp_area_on_registry,section_of_noushinhou_code_name,section_of_toshikeikakuhou_code_name,owner_farm_intention_code_name,farmer,kind_of_right_code_name,commencement_and_end_stages_from_to,right_setting_contents_code_name,usage_situation_investigation_result_code_name,disp_usage_situation_investigation_date,owner_ascertainment_status_code_name,disp_public_date_by_nouchihou_no_323,owner_statement_intent_survey_results_code_name,disp_useIntention_investigation_date,disp_recommendation_conten_date,disp_notice_date_by_nouchihou_no_43,disp_order_date_nouchihou_no_441,disp_notice_date_by_nouchihou_no_443,farm_committee_name,processed_time,zyuusinnlongitude,zyuusinnLatitude,(6378.137 * acos(cos(radians(zyuusinnLatitude))* cos(radians(latitude))* cos(radians(longitude) - radians(zyuusinnlongitude))+ sin(radians(zyuusinnLatitude))* sin(radians(latitude)))) AS distance ,null ,null from noutinavi_addzyuusinn_shudou where ( " + str(farmers) + ") and classification_of_land_code_name = '田' ORDER BY farmer;"
		#print(sql)
		cur.execute(sql)
		# 実行結果を取得する
		rows = cur.fetchall()
		# 接続を閉じる
		cur.close
		conn.close
		return rows

def farmersretrievefromdb(areas):
	#if __name__ == '__main__':
		# 接続する
		rows = []
		conn = MySQLdb.connect(
		user='root',
		passwd='',
		host='localhost',
		db='db')
		# カーソルを取得する
		cur = conn.cursor()
		for area in areas:
			# SQL（データベースを操作するコマンド）を実行する
			sql = "select distinct id,latitude,longitude,farmer,zyuusinnLatitude,zyuusinnlongitude,address,null,null,selectedfarm_disp_area_on_registry from noutinavi_addzyuusinn where address like '%" + str(area) + "%' and classification_of_land_code_name = '田'  order by farmer;"
			cur.execute(sql)
			# 実行結果を取得する
			#print(cur.fetchall())
			rows.append(list(cur.fetchall()))
		# 接続を閉じる
		cur.close
		conn.close
		#print(sum(rows,[]))
		return sum(rows,[])
		
def farmersretrievefromdb2(areas):
	#if __name__ == '__main__':
		# 接続する
		rows = []
		conn = MySQLdb.connect(
		user='root',
		passwd='',
		host='localhost',
		db='db')
		# カーソルを取得する
		cur = conn.cursor()
		for area in areas:
			# SQL（データベースを操作するコマンド）を実行する
			sql = "select distinct *,(6371 * acos(cos(radians(zyuusinnLatitude))* cos(radians(latitude))* cos(radians(longitude) - radians(zyuusinnlongitude))+ sin(radians(zyuusinnLatitude))* sin(radians(latitude)))) AS distance ,null,null from noutinavi_addzyuusinn where address like '%" + str(area) + "%' and classification_of_land_code_name = '田'  order by farmer;"
			cur.execute(sql)
			# 実行結果を取得する
			#print(cur.fetchall())
			rows.append(list(cur.fetchall()))
		# 接続を閉じる
		cur.close
		conn.close
		#print(sum(rows,[]))
		return sum(rows,[])

def farmersretrievefromdb3(areas):
	#if __name__ == '__main__':
		# 接続する
		rows = []
		conn = MySQLdb.connect(
		user='root',
		passwd='',
		host='localhost',
		db='db',
		charset='utf8')
		#カーソルを取得する
		#print(areas)
		cur = conn.cursor()
		#print(areas)
		for area in areas:
			# SQL（データベースを操作するコマンド）を実行する
			sql = "select distinct *,(6371 * acos(cos(radians(zyuusinnLatitude))* cos(radians(latitude))* cos(radians(longitude) - radians(zyuusinnlongitude))+ sin(radians(zyuusinnLatitude))* sin(radians(latitude)))) AS distance ,null,null,null from noutinavi_addzyuusinn2 where address like '%" + str(area) + "%' and classification_of_land_code_name = '田'  order by farmer;"
			#print(sql)
			#sql = "select distinct * from noutinavi_addzyuusinn where address like '%" + str(area) + "%' and classification_of_land_code_name = '田'  order by farmer;"
			cur.execute(sql)
			# 実行結果を取得する
			#print(cur.fetchall())
			rows.append(list(cur.fetchall()))
		# 接続を閉じる
		cur.close
		conn.close
		#print(sum(rows,[]))
		return sum(rows,[])

def farmersretrievefromdb4(area):
	#if __name__ == '__main__':
		# 接続する
		rows = []
		conn = MySQLdb.connect(
		user='root',
		passwd='',
		host='localhost',
		db='db',
		charset='utf8')
		#カーソルを取得する
		cur = conn.cursor()
		# SQL（データベースを操作するコマンド）を実行する
		sql = "select id,farmer,zyuusinnLatitude,zyuusinnlongitude,checkfarmer,maximumdistancefarmland,(6378.137 * acos(cos(radians(zyuusinnlat))* cos(radians(latitude))* cos(radians(longitude) - radians(zyuusinnlon))+ sin(radians(zyuusinnlat))* sin(radians(latitude)))) AS distance from noutinavi_addzyuusinn2 inner join (select max((6378.137 * acos(cos(radians(zyuusinnLatitude))* cos(radians(latitude))* cos(radians(longitude) - radians(zyuusinnlongitude))+ sin(radians(zyuusinnLatitude))* sin(radians(latitude))))) AS maximumdistancefarmland,farmer as checkfarmer,GROUP_CONCAT(distinct(zyuusinnLatitude)) as zyuusinnlat,GROUP_CONCAT(distinct(zyuusinnlongitude)) as zyuusinnlon from noutinavi_addzyuusinn2 where farmer in ( select distinct farmer from noutinavi_addzyuusinn2 where address like '%" + str(area) + "%' and classification_of_land_code_name = '田'  order by farmer) group by farmer )as tmp2 on (6378.137 * acos(cos(radians(zyuusinnlat))* cos(radians(latitude))* cos(radians(longitude) - radians(zyuusinnlon))+ sin(radians(zyuusinnlat))* sin(radians(latitude)))) <= tmp2.maximumdistancefarmland order by checkfarmer,distance;"
		print(sql)
		cur.execute(sql)
		# 実行結果を取得する
		rows = cur.fetchall()
		# 接続を閉じる
		cur.close
		conn.close
		return rows
		
def farmersretrievefromdb5(areas):
	#if __name__ == '__main__':
		# 接続する
		rows = []
		conn = MySQLdb.connect(
		user='root',
		passwd='',
		host='localhost',
		db='db')
		# カーソルを取得する
		cur = conn.cursor()
		for area in areas:
			# SQL（データベースを操作するコマンド）を実行する
			sql = "select distinct id,latitude,longitude,farmer,zyuusinnLatitude,zyuusinnlongitude,address from noutinavi_addzyuusinn2 where address like '%" + str(area) + "%' and classification_of_land_code_name = '田'  order by farmer;"
			cur.execute(sql)
			# 実行結果を取得する
			rows.append(list(cur.fetchall()))
		# 接続を閉じる
		cur.close
		conn.close
		#print(sum(rows,[]))
		return sum(rows,[])
		

def farmersretrievefromdb6(areas):
	#if __name__ == '__main__':
		# 接続する
		rows = []
		conn = MySQLdb.connect(
		user='root',
		passwd='',
		host='localhost',
		db='db',
		charset='utf8')
		#カーソルを取得する
		#print(areas)
		cur = conn.cursor()
		#print(areas)
		for area in areas:
			# SQL（データベースを操作するコマンド）を実行する
			sql = "select distinct farmer from noutinavi_addzyuusinn where address like '%" + str(area) + "%' and classification_of_land_code_name = '田'  order by farmer;"
			print(sql)
			#sql = "select distinct * from noutinavi_addzyuusinn where address like '%" + str(area) + "%' and classification_of_land_code_name = '田'  order by farmer;"
			cur.execute(sql)
			# 実行結果を取得する
			#print(cur.fetchall())
			rows.append(list(cur.fetchall()))
		# 接続を閉じる
		cur.close
		conn.close
		#print(sum(rows,[]))
		return sum(rows,[])

def farmersretrievefromdb7(area):
	#if __name__ == '__main__':
		# 接続する
		rows = []
		conn = MySQLdb.connect(
		user='root',
		passwd='',
		host='localhost',
		db='db',
		charset='utf8')
		#カーソルを取得する
		#print(areas)
		cur = conn.cursor()
		#print(areas)
			# SQL（データベースを操作するコマンド）を実行する
		sql = "select distinct farmer from noutinavi_addzyuusinn where address like '%" + str(area) + "%' and classification_of_land_code_name = '田'  order by farmer;"
		#print(sql)
		#sql = "select distinct * from noutinavi_addzyuusinn where address like '%" + str(area) + "%' and classification_of_land_code_name = '田'  order by farmer;"
		cur.execute(sql)
		# 実行結果を取得する
		#print(cur.fetchall())
		rows.append(list(cur.fetchall()))
		# 接続を閉じる
		cur.close
		conn.close
		#print(sum(rows,[]))
		return sum(rows,[])
		
def farmersretrievefromdb8(areas):
	#if __name__ == '__main__':
		# 接続する
		rows = []
		conn = MySQLdb.connect(
		user='root',
		passwd='',
		host='localhost',
		db='db')
		# カーソルを取得する
		cur = conn.cursor()
		for area in areas:
			# SQL（データベースを操作するコマンド）を実行する
			sql = "select id,latitude,longitude,farmer,zyuusinnLatitude,zyuusinnlongitude,address from noutinavi_addzyuusinn2 where farmer in (select farmer from noutinavi_addzyuusinn where classification_of_land_code_name = '田' and address like '%" +str(area) + "%' group by farmer having sum(selectedfarm_disp_area_on_registry) > 50000 ) order by farmer;"
			cur.execute(sql)
			# 実行結果を取得する
			rows.append(list(cur.fetchall()))
		# 接続を閉じる
		cur.close
		conn.close
		#print(sum(rows,[]))
		return sum(rows,[])

def farmersretrievefromdb9(area):		
	#if __name__ == '__main__':
		# 接続する
		rows = []
		conn = MySQLdb.connect(
		user='root',
		passwd='',
		host='localhost',
		db='db',
		charset='utf8')
		#カーソルを取得する
		#print(areas)
		cur = conn.cursor()
		#print(areas)
			# SQL（データベースを操作するコマンド）を実行する
		sql = "select distinct farmer from noutinavi_addzyuusinn2 where classification_of_land_code_name = '田' and farmer in (select farmer from noutinavi_addzyuusinn2 where classification_of_land_code_name = '田' and address like '%" +str(area) + "%' group by farmer having sum(selectedfarm_disp_area_on_registry) > 50000 ) order by farmer;"
		#print(sql)
		#sql = "select distinct * from noutinavi_addzyuusinn where address like '%" + str(area) + "%' and classification_of_land_code_name = '田'  order by farmer;"
		cur.execute(sql)
		# 実行結果を取得する
		#print(cur.fetchall())
		rows.append(list(cur.fetchall()))
		# 接続を閉じる
		cur.close
		conn.close
		#print(sum(rows,[]))
		return sum(rows,[])
		
def farmersretrievefromdb10(areas):		#交換前
	#if __name__ == '__main__':
		# 接続する
		rows = []
		conn = MySQLdb.connect(
		user='root',
		passwd='',
		host='localhost',
		db='db')
		# カーソルを取得する
		cur = conn.cursor()
		for area in areas:
			# SQL（データベースを操作するコマンド）を実行する
			sql = "select id,latitude,longitude,farmer,zyuusinnLatitude,zyuusinnlongitude,address from noutinavi_addzyuusinn where farmer in (select farmer from noutinavi_addzyuusinn where classification_of_land_code_name = '田' and address like '%" +str(area) + "%' group by farmer having sum(selectedfarm_disp_area_on_registry) > 50000 ) order by farmer;"
			cur.execute(sql)
			# 実行結果を取得する
			rows.append(list(cur.fetchall()))
		# 接続を閉じる
		cur.close
		conn.close
		#print(sum(rows,[]))
		return sum(rows,[])
		
def farmersretrievefromdb11(areas):		#交換後
	#if __name__ == '__main__':
		# 接続する
		rows = []
		conn = MySQLdb.connect(
		user='root',
		passwd='',
		host='localhost',
		db='db')
		# カーソルを取得する
		cur = conn.cursor()
		for area in areas:
			# SQL（データベースを操作するコマンド）を実行する
			sql = "select id,latitude,longitude,farmer,zyuusinnLatitude,zyuusinnlongitude,address from noutinavi_addzyuusinn2 where farmer in (select farmer from noutinavi_addzyuusinn where classification_of_land_code_name = '田' and address like '%" +str(area) + "%' group by farmer having sum(selectedfarm_disp_area_on_registry) > 50000 ) order by farmer;"
			cur.execute(sql)
			# 実行結果を取得する
			rows.append(list(cur.fetchall()))
		# 接続を閉じる
		cur.close
		conn.close
		#print(sum(rows,[]))
		return sum(rows,[])

def farmersretrievefromdb12(areas):		#交換前
	#if __name__ == '__main__':
		# 接続する
		rows = []
		conn = MySQLdb.connect(
		user='root',
		passwd='',
		host='localhost',
		db='db')
		# カーソルを取得する
		cur = conn.cursor()
		for area in areas:
			# SQL（データベースを操作するコマンド）を実行する
			sql = "select id,latitude,longitude,farmer,zyuusinnLatitude,zyuusinnlongitude,address from noutinavi_addzyuusinn where address like '%" + str(area) + "%' and classification_of_land_code_name = '田' and (farmer in (select farmer from noutinavi_addzyuusinn where classification_of_land_code_name = '田' and address like '%岩手県%' group by farmer having sum(selectedfarm_disp_area_on_registry) > 50000 ) or farmer in (select farmer from noutinavi_addzyuusinn2 where classification_of_land_code_name = '田' and address like '%岩手県%' group by farmer having sum(selectedfarm_disp_area_on_registry) > 50000 )) order by farmer;"
			cur.execute(sql)
			# 実行結果を取得する
			rows.append(list(cur.fetchall()))
		# 接続を閉じる
		cur.close
		conn.close
		#print(sum(rows,[]))
		return sum(rows,[])
		
def farmersretrievefromdb13(areas):		#交換後
	#if __name__ == '__main__':
		# 接続する
		rows = []
		conn = MySQLdb.connect(
		user='root',
		passwd='',
		host='localhost',
		db='db')
		# カーソルを取得する
		cur = conn.cursor()
		for area in areas:
			# SQL（データベースを操作するコマンド）を実行する
			sql = "select id,latitude,longitude,farmer,zyuusinnLatitude,zyuusinnlongitude,address from noutinavi_addzyuusinn2 where address like '%" +str(area) + "%' and classification_of_land_code_name = '田' and (farmer in (select farmer from noutinavi_addzyuusinn where classification_of_land_code_name = '田' and address like '%岩手県%' group by farmer having sum(selectedfarm_disp_area_on_registry) > 50000 ) or farmer in (select farmer from noutinavi_addzyuusinn2 where classification_of_land_code_name = '田' and address like '%岩手県%' group by farmer having sum(selectedfarm_disp_area_on_registry) > 50000 ))order by farmer;"
			cur.execute(sql)
			# 実行結果を取得する
			rows.append(list(cur.fetchall()))
		# 接続を閉じる
		cur.close
		conn.close
		#print(sum(rows,[]))
		return sum(rows,[])

def farmersretrievefromdb14(areas):		#交換後
	#if __name__ == '__main__':
		# 接続する
		rows = []
		conn = MySQLdb.connect(
		user='root',
		passwd='',
		host='localhost',
		db='db')
		# カーソルを取得する
		cur = conn.cursor()
		for area in areas:
			# SQL（データベースを操作するコマンド）を実行する
			sql = "select id,latitude,longitude,farmer,zyuusinnLatitude,zyuusinnlongitude,address from noutinavi_addzyuusinn2 where address like '%" +str(area) + "%' and classification_of_land_code_name = '田' and (farmer in (select farmer from noutinavi_addzyuusinn where classification_of_land_code_name = '田' and address like '%岩手県%' group by farmer having sum(selectedfarm_disp_area_on_registry) > 50000 ) or farmer in (select farmer from noutinavi_addzyuusinn2 where classification_of_land_code_name = '田' and address like '%岩手県%' group by farmer having sum(selectedfarm_disp_area_on_registry) > 50000 ))order by farmer;"
			cur.execute(sql)
			# 実行結果を取得する
			rows.append(list(cur.fetchall()))
		# 接続を閉じる
		cur.close
		conn.close
		#print(sum(rows,[]))
		return sum(rows,[])

def farmersretrievefromdb15(area):		#farmerごとのID情報等の取得
	#if __name__ == '__main__':
		# 接続する
		rows = []
		conn = MySQLdb.connect(
		user='root',
		passwd='',
		host='localhost',
		db='db',
		charset='utf8')
		#カーソルを取得する
		#print(areas)
		cur = conn.cursor()
		#print(areas)
			# SQL（データベースを操作するコマンド）を実行する
		sql = "select farmer,id,longitude,Latitude,zyuusinnlongitude,zyuusinnLatitude from noutinavi_addzyuusinn2 where classification_of_land_code_name = '田' and farmer in (select farmer from noutinavi_addzyuusinn2 where classification_of_land_code_name = '田' and address like '%" +str(area) + "%' group by farmer having sum(selectedfarm_disp_area_on_registry) > 50000 ) order by farmer;"
		#print(sql)
		#sql = "select distinct * from noutinavi_addzyuusinn where address like '%" + str(area) + "%' and classification_of_land_code_name = '田'  order by farmer;"
		cur.execute(sql)
		# 実行結果を取得する
		#print(cur.fetchall())
		rows.append(list(cur.fetchall()))
		# 接続を閉じる
		cur.close
		conn.close
		#print(sum(rows,[]))
		return sum(rows,[])

def farmersretrievefromdb16(areas):		#交換後
	#if __name__ == '__main__':
		# 接続する
		rows = []
		conn = MySQLdb.connect(
		user='root',
		passwd='',
		host='localhost',
		db='db')
		# カーソルを取得する
		cur = conn.cursor()
		for area in areas:
			# SQL（データベースを操作するコマンド）を実行する
			sql = "select id,latitude,longitude,farmer,zyuusinnLatitude,zyuusinnlongitude,address from noutinavi_addzyuusinn_shudou where address like '%" +str(area) + "%' and classification_of_land_code_name = '田' and (farmer in (select farmer from noutinavi_addzyuusinn where classification_of_land_code_name = '田' and address like '%岩手県%' group by farmer having sum(selectedfarm_disp_area_on_registry) > 50000 ) or farmer in (select farmer from noutinavi_addzyuusinn_shudou where classification_of_land_code_name = '田' and address like '%岩手県%' group by farmer having sum(selectedfarm_disp_area_on_registry) > 50000 ))order by farmer;"
			cur.execute(sql)
			# 実行結果を取得する
			rows.append(list(cur.fetchall()))
		# 接続を閉じる
		cur.close
		conn.close
		#print(sum(rows,[]))
		return sum(rows,[])

def farmerlist(city):
	#city = "盛岡市"
	# 接続する
	conn = MySQLdb.connect(
	user='root',
	passwd='',
	host='localhost',
	db='db')
	# カーソルを取得する
	cur = conn.cursor()		
	# SQL（データベースを操作するコマンド）を実行する
	sql = "select distinct farmer from noutinavi where address like '%" + str(city) + "%' order by farmer;"
	cur.execute(sql)
	# 実行結果を取得する
	rows = cur.fetchall()
	cur.close
	# 接続を閉じる
	conn.close
	return rows

def addresslist(address):
	#city = "盛岡市"
	# 接続する
	conn = MySQLdb.connect(
	user='root',
	passwd='',
	host='localhost',
	db='db')
	# カーソルを取得する
	cur = conn.cursor()		
	# SQL（データベースを操作するコマンド）を実行する
	sql = "select distinct id,latitude,longitude from noutinavi2 where address like '%" + str(address) + "%' and classification_of_land_code_name = '田';"
	cur.execute(sql)
	# 実行結果を取得する
	rows = cur.fetchall()
	cur.close
	# 接続を閉じる
	conn.close
	return rows

def conditionalareatotal(address):				#"田"に限定した面積合計
	#city = "盛岡市"
	# 接続する
	conn = MySQLdb.connect(
	user='root',
	passwd='',
	host='localhost',
	db='db')
	# カーソルを取得する
	cur = conn.cursor()		
	# SQL（データベースを操作するコマンド）を実行する
	sql = "select sum(selectedfarm_disp_area_on_registry) from (select distinct id,selectedfarm_disp_area_on_registry from noutinavi2 where address like '%" + str(address) + "%' and classification_of_land_code_name = '田') as hoge;"
	cur.execute(sql)
	# 実行結果を取得する
	total = cur.fetchall()
	#SQLを実行
	sql = "select count(selectedfarm_disp_area_on_registry) from (select distinct id,selectedfarm_disp_area_on_registry from noutinavi2 where address like '%" + str(address) + "%' and classification_of_land_code_name = '田') as hoge;"
	cur.execute(sql)
	# 実行結果を取得する
	number = cur.fetchall()
	cur.close
	# 接続を閉じる
	conn.close
	print(address,"の田面積合計:",'{:.0f}'.format(total[0][0]/10000),"ha(",number[0][0],"件)")

def farmlandsdistance():
#if __name__ == '__main__':
	# 接続する
	conn = MySQLdb.connect(
	user='root',
	passwd='',
	host='localhost',
	db='db')
	# カーソルを取得する
	cur = conn.cursor()		
	# SQL（データベースを操作するコマンド）を実行する
	sql = "select distance from noutinavi_distance_between_farmlands;"
	cur.execute(sql)
	# 実行結果を取得する
	rows = cur.fetchall()
	# 接続を閉じる
	cur.close
	conn.close
	return rows


def writedistancebetweenfarmlands(completedlist):
	#if __name__ == '__main__':
		# 接続する
		conn = MySQLdb.connect(
		user='root',
		passwd='',
		host='localhost',
		db='db')
		# カーソルを取得する
		cur = conn.cursor()		
		# SQL（データベースを操作するコマンド）を実行する
		for i,j,k in completedlist:
			sql = "INSERT INTO noutinavi_distance_between_farmlands(farmer,distance,number_of_farmlands) VALUES ('" + i[0] + "'," + str(j) + "," + str(k) + ")"
			cur.execute(sql)

		conn.commit()
		# 接続を閉じる
		cur.close
		conn.close

def exchange_reset():
	#city = "盛岡市"
	# 接続する
	conn = MySQLdb.connect(
	user='root',
	passwd='',
	host='localhost',
	db='db')
	# カーソルを取得する
	cur = conn.cursor()
	# SQL（データベースを操作するコマンド）を実行する
	sql = "delete from noutinavi_addzyuusinn_shudou;"
	cur.execute(sql)
	sql = "insert into noutinavi_addzyuusinn_shudou select * from noutinavi_addzyuusinn;"
	cur.execute(sql)
	conn.commit()
	cur.close()
	# 接続を閉じる
	conn.close()

from math import sin, cos, acos, radians
earth_rad = 6378.137

def latlng_to_xyz(lat, lng):
    rlat, rlng = radians(lat), radians(lng)
    coslat = cos(rlat)
    return coslat*cos(rlng), coslat*sin(rlng), sin(rlat)

def distance_to_center_of_gravity(rows):
	#cnt = 0
	#a = {}
	distance = 0
	#全ての農地と重心までの距離を計算
	for i in range(len(rows)):
		distance += dist_on_sphere((float(rows[i][2]),float(rows[i][1])),(float(rows[0][9]),float(rows[0][8]))) #緯度　経度の順
		#distance += 0
		#cnt += 1
		#a[str(rows[i][2]),str(rows[j][1])]=distance
	#print(a)
	
	#重心までの距離を求める
	#result = dist_on_sphere(pos0, pos1, radious=earth_rad)
	#result = minimumspanningtree3(rows,a)
	#ワーシャルフロイド法
	#result = warshall_floyd(rows,a)
	return distance


def distance_to_center_of_gravity_eachfarmer(farmer):
	conn = MySQLdb.connect(user='root',passwd='',host='localhost',db='db')
	# カーソルを取得する
	cur = conn.cursor()
	# SQL（データベースを操作するコマンド）を実行する
	sql = "select longitude,Latitude,zyuusinnlongitude,zyuusinnLatitude from noutinavi_addzyuusinn where farmer ='" + str(farmer) + "' and classification_of_land_code_name = '田';"
	cur.execute(sql)
	conn.commit()
	# 実行結果を取得する
	rows_pre = cur.fetchall()
	sql = "select longitude,Latitude,zyuusinnlongitude,zyuusinnLatitude from noutinavi_addzyuusinn_shudou where farmer ='" + str(farmer) + "' and classification_of_land_code_name = '田';"
	cur.execute(sql)
	conn.commit()
	# 実行結果を取得する
	rows_post = cur.fetchall()
	# 接続を閉じる
	cur.close
	conn.close
	distance_pre = 0
	distance_post = 0
	# 全ての農地と重心までの距離を計算
	for row in rows_pre:
		distance_pre += dist_on_sphere((float(row[1]), float(row[0])),(float(row[3]), float(row[2])))  # 緯度　経度の順
	for row in rows_post:
		distance_post += dist_on_sphere((float(row[1]), float(row[0])),(float(row[3]), float(row[2])))  # 緯度　経度の順
	return distance_pre,distance_post

def dist_on_sphere(pos0, pos1, radious=earth_rad):
    xyz0, xyz1 = latlng_to_xyz(*pos0), latlng_to_xyz(*pos1)
    #print(sum(x * y for x, y in zip(xyz0, xyz1)))
    hoge =  acos(round(sum(x * y for x, y in zip(xyz0, xyz1)),15))*radious		#小数第１５位で丸める
    return hoge
    #print(hoge)
    #if hoge != 0.0:
    	#return hoge
    #else:
	   # return 0

def  warshall_floyd(rows,weightdic):	#id:配列、weightdic:辞書
		#if __name__ == '__main__':
			graph = nx.Graph()
			
			# ノードを追加する
			for i in rows:	
				graph.add_node(str(i[0]))
			
			# ノード間をエッジでつなぐ
			for k,v in weightdic.items():
				graph.add_edge(k[0],k[1],weight=v)
			#nx.draw_networkx(graph)
			#plt.show()
				
			#minimum_spanning_treeで最小全域木問題を解く
			#print("minimum_spanning_tree_edges:")
			T = nx.minimum_spanning_tree(graph)
			#for i in sorted(T.edges(data=True)):
				#print (i)
			#print("minimum_spanning_tree_weight:")
			#print(T.size(weight='weight'))
			return T.size(weight='weight')

def  minimumspanningtree(rows,weightdic):	#id:配列、weightdic:辞書
		#if __name__ == '__main__':
			graph = nx.Graph()
			#緯度で昇順にソート
			rows = np.array(rows)
			rows = rows[rows[:,1].argsort(),:]
			#農家で昇順にソート
			rows = rows[rows[:,3].argsort(),:]
			#print(rows)
			# ノードを追加する
			for i in rows:	
				graph.add_node(str(i[0]))
			
			# ノード間をエッジでつなぐ
			for k,v in weightdic.items():
				graph.add_edge(k[0],k[1],weight=v)
			#nx.draw_networkx(graph)
			#plt.show()
			#print(nx.is_connected(graph))
			#minimum_spanning_treeで最小全域木問題を解く
			#print("minimum_spanning_tree_edges:")
			T = nx.minimum_spanning_tree(graph)
			#nx.draw_networkx(T)
			#plt.show()
			#T = nx.shortest_path_length(graph)
			#T = nx.floyd_warshall(graph)
			#T = nx.floyd_warshall_predecessor_and_distance(graph)
			#for i in sorted(T.edges(data=True)):
				#print (i)
			#print("minimum_spanning_tree_weight:")
			#print(T.size(weight='weight'))
			#hoge = np.array(rows)
			#print(set(hoge[:,0]))
			#for n,l in enumerate(T):
				#for value in l.values():
					#for m in hoge[:,0]:
						#print(value[m])
			'''
			for m in hoge[:,0]:
				print(m)
				#print(l[str(m)])
				if n > 0:
					for o in l:
						print(o.values())
					#print(l[str(m)][str(m)])
			'''
			#print(T)
			return T.size(weight='weight')

def  minimumspanningtree2(rows,weightdic):	#id:配列、weightdic:辞書
		#if __name__ == '__main__':
			graph = nx.Graph()
			#緯度で昇順にソート
			rows = np.array(rows)
			rows = rows[rows[:,1].argsort(),:]
			#農家で昇順にソート
			rows = rows[rows[:,9].argsort(),:]
			#print(rows)
			# ノードを追加する
			for i in rows:	
				graph.add_node(str(i[0]))
			
			# ノード間をエッジでつなぐ
			for k,v in weightdic.items():
				graph.add_edge(k[0],k[1],weight=v)
			#nx.draw_networkx(graph)
			#plt.show()
			#print(nx.is_connected(graph))
			#minimum_spanning_treeで最小全域木問題を解く
			#print("minimum_spanning_tree_edges:")
			T = nx.minimum_spanning_tree(graph)
			#nx.draw_networkx(T)
			#plt.show()
			#T = nx.shortest_path_length(graph)
			#T = nx.floyd_warshall(graph)
			#T = nx.floyd_warshall_predecessor_and_distance(graph)
			#for i in sorted(T.edges(data=True)):
				#print (i)
			#print("minimum_spanning_tree_weight:")
			#print(T.size(weight='weight'))
			#hoge = np.array(rows)
			#print(set(hoge[:,0]))
			#for n,l in enumerate(T):
				#for value in l.values():
					#for m in hoge[:,0]:
						#print(value[m])
			'''
			for m in hoge[:,0]:
				print(m)
				#print(l[str(m)])
				if n > 0:
					for o in l:
						print(o.values())
					#print(l[str(m)][str(m)])
			'''
			#print(T)
			return T.size(weight='weight')

def  minimumspanningtree3(rows,weightdic):	#id:配列、weightdic:辞書
		#if __name__ == '__main__':
			graph = nx.Graph()
			#緯度で昇順にソート
			rows = np.array(rows)
			rows = rows[rows[:,1].argsort(),:]
			#農家で昇順にソート
			rows = rows[rows[:,4].argsort(),:]
			#print(rows)
			# ノードを追加する
			for i in rows:	
				graph.add_node(str(i[0]))
			
			# ノード間をエッジでつなぐ
			for k,v in weightdic.items():
				graph.add_edge(k[0],k[1],weight=v)
			#nx.draw_networkx(graph)
			#plt.show()
			#print(nx.is_connected(graph))
			#minimum_spanning_treeで最小全域木問題を解く
			#print("minimum_spanning_tree_edges:")
			T = nx.minimum_spanning_tree(graph)
			#nx.draw_networkx(T)
			#plt.show()
			#T = nx.shortest_path_length(graph)
			#T = nx.floyd_warshall(graph)
			#T = nx.floyd_warshall_predecessor_and_distance(graph)
			#for i in sorted(T.edges(data=True)):
				#print (i)
			#print("minimum_spanning_tree_weight:")
			#print(T.size(weight='weight'))
			#hoge = np.array(rows)
			#print(set(hoge[:,0]))
			#for n,l in enumerate(T):
				#for value in l.values():
					#for m in hoge[:,0]:
						#print(value[m])
			'''
			for m in hoge[:,0]:
				print(m)
				#print(l[str(m)])
				if n > 0:
					for o in l:
						print(o.values())
					#print(l[str(m)][str(m)])
			'''
			#print(T)
			return T.size(weight='weight')
			
import folium
import pandas as pd
import numpy as np
import random
import re

def searchfarmland(rows):
	hoge = []
	for i,j in enumerate(rows):
		hoge.append(re.sub(r"[0-9\-]", "",list(j)[6]))
	return set(hoge)

def searchsurroundfarmland(rows):
	hoge = surroundfarmlandinformation(rows[0][4],rows[0][5],rows[0][3],rows[0][7])
	#print(hoge[:5][2:])
	return hoge

def mapplot(rows,applicablearea=""):
	#print(rows)
	arr_1 = np.array(rows)
	#print(arr_1)
	paddy = pd.DataFrame(arr_1)
	paddy.columns = ['id','latitude','longitude','farmer','zyuusinnLatitude','zyuusinnlongitude','address','distance','owndistance','area']
	paddy['id'].astype(np.int64)
	paddy['latitude'].astype(np.float64)
	paddy['longitude'].astype(np.float64)
	paddy['zyuusinnLatitude'].astype(np.float64)
	paddy['zyuusinnlongitude'].astype(np.float64)

	#print(paddy)
	colors = [ 
	    'red', 
	    'blue', 
	    'gray', 
	    'darkred', 
	    'lightred', 
	    'orange', 
	    'beige', 
	    'green', 
	    'darkgreen', 
	    'lightgreen', 
	    'darkblue', 
	    'lightblue', 
	    'purple', 
	    'darkpurple', 
	    'pink', 
	    'cadetblue', 
	    'lightgray', 
	    'black' 
	] 
	
	map = folium.Map(location=[float(paddy.iat[0,4]),float(paddy.iat[0,5])], zoom_start=14)
	
	#ランダムで色を指定
	randomcolor = random.choice(colors)
	randomicon_color = random.choice(colors)
	#農地をプロット
	for i, r in paddy.iterrows():
	    folium.Marker([float(r['latitude']), float(r['longitude'])],popup="ID:" + str(r['id']) + " " + "farmer:" + str(r['farmer']) + ' ' + '農地数:' + str(len(rows)), icon=folium.Icon(icon='star',color=randomcolor,icon_color=randomicon_color)).add_to(map)
	#重心をプロット
	folium.Marker([float(r['zyuusinnLatitude']), float(r['zyuusinnlongitude'])],popup="重心点 " + "farmer:" + str(r['farmer']), icon=folium.Icon(color='white')).add_to(map)
	map.save("map_paddy.html")
	
def mapplot2(rows,applicablearea=""):
	#print(rows)
	arr_1 = np.array(rows)
	#print(arr_1)
	paddy = pd.DataFrame(arr_1)
	paddy.columns = ['id','latitude','longitude','farmer','zyuusinnLatitude','zyuusinnlongitude','address','distance','owndistance','area']
	paddy['id'].astype(np.int64)
	paddy['latitude'].astype(np.float64)
	paddy['longitude'].astype(np.float64)
	paddy['zyuusinnLatitude'].astype(np.float64)
	paddy['zyuusinnlongitude'].astype(np.float64)

	#print(paddy)
	colors = [ 
	    'red', 
	    'blue', 
	    'gray', 
	    'darkred', 
	    'lightred', 
	    'orange', 
	    'beige', 
	    'green', 
	    'darkgreen', 
	    'lightgreen', 
	    'darkblue', 
	    'lightblue', 
	    'purple', 
	    'darkpurple', 
	    'pink', 
	    'cadetblue', 
	    'lightgray', 
	    'black' 
	] 
	
	map = folium.Map(location=[float(paddy.iat[0,4]),float(paddy.iat[0,5])], zoom_start=14)
	
	#ランダムで色を指定
	randomcolor = random.choice(colors)
	randomicon_color = random.choice(colors)
	#農地をプロット
	for i, r in paddy.iterrows():
	    folium.Marker([float(r['latitude']), float(r['longitude'])],popup="ID:" + str(r['id']) + " " + "farmer:" + str(r['farmer']) + ' ' + '農地数:' + str(len(rows)), icon=folium.Icon(icon='star',color=randomcolor,icon_color=randomicon_color)).add_to(map)
	#重心をプロット
	folium.Marker([float(r['zyuusinnLatitude']), float(r['zyuusinnlongitude'])],popup="重心点 " + "farmer:" + str(r['farmer']), icon=folium.Icon(color='white')).add_to(map)
	map.save("map_paddy.html")

def mapplotfarmers(rows="",rows2="",applicablefarmer=""):
#def mapplotfarmers(rows):
	#print(rows2)
	#paddy_50over = 50
	#print(applicablefarmer)
	colors = [ 
	    #'red', 
	    'blue', 
	    'gray', 
	    'darkred', 
	    'lightred', 
	    'orange', 
	    'beige', 
	    'green', 
	    'darkgreen', 
	    #'lightgreen', 
	    'darkblue', 
	    'lightblue', 
	    'purple', 
	    'darkpurple', 
	    'pink', 
	    'cadetblue', 
	    'lightgray'#, 
	    #'black' 
	] 
	icons = [
		'cloud',
		'bell',
		'music',
		'phone-alt',
		'plane',
		'print',
		#'queen',
		'shopping-cart',
		'signal',
		#'star',
		'time',
		'tint',
		'phone',
		'tree-conifer',
		#'archway',
		'align-center',
		#'apple',
		'arrow-up',
		'asterisk',
		'arrow-left',
		'arrow-down',
		'arrow-right',
		'camera',
		'calendar',
		'bullhorn',
		#'cd'
		#'blackboard'
		#'erase'
		'envelope',
		'file',
		'filter',
		'flash',
		'headphones',
		'send',
		'sd-video',
		'screenshot',
		'search',
		'share',
		'sort',
		'resize-full',
		'qrcode',
		'refresh',
		'saved',
		'registration-mark',
		'repeat',
		'sort-by-order'
	]

	#print(arr_2)
	#print(rows2[0][0])
	#arr_2 = np.squeeze(rows2,axis=0)
	#if rows != "":
		#arr_1 = np.array(rows)[:,:7]
		#arr_1 = arr_1[arr_1[:,3].argsort(),:]
	arr_1 = np.array(rows)
	paddy = pd.DataFrame(arr_1)
	#print(paddy)
	paddy.columns = ['id','latitude','longitude','farmer','zyuusinnLatitude','zyuusinnlongitude','address','distance','temp','area']
	paddy['id'].astype(np.int64)
	paddy['latitude'].astype(np.float64)
	paddy['longitude'].astype(np.float64)
	#paddy['farmer'].astype(np.int64)
	paddy['zyuusinnLatitude'].astype(np.float64)
	paddy['zyuusinnlongitude'].astype(np.float64)
	paddy['distance'].astype(np.float64)
		
	map = folium.Map(location=[float(paddy.iat[0,1]),float(paddy.iat[0,2])], zoom_start=14)
	farmer = ''
	paddynumber = [[],]
	yousosuu = len(paddy)
	area = 0
	
	#面積の合計
	for row in rows:
		area += row[9]
	
	#重心情報の追加		
	map = folium.Map(location=[float(paddy.iat[0,1]),float(paddy.iat[0,2])], zoom_start=14)
	folium.Marker([float(paddy['zyuusinnLatitude'][0]), float(paddy['zyuusinnlongitude'][0])],popup='Farmer:' + str(paddy['farmer'][0]) + '\n' + 'number of paddy:' + str(yousosuu) + '\n' + 'area:' + str(area), icon=folium.Icon(icon='star',color='black',icon_color='red')).add_to(map)

	#rowsの操作
	for i, r in paddy.iterrows():
		paddynumber = [ j for j in rows if j[3] == r['farmer'] ]
		farmer = r['farmer']
		folium.Marker([float(r['latitude']), float(r['longitude'])],popup='ID:' + str(r['id']) + '\n' + 'Farmer:' + str(r['farmer']) + '\n' + 'number of paddy:' + str(len(paddynumber)) , icon=folium.Icon(icon='star',color='red',icon_color='white')).add_to(map)
	
	#rows2の操作
	#arr_2 = np.array(rows2)[:,:7]
	#arr_2 = arr_2[arr_2[:,3].argsort(),:]
	arr_2 = np.array(rows2)
	paddy2 = pd.DataFrame(arr_2)
	#print(paddy2)
	paddy2.columns = ['id','latitude','longitude','farmer','zyuusinnLatitude','zyuusinnlongitude','address','distance','owndistance','area']
	#paddy2[paddy2[:,0].argsort(),:]
	#print(paddy2)
	#print(paddy2.head())
	#paddy['address'].astype(np.int64)
	paddy2['id'].astype(np.int64)
	paddy2['latitude'].astype(np.float64)
	paddy2['longitude'].astype(np.float64)
	#paddy2['farmer'].astype(np.int64)
	paddy2['zyuusinnLatitude'].astype(np.float64)
	paddy2['zyuusinnlongitude'].astype(np.float64)
	#paddy2['address'].astype(np.int64)
	paddy2['distance'].astype(np.float64)
	paddy2['owndistance'].astype(np.float64)

	#print(len(paddy2))
	farmer = ""
	paddynumber = [[],]
	for k, s in paddy2.iterrows():
		#前の要素から農家が変わった場合
		if farmer != s['farmer']:
			#農家が変わってすぐの場合のみ
			if s['farmer'] != paddy2.iat[k-1,3] or k == 0:
				paddynumber = [ j for j in rows2 if j[3] == s['farmer'] ]
				#print(len(paddynumber))
				farmer = s['farmer']
				#print(farmer)
				#ランダムで色を指定
				randomcolor = random.choice(colors)
				randomicon = random.choice(icons)
				randomicon_color = random.choice(colors)
				#重心のiconを打つ
				#print(applicablefarmer[0])
				#print(s)
				#if s['farmer'] == applicablefarmer[0]:
					#print(str(s['zyuusinnLatitude']) + " " + str(s['zyuusinnlongitude']))
					#folium.Marker([float(s['zyuusinnLatitude']), float(s['zyuusinnlongitude'])],popup='Farmer:' + str(s['farmer']) + '\n' + 'number of paddy:' + str(len(paddynumber)) , icon=folium.Icon(icon='star',color='black',icon_color='red')).add_to(map)
				#else:
					#print(str(s['zyuusinnLatitude']) + " " + str(s['zyuusinnlongitude']))
				folium.Marker([float(s['zyuusinnLatitude']), float(s['zyuusinnlongitude'])],popup='ID:' + str(s['id']) + '\n' + 'Farmer:' + str(s['farmer']) + '\n' + 'number of paddy:' + str(len(paddynumber)) , icon=folium.Icon(icon=randomicon,color='lightgreen',icon_color=randomicon_color)).add_to(map)
		if s['farmer'] != applicablefarmer[0]:
			#folium.Marker([float(s['latitude']), float(s['longitude'])],popup='Farmer:' + str(s['farmer']) + '\n' + 'number of paddy:' + str(len(paddynumber)) , icon=folium.Icon(icon=randomcolor,color=randomicon,icon_color=randomicon_color)).add_to(map)
			folium.Marker([float(s['latitude']), float(s['longitude'])],popup='ID:' + str(s['id']) + '\n' + 'Farmer:' + str(s['farmer']) + '\n' + 'number of paddy:' + str(len(paddynumber)) , icon=folium.Icon(icon=randomicon,color='white',icon_color=randomicon_color)).add_to(map)	
	map.save("map_paddy.html")
	#print(j)	

def mapplotfarmers2(rows="",rows2="",applicablefarmer=""):	
#def mapplotfarmers(rows):
	#print(rows2)
	#paddy_50over = 50
	#print(applicablefarmer)
	colors = [ 
	    #'red', 
	    'blue', 
	    'gray', 
	    'darkred', 
	    'lightred', 
	    'orange', 
	    'beige', 
	    'green', 
	    'darkgreen', 
	    #'lightgreen', 
	    'darkblue', 
	    'lightblue', 
	    'purple', 
	    'darkpurple', 
	    'pink', 
	    'cadetblue', 
	    'lightgray'#, 
	    #'black' 
	] 
	icons = [
		'cloud',
		'bell',
		'music',
		'phone-alt',
		'plane',
		'print',
		#'queen',
		'shopping-cart',
		'signal',
		#'star',
		'time',
		'tint',
		'phone',
		'tree-conifer',
		#'archway',
		'align-center',
		#'apple',
		'arrow-up',
		'asterisk',
		'arrow-left',
		'arrow-down',
		'arrow-right',
		'camera',
		'calendar',
		'bullhorn',
		#'cd'
		#'blackboard'
		#'erase'
		'envelope',
		'file',
		'filter',
		'flash',
		'headphones',
		'send',
		'sd-video',
		'screenshot',
		'search',
		'share',
		'sort',
		'resize-full',
		'qrcode',
		'refresh',
		'saved',
		'registration-mark',
		'repeat',
		'sort-by-order'
	]

	#print(arr_2)
	#print(rows2[0][0])
	#arr_2 = np.squeeze(rows2,axis=0)
	#if rows != "":
		#arr_1 = np.array(rows)[:,:7]
		#arr_1 = arr_1[arr_1[:,3].argsort(),:]
	arr_1 = np.array(rows)
	paddy = pd.DataFrame(arr_1)
	#print(paddy)
	paddy.columns = ['id','latitude','longitude','farmer','zyuusinnLatitude','zyuusinnlongitude','address','distance','temp','area']
	paddy['id'].astype(np.int64)
	paddy['latitude'].astype(np.float64)
	paddy['longitude'].astype(np.float64)
	#paddy['farmer'].astype(np.int64)
	paddy['zyuusinnLatitude'].astype(np.float64)
	paddy['zyuusinnlongitude'].astype(np.float64)
	paddy['distance'].astype(np.float64)
	farmer = ''
	paddynumber = [[],]
	yousosuu = len(paddy)
	area = 0
	
	#面積の合計
	for row in rows:
		area += row[9]

	#重心情報の追加		
	map = folium.Map(location=[float(paddy.iat[0,1]),float(paddy.iat[0,2])], zoom_start=14)
	folium.Marker([float(paddy['zyuusinnLatitude'][0]), float(paddy['zyuusinnlongitude'][0])],popup='Farmer:' + str(paddy['farmer'][0]) + '\n' + 'number of paddy:' + str(yousosuu) + '\n' + 'area:' + str(area), icon=folium.Icon(icon='star',color='black',icon_color='red')).add_to(map)

	#rowsの操作
	for i, r in paddy.iterrows():
		paddynumber = [ j for j in rows if j[3] == r['farmer'] ]
		#farmer = r['farmer']
		folium.Marker([float(r['latitude']), float(r['longitude'])],popup='ID:' + str(r['id']) + '\n' + 'Farmer:' + str(r['farmer']) + '\n' + 'number of paddy:' + str(len(paddynumber)) , icon=folium.Icon(icon='star',color='red',icon_color='white')).add_to(map)
	
	#rows2の操作
	#arr_2 = np.array(rows2)[:,:7]
	#arr_2 = arr_2[arr_2[:,3].argsort(),:]
	arr_2 = np.array(rows2)
	paddy2 = pd.DataFrame(arr_2)
	#print(paddy2)
	paddy2.columns = ['id','latitude','longitude','farmer','zyuusinnLatitude','zyuusinnlongitude','address','distance','owndistance','area']
	#paddy2[paddy2[:,0].argsort(),:]
	#print(paddy2)
	#print(paddy2.head())
	#paddy['address'].astype(np.int64)
	paddy2['id'].astype(np.int64)
	paddy2['latitude'].astype(np.float64)
	paddy2['longitude'].astype(np.float64)
	#paddy2['farmer'].astype(np.int64)
	paddy2['zyuusinnLatitude'].astype(np.float64)
	paddy2['zyuusinnlongitude'].astype(np.float64)
	#paddy2['address'].astype(np.int64)
	paddy2['distance'].astype(np.float64)
	paddy2['owndistance'].astype(np.float64)

	#print(len(paddy2))
	farmer = ""
	paddynumber = [[],]
	for k, s in paddy2.iterrows():
		#前の要素から農家が変わった場合
		if farmer != s['farmer']:
			#農家が変わってすぐの場合のみ
			if s['farmer'] != paddy2.iat[k-1,3] or k == 0:
				paddynumber = [ j for j in rows2 if j[3] == s['farmer'] ]
				#print(len(paddynumber))
				farmer = s['farmer']
				#print(farmer)
				#ランダムで色を指定
				randomcolor = random.choice(colors)
				randomicon = random.choice(icons)
				randomicon_color = random.choice(colors)
				#重心のiconを打つ
				#print(applicablefarmer[0])
				#print(s)
				#if s['farmer'] == applicablefarmer[0]:
					#print(str(s['zyuusinnLatitude']) + " " + str(s['zyuusinnlongitude']))
					#folium.Marker([float(s['zyuusinnLatitude']), float(s['zyuusinnlongitude'])],popup='Farmer:' + str(s['farmer']) + '\n' + 'number of paddy:' + str(len(paddynumber)) , icon=folium.Icon(icon='star',color='black',icon_color='red')).add_to(map)
				#else:
					#print(str(s['zyuusinnLatitude']) + " " + str(s['zyuusinnlongitude']))
				folium.Marker([float(s['zyuusinnLatitude']), float(s['zyuusinnlongitude'])],popup='Farmer:' + str(s['farmer']) + '\n' + 'number of paddy:' + str(len(paddynumber)) , icon=folium.Icon(icon=randomicon,color='lightgreen',icon_color=randomicon_color)).add_to(map)
		if s['farmer'] != applicablefarmer[0]:
			#folium.Marker([float(s['latitude']), float(s['longitude'])],popup='Farmer:' + str(s['farmer']) + '\n' + 'number of paddy:' + str(len(paddynumber)) , icon=folium.Icon(icon=randomcolor,color=randomicon,icon_color=randomicon_color)).add_to(map)
			folium.Marker([float(s['latitude']), float(s['longitude'])],popup='ID:' + str(s['id']) + '\n' + 'Farmer:' + str(s['farmer']) + '\n' + 'number of paddy:' + str(len(paddynumber)) , icon=folium.Icon(icon=randomicon,color='white',icon_color=randomicon_color)).add_to(map)	
	map.save("map_paddy2.html")
	#print(j)	


def measuredistancebetweenfarmland(rows):
	cnt = 0
	a = {}
	#全ての通りの距離を計算
	for i in range(len(rows)):
		for j in range(i+1,len(rows)): 
			distance = dist_on_sphere((rows[i][1],rows[i][2]),(rows[j][1],rows[j][2])) #緯度　経度の順
			cnt += 1
			a[str(rows[i][0]),str(rows[j][0])]=distance
	#print(a)
	
	# 最小全域木問題を解く
	result = minimumspanningtree(rows,a)
	#ワーシャルフロイド法
	#result = warshall_floyd(rows,a)
	return result

def measuredistancebetweenfarmland2(rows):
	cnt = 0
	a = {}
	#全ての通りの距離を計算
	for i in range(len(rows)):
		for j in range(i+1,len(rows)): 
			distance = dist_on_sphere((float(rows[i][2]),float(rows[i][1])),(float(rows[j][2]),float(rows[j][1]))) #緯度lat　経度lonの順
			cnt += 1
			a[str(rows[i][2]),str(rows[j][1])]=distance
	#print(a)
	
	# 最小全域木問題を解く
	result = minimumspanningtree3(rows,a)
	#ワーシャルフロイド法
	#result = warshall_floyd(rows,a)
	return result

def main(city):
	#農家一覧の取得（farmerでソート）	現在は盛岡市のみ取ってきている
	#farmers = farmerlist(city)
	farmers = (["e89e4d1f26ce048a97b25ccbd01bc68d",],)
	
	completedlist = []
	
	for farmer in tqdm(farmers):
	#該当する農家の農地の経緯度を取ってくる	
		rows = retrievefromdb(farmer)	
		print(rows)
	
		cnt = 0
		a = {}
		#全ての通りの距離を計算
		for i in range(len(rows)):
			for j in range(i+1,len(rows)): 
				distance = dist_on_sphere((rows[i][1],rows[i][2]),(rows[j][1],rows[j][2])) #緯度　経度の順
				cnt += 1
				a[str(rows[i][0]),str(rows[j][0])]=distance
		# 最小全域木問題を解く
		result = minimumspanningtree(rows,a)
		#mapplot(rows)
		#結果を代入
		completedlist.append([farmer,result,len(rows)])
	
	#全ての結果を保存
	print(completedlist)
	writedistancebetweenfarmlands(completedlist)


def calculatecenterofgravity():
	lat = 0
	lon = 0
	
	rows = latitudeandlongitudeinformation()
	arr = np.array(rows)
	farmers = set(arr[:,3])
	#print(len(farmer))
	#print([i for i, x in enumerate(arr[:,3]) if x == 'f877984da4b8d45cf586a085f88deedb'])
	for j,farmer in enumerate(farmers):
		targetindex = [i for i, x in enumerate(arr[:,3]) if x == farmer]
		for hoge in targetindex:
			lat = lat + float(arr[hoge,1])
			lon = lon + float(arr[hoge,2])
			#print(str(lat) + " " + str(lon))
		adddblatitudeandlongitudeinformation(lat/len(targetindex),lon/len(targetindex),farmer)
		print(str(j) + "/"+str(len(farmers)) + " " + farmer + " " + "農地数:" + str(len(targetindex))+" "+str(lat/len(targetindex))+" "+str(lon/len(targetindex)))
		lat = 0
		lon = 0
		#print(hoge)
	#print(j)

def adddblatitudeandlongitudeinformation(latzyuusinn,lonzyuusinn,farmer):
	#print(latzyuusinn)
	conn = MySQLdb.connect(
	user='root',
	passwd='',
	host='localhost',
	db='db')
	# カーソルを取得する
	cur = conn.cursor()		
	# SQL（データベースを操作するコマンド）を実行する
	sql = "update noutinavi_addzyuusinn set zyuusinnlongitude=" + str(latzyuusinn) + ", zyuusinnLatitude=" + str(lonzyuusinn) + " where farmer='" + farmer +"';"
	#print(sql)
	cur.execute(sql)
	conn.commit()
	# 実行結果を取得する
	#rows = cur.fetchall()
	# 接続を閉じる
	cur.close
	conn.close
	
def latitudeandlongitudeinformation():
	#if __name__ == '__main__':
	# 接続する
	conn = MySQLdb.connect(
	user='root',
	passwd='',
	host='localhost',
	db='db')
	# カーソルを取得する
	cur = conn.cursor()		
	# SQL（データベースを操作するコマンド）を実行する
	sql = "select id,longitude,latitude,farmer from noutinavi_addzyuusinn where address like '%岩手県%' and classification_of_land_code_name = '田';"
	#sql = "select count(*) from noutinavi_addzyuusinn where address like '%花巻市%' and classification_of_land_code_name = '田';"
	cur.execute(sql)
	# 実行結果を取得する
	rows = cur.fetchall()
	# 接続を閉じる
	cur.close
	conn.close
	return rows

def surroundfarmlandinformation(lat,lon,farmer,dis=1):
	#if __name__ == '__main__':
	# 接続する
	conn = MySQLdb.connect(
	user='root',
	passwd='',
	host='localhost',
	db='db')
	# カーソルを取得する
	cur = conn.cursor()		
	# SQL（データベースを操作するコマンド）を実行する
	#sql = "SELECT distinct id,latitude,longitude,farmer,zyuusinnLatitude,zyuusinnlongitude,address,(6371 * acos(cos(radians(" + str(lat) + "))* cos(radians(latitude))* cos(radians(longitude) - radians(" + str(lon) + "))+ sin(radians(" + str(lat) + "))* sin(radians(latitude)))) AS distance,(6371 * acos(cos(radians(zyuusinnLatitude))* cos(radians(latitude))* cos(radians(longitude) - radians(zyuusinnlongitude))+ sin(radians(zyuusinnLatitude))* sin(radians(latitude)))) AS owndistance,selectedfarm_disp_area_on_registry FROM noutinavi_addzyuusinn where farmer <> '" + str(farmer) + "' and classification_of_land_code_name = '田' HAVING distance <= " + str(dis) + " ORDER BY distance;"
	sql = "SELECT distinct id,latitude,longitude,farmer,zyuusinnLatitude,zyuusinnlongitude,address,(6378.137 * acos(cos(radians(" + str(lat) + "))* cos(radians(latitude))* cos(radians(longitude) - radians(" + str(lon) + "))+ sin(radians(" + str(lat) + "))* sin(radians(latitude)))) AS distance,(6378.137 * acos(cos(radians(zyuusinnLatitude))* cos(radians(latitude))* cos(radians(longitude) - radians(zyuusinnlongitude))+ sin(radians(zyuusinnLatitude))* sin(radians(latitude)))) AS owndistance,selectedfarm_disp_area_on_registry FROM noutinavi_addzyuusinn where farmer <> '" + str(farmer) + "' and classification_of_land_code_name = '田' HAVING distance <= " + str(dis) + " ORDER BY distance;"
	#print(sql)
	cur.execute(sql)
	# 実行結果を取得する
	rows = cur.fetchall()
	# 接続を閉じる
	cur.close
	conn.close
	return rows

def surroundfarmlandinformation2(lat,lon,farmer,dis=1):
	#if __name__ == '__main__':
	# 接続する
	conn = MySQLdb.connect(
	user='root',
	passwd='',
	host='localhost',
	db='db')
	# カーソルを取得する
	cur = conn.cursor()		
	# SQL（データベースを操作するコマンド）を実行する
	#sql = "SELECT distinct *,(6371 * acos(cos(radians(" + str(lat) + "))* cos(radians(latitude))* cos(radians(longitude) - radians(" + str(lon) + "))+ sin(radians(" + str(lat) + "))* sin(radians(latitude)))) AS distance,(6371 * acos(cos(radians(zyuusinnLatitude))* cos(radians(latitude))* cos(radians(longitude) - radians(zyuusinnlongitude))+ sin(radians(zyuusinnLatitude))* sin(radians(latitude)))) AS owndistance FROM noutinavi_addzyuusinn where farmer <> '" + str(farmer) + "' and classification_of_land_code_name = '田' HAVING distance <= " + str(dis) + " ORDER BY distance;"
	sql = "SELECT distinct *,(6378.137 * acos(cos(radians(" + str(lat) + "))* cos(radians(latitude))* cos(radians(longitude) - radians(" + str(lon) + "))+ sin(radians(" + str(lat) + "))* sin(radians(latitude)))) AS distance,(6378.137 * acos(cos(radians(zyuusinnLatitude))* cos(radians(latitude))* cos(radians(longitude) - radians(zyuusinnlongitude))+ sin(radians(zyuusinnLatitude))* sin(radians(latitude)))) AS owndistance ,null FROM noutinavi_addzyuusinn where (farmer <> '" + str(farmer) + "') and classification_of_land_code_name = '田' HAVING (distance <= " + str(dis) + ") ORDER BY distance;"
	#print(sql)
	cur.execute(sql)
	# 実行結果を取得する
	rows = cur.fetchall()
	# 接続を閉じる
	cur.close
	conn.close
	return rows

def surroundfarmlandinformation3(lat,lon,farmer,dis=1):
	#if __name__ == '__main__':
	# 接続する
	conn = MySQLdb.connect(
	user='root',
	passwd='',
	host='localhost',
	db='db',
	charset='utf8')
	# カーソルを取得する
	cur = conn.cursor()		
	# SQL（データベースを操作するコマンド）を実行する
	#sql = "SELECT distinct *,(6371 * acos(cos(radians(" + str(lat) + "))* cos(radians(latitude))* cos(radians(longitude) - radians(" + str(lon) + "))+ sin(radians(" + str(lat) + "))* sin(radians(latitude)))) AS distance,(6371 * acos(cos(radians(zyuusinnLatitude))* cos(radians(latitude))* cos(radians(longitude) - radians(zyuusinnlongitude))+ sin(radians(zyuusinnLatitude))* sin(radians(latitude)))) AS owndistance FROM noutinavi_addzyuusinn where farmer <> '" + str(farmer) + "' and classification_of_land_code_name = '田' HAVING distance <= " + str(dis) + " ORDER BY distance;"
	sql = "SELECT distinct *,(6378.137 * acos(cos(radians(" + str(lat) + "))* cos(radians(latitude))* cos(radians(longitude) - radians(" + str(lon) + "))+ sin(radians(" + str(lat) + "))* sin(radians(latitude)))) AS distance,(6378.137 * acos(cos(radians(zyuusinnLatitude))* cos(radians(latitude))* cos(radians(longitude) - radians(zyuusinnlongitude))+ sin(radians(zyuusinnLatitude))* sin(radians(latitude)))) AS owndistance ,null, null FROM noutinavi_addzyuusinn2 where (farmer <> '" + str(farmer) + "') and classification_of_land_code_name = '田' HAVING (distance <= " + str(dis) + ") ORDER BY distance;"
	#print(sql)
	cur.execute(sql)
	# 実行結果を取得する
	rows = cur.fetchall()
	# 接続を閉じる
	cur.close
	conn.close
	return rows

def surroundfarmlandinformation4(lat,lon,farmer,dis=1):
	#if __name__ == '__main__':
	# 接続する
	conn = MySQLdb.connect(
	user='root',
	passwd='',
	host='localhost',
	db='db',
	charset='utf8')
	# カーソルを取得する
	cur = conn.cursor()		
	# SQL（データベースを操作するコマンド）を実行する
	sql = "SELECT id,longitude,Latitude,selectedfarm_disp_area_on_registry,farmer,zyuusinnlongitude,zyuusinnLatitude,exchangerecord,(6378.137 * acos(cos(radians(" + str(lat) + "))* cos(radians(latitude))* cos(radians(longitude) - radians(" + str(lon) + "))+ sin(radians(" + str(lat) + "))* sin(radians(latitude)))) AS distance,(6378.137 * acos(cos(radians(zyuusinnLatitude))* cos(radians(latitude))* cos(radians(longitude) - radians(zyuusinnlongitude))+ sin(radians(zyuusinnLatitude))* sin(radians(latitude)))) AS owndistance ,null  FROM noutinavi_addzyuusinn2 where (farmer <> '" + str(farmer) + "') and classification_of_land_code_name = '田' HAVING (distance <= " + str(dis) + ") ORDER BY distance;"
	#print(sql)
	cur.execute(sql)
	# 実行結果を取得する
	rows = cur.fetchall()
	# 接続を閉じる
	cur.close
	conn.close
	return rows
	
def surroundfarmlandinformation5(lat,lon,farmer,areaname,dis=1):
	#if __name__ == '__main__':
	# 接続する
	conn = MySQLdb.connect(
	user='root',
	passwd='',
	host='localhost',
	db='db',
	charset='utf8')
	# カーソルを取得する
	cur = conn.cursor()		
	# SQL（データベースを操作するコマンド）を実行する
	sql = "SELECT id,longitude,Latitude,selectedfarm_disp_area_on_registry,farmer,zyuusinnlongitude,zyuusinnLatitude,exchangerecord,(6378.137 * acos(cos(radians(" + str(lat) + "))* cos(radians(latitude))* cos(radians(longitude) - radians(" + str(lon) + "))+ sin(radians(" + str(lat) + "))* sin(radians(latitude)))) AS distance,(6378.137 * acos(cos(radians(zyuusinnLatitude))* cos(radians(latitude))* cos(radians(longitude) - radians(zyuusinnlongitude))+ sin(radians(zyuusinnLatitude))* sin(radians(latitude)))) AS owndistance ,null  FROM noutinavi_addzyuusinn2 where (farmer <> '" + str(farmer) + "') and classification_of_land_code_name = '田' and farmer in (select farmer from noutinavi_addzyuusinn2 where classification_of_land_code_name = '田' and address like '%" + str(areaname) + "%' group by farmer having sum(selectedfarm_disp_area_on_registry) > 50000)  HAVING (distance <= " + str(dis) + ") ORDER BY distance;"
	#print(sql)
	cur.execute(sql)
	# 実行結果を取得する
	rows = cur.fetchall()
	# 接続を閉じる
	cur.close
	conn.close
	return rows

def surroundfarmlandinformation6(zyuusinndistance):		#zyuusinndistance [0]:farmer,[1]:zyuusinnLatitude,[2]zyuusinnlongitude,[3]distance
	#areaname='花巻市上根子'
	#if __name__ == '__main__':
	# 接続する
	#conn = MySQLdb.connect(
	#user='root',
	#passwd='',
	#host='localhost',
	#db='db',
	#charset='utf8')
	# カーソルを取得する
	#print(zyuusinndistance)
	#print(glbareaname)
	cur = cnx.cursor()		
	# SQL（データベースを操作するコマンド）を実行する
	sql = "SELECT id,farmer,(6378.137 * acos(cos(radians(" + str(zyuusinndistance[1]) + "))* cos(radians(latitude))* cos(radians(longitude) - radians(" + str(zyuusinndistance[2]) + "))+ sin(radians(" + str(zyuusinndistance[1]) + "))* sin(radians(latitude)))) AS distance FROM noutinavi_addzyuusinn2 where (farmer <> '" + str(zyuusinndistance[0]) + "') and classification_of_land_code_name = '田' and farmer in (select farmer from noutinavi_addzyuusinn2 where classification_of_land_code_name = '田' and address like '%" + str(glbareaname) + "%' group by farmer having sum(selectedfarm_disp_area_on_registry) > 50000)  HAVING (distance <= " + str(zyuusinndistance[3]) + ") ORDER BY distance;"
	#print(sql)
	cur.execute(sql)
	# 実行結果を取得する
	#rows =  list(cur.fetchall()).insert(0,str(zyuusinndistance[0]))
	rows =  list(cur.fetchall())
	rows.insert(0,zyuusinndistance[0])
	#rows.append("test")
	# 接続を閉じる
	#cur.close
	#conn.close
	#print(rows)
	return rows
	#rowsreceiver(rows)
#args = sys.argv
#main(args[1])
#calculatecenterofgravity()