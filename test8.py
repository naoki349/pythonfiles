import test2 as t2 
import test7 as t7

def farmerplot(farmers):
	farmer_temp = ""
	for hoge in farmers:
		if hoge == '':
			break
		farmer_temp = farmer_temp + "'" + hoge + "',"
	farmerstr = "farmer in (" + farmer_temp[:-1] + ")"
	#farmerstr = "farmer in( '173369061884f46eff12f21a510bdcca' ,'5f68fc2d5ddc067b1807122cb6595ae7')"
	#noutinavi_addzyuusinnからデータを入手
	farmerinfo = t2.retrievefromdb4(farmerstr)
	#print(farmerinfo)
	iconinfo = {}
	iconinfo = t7.mapplotfarmers3(farmerinfo,iconinfo)
	#noutinavi_addzyuusinn2からデータを入手
	#farmerinfo = t2.retrievefromdb3(farmerstr)
	farmerinfo = t2.retrievefromdb8(farmerstr)
	#print(farmerinfo)
	iconinfo = t7.mapplotfarmers4(farmerinfo,iconinfo)
	

#farmerplot()