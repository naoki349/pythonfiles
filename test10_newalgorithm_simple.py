import test2 as t2 
import test7 as t7
import test8 as t8
import MySQLdb
import numpy as np
import pandas as pd
import folium
import sys
import random
from tqdm import tqdm
import csv
import datetime
import re
from itertools import groupby
import os
from multiprocessing import Pool
import matplotlib.pyplot as plt
import array
from socket import gethostname
#from compiler.ast import flatten
#glbareaname = ""

paddydemandlist = []
PADDY_EXCHANGE_LIST = np.array([])
MOTO = []
SAKI = []

#from colorama import Fore,Back,Style
def receiverows2(x):
	global rows2
	rows2 = x

def farmlandoptimization4():
	rows1 = []
	rows2 = []
	id_count = {}
	id_duplication_farmer = {}
	MYSQL_UPDATE = {}
	DUP_MYSQL_UPDATE = {}
	MAX_RETU = 0
	global paddydemandlist
	global PADDY_EXCHANGE_LIST
	global MOTO
	global SAKI
	global DUP_MOTO
	global DUP_SAKI
	global hostname
	hostname = ''
	EXCHANGE_COUNT = 1
	PADDY_EXCHANGE_LIST = np.array([])
	DUP_SAKI_READ_CUL_NUM = {}
	DUP_SAKI_READ_NONCUL_NUM = {}

	#ホスト名の取得（ホストごとにfarmerデータを使い分ける）
	if gethostname() == 'onoderanaokinoiMac.local':
		hostname = 'imac/'
	elif gethostname() == 'onoderanaokinoMacBook-Pro-2.local':
		hostname = 'macbookpro/'
	else:
		print('登録されていないホストからの接続です。')
		sys.exit()
	#paddydemandlistの読み込み
	with open('csv/paddydemandlist_pre.csv', "r",encoding='shift_jis') as f:
		#rows = list(csv.reader(f))
		for gyou in tqdm(csv.reader(f)):
			for youso_i,youso in enumerate(gyou):
				if youso_i == 0:
					rows1.append([youso,"",""])
				else:
					table = youso.maketrans({'(': '',')': '','\'': '',' ' : '',})
					rows1.append(youso.translate(table).split(','))
			if youso_i > MAX_RETU:
				MAX_RETU = youso_i + 1
			rows2.append(rows1)
			rows1 = []
	paddydemandlist = np.array(rows2)

	#PADDY_EXCHANGE_LISTの読み込み
	if os.path.isfile('csv/farmersdata/' + hostname + 'PADDY_EXCHANGE_LIST.csv'):
		with open('csv/farmersdata/' + hostname + 'PADDY_EXCHANGE_LIST.csv', "r",encoding='shift_jis') as f:
			for gyou in tqdm(csv.reader(f)):
					rows1.append([gyou[0],gyou[1],gyou[2],gyou[3],gyou[4]])
		PADDY_EXCHANGE_LIST = np.array(rows1)
		EXCHANGE_COUNT = int(PADDY_EXCHANGE_LIST[-1][0]) + 1
	else:
		PADDY_EXCHANGE_LIST = np.array(PADDY_EXCHANGE_LIST)

	MAX_RETU_check = 0
	MIN_RETU_check = 1000000

	#id_duplicatioon_farmerの作成
	for demandfarmer in tqdm(paddydemandlist):
		for demandpaddy in demandfarmer[1:]:
			if demandpaddy[0] == "" and demandpaddy[1] == "" and demandpaddy[2] == "":
				break
			if demandpaddy[0] in id_count:
				id_count[demandpaddy[0]] += 1
				id_duplication_farmer[demandpaddy[0]].append(demandfarmer[0][0])
			else:
				id_count[demandpaddy[0]] = 0
				id_duplication_farmer[demandpaddy[0]] = [demandpaddy[1],demandfarmer[0][0]]		#[0]:交換前の耕作farmer(MOTO),[1]:欲しいfarmer(SAKI)

	# 重複しているものについて、ベストを探す
	for DUP_i,key in enumerate(tqdm(id_duplication_farmer)):
		#開始位置を指定（テストをする際、指定した位置から再開させたい時に使用）
		#if DUP_i == 550:
			#print("DUP_i=550です")
		# DUP_iを書き込む
		with open('csv/farmersdata/' + hostname + 'DUP_i.csv', "w", encoding='shift_jis') as f:
			f.write(str(DUP_i))
		DUP_SOCIAL_BEST_search = ["","",1000]
		DUP_MOTO = []
		DUP_SAKI = []
		DUP_MOTO_farmer = ""
		DUP_SAKI_farmer = ""
		DUP_SOCIAL_BEST = ["", "", 1000]  # デフォルトでありえない1000kmを設定。
		DUP_SAKI_search = {}
		RENEW_NONDIS_flag = 0
		RENEW_DIS_flag = 0
		RENEW_EXCHANGE = []
		DUP_MOTO_READ_CUL_NUM,DUP_MOTO_READ_NONCUL_NUM = 0,0
		DUP_MOTO_orig_READ_CUL_NUM, DUP_MOTO_orig_READ_NONCUL_NUM = 0, 0
		DUP_SAKI_orig_READ_CUL_NUM, DUP_SAKI_orig_READ_NONCUL_NUM = 0, 0

		# valueが重複していないものは次のkeyへ
		if len(id_duplication_farmer[key]) < 2:
			continue
		#farmerの代入
		DUP_MOTO_farmer = id_duplication_farmer[key][0]
		# 交換元農家情報の取得 [0]:id,[1]:longitude,[2]:Latitude,[3]:zyuusinnlongitude,[4]:zyuusinnLatitude
		with open('csv/farmersdata/' + hostname + str(DUP_MOTO_farmer) + '.csv', "r", encoding='shift_jis') as f:
			for gyou in csv.reader(f):
				DUP_MOTO.append(gyou)
				if all(youso != "none" for youso in gyou):
					DUP_MOTO_READ_CUL_NUM += 1
				else:
					DUP_MOTO_READ_NONCUL_NUM += 1
		# 交換先農家情報の取得 [0]:id,[1]:longitude,[2]:Latitude,[3]:zyuusinnlongitude,[4]:zyuusinnLatitude
		for farmer in id_duplication_farmer[key][1:]:		#[0]:耕作しているfarmer,[1:]:欲しいfarmer
			DUP_SAKI = []
			DUP_SAKI_farmer = ""
			DUP_SAKI_READ_CUL_NUM[farmer] = 0
			DUP_SAKI_READ_NONCUL_NUM[farmer] = 0
			with open('csv/farmersdata/' + hostname + str(farmer) + '.csv', "r", encoding='shift_jis') as f:
				for gyou in csv.reader(f):
					DUP_SAKI.append(gyou)
					if all(youso != "none" for youso in gyou):
						DUP_SAKI_READ_CUL_NUM[farmer] += 1
					else:
						DUP_SAKI_READ_NONCUL_NUM[farmer] += 1
			# farmerの代入
			DUP_SAKI_farmer = farmer
			# 交換前の交換元農家の農地と重心までの距離
			DUP_MOTO = np.array(DUP_MOTO)
			DUP_MOTO_koukannmae_gyouretu = np.where(DUP_MOTO == key)[0]
			# MOTOの重心の経緯度を取得
			DUP_MOTO_zyuusinnlon, DUP_MOTO_zyuusinnlat = DUP_MOTO[DUP_MOTO_koukannmae_gyouretu[0]][3], DUP_MOTO[DUP_MOTO_koukannmae_gyouretu[0]][4]
			DUP_MOTO_koukannmae = t2.dist_on_sphere((float(DUP_MOTO[DUP_MOTO_koukannmae_gyouretu[0]][2]), float(DUP_MOTO[DUP_MOTO_koukannmae_gyouretu[0]][1])),(float(DUP_MOTO[DUP_MOTO_koukannmae_gyouretu[0]][4]), float(DUP_MOTO[DUP_MOTO_koukannmae_gyouretu[0]][3])))

			DUP_SAKI = np.array(DUP_SAKI)
			#DUP_SAKIの全ての中で、一番MOTOと距離が短くなるものを検索
			for DUP_SAKI_individual in DUP_SAKI:
				DUP_SAKI_koukannmae = t2.dist_on_sphere((float(DUP_SAKI_individual[2]), float(DUP_SAKI_individual[1])),(float(DUP_SAKI_individual[4]), float(DUP_SAKI_individual[3])))
				DUP_SAKI_temp = t2.dist_on_sphere((float(DUP_MOTO[DUP_MOTO_koukannmae_gyouretu[0]][2]),float(DUP_MOTO[DUP_MOTO_koukannmae_gyouretu[0]][1])), (float(DUP_SAKI_individual[4]),float(DUP_SAKI_individual[3])))
				DUP_MOTO_temp = t2.dist_on_sphere((float(DUP_SAKI_individual[2]),float(DUP_SAKI_individual[1])),(float(DUP_MOTO[DUP_MOTO_koukannmae_gyouretu[0]][4]), float(DUP_MOTO[DUP_MOTO_koukannmae_gyouretu[0]][3])))
				#if DUP_SAKI_temp < DUP_SAKI_koukannmae and DUP_SAKI_temp + DUP_MOTO_temp < DUP_SAKI_search[2]:
				if DUP_SAKI_temp < DUP_SAKI_koukannmae and DUP_MOTO_temp < DUP_MOTO_koukannmae:
					DUP_SAKI_search[DUP_MOTO_farmer,DUP_MOTO[DUP_MOTO_koukannmae_gyouretu[0]][0],DUP_SAKI_farmer,DUP_SAKI_individual[0]] = DUP_MOTO_temp + DUP_SAKI_temp		 #[0]:MOTO_id,[1]:SAKI id,[2]:社会的距離
					DUP_SAKI_zyuusinnlon,DUP_SAKI_zyuusinnlat = DUP_SAKI_individual[3],DUP_SAKI_individual[4]
		#DUP_SAKI_searchがない場合は、次のkeyへ移行
		if len(DUP_SAKI_search) == 0:
			continue
		#DUP_SAKI_searchを距離の短い順に並び替え、noneか確認し、noneでなければ交換。noneであれば、破棄前後の距離を比較し、破棄した方が距離が短く、かつ、さらに深いところでnoneになっていないのであれば破棄し、そうでなければ次にDUP_SAKI_searchの距離が短いものについて、同様に確認。全てのDUP_SAKI_searchで条件を満たさなければ、交換せずに終了。
		for k, v in sorted(DUP_SAKI_search.items(), key=lambda x: x[1]):
			syoricase = 0
			samefarmcheck = 0
			hoge_flag = 0
			if DUP_SAKI_farmer != k[2]:
				DUP_SAKI_READ_CUL_NUM[k[2]] = 0
				DUP_SAKI_READ_NONCUL_NUM[k[2]] = 0
				DUP_SAKI = []
				DUP_SAKI_farmer = str(k[2])
				# DUP_SAKIの情報を更新
				with open('csv/farmersdata/' + hostname + str(k[2]) + '.csv', "r", encoding='shift_jis') as f:
					for gyou in csv.reader(f):
						DUP_SAKI.append(gyou)
						if all(youso != "none" for youso in gyou):
							DUP_SAKI_READ_CUL_NUM[k[2]] += 1
						else:
							DUP_SAKI_READ_NONCUL_NUM[k[2]] += 1
				DUP_SAKI = np.array(DUP_SAKI)
				DUP_SAKI_zyuusinnlon, DUP_SAKI_zyuusinnlat = DUP_SAKI[0][3],DUP_SAKI[0][4]
			#if DUP_i == 1156:
				#print("DUP_i=1156!")
			DUP_SOCIAL_BEST_SAKI_index = np.where(k[3] == DUP_SAKI)[0][-1]
			#以前行った交換の破棄の検討（次に距離が短い組みの検討）
			if np.all(DUP_SAKI[DUP_SOCIAL_BEST_SAKI_index] != "none"):
				RENEW_EXCHANGE = k
				RENEW_NONDIS_flag = 1
				break
			else:
				#PADDY_EXCHANGE_LISTの該当箇所の検索
				if PADDY_EXCHANGE_LIST.ndim > 1:
					targetindex = np.where(PADDY_EXCHANGE_LIST == str(DUP_SAKI[DUP_SOCIAL_BEST_SAKI_index][0]))[0][-1]
					TARGET_EXCHANGE = PADDY_EXCHANGE_LIST[targetindex]
				else:
					targetindex = 0
					TARGET_EXCHANGE = PADDY_EXCHANGE_LIST
				# さらに深いところでnoneがあれば、破棄せず次の組みにいく（TARGET_EXCHAGEのMOTO?についても、前に交換をしていないか確認する）
				if PADDY_EXCHANGE_LIST.ndim > 1:
					DUP_MOTO_none_check_gyou,DUP_MOTO_none_check_retu = np.where(PADDY_EXCHANGE_LIST == TARGET_EXCHANGE[2])
					DUP_SAKI_none_check_gyou,DUP_SAKI_none_check_retu = np.where(PADDY_EXCHANGE_LIST == TARGET_EXCHANGE[4])
				else:
					DUP_MOTO_none_check_gyou, DUP_MOTO_none_check_retu = [0,],np.where(PADDY_EXCHANGE_LIST == TARGET_EXCHANGE[2])
					DUP_SAKI_none_check_gyou, DUP_SAKI_none_check_retu = [0,],np.where(PADDY_EXCHANGE_LIST == TARGET_EXCHANGE[4])

				if len(DUP_MOTO_none_check_gyou) > 1:
					for ho_i,ho in enumerate(DUP_MOTO_none_check_gyou):
						if int(PADDY_EXCHANGE_LIST[ho][0]) < int(TARGET_EXCHANGE[0]):
							hoge_flag = 1
							break
						elif int(PADDY_EXCHANGE_LIST[ho][0]) > int(TARGET_EXCHANGE[0]) and ((int(DUP_MOTO_none_check_retu[ho_i]) == 4) or (int(DUP_MOTO_none_check_retu[ho_i]) == 2)):	#検索しているTARGET_EXCHANGE[2]が既に別の耕作者になっている場合
							hoge_flag = 1
							break
				if len(DUP_SAKI_none_check_gyou) > 1:
					for ho_i,ho in enumerate(DUP_SAKI_none_check_gyou):
						if int(PADDY_EXCHANGE_LIST[ho][0]) < int(TARGET_EXCHANGE[0]):
							hoge_flag = 1
							break
						elif int(PADDY_EXCHANGE_LIST[ho][0]) > int(TARGET_EXCHANGE[0]) and ((int(DUP_SAKI_none_check_retu[ho_i]) == 2) or (int(DUP_SAKI_none_check_retu[ho_i]) == 4)):	#検索しているTARGET_EXCHANGE[4]が既に別の耕作者になっている場合
							hoge_flag = 1
							break
				if hoge_flag == 1:
					continue
				#MOTO_origの距離を計測
				DUP_MOTO_orig = []
				with open('csv/farmersdata/' + hostname + str(TARGET_EXCHANGE[1]) + '.csv', "r",encoding='shift_jis') as f:
					for gyou in csv.reader(f):
						DUP_MOTO_orig.append(gyou)
						if all(youso != "none" for youso in gyou):
							DUP_MOTO_orig_READ_CUL_NUM += 1
						else:
							DUP_MOTO_orig_READ_NONCUL_NUM += 1
				DUP_MOTO_orig = np.array(DUP_MOTO_orig)
				MOTO_targetindex = np.where(TARGET_EXCHANGE[2] == DUP_MOTO_orig)[0]
				#MOTO_targetindexが複数ある場合は、EXCHANGE_COUNTで該当のindexを見つける
				if len(MOTO_targetindex) > 1:
					for hoge in MOTO_targetindex:
						if str(DUP_MOTO_orig[hoge][6]) == str(TARGET_EXCHANGE[0]):
							MOTO_targetindex = hoge
							break
				else:
					MOTO_targetindex = MOTO_targetindex[0]
				DUP_SAKI_orig = []
				#SAKI_origの距離を計測
				with open('csv/farmersdata/' + hostname + str(TARGET_EXCHANGE[3]) + '.csv', "r", encoding='shift_jis') as f:
					for gyou in csv.reader(f):
						DUP_SAKI_orig.append(gyou)
						if all(youso != "none" for youso in gyou):
							DUP_SAKI_orig_READ_CUL_NUM += 1
						else:
							DUP_SAKI_orig_READ_NONCUL_NUM += 1
				DUP_SAKI_orig = np.array(DUP_SAKI_orig)
				SAKI_targetindex = np.where(TARGET_EXCHANGE[4] == DUP_SAKI_orig)[0]
				# SAKI_targetindexが複数ある場合は、EXCHANGE_COUNTで該当のindexを見つける
				if len(SAKI_targetindex) > 1:
					for hoge in SAKI_targetindex:
						if str(DUP_SAKI_orig[hoge][6]) == str(TARGET_EXCHANGE[0]):
							SAKI_targetindex = hoge
							break
				else:
					SAKI_targetindex = SAKI_targetindex[0]
				#DUP_MOTO_orig、DUP_SAKI_origの距離の計測
				DUP_MOTO_orig_dis = t2.dist_on_sphere((float(DUP_SAKI_orig[SAKI_targetindex][2]), float(DUP_SAKI_orig[SAKI_targetindex][1])),(float(DUP_MOTO_orig[MOTO_targetindex][4]), float(DUP_MOTO_orig[MOTO_targetindex][3])))
				DUP_SAKI_orig_dis = t2.dist_on_sphere((float(DUP_MOTO_orig[MOTO_targetindex][2]), float(DUP_MOTO_orig[MOTO_targetindex][1])),(float(DUP_SAKI_orig[SAKI_targetindex][4]), float(DUP_SAKI_orig[SAKI_targetindex][3])))
				#以前交換していたものよりも距離が短い場合は破棄
				if DUP_MOTO_orig_dis + DUP_SAKI_orig_dis <= v:
					break
				#以降、破棄の処理を行う。
				else:
					RENEW_EXCHANGE = k
					#今回の処理で想定されるケースは4つ。それぞれ分岐させる。
					if TARGET_EXCHANGE[2] != RENEW_EXCHANGE[1] and TARGET_EXCHANGE[4] == RENEW_EXCHANGE[3] and TARGET_EXCHANGE[2] != RENEW_EXCHANGE[3] and TARGET_EXCHANGE[4] != RENEW_EXCHANGE[1]:
						syoricase = 1
						#DUP_MOTO_orig = DUP_MOTO and DUP_SAKI_orig = DUP_SAKI(編集必要：DUP_MOTO,DUP_SAKI)
						if TARGET_EXCHANGE[1] == RENEW_EXCHANGE[0] and TARGET_EXCHANGE[3] == RENEW_EXCHANGE[2]:
							samefarmcheck = 1
						#DUP_MOTO_orig != DUP_MOTO and DUP_SAKI_orig = DUP_SAKI(編集必要：DUP_MOTO,DUP_MOTO_orig,DUP_SAKI)
						elif TARGET_EXCHANGE[1] != RENEW_EXCHANGE[0] and TARGET_EXCHANGE[3] == RENEW_EXCHANGE[2]:
							samefarmcheck = 2
						#elif TARGET_EXCHANGE[1] == RENEW_EXCHANGE[2]:
							#samefarmcheck = 3
						#DUP_SAKI_orig = DUP_MOTO(編集必要：DUP_MOTO,DUP_MOTO_orig,DUP_SAKI)
						elif TARGET_EXCHANGE[3] == RENEW_EXCHANGE[0]:
							samefarmcheck = 4
						else:
							print("syoricase=1にて、samefarmcheckに該当なし！")
							sys.exit()
					elif TARGET_EXCHANGE[2] != RENEW_EXCHANGE[1] and TARGET_EXCHANGE[4] != RENEW_EXCHANGE[3] and TARGET_EXCHANGE[2] == RENEW_EXCHANGE[3] and TARGET_EXCHANGE[4] == RENEW_EXCHANGE[1]:
						continue	#このケースは、TARGET_EXCHANGEとRENEW_EXCHANGEが同じく身であるため、破棄の処理を行わない。
						#syoricase = 2
					elif TARGET_EXCHANGE[2] != RENEW_EXCHANGE[1] and TARGET_EXCHANGE[4] != RENEW_EXCHANGE[3] and TARGET_EXCHANGE[2] == RENEW_EXCHANGE[3] and TARGET_EXCHANGE[4] != RENEW_EXCHANGE[1]:
						syoricase = 3
						if TARGET_EXCHANGE[3] == RENEW_EXCHANGE[0]:
							samefarmcheck = 1
						else:
							samefarmcheck = 2
					elif TARGET_EXCHANGE[2] != RENEW_EXCHANGE[1] and TARGET_EXCHANGE[4] != RENEW_EXCHANGE[3] and TARGET_EXCHANGE[2] != RENEW_EXCHANGE[3] and TARGET_EXCHANGE[4] == RENEW_EXCHANGE[1]:
						syoricase = 4
						if TARGET_EXCHANGE[1] == RENEW_EXCHANGE[2]:
							samefarmcheck = 1
					else:
						print("syoricaseに該当なし！")
						sys.exit()
					#ケース1の場合（DUP_MOTO_orig != DUP_MOTO,DUP_SAKI_orig = DUP_SAKI）
					if syoricase == 1:
						if samefarmcheck == 1 or samefarmcheck == 2:
							#DUP_MOTO = DUP_MOTO_orig
							if samefarmcheck == 1:
								#DUP_MOTOの該当箇所の修正
								#破棄の処理
								DUP_MOTO_renew_targetindex = np.where(DUP_MOTO == TARGET_EXCHANGE[2])[0]
								if len(DUP_MOTO_renew_targetindex) > 1:
									for hoge in DUP_MOTO_renew_targetindex:
										if hoge[6] == TARGET_EXCHANGE[0]:
											DUP_MOTO_renew_targetindex = hoge
											break
								else:
									DUP_MOTO_renew_targetindex = DUP_MOTO_renew_targetindex[0]
								DUP_MOTO[DUP_MOTO_renew_targetindex][5] = ""
								DUP_MOTO[DUP_MOTO_renew_targetindex][6] = ""
								# 前の交換で入手したものを削除
								DUP_MOTO_renew_targetindex = np.where(DUP_MOTO == TARGET_EXCHANGE[4])[0]
								if len(DUP_MOTO_renew_targetindex) > 2:
									print("前の交換で入手したものが複数あります！処理を中止します。")
									sys.exit()
								else:
									DUP_MOTO_renew_targetindex = DUP_MOTO_renew_targetindex[0]
								DUP_MOTO = np.delete(DUP_MOTO,DUP_MOTO_renew_targetindex,0)
							#DUP_MOTO != DUP_MOTO_orig
							if samefarmcheck == 2:
								#DUP_MOTO_origの該当箇所の修正
								#破棄の処理
								DUP_MOTO_renew_targetindex = np.where(DUP_MOTO_orig == TARGET_EXCHANGE[2])[0]
								if len(DUP_MOTO_renew_targetindex) > 1:
									for hoge in DUP_MOTO_renew_targetindex:
										if hoge[6] == TARGET_EXCHANGE[0]:
											DUP_MOTO_renew_targetindex = hoge
											break
								else:
									DUP_MOTO_renew_targetindex = DUP_MOTO_renew_targetindex[0]
								DUP_MOTO_orig[DUP_MOTO_renew_targetindex][5] = ""
								DUP_MOTO_orig[DUP_MOTO_renew_targetindex][6] = ""
								# 前の交換で入手したものを削除
								DUP_MOTO_renew_targetindex = np.where(DUP_MOTO_orig == TARGET_EXCHANGE[4])[0]
								if len(DUP_MOTO_renew_targetindex) > 2:
									print("前の交換で入手したものが複数あります！処理を中止します。")
									sys.exit()
								else:
									DUP_MOTO_renew_targetindex = DUP_MOTO_renew_targetindex[0]
								DUP_MOTO_orig = np.delete(DUP_MOTO_orig,DUP_MOTO_renew_targetindex,0)

							#DUP_SAKI(=DUP_SAKI_orig)の該当箇所の修正
							# 破棄の処理
							DUP_SAKI_renew_targetindex = np.where(DUP_SAKI == TARGET_EXCHANGE[4])[0]
							if len(DUP_SAKI_renew_targetindex) > 1:
								for hoge in DUP_SAKI_renew_targetindex:
									if np.any(DUP_SAKI[hoge] == TARGET_EXCHANGE[0]):
										DUP_SAKI_renew_targetindex = hoge
										break
							else:
								DUP_SAKI_renew_targetindex = DUP_SAKI_renew_targetindex[0]
							DUP_SAKI[DUP_SAKI_renew_targetindex][5] = ""
							DUP_SAKI[DUP_SAKI_renew_targetindex][6] = ""
							# 前の交換で入手したものを削除
							DUP_SAKI_renew_targetindex = np.where(DUP_SAKI == TARGET_EXCHANGE[2])[0]
							if len(DUP_SAKI_renew_targetindex) > 2:
								print("前の交換で入手したものが複数あります！処理を中止します。")
								sys.exit()
							else:
								DUP_SAKI_renew_targetindex = DUP_SAKI_renew_targetindex[0]
							DUP_SAKI = np.delete(DUP_SAKI, DUP_SAKI_renew_targetindex, 0)
						elif samefarmcheck == 4:
							# DUP_MOTO(=DUP_SAKI_orig)の該当箇所の修正
							# 破棄の処理
							DUP_MOTO_renew_targetindex = np.where(DUP_MOTO == TARGET_EXCHANGE[4])[0]
							if len(DUP_MOTO_renew_targetindex) > 1:
								for hoge in DUP_MOTO_renew_targetindex:
									if hoge[6] == TARGET_EXCHANGE[0]:
										DUP_MOTO_renew_targetindex = hoge
										break
							else:
								DUP_MOTO_renew_targetindex = DUP_MOTO_renew_targetindex[0]
							DUP_MOTO[DUP_MOTO_renew_targetindex][5] = ""
							DUP_MOTO[DUP_MOTO_renew_targetindex][6] = ""
							# 前の交換で入手したものを削除
							DUP_MOTO_renew_targetindex = np.where(DUP_MOTO == TARGET_EXCHANGE[2])[0]
							if len(DUP_MOTO_renew_targetindex) > 2:
								print("前の交換で入手したものが複数あります！処理を中止します。")
								sys.exit()
							else:
								DUP_MOTO_renew_targetindex = DUP_MOTO_renew_targetindex[0]
							DUP_MOTO = np.delete(DUP_MOTO, DUP_MOTO_renew_targetindex, 0)
							# DUP_MOTO_origの該当箇所の修正
							# 破棄の処理
							DUP_SAKI_renew_targetindex = np.where(DUP_MOTO_orig == TARGET_EXCHANGE[2])[0]
							if len(DUP_SAKI_renew_targetindex) > 1:
								for hoge in DUP_SAKI_renew_targetindex:
									if np.any(DUP_MOTO_orig[hoge] == TARGET_EXCHANGE[0]):
										DUP_SAKI_renew_targetindex = hoge
										break
							else:
								DUP_SAKI_renew_targetindex = DUP_SAKI_renew_targetindex[0]
							DUP_MOTO_orig[DUP_SAKI_renew_targetindex][5] = ""
							DUP_MOTO_orig[DUP_SAKI_renew_targetindex][6] = ""
							# 前の交換で入手したものを削除
							DUP_SAKI_renew_targetindex = np.where(DUP_MOTO_orig == TARGET_EXCHANGE[4])[0]
							if len(DUP_SAKI_renew_targetindex) > 2:
								print("前の交換で入手したものが複数あります！処理を中止します。")
								sys.exit()
							else:
								DUP_SAKI_renew_targetindex = DUP_SAKI_renew_targetindex[0]
							DUP_MOTO_orig = np.delete(DUP_MOTO_orig, DUP_SAKI_renew_targetindex, 0)
					elif syoricase == 2:
						#DUP_SAKI(=DUP_MOTO_orig)の該当箇所の修正
						#破棄の処理
						DUP_MOTO_renew_targetindex = np.where(DUP_SAKI == TARGET_EXCHANGE[2])[0]
						if len(DUP_MOTO_renew_targetindex) > 1:
							for hoge in DUP_MOTO_renew_targetindex:
								if hoge[6] == TARGET_EXCHANGE[0]:
									DUP_MOTO_renew_targetindex = hoge
									break
						else:
							DUP_MOTO_renew_targetindex = DUP_MOTO_renew_targetindex[0]
						DUP_SAKI[DUP_MOTO_renew_targetindex][5] = ""
						DUP_SAKI[DUP_MOTO_renew_targetindex][6] = ""
						# 前の交換で入手したものを削除
						DUP_MOTO_renew_targetindex = np.where(DUP_SAKI == TARGET_EXCHANGE[4])[0]
						if len(DUP_MOTO_renew_targetindex) > 2:
							print("前の交換で入手したものが複数あります！処理を中止します。")
							sys.exit()
						else:
							DUP_MOTO_renew_targetindex = DUP_MOTO_renew_targetindex[0]
						DUP_SAKI = np.delete(DUP_SAKI,DUP_MOTO_renew_targetindex,0)
						#DUP_MOTO(=DUP_SAKI_orig)の該当箇所の修正
						# 破棄の処理
						DUP_SAKI_renew_targetindex = np.where(DUP_MOTO == TARGET_EXCHANGE[4])[0]
						if len(DUP_SAKI_renew_targetindex) > 1:
							for hoge in DUP_SAKI_renew_targetindex:
								if np.any(DUP_MOTO[hoge] == TARGET_EXCHANGE[0]):
									DUP_SAKI_renew_targetindex = hoge
									break
						else:
							DUP_SAKI_renew_targetindex = DUP_SAKI_renew_targetindex[0]
						DUP_MOTO[DUP_SAKI_renew_targetindex][5] = ""
						DUP_MOTO[DUP_SAKI_renew_targetindex][6] = ""
						# 前の交換で入手したものを削除
						DUP_SAKI_renew_targetindex = np.where(DUP_MOTO == TARGET_EXCHANGE[2])[0]
						if len(DUP_SAKI_renew_targetindex) > 2:
							print("前の交換で入手したものが複数あります！処理を中止します。")
							sys.exit()
						else:
							DUP_SAKI_renew_targetindex = DUP_SAKI_renew_targetindex[0]
						DUP_MOTO = np.delete(DUP_MOTO, DUP_SAKI_renew_targetindex, 0)

					elif syoricase == 3:
						#DUP_SAKI(=DUP_MOTO_orig)の該当箇所の修正
						#破棄の処理
						DUP_MOTO_renew_targetindex = np.where(DUP_SAKI == TARGET_EXCHANGE[2])[0]
						if len(DUP_MOTO_renew_targetindex) > 1:
							for hoge in DUP_MOTO_renew_targetindex:
								if hoge[6] == TARGET_EXCHANGE[0]:
									DUP_MOTO_renew_targetindex = hoge
									break
						else:
							DUP_MOTO_renew_targetindex = DUP_MOTO_renew_targetindex[0]
						DUP_SAKI[DUP_MOTO_renew_targetindex][5] = ""
						DUP_SAKI[DUP_MOTO_renew_targetindex][6] = ""
						# 前の交換で入手したものを削除
						DUP_MOTO_renew_targetindex = np.where(DUP_SAKI == TARGET_EXCHANGE[4])[0]
						if len(DUP_MOTO_renew_targetindex) > 2:
							print("前の交換で入手したものが複数あります！処理を中止します。")
							sys.exit()
						else:
							DUP_MOTO_renew_targetindex = DUP_MOTO_renew_targetindex[0]
						DUP_SAKI = np.delete(DUP_SAKI,DUP_MOTO_renew_targetindex,0)

						# DUP_MOTO　== DUP_SAKI_origの場合の処理
						#DUP_MOTO(DUP_SAKI_orig）の該当箇所の修正
						if samefarmcheck == 1:
							DUP_SAKI_renew_targetindex = np.where(DUP_MOTO == TARGET_EXCHANGE[4])[0]
							if len(DUP_SAKI_renew_targetindex) > 1:
								for hoge in DUP_SAKI_renew_targetindex:
									if np.any(DUP_MOTO[hoge] == TARGET_EXCHANGE[0]):
										DUP_SAKI_renew_targetindex = hoge
										break
							else:
								DUP_SAKI_renew_targetindex = DUP_SAKI_renew_targetindex[0]
							DUP_MOTO[DUP_SAKI_renew_targetindex][5] = ""
							DUP_MOTO[DUP_SAKI_renew_targetindex][6] = ""
							# 前の交換で入手したものを削除
							DUP_SAKI_renew_targetindex = np.where(DUP_MOTO == TARGET_EXCHANGE[2])[0]
							if len(DUP_SAKI_renew_targetindex) > 2:
								print("前の交換で入手したものが複数あります！処理を中止します。")
								sys.exit()
							else:
								DUP_SAKI_renew_targetindex = DUP_SAKI_renew_targetindex[0]
							DUP_MOTO = np.delete(DUP_MOTO, DUP_SAKI_renew_targetindex, 0)

						# farmerがDUP_MOTO != DUP_SAKI_origの場合の処理
						if samefarmcheck == 2:
							#DUP_SAKI_orig
							DUP_SAKI_renew_targetindex = np.where(DUP_SAKI_orig == TARGET_EXCHANGE[4])[0]
							if len(DUP_SAKI_renew_targetindex) > 1:
								for hoge in DUP_SAKI_renew_targetindex:
									if np.any(DUP_SAKI_orig[hoge] == TARGET_EXCHANGE[0]):
										DUP_SAKI_renew_targetindex = hoge
										break
							else:
								DUP_SAKI_renew_targetindex = DUP_SAKI_renew_targetindex[0]
							DUP_SAKI_orig[DUP_SAKI_renew_targetindex][5] = ""
							DUP_SAKI_orig[DUP_SAKI_renew_targetindex][6] = ""
							# 前の交換で入手したものを削除
							DUP_SAKI_renew_targetindex = np.where(DUP_SAKI_orig == TARGET_EXCHANGE[2])[0]
							if len(DUP_SAKI_renew_targetindex) > 2:
								print("前の交換で入手したものが複数あります！処理を中止します。")
								sys.exit()
							else:
								DUP_SAKI_renew_targetindex = DUP_SAKI_renew_targetindex[0]
							DUP_SAKI_orig = np.delete(DUP_SAKI_orig, DUP_SAKI_renew_targetindex, 0)

					elif syoricase == 4:
						if samefarmcheck == 0:
							#DUP_MOTO_origの該当箇所の修正
							#破棄の処理
							DUP_MOTO_renew_targetindex = np.where(DUP_MOTO_orig == TARGET_EXCHANGE[2])[0]
							if len(DUP_MOTO_renew_targetindex) > 1:
								for hoge in DUP_MOTO_renew_targetindex:
									if hoge[6] == TARGET_EXCHANGE[0]:
										DUP_MOTO_renew_targetindex = hoge
										break
							else:
								DUP_MOTO_renew_targetindex = DUP_MOTO_renew_targetindex[0]
							DUP_MOTO_orig[DUP_MOTO_renew_targetindex][5] = ""
							DUP_MOTO_orig[DUP_MOTO_renew_targetindex][6] = ""
							# 前の交換で入手したものを削除
							DUP_MOTO_renew_targetindex = np.where(DUP_MOTO_orig == TARGET_EXCHANGE[4])[0]
							if len(DUP_MOTO_renew_targetindex) > 2:
								print("前の交換で入手したものが複数あります！処理を中止します。")
								sys.exit()
							else:
								DUP_MOTO_renew_targetindex = DUP_MOTO_renew_targetindex[0]
							DUP_MOTO_orig = np.delete(DUP_MOTO_orig,DUP_MOTO_renew_targetindex,0)
						else:
							#DUP_SAKIの該当箇所の修正
							#破棄の処理
							DUP_MOTO_renew_targetindex = np.where(DUP_SAKI == TARGET_EXCHANGE[2])[0]
							if len(DUP_MOTO_renew_targetindex) > 1:
								for hoge in DUP_MOTO_renew_targetindex:
									if hoge[6] == TARGET_EXCHANGE[0]:
										DUP_MOTO_renew_targetindex = hoge
										break
							else:
								DUP_MOTO_renew_targetindex = DUP_MOTO_renew_targetindex[0]
							DUP_SAKI[DUP_MOTO_renew_targetindex][5] = ""
							DUP_SAKI[DUP_MOTO_renew_targetindex][6] = ""
							# 前の交換で入手したものを削除
							DUP_MOTO_renew_targetindex = np.where(DUP_SAKI == TARGET_EXCHANGE[4])[0]
							if len(DUP_MOTO_renew_targetindex) > 2:
								print("前の交換で入手したものが複数あります！処理を中止します。")
								sys.exit()
							else:
								DUP_MOTO_renew_targetindex = DUP_MOTO_renew_targetindex[0]
							DUP_SAKI = np.delete(DUP_SAKI,DUP_MOTO_renew_targetindex,0)

						#DUP_MOTO(=DUP_SAKI_orig)の該当箇所の修正
						# 破棄の処理
						DUP_SAKI_renew_targetindex = np.where(DUP_MOTO == TARGET_EXCHANGE[4])[0]
						if len(DUP_SAKI_renew_targetindex) > 1:
							for hoge in DUP_SAKI_renew_targetindex:
								if np.any(DUP_MOTO[hoge] == TARGET_EXCHANGE[0]):
									DUP_SAKI_renew_targetindex = hoge
									break
						else:
							DUP_SAKI_renew_targetindex = DUP_SAKI_renew_targetindex[0]
						DUP_MOTO[DUP_SAKI_renew_targetindex][5] = ""
						DUP_MOTO[DUP_SAKI_renew_targetindex][6] = ""
						# 前の交換で入手したものを削除
						DUP_SAKI_renew_targetindex = np.where(DUP_MOTO == TARGET_EXCHANGE[2])[0]
						if len(DUP_SAKI_renew_targetindex) > 2:
							print("前の交換で入手したものが複数あります！処理を中止します。")
							sys.exit()
						else:
							DUP_SAKI_renew_targetindex = DUP_SAKI_renew_targetindex[0]
						DUP_MOTO = np.delete(DUP_MOZTO, DUP_SAKI_renew_targetindex, 0)
					#MYSQLの更新の修正（共通）
					#MOTO_origの削除
					del DUP_MYSQL_UPDATE[TARGET_EXCHANGE[2]]
					#SAKIの削除
					del DUP_MYSQL_UPDATE[TARGET_EXCHANGE[4]]
					#id_duplication_farmerの更新
					hoge_index = id_duplication_farmer[TARGET_EXCHANGE[2]].index(TARGET_EXCHANGE[1])
					id_duplication_farmer[TARGET_EXCHANGE[2]][hoge_index] = TARGET_EXCHANGE[3]
					id_duplication_farmer[TARGET_EXCHANGE[2]][0] = TARGET_EXCHANGE[1]					#耕作している

					hoge_index = id_duplication_farmer[TARGET_EXCHANGE[4]].index(TARGET_EXCHANGE[3])
					id_duplication_farmer[TARGET_EXCHANGE[4]][hoge_index] = TARGET_EXCHANGE[1]
					id_duplication_farmer[TARGET_EXCHANGE[4]][0] = TARGET_EXCHANGE[3]

					# PADDY_EXCHANGE_LISTの該当箇所の削除（破棄後の交換は通常の処理で行う）（共通）
					if len(PADDY_EXCHANGE_LIST) == 5:
						with open('csv/farmersdata/' + hostname + 'PADDY_EXCHANGE_LIST(del).csv', 'a',encoding='shift_jis') as f:
							f.write('\n' + str(PADDY_EXCHANGE_LIST[0]) + ',' + str(PADDY_EXCHANGE_LIST[1]) + ',' + str(PADDY_EXCHANGE_LIST[2]) + '+' + str(PADDY_EXCHANGE_LIST[3]) + '+' + str(PADDY_EXCHANGE_LIST[4]))
						PADDY_EXCHANGE_LIST = np.array([])
					else:
						targetindex = np.where(PADDY_EXCHANGE_LIST == TARGET_EXCHANGE[0])[0][0]
						with open('csv/farmersdata/' + hostname + 'PADDY_EXCHANGE_LIST(del).csv', 'a',encoding='shift_jis') as f:
							f.write(str(PADDY_EXCHANGE_LIST[targetindex][0]) + ',' + str(PADDY_EXCHANGE_LIST[targetindex][1]) + ',' + str(PADDY_EXCHANGE_LIST[targetindex][2]) + ',' + str(PADDY_EXCHANGE_LIST[targetindex][3]) + ',' + str(PADDY_EXCHANGE_LIST[targetindex][4]) + '\n')
						PADDY_EXCHANGE_LIST = np.delete(PADDY_EXCHANGE_LIST, targetindex, 0)
					RENEW_DIS_flag = 1
					break

		if RENEW_NONDIS_flag != 1 and RENEW_DIS_flag != 1:
			continue
		#交換する（破棄なし、破棄ありどちらもこちらで処理）
		else:
			DUP_MOTO_WRITE_CUL_NUM, DUP_MOTO_WRITE_NONCUL_NUM = 0, 0
			DUP_SAKI_WRITE_CUL_NUM, DUP_SAKI_WRITE_NONCUL_NUM = 0, 0
			DUP_MOTO_orig_WRITE_CUL_NUM, DUP_MOTO_orig_WRITE_NONCUL_NUM = 0, 0
			DUP_SAKI_orig_WRITE_CUL_NUM, DUP_SAKI_orig_WRITE_NONCUL_NUM = 0, 0
			# 辞書配列を更新（mysqlデータの更新）（共通）
			DUP_MYSQL_UPDATE[RENEW_EXCHANGE[1]] = (RENEW_EXCHANGE[2], DUP_SAKI_zyuusinnlon,DUP_SAKI_zyuusinnlat)  # 交換元idの更新(farmer,zyuusinnlon,zyuusinnlat)
			DUP_MYSQL_UPDATE[RENEW_EXCHANGE[3]] = (RENEW_EXCHANGE[0], DUP_MOTO_zyuusinnlon,DUP_MOTO_zyuusinnlat)  # 交換先idの更新(farmer,zyuusinnlon,zyuusinnlat)
			# PADDY_EXCHANGE_LISTの更新（共通）
			if len(PADDY_EXCHANGE_LIST) == 0:
				PADDY_EXCHANGE_LIST = np.array([EXCHANGE_COUNT, str(RENEW_EXCHANGE[0]), RENEW_EXCHANGE[1], str(RENEW_EXCHANGE[2]), RENEW_EXCHANGE[3]])
			else:
				PADDY_EXCHANGE_LIST = np.vstack([PADDY_EXCHANGE_LIST, [EXCHANGE_COUNT, str(RENEW_EXCHANGE[0]), RENEW_EXCHANGE[1], str(RENEW_EXCHANGE[2]), RENEW_EXCHANGE[3]]])
			if syoricase == 0:
				# DUP_MOTO情報の更新
				with open('csv/farmersdata/' + hostname + str(RENEW_EXCHANGE[0]) + '.csv', 'w', encoding='shift_jis') as f:
					writer = csv.writer(f)
					for gyou in DUP_MOTO:
						if np.all(gyou != "none"):
							if gyou[0] == RENEW_EXCHANGE[1]:
								writer.writerow([str(gyou[0]), str(gyou[1]), str(gyou[2]), str(gyou[3]), str(gyou[4]), "none",str(EXCHANGE_COUNT)])
								DUP_MOTO_WRITE_NONCUL_NUM += 1
							else:
								writer.writerow([str(gyou[0]), str(gyou[1]), str(gyou[2]), str(gyou[3]), str(gyou[4]), "", ""])
								DUP_MOTO_WRITE_CUL_NUM += 1
						else:
							writer.writerow([str(gyou[0]), str(gyou[1]), str(gyou[2]), str(gyou[3]), str(gyou[4]), str(gyou[5]),str(gyou[6])])
							DUP_MOTO_WRITE_NONCUL_NUM += 1
					DUP_SAKI_targetindex = np.where(DUP_SAKI == RENEW_EXCHANGE[3])[0][-1]
					writer.writerow([DUP_SAKI[DUP_SAKI_targetindex][0], DUP_SAKI[DUP_SAKI_targetindex][1], DUP_SAKI[DUP_SAKI_targetindex][2],DUP_MOTO[0][3], DUP_MOTO[0][4], "", ""])
					DUP_MOTO_WRITE_CUL_NUM += 1
				#耕作農地数のチェック
				if DUP_MOTO_READ_CUL_NUM != (DUP_MOTO_WRITE_CUL_NUM):
					print("DUP_MOTO_READ_CUL_NUM != DUP_MOTO_WRITE_CUL_NUM")
					print("syoricase:" + str(syoricase))
					print("samefarmcheck:" + str(samefarmcheck))
					sys.exit()
				# DUP_SAKI情報の更新
				with open('csv/farmersdata/' + hostname + str(RENEW_EXCHANGE[2]) + '.csv', 'w', encoding='shift_jis') as f:
					writer = csv.writer(f)
					for gyou in DUP_SAKI:
						if np.all(gyou != "none"):
							if gyou[0] == RENEW_EXCHANGE[3]:
								writer.writerow([str(gyou[0]), str(gyou[1]), str(gyou[2]), str(gyou[3]), str(gyou[4]), "none",str(EXCHANGE_COUNT)])
								DUP_SAKI_WRITE_NONCUL_NUM += 1
							else:
								writer.writerow([str(gyou[0]), str(gyou[1]), str(gyou[2]), str(gyou[3]), str(gyou[4]), "", ""])
								DUP_SAKI_WRITE_CUL_NUM += 1
						else:
							writer.writerow([str(gyou[0]), str(gyou[1]), str(gyou[2]), str(gyou[3]), str(gyou[4]), str(gyou[5]),str(gyou[6])])
							DUP_SAKI_WRITE_NONCUL_NUM += 1
					DUP_MOTO_targetindex = np.where(DUP_MOTO == RENEW_EXCHANGE[1])[0][-1]
					writer.writerow([DUP_MOTO[DUP_MOTO_targetindex][0], DUP_MOTO[DUP_MOTO_targetindex][1], DUP_MOTO[DUP_MOTO_targetindex][2],DUP_SAKI[0][3], DUP_SAKI[0][4], "", ""])
					DUP_SAKI_WRITE_CUL_NUM += 1
				# 耕作農地数のチェック
				if DUP_SAKI_READ_CUL_NUM[k[2]] != (DUP_SAKI_WRITE_CUL_NUM):
					print("DUP_SAKI_READ_CUL_NUM != DUP_SAKI_WRITE_CUL_NUM")
					print("syoricase:" + str(syoricase))
					print("samefarmcheck:" + str(samefarmcheck))
					sys.exit()
			elif syoricase == 1:
				if samefarmcheck == 1 or samefarmcheck == 2:
					# DUP_MOTO情報の更新
					with open('csv/farmersdata/' + hostname + str(RENEW_EXCHANGE[0]) + '.csv', 'w', encoding='shift_jis') as f:
						writer = csv.writer(f)
						for gyou in DUP_MOTO:
							if np.all(gyou != "none"):
								if gyou[0] == RENEW_EXCHANGE[1]:
									writer.writerow([str(gyou[0]), str(gyou[1]), str(gyou[2]), str(gyou[3]), str(gyou[4]), "none",str(EXCHANGE_COUNT)])
									DUP_MOTO_WRITE_NONCUL_NUM += 1
								else:
									writer.writerow([str(gyou[0]), str(gyou[1]), str(gyou[2]), str(gyou[3]), str(gyou[4]), "", ""])
									DUP_MOTO_WRITE_CUL_NUM += 1
							else:
								writer.writerow([str(gyou[0]), str(gyou[1]), str(gyou[2]), str(gyou[3]), str(gyou[4]), str(gyou[5]),str(gyou[6])])
								DUP_MOTO_WRITE_NONCUL_NUM += 1
						DUP_SAKI_targetindex = np.where(DUP_SAKI == RENEW_EXCHANGE[3])[0][-1]
						writer.writerow([DUP_SAKI[DUP_SAKI_targetindex][0], DUP_SAKI[DUP_SAKI_targetindex][1], DUP_SAKI[DUP_SAKI_targetindex][2],DUP_MOTO[0][3], DUP_MOTO[0][4], "", ""])
						DUP_MOTO_WRITE_CUL_NUM += 1
					# 耕作農地数のチェック
					if DUP_MOTO_READ_CUL_NUM != (DUP_MOTO_WRITE_CUL_NUM):
						print("DUP_MOTO_READ_CUL_NUM != DUP_MOTO_WRITE_CUL_NUM")
						print("syoricase:" + str(syoricase))
						print("samefarmcheck:" + str(samefarmcheck))
						sys.exit()
					# DUP_SAKI情報の更新
					with open('csv/farmersdata/' + hostname + str(RENEW_EXCHANGE[2]) + '.csv', 'w', encoding='shift_jis') as f:
						writer = csv.writer(f)
						for gyou in DUP_SAKI:
							if np.all(gyou != "none"):
								if gyou[0] == RENEW_EXCHANGE[3]:
									writer.writerow([str(gyou[0]), str(gyou[1]), str(gyou[2]), str(gyou[3]), str(gyou[4]), "none",str(EXCHANGE_COUNT)])
									DUP_SAKI_WRITE_NONCUL_NUM += 1
								else:
									writer.writerow([str(gyou[0]), str(gyou[1]), str(gyou[2]), str(gyou[3]), str(gyou[4]), "", ""])
									DUP_SAKI_WRITE_CUL_NUM += 1
							else:
								writer.writerow([str(gyou[0]), str(gyou[1]), str(gyou[2]), str(gyou[3]), str(gyou[4]), str(gyou[5]),str(gyou[6])])
								DUP_SAKI_WRITE_NONCUL_NUM += 1
							# 耕作農地数等のカウント
						DUP_MOTO_targetindex = np.where(DUP_MOTO == RENEW_EXCHANGE[1])[0][-1]
						writer.writerow([DUP_MOTO[DUP_MOTO_targetindex][0], DUP_MOTO[DUP_MOTO_targetindex][1], DUP_MOTO[DUP_MOTO_targetindex][2],DUP_SAKI[0][3], DUP_SAKI[0][4], "", ""])
						DUP_SAKI_WRITE_CUL_NUM += 1
					# 耕作農地数のチェック
					if DUP_SAKI_READ_CUL_NUM[k[2]] != (DUP_SAKI_WRITE_CUL_NUM):
						print("DUP_SAKI_READ_CUL_NUM != DUP_SAKI_WRITE_CUL_NUM")
						print("syoricase:" + str(syoricase))
						print("samefarmcheck:" + str(samefarmcheck))
						sys.exit()
					if samefarmcheck == 2:
						# DUP_MOTO_orig情報の更新
						with open('csv/farmersdata/' + hostname + str(TARGET_EXCHANGE[1]) + '.csv', 'w',encoding='shift_jis') as f:
							writer = csv.writer(f)
							for gyou in DUP_MOTO_orig:
								writer.writerow([str(gyou[0]), str(gyou[1]), str(gyou[2]), str(gyou[3]), str(gyou[4]), str(gyou[5]),str(gyou[6])])
								# 耕作農地数等のカウント
								if all(youso != "none" for youso in gyou):
									DUP_MOTO_orig_WRITE_CUL_NUM += 1
								else:
									DUP_MOTO_orig_WRITE_NONCUL_NUM += 1
						# 耕作農地数のチェック
						if DUP_MOTO_orig_READ_CUL_NUM != (DUP_MOTO_orig_WRITE_CUL_NUM):
							print("DUP_MOTO_orig_READ_CUL_NUM != DUP_MOTO_orig_WRITE_CUL_NUM")
							print("syoricase:" + str(syoricase))
							print("samefarmcheck:" + str(samefarmcheck))
							sys.exit()
				elif samefarmcheck == 4:
					# DUP_MOTO(=DUP_SAKI_orig)情報の更新
					with open('csv/farmersdata/' + hostname + str(RENEW_EXCHANGE[0]) + '.csv', 'w', encoding='shift_jis') as f:
						writer = csv.writer(f)
						for gyou in DUP_MOTO:
							if np.all(gyou != "none"):
								if gyou[0] == RENEW_EXCHANGE[1]:
									writer.writerow([str(gyou[0]), str(gyou[1]), str(gyou[2]), str(gyou[3]), str(gyou[4]), "none",str(EXCHANGE_COUNT)])
									DUP_MOTO_WRITE_NONCUL_NUM += 1
								else:
									writer.writerow([str(gyou[0]), str(gyou[1]), str(gyou[2]), str(gyou[3]), str(gyou[4]), "", ""])
									DUP_MOTO_WRITE_CUL_NUM += 1
							else:
								writer.writerow([str(gyou[0]), str(gyou[1]), str(gyou[2]), str(gyou[3]), str(gyou[4]), str(gyou[5]),str(gyou[6])])
								DUP_MOTO_WRITE_NONCUL_NUM += 1
						DUP_SAKI_targetindex = np.where(DUP_SAKI == RENEW_EXCHANGE[3])[0][-1]
						writer.writerow([DUP_SAKI[DUP_SAKI_targetindex][0], DUP_SAKI[DUP_SAKI_targetindex][1], DUP_SAKI[DUP_SAKI_targetindex][2],DUP_MOTO[0][3], DUP_MOTO[0][4], "", ""])
						DUP_MOTO_WRITE_CUL_NUM += 1
					# 耕作農地数のチェック
					if DUP_MOTO_READ_CUL_NUM != (DUP_MOTO_WRITE_CUL_NUM):
						print("DUP_MOTO_READ_CUL_NUM != DUP_MOTO_WRITE_CUL_NUM")
						print("syoricase:" + str(syoricase))
						print("samefarmcheck:" + str(samefarmcheck))
						sys.exit()
					# DUP_SAKI情報の更新
					with open('csv/farmersdata/' + hostname + str(RENEW_EXCHANGE[2]) + '.csv', 'w', encoding='shift_jis') as f:
						writer = csv.writer(f)
						for gyou in DUP_SAKI:
							if np.all(gyou != "none"):
								if gyou[0] == RENEW_EXCHANGE[3]:
									writer.writerow([str(gyou[0]), str(gyou[1]), str(gyou[2]), str(gyou[3]), str(gyou[4]), "none",str(EXCHANGE_COUNT)])
									DUP_SAKI_WRITE_NONCUL_NUM += 1
								else:
									writer.writerow([str(gyou[0]), str(gyou[1]), str(gyou[2]), str(gyou[3]), str(gyou[4]), "", ""])
									DUP_SAKI_WRITE_CUL_NUM += 1
							else:
								writer.writerow([str(gyou[0]), str(gyou[1]), str(gyou[2]), str(gyou[3]), str(gyou[4]), str(gyou[5]),str(gyou[6])])
								DUP_SAKI_WRITE_NONCUL_NUM += 1
						DUP_MOTO_targetindex = np.where(DUP_MOTO == RENEW_EXCHANGE[1])[0][-1]
						writer.writerow([DUP_MOTO[DUP_MOTO_targetindex][0], DUP_MOTO[DUP_MOTO_targetindex][1], DUP_MOTO[DUP_MOTO_targetindex][2],DUP_SAKI[0][3], DUP_SAKI[0][4], "", ""])
						DUP_SAKI_WRITE_CUL_NUM += 1
					# 耕作農地数のチェック
					if DUP_SAKI_READ_CUL_NUM[k[2]] != (DUP_SAKI_WRITE_CUL_NUM):
						print("DUP_SAKI_READ_CUL_NUM != DUP_SAKI_WRITE_CUL_NUM")
						print("syoricase:" + str(syoricase))
						print("samefarmcheck:" + str(samefarmcheck))
						sys.exit()
					# DUP_MOTO_orig情報の更新
					with open('csv/farmersdata/' + hostname + str(TARGET_EXCHANGE[1]) + '.csv', 'w',encoding='shift_jis') as f:
						writer = csv.writer(f)
						for gyou in DUP_MOTO_orig:
							writer.writerow([str(gyou[0]), str(gyou[1]), str(gyou[2]), str(gyou[3]), str(gyou[4]), str(gyou[5]),str(gyou[6])])
							# 耕作農地数等のカウント
							if all(youso != "none" for youso in gyou):
								DUP_MOTO_orig_WRITE_CUL_NUM += 1
							else:
								DUP_MOTO_orig_WRITE_NONCUL_NUM += 1
					# 耕作農地数のチェック
					if DUP_MOTO_orig_READ_CUL_NUM != DUP_MOTO_orig_WRITE_CUL_NUM:
						print("DUP_MOTO_orig_READ_CUL_NUM != DUP_MOTO_orig_WRITE_CUL_NUM")
						print("syoricase:" + str(syoricase))
						print("samefarmcheck:" + str(samefarmcheck))
						sys.exit()
			elif syoricase == 2:
				# DUP_MOTO(=DUP_SAKI_orig)情報の更新
				with open('csv/farmersdata/' + hostname + str(RENEW_EXCHANGE[0]) + '.csv', 'w', encoding='shift_jis') as f:
					writer = csv.writer(f)
					for gyou in DUP_MOTO:
						if np.all(gyou != "none"):
							if gyou[0] == RENEW_EXCHANGE[1]:
								writer.writerow([str(gyou[0]), str(gyou[1]), str(gyou[2]), str(gyou[3]), str(gyou[4]), "none",str(EXCHANGE_COUNT)])
								DUP_MOTO_WRITE_NONCUL_NUM += 1
							else:
								writer.writerow([str(gyou[0]), str(gyou[1]), str(gyou[2]), str(gyou[3]), str(gyou[4]), "", ""])
								DUP_MOTO_WRITE_CUL_NUM += 1
						else:
							writer.writerow([str(gyou[0]), str(gyou[1]), str(gyou[2]), str(gyou[3]), str(gyou[4]), str(gyou[5]),str(gyou[6])])
							DUP_MOTO_WRITE_NONCUL_NUM += 1
					DUP_SAKI_targetindex = np.where(DUP_SAKI == RENEW_EXCHANGE[3])[0][-1]	#DUP_MOTO_orig?
					writer.writerow([DUP_SAKI[DUP_SAKI_targetindex][0], DUP_SAKI[DUP_SAKI_targetindex][1], DUP_SAKI[DUP_SAKI_targetindex][2],DUP_MOTO[0][3], DUP_MOTO[0][4], "", ""])
					DUP_MOTO_WRITE_CUL_NUM += 1
				# 耕作農地数のチェック
				if DUP_MOTO_READ_CUL_NUM != (DUP_MOTO_WRITE_CUL_NUM):
					print("DUP_MOTO_READ_CUL_NUM != DUP_MOTO_WRITE_CUL_NUM")
					print("syoricase:" + str(syoricase))
					print("samefarmcheck:" + str(samefarmcheck))
					sys.exit()
				# DUP_SAKI(=DUP_MOTO_orig)情報の更新
				with open('csv/farmersdata/' + hostname + str(RENEW_EXCHANGE[2]) + '.csv', 'w', encoding='shift_jis') as f:
					writer = csv.writer(f)
					for gyou in DUP_SAKI:
						if np.all(gyou != "none"):
							if gyou[0] == RENEW_EXCHANGE[3]:
								writer.writerow([str(gyou[0]), str(gyou[1]), str(gyou[2]), str(gyou[3]), str(gyou[4]), "none",str(EXCHANGE_COUNT)])
								DUP_SAKI_WRITE_NONCUL_NUM += 1
							else:
								writer.writerow([str(gyou[0]), str(gyou[1]), str(gyou[2]), str(gyou[3]), str(gyou[4]), "", ""])
								DUP_SAKI_WRITE_CUL_NUM += 1
						else:
							writer.writerow([str(gyou[0]), str(gyou[1]), str(gyou[2]), str(gyou[3]), str(gyou[4]), str(gyou[5]),str(gyou[6])])
							DUP_SAKI_WRITE_NONCUL_NUM += 1
					DUP_MOTO_targetindex = np.where(DUP_MOTO == RENEW_EXCHANGE[1])[0][-1]
					writer.writerow([DUP_MOTO[DUP_MOTO_targetindex][0], DUP_MOTO[DUP_MOTO_targetindex][1], DUP_MOTO[DUP_MOTO_targetindex][2],DUP_SAKI[0][3], DUP_SAKI[0][4], "", ""])
					DUP_SAKI_WRITE_CUL_NUM += 1
				# 耕作農地数のチェック
				if DUP_SAKI_READ_CUL_NUM[k[2]] != (DUP_SAKI_WRITE_CUL_NUM):
					print("DUP_SAKI_READ_CUL_NUM != DUP_SAKI_WRITE_CUL_NUM")
					print("syoricase:" + str(syoricase))
					print("samefarmcheck:" + str(samefarmcheck))
					sys.exit()
			elif syoricase == 3:
				# DUP_MOTO情報の更新
				with open('csv/farmersdata/' + hostname + str(RENEW_EXCHANGE[0]) + '.csv', 'w', encoding='shift_jis') as f:
					writer = csv.writer(f)
					for gyou in DUP_MOTO:
						if np.all(gyou != "none"):
							if gyou[0] == RENEW_EXCHANGE[1]:
								writer.writerow([str(gyou[0]), str(gyou[1]), str(gyou[2]), str(gyou[3]), str(gyou[4]), "none",str(EXCHANGE_COUNT)])
								DUP_MOTO_WRITE_NONCUL_NUM += 1
							else:
								writer.writerow([str(gyou[0]), str(gyou[1]), str(gyou[2]), str(gyou[3]), str(gyou[4]), "", ""])
								DUP_MOTO_WRITE_CUL_NUM += 1
						else:
							writer.writerow([str(gyou[0]), str(gyou[1]), str(gyou[2]), str(gyou[3]), str(gyou[4]), str(gyou[5]),str(gyou[6])])
							DUP_MOTO_WRITE_NONCUL_NUM += 1
					DUP_SAKI_targetindex = np.where(DUP_SAKI == RENEW_EXCHANGE[3])[0][-1]
					writer.writerow([DUP_SAKI[DUP_SAKI_targetindex][0], DUP_SAKI[DUP_SAKI_targetindex][1], DUP_SAKI[DUP_SAKI_targetindex][2],DUP_MOTO[0][3], DUP_MOTO[0][4], "", ""])
					DUP_MOTO_WRITE_CUL_NUM += 1
				# 耕作農地数のチェック
				if DUP_MOTO_READ_CUL_NUM != (DUP_MOTO_WRITE_CUL_NUM):
					print("DUP_MOTO_READ_CUL_NUM != DUP_MOTO_WRITE_CUL_NUM")
					print("syoricase:" + str(syoricase))
					print("samefarmcheck:" + str(samefarmcheck))
					sys.exit()
				# DUP_SAKI(=DUP_MOTO_orig)情報の更新
				with open('csv/farmersdata/' + hostname + str(RENEW_EXCHANGE[2]) + '.csv', 'w', encoding='shift_jis') as f:
					writer = csv.writer(f)
					for gyou in DUP_SAKI:
						if np.all(gyou != "none"):
							if gyou[0] == RENEW_EXCHANGE[3]:
								writer.writerow([str(gyou[0]), str(gyou[1]), str(gyou[2]), str(gyou[3]), str(gyou[4]), "none",str(EXCHANGE_COUNT)])
								DUP_SAKI_WRITE_NONCUL_NUM += 1
							else:
								writer.writerow([str(gyou[0]), str(gyou[1]), str(gyou[2]), str(gyou[3]), str(gyou[4]), "", ""])
								DUP_SAKI_WRITE_CUL_NUM += 1
						else:
							writer.writerow([str(gyou[0]), str(gyou[1]), str(gyou[2]), str(gyou[3]), str(gyou[4]), str(gyou[5]),str(gyou[6])])
							DUP_SAKI_WRITE_NONCUL_NUM += 1
					DUP_MOTO_targetindex = np.where(DUP_MOTO == RENEW_EXCHANGE[1])[0][-1]
					writer.writerow([DUP_MOTO[DUP_MOTO_targetindex][0], DUP_MOTO[DUP_MOTO_targetindex][1], DUP_MOTO[DUP_MOTO_targetindex][2],DUP_SAKI[0][3], DUP_SAKI[0][4], "", ""])
					DUP_SAKI_WRITE_CUL_NUM += 1
				# 耕作農地数のチェック
				if DUP_SAKI_READ_CUL_NUM[k[2]] != (DUP_SAKI_WRITE_CUL_NUM):
					print("DUP_SAKI_READ_CUL_NUM != DUP_SAKI_WRITE_CUL_NUM")
					print("syoricase:" + str(syoricase))
					print("samefarmcheck:" + str(samefarmcheck))
					sys.exit()
				if samefarmcheck == 2:
					# DUP_SAKI_orig情報の更新
					with open('csv/farmersdata/' + hostname + str(TARGET_EXCHANGE[3]) + '.csv', 'w',encoding='shift_jis') as f:
						writer = csv.writer(f)
						for gyou in DUP_SAKI_orig:
							writer.writerow([str(gyou[0]), str(gyou[1]), str(gyou[2]), str(gyou[3]), str(gyou[4]), str(gyou[5]),str(gyou[6])])
							# 耕作農地数等のカウント
							if all(youso != "none" for youso in gyou):
								DUP_SAKI_orig_WRITE_CUL_NUM += 1
							else:
								DUP_SAKI_orig_WRITE_NONCUL_NUM += 1
					# 耕作農地数のチェック
					if DUP_SAKI_orig_READ_CUL_NUM != (DUP_SAKI_orig_WRITE_CUL_NUM):
						print("DUP_SAKI_orig_READ_CUL_NUM != DUP_SAKI_orig_WRITE_CUL_NUM")
						print("syoricase:" + str(syoricase))
						print("samefarmcheck:" + str(samefarmcheck))
			elif syoricase == 4:
				# DUP_MOTO(=DUP_SAKI_orig)情報の更新
				with open('csv/farmersdata/' + hostname + str(RENEW_EXCHANGE[0]) + '.csv', 'w', encoding='shift_jis') as f:
					writer = csv.writer(f)
					for gyou in DUP_MOTO:
						if np.all(gyou != "none"):
							if gyou[0] == RENEW_EXCHANGE[1]:
								writer.writerow([str(gyou[0]), str(gyou[1]), str(gyou[2]), str(gyou[3]), str(gyou[4]), "none",str(EXCHANGE_COUNT)])
							else:
								writer.writerow([str(gyou[0]), str(gyou[1]), str(gyou[2]), str(gyou[3]), str(gyou[4]), "", ""])
						else:
							writer.writerow([str(gyou[0]), str(gyou[1]), str(gyou[2]), str(gyou[3]), str(gyou[4]), str(gyou[5]),str(gyou[6])])
					DUP_SAKI_targetindex = np.where(DUP_MOTO == RENEW_EXCHANGE[1])[0][-1]
					writer.writerow([DUP_SAKI[DUP_SAKI_targetindex][0], DUP_SAKI[DUP_SAKI_targetindex][1],DUP_SAKI[DUP_SAKI_targetindex][2], DUP_MOTO[0][3],DUP_MOTO[0][4], "", ""])
				# DUP_SAKI情報の更新
				with open('csv/farmersdata/' + hostname + str(RENEW_EXCHANGE[2]) + '.csv', 'w', encoding='shift_jis') as f:
					writer = csv.writer(f)
					for gyou in DUP_SAKI:
						if np.all(gyou != "none"):
							if gyou[0] == RENEW_EXCHANGE[3]:
								writer.writerow([str(gyou[0]), str(gyou[1]), str(gyou[2]), str(gyou[3]), str(gyou[4]), "none",str(EXCHANGE_COUNT)])
							else:
								writer.writerow([str(gyou[0]), str(gyou[1]), str(gyou[2]), str(gyou[3]), str(gyou[4]), "", ""])
						else:
							writer.writerow([str(gyou[0]), str(gyou[1]), str(gyou[2]), str(gyou[3]), str(gyou[4]), str(gyou[5]),str(gyou[6])])
					DUP_MOTO_targetindex = np.where(DUP_MOTO == RENEW_EXCHANGE[1])[0][-1]
					writer.writerow([DUP_MOTO[DUP_MOTO_targetindex][0], DUP_MOTO[DUP_MOTO_targetindex][1], DUP_MOTO[DUP_MOTO_targetindex][2],DUP_SAKI[0][3], DUP_SAKI[0][4], "", ""])
				if samefarmcheck == 0:
					# DUP_MOTO_orig情報の更新
					with open('csv/farmersdata/' + hostname + str(TARGET_EXCHANGE[1]) + '.csv', 'w',encoding='shift_jis') as f:
						writer = csv.writer(f)
						for gyou in DUP_MOTO_orig:
							writer.writerow([str(gyou[0]), str(gyou[1]), str(gyou[2]), str(gyou[3]), str(gyou[4]), str(gyou[5]),str(gyou[6])])
			# id_duplication_farmerの更新
			hoge_index = id_duplication_farmer[RENEW_EXCHANGE[1]].index(RENEW_EXCHANGE[2])
			id_duplication_farmer[RENEW_EXCHANGE[1]][hoge_index] = RENEW_EXCHANGE[0]			#
			id_duplication_farmer[RENEW_EXCHANGE[1]][0] = RENEW_EXCHANGE[2]						#

			#if id_duplication_farmer[RENEW_EXCHANGE[3]]  RENEW_EXCHANGE[0]:
			if True in [i in RENEW_EXCHANGE[0] for i in id_duplication_farmer[RENEW_EXCHANGE[3]]]:
				hoge_index = id_duplication_farmer[RENEW_EXCHANGE[3]].index(RENEW_EXCHANGE[0])
				id_duplication_farmer[RENEW_EXCHANGE[3]][hoge_index] = RENEW_EXCHANGE[2]  #
			else:
				id_duplication_farmer[RENEW_EXCHANGE[3]].append(RENEW_EXCHANGE[2])
			id_duplication_farmer[RENEW_EXCHANGE[3]][0] = RENEW_EXCHANGE[0]						#

			#PADDY_EXCHANGE_LISTの更新（共通）
			with open('csv/farmersdata/' + hostname + 'PADDY_EXCHANGE_LIST.csv', 'w', encoding='shift_jis') as f:
				writer = csv.writer(f)
				if PADDY_EXCHANGE_LIST.ndim > 1:
					for gyou in PADDY_EXCHANGE_LIST:
						writer.writerow([str(gyou[0]), str(gyou[1]), str(gyou[2]), str(gyou[3]), str(gyou[4])])
				else:
					writer.writerow([str(PADDY_EXCHANGE_LIST[0]),str(PADDY_EXCHANGE_LIST[1]),str(PADDY_EXCHANGE_LIST[2]),str(PADDY_EXCHANGE_LIST[3]),str(PADDY_EXCHANGE_LIST[4])])
			EXCHANGE_COUNT += 1
			continue
	# mysqlの更新
	updateid = ""
	updatefarmer = ""
	updatezyuusinnLatitude = ""
	updatezyuusinnlongitude = ""
	# updateexchangerecord = ""
	for mykey, myvalue in DUP_MYSQL_UPDATE.items():
		updateid += str(mykey) + ","  # id
		updatefarmer += "'" + str(myvalue[0]) + "',"  # farmer
		updatezyuusinnLatitude += str(myvalue[2]) + ","  # zyuusinnLatitude
		updatezyuusinnlongitude += str(myvalue[1]) + ","  # zyuusinnlongitude
	# updateexchangerecord = join(fish[27])
	# 文字列の最後の「,」を削除し、dbを更新する
	if updateid != "":
		updateid = updateid[:-1]
		updatefarmer = updatefarmer[:-1]
		updatezyuusinnLatitude = updatezyuusinnLatitude[:-1]
		updatezyuusinnlongitude = updatezyuusinnlongitude[:-1]
		t7.massinputsql3(updateid, updatefarmer, updatezyuusinnLatitude, updatezyuusinnlongitude)

	sys.exit()

