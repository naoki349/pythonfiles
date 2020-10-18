#-*- coding:utf-8 -*-
import tkinter as tk
import tkinter.ttk as ttk
from selenium import webdriver
import time
import test10_newalgorithm as t10
import test2 as t2
import test8 as t8
import test7 as t7

global iconinfo

def press_button1():
    #val_en = en.get()
    farmers = txt1_1.get(),txt1_2.get(),txt1_3.get(),txt1_4.get(),txt1_5.get()
    #label1["text"] = val_en
    t8.farmerplot(farmers)
    print("処理が終わりました")
    browser.switch_to_window(allHandles[0])
    browser.refresh()
    browser.switch_to_window(allHandles[1])
    browser.refresh()

def press_button2():
    #label2["text"] = hoge
    areaname = []
    iconinfo = {}
    #val_en = en.get()
    #val_en = txt1
    print(txt1.get())
    areaname.append(txt1.get())
    iconinfo = t7.mapplotfarmers7(areaname,iconinfo)
    t7.mapplotfarmers7(areaname,iconinfo)
    print("処理が終わりました")
    browser.switch_to_window(allHandles[0])
    browser.refresh()
    browser.switch_to_window(allHandles[1])
    browser.refresh()

def press_button3():
    global iconinfo

    EXCHANGE_DATA_DIC = {}
    #if len(iconinfo) == 0: iconinfo = {}
    id1 = [txt1_pre.get(), txt1_post.get()]
    id2 = [txt2_pre.get(), txt2_post.get()]
    id3 = [txt3_pre.get(), txt3_post.get()]
    id4 = [txt4_pre.get(), txt4_post.get()]
    id5 = [txt5_pre.get(), txt5_post.get()]

    EXCHANGE_ID =[id1,id2,id3,id4,id5]
    #重複を除く
    #EXCHANGE_ID = set(EXCHANGE_ID)
    EXCHANGE_ID = [a for a in EXCHANGE_ID if a != ['','']]
    #dbから、交換する農地の情報を入手する
    EXCHANGE_DATA = t7.farmlandinformation2(sum(EXCHANGE_ID,[]))
    for DATA in EXCHANGE_DATA:
        EXCHANGE_DATA_DIC[DATA[0]] = DATA[1:4]
    updateid = ""
    updatefarmer = ""
    updatezyuusinnLatitude = ""
    updatezyuusinnlongitude = ""

    for ID in EXCHANGE_ID:
        updateid += str(ID[0]) + "," +str(ID[1]) + ","# id
        updatefarmer += "'" + str(EXCHANGE_DATA_DIC[int(ID[1])][0]) + "', '" + str(EXCHANGE_DATA_DIC[int(ID[0])][0]) + "',"# farmer
        updatezyuusinnLatitude += str(EXCHANGE_DATA_DIC[int(ID[1])][1]) + "," + str(EXCHANGE_DATA_DIC[int(ID[0])][1]) + "," # zyuusinnLatitude緯度
        updatezyuusinnlongitude += str(EXCHANGE_DATA_DIC[int(ID[1])][2]) + "," + str(EXCHANGE_DATA_DIC[int(ID[0])][2]) + "," # zyuusinnlongitude経度
        # updateexchangerecord = join(fish[27])
        # print(fish[27])
        #updateexchangerecord += "'" + str(fish[27]) + "',"  # exchangerecord
        #hohoho[i][30] = 0
    # 文字列の最後の「,」を削除し、dbを更新する
    updateid = updateid[:-1]
    updatefarmer = updatefarmer[:-1]
    updatezyuusinnLatitude = updatezyuusinnLatitude[:-1]
    updatezyuusinnlongitude = updatezyuusinnlongitude[:-1]
    #updateexchangerecord = updateexchangerecord[:-1]
    #t7.massinputsql4(updateid, updatefarmer, updatezyuusinnLatitude, updatezyuusinnlongitude, updateexchangerecord)
    t7.massinputsql5(updateid, updatefarmer, updatezyuusinnLatitude, updatezyuusinnlongitude)
    #地図情報の更新
    iconinfo = {}
    iconinfo = t7.mapplotfarmers7([txt3_0.get(),], iconinfo)
    t7.mapplotfarmers7([txt3_0.get(),], iconinfo)

    #距離の計測
    SELECT_FARMER = updatefarmer.split(',')
    SELECT_FARMER_KAKOUGO = []
    #配列の文字列を整理
    for FARMER in SELECT_FARMER:
        hoge = FARMER
        hoge = hoge.replace("'","")
        hoge = hoge.replace(" ","")
        SELECT_FARMER_KAKOUGO.append(hoge)
    #重複をなくす
    SELECT_FARMER_KAKOUGO = set(SELECT_FARMER_KAKOUGO)

    SELECT_FARMER_DISTANCE = {}
    for FARMER in SELECT_FARMER_KAKOUGO:
        SELECT_FARMER_DISTANCE[FARMER] = t2.distance_to_center_of_gravity_eachfarmer(FARMER)

    #ブラウザの更新
    browser.switch_to_window(allHandles[0])
    browser.refresh()
    browser.switch_to_window(allHandles[1])
    browser.refresh()
    distance = []
    textbox3.delete('1.0','end')
    for i,FARMER in enumerate(SELECT_FARMER_KAKOUGO):
        #distance = SELECT_FARMER_DISTANCE[FARMER]
        textbox3.insert('1.0', "■" + str(FARMER) + "\n　変更前：" + str(round(SELECT_FARMER_DISTANCE[FARMER][0],2)) + "　変更後：" + str(round(SELECT_FARMER_DISTANCE[FARMER][1],2)) + "\n")
    print("処理が終わりました")

