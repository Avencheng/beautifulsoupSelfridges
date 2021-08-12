from selenium import webdriver
import pandas as pd
import requests
from bs4 import BeautifulSoup 
import shutil
import time
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import Label
import json
from datetime import date
import cv2
import os
import io  
from PIL import Image, ImageTk  

def gift(*args):#回覆給Line
    def lineNotify(token, msg, picURI):
        url = "https://notify-api.line.me/api/notify"
        headers = {
            "Authorization": "Bearer " +"d9CTh3gMNDc0HHFvSSGuySLWJ2BdkuRl4PteuH1C8iS"}
    
        payload = {'message': msg}
        files = {'imageFile': open(picURI, 'rb')}
        r = requests.post(url, headers = headers, params = payload, files = files)
        return r.status_code
    
    token = '你的權杖內容'
    need_things=variable2.get()
    need_things=str(need_things)
    num=need_things.split('.')[0]
    msg=need_things.split('.')[1]
    picURI='/Users/user/Downloads/pic{}.jpg'.format(num)
       
    lineNotify(token, msg, picURI)
    
def find(*args):
    for d in range(1,61):
        fileTest=r"\Users\user\Downloads\pic{}.jpg".format(d)
        
        try:
            os.remove(fileTest)
        except OSError as e:
            continue
        else:
            continue
    x= combo1.get() 
    y= combo2.get()
    x=str(x)
    y=str(y)
    if x == sex[0]:
        url_1= "mens/"
        if y == boys[0]:
            url_2 = "bags/backpacks/"
        elif y == boys[1]:
            url_2 = "accessories/wallets/"
        elif y== boys[2]:
            url_2 = "bags/briefcases/"
        
    else:
        url_1 = "womens/"
        if y == womens[0]:
            url_2 = "bags/shoulder-bags/"
        elif y == womens[1]:
            url_2 = "bags/tote-bags/"
        elif y == womens[2]:
            url_2 = "bags/clutch-bags/"
            
    url = first_url + url_1 + url_2
    browser = webdriver.Chrome(executable_path='./chromedriver')
    browser.minimize_window()
    browser.get(url) 
    '''讀取網站'''
    time.sleep(5)
    '''讀取網頁原始碼'''
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    '''關閉網站'''
    browser.close()
    
    '''商品名稱'''
    numb=1
    names = soup.select(".c-prod-card__cta-box-description")# . =class
    to_name=[]
    for i in names:
        to_name.append(str(numb)+"."+i.text)
        numb+=1

    '''商品價格'''
    prices=soup.select(".c-prod-card__cta-box-price")
    to_price=[]
    for j in prices:
        j = str(j)
        j = (j.split("$")[1]).split("<")[0]
        to_price.append(j)
        
        '''商品圖片'''
    pics = soup.select("img")
    sort=[]
    for i in pics:
        if str("包") in str(i) or str("夹") in str(i) or str("袋") in str(i):
            sort.append(i)      
    ww=[] #圖片網址
    for src in sort:
        if str("data-src") in str(src):
            ww.append("https:"+str(src["data-src"]))
        elif str("src") in str(src):
            ww.append("https:"+str(src["src"]))
    '''抓圖片'''
    n=1
    for x in ww:
        fname= "pic" + str(n) +".jpg"
        res2 = requests.get(x,stream = True)
        time.sleep(1)
        f = open(fname,'wb')
        shutil.copyfileobj(res2.raw, f)
        print(n)
        n+=1
        if n==12:
            break
        f.close()
        del res2
        
        total=[]
    for k in range(len(to_name)):
        msg=str(str(to_name[k])+"$"+str(to_price[k]))
        total.append(msg)
        
    def showpic(*args):
        x=variable2.get()
        x=str(x)
        print(x)
        num=str(x).split('.')[0]
        ioc='pic{}.jpg'.format(num)
        print(ioc)
        img=cv2.imread(ioc)
        cv2.imshow('image',img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    option2=tk.OptionMenu(root, variable2, *total, command=showpic)
    option2.config(width=40, font=(20))
    option2.place(x=200,y=250)
    
    btn_send = Button(root, text='傳到 Line',command=gift)
    btn_send.config(width=10, font=(20))
    btn_send.place(x=200,y=300)
 

# def cmd1():
#     print(combo1.current(), combo1.get(), combo2.current())
#     if combo1.current()==1:
#         combo2['value']=['雙肩包','錢夾','公文包']
#     elif combo1.current()==2:
#         combo2['value']=['單肩包','托特包','手拿包']   
#     combo2.current(0)
    
#scaled logo
def resize(w, h, w_box, h_box, pil_image):  
  ''' 
  resize a pil_image object so it will fit into 
  a box of size w_box times h_box, but retain aspect ratio 
  對一個pil_image對象進行縮放，讓它在一個矩形框內，還能保持比例 
  '''  
  f1 = 1.0*w_box/w # 1.0 forces float division in Python2  
  f2 = 1.0*h_box/h  
  factor = min([f1, f2])  
  #print(f1, f2, factor) # test  
  # use best down-sizing filter  
  width = int(w*factor)  
  height = int(h*factor)  
  return pil_image.resize((width, height), Image.ANTIALIAS)  


first_url="https://www.selfridges.com/TW/zh/cat/"
root = tk.Tk() 
root.geometry('600x450')

root.title("歡迎使用Selfrides包袋查詢系統")
root.configure(background = 'yellow')

#scaled logo
w_box =200
h_box =80

pil_image = Image.open(r'/Users/user/Downloads/logo.jpg')  
w, h = pil_image.size  
pil_image_resized = resize(w, h, w_box, h_box, pil_image)  
tk_image = ImageTk.PhotoImage(pil_image_resized)  
label = tk.Label(root, image=tk_image, width=w_box, height=h_box)  
label.place(x=190,y=0)

sex=["男包","女包"]
boys=['雙肩包','錢夾','公文包']
womens=['單肩包','托特包','手拿包']
pagges=['1','2','3','4','5']

tk.Label(root, text = "男包/女包:",bg='yellow').place(x=120, y=103)
combo1 = ttk.Combobox(root, values=["男包","女包"], state="readonly")
combo1.current(0)
combo1.place(x=200,y=100)

tk.Label(root, text = "類型:",bg='yellow').place(x=120, y=150)
combo2 = ttk.Combobox(root,values=['雙肩包','錢夾','公文包'],state="readonly")
combo2.current(0)
combo2.place(x=200,y=150)

tk.Label(root, text = "頁面:",bg='yellow').place(x=120, y=200)
combo3 = ttk.Combobox(root,values=['1','2','3','4','5'],state="readonly")
combo3.current(0)
combo3.place(x=200,y=200)

variable2 = tk.StringVar(root)

x=tk.Button(root,text="尋找",command = find)
x.place(x=410,y=203)


def on_select1(event):
    if combo1.current()==0:
        combo2['value']=['雙肩包','錢夾','公文包']
    elif combo1.current()==1:
        combo2['value']=['單肩包','托特包','手拿包']
    combo2.current(0)
    # print(combo1.get(),combo2.get())
combo1.bind('<<ComboboxSelected>>', on_select1)

def on_select2(event):
    print(combo1.get(),combo2.get())
combo2.bind('<<ComboboxSelected>>', on_select2)

btn_exit = Button(root, text="離開" ,command = root.destroy)
btn_exit.place(x=280,y=400)

root.mainloop()