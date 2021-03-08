import matplotlib.pyplot as plt
from matplotlib import rcParams
import pandas as pd
import requests
from bs4 import BeautifulSoup
import datetime


def Make_Schedule():
    print("時間表を取得中...")
    # get url
    load_url = "http://pso2.jp/players/boost/"
    html = requests.get(load_url)
    soup = BeautifulSoup(html.content,"html.parser")
    title = soup.find("li",class_="pager--date").text
    rcParams['font.family'] = 'sans-serif'
    rcParams['font.sans-serif'] = ['Hiragino Maru Gothic Pro', 'Yu Gothic', 'Meirio', 'Takao', 'IPAexGothic', 'IPAPGothic', 'Noto Sans CJK JP']

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
    #dt_now = datetime.date(2021,3,7)
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

    print("画像生成中...")
    print("しばらくお待ちください...")
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
    tb.set_fontsize(300)
    plt.subplots_adjust(left=0.01, right=0.99, bottom=0.01, top=0.9)
    plt.savefig("emergency.png",format="png",dpi=100)

    
