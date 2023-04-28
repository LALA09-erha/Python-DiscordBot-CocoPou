from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import re
import datetime


# videos yt
def api(user):
    channel = f"https://www.youtube.com/@{user}"
    html = requests.get(channel + "/videos").text
    url = "https://www.youtube.com/watch?v=" + re.search('(?<="videoId":").*?(?=")', html).group()
    return url

# stream yt
def getstream(user):
    channel = f"https://www.youtube.com/@{user}"
    html = requests.get(channel + "/streams").text
    url = "https://www.youtube.com/watch?v=" + re.search('(?<="videoId":").*?(?=")', html).group()
    info = re.search('(?<={"label":").*?(?="})', html).group()
    return [url,info]

# short yt
def getshort(user):
    channel = f"https://www.youtube.com/@{user}"
    html = requests.get(channel + "/shorts").text
    url = "https://www.youtube.com/watch?v=" + re.search('(?<="videoId":").*?(?=")', html).group()
    info = re.search('(?<={"label":").*?(?="})', html).group()
    return [url,info]


# get title yt
def gettitle(user):
    channel = f"https://www.youtube.com/@{user}"

    html = requests.get(channel + "/videos").text
    info = re.search('(?<={"label":").*?(?="})', html).group()
    # url = "https://www.youtube.com/watch?v=" + re.search('(?<="videoId":").*?(?=")', html).group()

    return info



def notfound(user):
    channel = f"https://www.youtube.com/@{user}"
    info = ''
    html = requests.get(channel + "/videos").text
    try:
        info = re.search('(?<={"label":").*?(?="})', html).group()
    except:
        return False
        
    
    print(info)

    if info == '':
        return False
    else:
        return True
    
# get jadwal bola 
def jadwalbola():
    # using now() to get current time
    ligas = ['liga-inggris' , 'liga-italia' , 'liga-spanyol' , 'liga-jermal' , 'liga-indonesia' , 'liga-champions']
    current_time = datetime.datetime.now()
    if(len(str(current_time.month)) == 1):
        date = str(current_time.day+1) +"/0" +str(current_time.month)+"/"+str(current_time.year)[2:4]
    else:
        date = str(current_time.day+1) +"/" +str(current_time.month)+"/"+str(current_time.year)[2:4]

    data_all = []
    for liga in ligas:
        # inisialisasi data
        wiki_link = "https://sport.detik.com/sepakbola/jadwal/" + liga
        
        # html = urlopen(wiki_link).read()
        html = requests.get(wiki_link).text
        soup = BeautifulSoup(html, 'html.parser')
        data = []
        # proses crawling
        for i in soup.findAll("ul", {"class" : "list_schedule"}):
            for j in i.findAll("li"):
                temp = []
                if(date in j.text):
                    for foto in j.findAll('img'):
                        if(j.find("div" , {"class" : "time"}).text.replace("\n"," ") not in temp):
                            temp.append(j.find("div" , {"class" : "time"}).text.replace("\n"," "))
                        temp.append([foto.parent.text.replace("\n",""),foto.get('src')])
                    data.append(temp)

        data_all.append(data)
    
    datanew = {}
    intr = 1
    for i in data_all:
        if(len(i) != 0):
            for tgl in i:
                fix = {
                    "jadwal" : tgl[0],
                    "home" : {
                        "team" : tgl[1][0],
                        "pict" : tgl[1][1]
                    },
                    "away" : {
                        "team" :tgl[2][0],
                        "pict" : tgl[2][1]
                    }
                    }

                datanew[str(intr)] = fix
                intr+=1

    return datanew