def press_button3_2():
    global iconinfo

    t2.exchange_reset()
    # 地図情報の更新
    iconinfo={}
    iconinfo = t7.mapplotfarmers7([txt3_0.get(), ], iconinfo)
    t7.mapplotfarmers7([txt3_0.get(), ], iconinfo)
    browser.switch_to_window(allHandles[0])
    browser.refresh()
    browser.switch_to_window(allHandles[1])
    browser.refresh()
    textbox3.delete('1.0','end')
def press_button4():
    browser.close()
    allHandles = browser.window_handles
    browser.switch_to_window(allHandles[0])
    browser.maximize_window()

#def chg_tab(event):
    #print(notebook.select())
iconinfo = {}

root = tk.Tk()
w = root.winfo_screenwidth()
#print(w)
h = root.winfo_screenheight()
#print(h)

browser = webdriver.Chrome()
browser.set_window_position(0,0)
browser.set_window_size(w/2,h)
#browser.maximize_window()
browser.get('file:///Users/onoderanaoki/Dropbox/農地プロジェクト/map_paddy.html')
#browser.execute_script("window.open('file:///Users/onoderanaoki/Dropbox/農地プロジェクト/map_paddy1.html',null)")

browser.execute_script("window.open('file:///Users/onoderanaoki/Dropbox/農地プロジェクト/map_paddy2.html',null, 'top=100+,left=720')")
allHandles = browser.window_handles
browser.switch_to_window(allHandles[1])
browser.set_window_position(w/2,0)
#browser.set_window_size(w/2,h)


root.attributes("-topmost", True)
root.geometry("400x620+" + str(w-300) + "+" + str(h-620))
root.title("コントローラー")

notebook = ttk.Notebook(root)

tab1 = tk.Frame(notebook)
tab2 = tk.Frame(notebook)
tab3 = tk.Frame(notebook)
notebook.add(tab1,text="耕作者検索")
notebook.add(tab2,text="大字検索")
notebook.add(tab3,text="交換の実行")
notebook.pack(expand=True,fill="both")

