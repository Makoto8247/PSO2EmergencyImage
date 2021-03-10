import matplotlib.pyplot as plt
from matplotlib import rcParams
import pandas as pd
import requests
from bs4 import BeautifulSoup
import datetime
import os
import pickle
from matplotlib.font_manager import FontProperties

# Linux
font_path = "/usr/share/fonts/truetype/migmix/migmix-1p-regular.ttf"
font_prop = FontProperties(fname=font_path)
rcParams["font.family"] = font_prop.get_name()
# Windows
#rcParams['font.family'] = 'sans-serif'
#rcParams['font.sans-serif'] = ['Hiragino Maru Gothic Pro', 'Yu Gothic', 'Meirio', 'Takao', 'IPAexGothic', 'IPAPGothic', 'VL PGothic', 'Noto Sans CJK JP']
font_size = 50

def int_to_day():
    day = datetime.date.today().weekday()
    if(day == 0):
        return "月"
    elif(day == 1):
        return "火"
    elif(day == 2):
        return "水"
    elif(day == 3):
        return "木"
    elif(day == 4):
        return "金"
    elif(day == 5):
        return "土"
    elif(day == 6):
        return "日"
    else:
        return 0

def Day_Img(id_time,id_day,dt_now):
    day = {}
    youbi = int_to_day() + str(dt_now.day)
    day[None] = id_time
    day[youbi] = id_day
    df = pd.DataFrame(day)

    fig, ax = plt.subplots(figsize=(10, 30))

    ax.axis('off')
    ax.axis('tight')

    tb = ax.table(cellText=df.values,
                  colLabels=df.columns,
                  bbox=[0, 0, 1, 1],
                  )
    # set color
    for i in range(49):
        if(dt_now.day == 5):
            tb[i,1].set_facecolor('#CCFFFF')
        if(dt_now.day == 6):
            tb[i,1].set_facecolor('#FFBEDA')
    for i in range(2):
        tb[0,i].set_facecolor('#000000')
        tb[0,i].set_text_props(color='w')
    if(dt_now.day == 5):
        tb[0,1].set_text_props(color='b')
    if(dt_now.day == 6):
        tb[0,1].set_text_props(color='r')
    
    for i in range(49):
        for j in range(2):
            if(dt_now.day == 5):
                if i % 2 == 1:
                    tb[i,j].set_facecolor('#B1DDDD')
            if(dt_now.day == 6):
                if i % 2 == 1:
                    tb[i,j].set_facecolor('#DDA5BD')
            else:
                if i % 2 == 1:
                    tb[i,j].set_facecolor('#DDDDDD')
    print(day)
    tb.set_fontsize(font_size)
    plt.subplots_adjust(left=0.01, right=0.99, bottom=0.01, top=0.99)
    plt.savefig("day.png",format="png",dpi=108)

def Make_Schedule():
    print("時間表を取得中...")
    # get url
    load_url = "http://pso2.jp/players/boost/"
    html = requests.get(load_url)
    soup = BeautifulSoup(html.content,"html.parser")
    title = soup.find("li",class_="pager--date").text
    
    # get week
    week = []
    wk = soup.find("tr",class_="eventTable--event-week")

    for i in wk.find_all("th"):
        week.append(i.text)
    

    # data
    data = {
        None : [], # time
    }
    for i in week:
        data.update([(i,[])])

    sum = 0
    for i in range(24):
        for j in range(2):
            sum += 1
            data[None].append(str(i).zfill(2) + ":" + str(j*30).zfill(2))
    
    for i in range(sum):
        for j in week:
            data[j].append("")

    # emergency
    cgvalue = 0
    for time in range(24):
        for minutes in range(2):
            date = "t"+str(time).zfill(2)+"m"+str(minutes*30).zfill(2)
            day = soup.find_all("tr",class_=date)
            for i in day:
                now_day = 0
                for j in i.find_all("td"):
                    if j.find("div",class_="event-emergency") == None:
                        data[week[now_day]][cgvalue] = ""
                    else:
                        data[week[now_day]][cgvalue] = j.find("span").text
                    now_day += 1
            cgvalue += 1
    
    # Bal Lodos Day
    dt_base = datetime.date(2021,3,7)
    dt_now = datetime.date.today()
    bal = []
    if dt_base <= dt_now:
        wk_day = []
        for i in week:
            num = 0
            for j in i:
                if j.isdigit():
                    num *= 10
                    num += int(j)
            wk_day.append(num)
        for i in wk_day:
            dt = datetime.date(dt_now.year,dt_now.month,i)
            dt -= dt_base
            if dt.days % 93 == 0:
                bal.append(i)
            elif dt.days % 6 == 0:
                bal.append(i)
    if len(bal) > 0:
        id_list_pass_bal = os.path.abspath("./bal_day.pkl")
        # リスト保存
        with open(id_list_pass_bal,mode='wb') as f:
            pickle.dump(bal,f)

    print("画像生成中...")
    print("しばらくお待ちください...")
    # day img
    youbi = int_to_day() + str(dt_now.day)
    Day_Img(data[None],data[youbi],dt_now)
    # data show
    df = pd.DataFrame(data)

    fig, ax = plt.subplots(figsize=(20, 11))

    ax.axis('off')
    ax.axis('tight')

    tb = ax.table(cellText=df.values,
                  colLabels=df.columns,
                  bbox=[0, 0, 1, 1],
                  )
    # set color
    for i in range(49):
        tb[i,4].set_facecolor('#CCFFFF')
        tb[i,5].set_facecolor('#FFBEDA')
    for i in range(9):
        if i == 4 or i == 5:
            continue
        tb[0,i].set_facecolor('#000000')
        tb[0,i].set_text_props(color='w')
    tb[0,4].set_text_props(color='b')
    tb[0,5].set_text_props(color='r')
    
    for i in range(49):
        for j in range(9):
            if i%2 == 1:
                if j == 4:
                    tb[i,j].set_facecolor('#B1DDDD')
                elif j == 5:
                    tb[i,j].set_facecolor('#DDA5BD')
                else:
                    tb[i,j].set_facecolor('#DDDDDD')
    # Bal Day
    for i in bal:
        for j in range(8):
            if i == wk_day[j]:
                tb[0,j+1].set_facecolor('#F0E68C')
                tb[0,j+1].set_text_props(color='black')
                break
                

    plt.title(title,fontsize = 50)
    tb.set_fontsize(font_size)
    plt.subplots_adjust(left=0.01, right=0.99, bottom=0.01, top=0.9)
    plt.savefig("emergency.png",format="png",dpi=100)
    print("画像生成完了しました。")