def paddydemandlist_update(RENEW_EXCHANGE,TARGET_EXCHANGE,EXCHANGE_CASE):		#TARGET_EXCHANGE [0]:交換番号,[1][0]:MOTOのfarmer,[1][1]:MOTOのid,[2][0]:SAKIのfarmer,[2][1]:SAKIのid,EXCHANGE_CASE=0:MOTOの場合,1:SAKIの場合
	global paddydemandlist
	global PADDY_EXCHANGE_LIST
	global MOTO
	global SAKI
	
	#MOTOの場合（このケースを検証すること。また、for文の中も再考すること）
	if EXCHANGE_CASE == 0:
		BEFORE_FARMER_ID = TARGET_EXCHANGE[2]
		AFTER_FARMER_ID = TARGET_EXCHANGE[1]
	#SAKIの場合（farmerが変更にならないため不要なはず）
	elif EXCHANGE_CASE == 1:
		#return
		#FARMER_ID_1 = TARGET_EXCHANGE[1]
		FARMER_ID_2 = TARGET_EXCHANGE[2]
		FARMER_ID_3 = RENEW_EXCHANGE[2]
	#paddydemandlistの更新
	for k,gyou in enumerate(paddydemandlist):
		for l,retu in enumerate(gyou):
			if l == 0:
				continue
			#paddydemandlistの元々MOTOのidだったものの更新
			if retu[0] == FARMER_ID_2[1]:
				paddydemandlist[k][l][1] = FARMER_ID_3[0] #交換先のfarmerを代入				入れるidが正しいか、あとで検証すること
			#paddydemandlistの元々SAKIのidだったものの更新
			elif retu[0] == FARMER_ID_3[1]:
				paddydemandlist[k][l][1] = FARMER_ID_2[0] #交換元のfarmerを代入



farmlandoptimization4()