#tab1の設定
label1 = tk.Label(tab1,text="耕作者検索を行います")
label1.pack()

frame1_1 = tk.Frame(tab1)
frame1_1.pack()

txt1_1 = tk.Entry(frame1_1,width=35)
txt1_1.pack()
txt1_2 = tk.Entry(frame1_1,width=35)
txt1_2.pack()
txt1_3 = tk.Entry(frame1_1,width=35)
txt1_3.pack()
txt1_4 = tk.Entry(frame1_1,width=35)
txt1_4.pack()
txt1_5 = tk.Entry(frame1_1,width=35)
txt1_5.pack()

button1 = tk.Button(tab1,text="実行",command=press_button1)

#tab2の設定
label2 = tk.Label(tab2,text="大字検索を行います")
label2.pack()

frame2 = tk.Frame(tab2)
frame2.pack()
txt1 = tk.Entry(frame2,width=15)
txt1.pack()

button2 = tk.Button(tab2,text="実行",command=press_button2)

#tab3の設定
label3_1 = tk.Label(tab3,text="表示したい大字を入力してください")
label3_1.pack()

frame3_0 = tk.Frame(tab3)
frame3_0.pack()
txt3_0 = tk.Entry(frame3_0,width=15)
txt3_0.insert(0,"岩手県雫石町御明神")
txt3_0.pack()

label3_2 = tk.Label(tab3,text="交換を実行します")
label3_2.pack()

#button3 = tk.Button(tab3,text="1画面",command=press_button4)
#button3.pack()

frame3_1 = tk.Frame(tab3)
frame3_1.pack()
txt1_pre = tk.Entry(frame3_1,width=15)
txt1_pre.pack(side="left")
txt1_post = tk.Entry(frame3_1,width=15)
txt1_post.pack(side="right")

frame3_2 = tk.Frame(tab3)
frame3_2.pack()
txt2_pre = tk.Entry(frame3_2,width=15)
txt2_pre.pack(side="left")
txt2_post = tk.Entry(frame3_2,width=15)
txt2_post.pack(side="right")

frame3_3 = tk.Frame(tab3)
frame3_3.pack()
txt3_pre = tk.Entry(frame3_3,width=15)
txt3_pre.pack(side="left")
txt3_post = tk.Entry(frame3_3,width=15)
txt3_post.pack(side="right")

frame3_4 = tk.Frame(tab3)
frame3_4.pack()
txt4_pre = tk.Entry(frame3_4,width=15)
txt4_pre.pack(side="left")
txt4_post = tk.Entry(frame3_4,width=15)
txt4_post.pack(side="right")

frame3_5 = tk.Frame(tab3)
frame3_5.pack()
txt5_pre = tk.Entry(frame3_5,width=15)
txt5_pre.pack(side="left")
txt5_post = tk.Entry(frame3_5,width=15)
txt5_post.pack(side="right")

button3 = tk.Button(tab3,text="実行",command=press_button3)
button3.pack()

frame3_6 = tk.Frame(tab3)
frame3_6.pack()
textbox3 = tk.Text(frame3_6,height=20)
textbox3.insert('1.0',"※交換を実行すると、ここに交換前後の距離が表示されます。")
textbox3.pack()

label3_3 = tk.Label(tab3,text="交換をリセットします")
label3_3.pack()
button3_2 = tk.Button(tab3,text="リセット",command=press_button3_2)
button3_2.pack()

#[widget.pack(pady=10) for widget in (en,label1,button1,label2,button2,label3,button3,frame3_1,txt1_pre,txt1_post,txt2_pre,txt2_post,txt3_pre,txt3_post,txt4_pre,txt4_post,txt5_pre,txt5_post)]
[widget.pack(pady=10) for widget in (button1,label2,button2)]
tabids = notebook.tabs()


notebook.select(tabids[2])

root.mainloop()

time.sleep(60)
browser.quit()

