import requests     
from bs4 import BeautifulSoup
import pandas
import re
from datetime import datetime 

from datetime import datetime 

records=[]


def dated(date):
    date=date.lower()
    if('min' in date or 'hours' in date or 'ago' in date):
        date=datetime.today().strftime('%Y-%m-%d')
        
    tm=re.findall('.[0-9][.|:][0-9].', date)
        
    if tm:
        for i in tm:
            date=date.replace(i,'')
        
    a = ['pm et','am et','thurs','friday','fri',',','wed','tue','thu','mon','monday','tuesday','wednesday','thursday','saturday','sunday','sat','sun','bst','day','   ','  ',':','-','rs s','rs','nes','th','am','pm','updated', 'published','gmt' ]
    dlist=list(filter(lambda x:  x in date, a))
    for i in dlist:
        date=date.replace(i, '').strip()
    print(date)
    
    monthsShort="jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec"
    monthsLong="january|february|march|april|may|june|july|august|september|october|november|december"
    months_s="("+monthsShort+")"
    months_l= "("+monthsLong+")"
    separators = " "
    days = "(\d{2}|\d{1})"
    years = "\d{4}"
    y="201[0-9]"
    m="[0-9][0-9]"
    s=" / "
    
    
    regex1 = months_s + separators + days+ separators+ years
    regex2 = months_l + separators + days+ separators+ years
    regex3 = days + separators + months_s +separators +years
    regex4 = days + separators + months_l +separators +years
    
    regex5 = y  +m +days
    regex6 = y + m +days
    regex7 = days+s+m+s+y

    
    
    r1=re.match(regex1,date)
    r2 =re.match(regex2,date)
    r3 =re.match(regex3,date)
    r4 =re.match(regex4,date)
    r5 =re.match(regex5,date)
    r6 =re.match(regex6,date)
    r7 =re.match(regex7,date)
    
    if r1:
        print(r1)
        d = datetime.strptime(date, "%b %d %Y")
        date = d.strftime("%d-%m-%Y")
        print(date)
     
    elif r2: 
        print(r2)
        d = datetime.strptime(date, "%B %d %Y")
        date = d.strftime("%d-%m-%Y")
        print(date)
    
    elif r3: 
        print(r3)
        d = datetime.strptime(date, "%d %b %Y")
        date = d.strftime("%d-%m-%Y")
        print(date) 
        
    elif r4:
        print(r4)
        d = datetime.strptime(date, "%d %B %Y")
        date = d.strftime("%d-%m-%Y")
        print(date)
        
    elif r5: 
        print(r5)
        d = datetime.strptime(date, "%Y%m%d")
        date = d.strftime("%d-%m-%Y")
        print(date) 
        
    elif r6:
        print(r6)
        d = datetime.strptime(date, "%Y%m%d")
        date = d.strftime("%d-%m-%Y")
        print(date)

    elif r7:
        print("r7:   ",r7)
        d = datetime.strptime(date, "%d %m %Y")
        date = d.strftime("%d-%m-%Y")
        print(date)
    
    else:
        date=date
        print(date)
    return date


def cnbc_headline(url="https://www.cnbc.com"):
    with requests.Session() as se:
        se.encoding = "UTF-8"
        res = se.get(url)
        text = res.text
    soup = BeautifulSoup(text,"lxml")
    news_headline = soup.find_all("div",class_="headline")
    news_ = [(url + div.a.get("href")) for div in news_headline if div.a]
    print(news_)
    for i in news_:
        if 'https://www.cnbc.com/2018/' in i:
            r = requests.get(i)
            c = r.content
            soup = BeautifulSoup(c,"html.parser")
            topic=soup.find("h1",{"class":"title"}).text.replace("\r","").replace("\n","")
            context=' '
            for content_tag in soup.find_all("p"):
                context = context+content_tag.text.replace("\r","").replace("\n","")
            context= context[18:-458]
            country ='United States'
            url2='https://www.cnbc.com/' 
            genre=''
            news='CNBC'
            date= soup.find("time",{"class":"datestamp"}).text.replace("\r","").replace("\n","")
            print(date)
            date= dated(date)
            records.append((news,url2,country,topic,i,genre,date,context))
    df=pandas.DataFrame(records)    
    df.to_csv("fyp2.csv",mode="a",header=False)

#cnbc_headline()



def Remove(duplicate): 
    final_list = [] 
    for num in duplicate: 
        if num not in final_list: 
            final_list.append(num) 
    return final_list



def cnbc_politics():
    
    temp=[]
    links=[]
    records=[]


    url=['https://www.cnbc.com/politics/']

    

    for j in url:
        for i in range(15,18):
            url=j+'?page='+str(i)
            with requests.Session() as se:
                se.encoding = "UTF-8"
                res = se.get(url) #'https://sports.ndtv.com/cricket/news'
                text = res.text
                
            soup = BeautifulSoup(text,"lxml")               # class for buisness 'ins_left_rhs'
            new = soup.find("ul",class_='stories_assetlist')   # class for cricket "post-list list-type-1"
            print(new)
            news_headline = new.find_all("a")
            
            temp.extend(news_headline)


    for link in temp:
        if link.get('href').startswith('/'):
            linkin='https://www.cnbc.com'+link.get("href")
            links.append(linkin)
        else:
            links.append(link.get("href"))
    links=Remove(links)
    
    for i in links:

        if 'https://www.cnbc.com/2019/' in i:
            r = requests.get(i)
            c = r.content
            soup = BeautifulSoup(c,"html.parser")
            topic=soup.find("h1",{"class":"title"}).text.replace("\r","").replace("\n","")
            print(topic)
            context=' '
            for content_tag in soup.find_all("p"):
                context = context+content_tag.text.replace("\r","").replace("\n","")
            context= context[18:-458]
            country ='United States'
            url2='https://www.cnbc.com/' 
            genre='Politics'
            news='CNBC'
            date= soup.find("time",{"class":"datestamp"}).text.replace("\r","").replace("\n","")
            print(date)
            date= dated(date)
            records.append((news,url2,country,topic,i,genre,date,context))
            print('#####################################################################')
    df=pandas.DataFrame(records)    
    with open('fyp.csv', 'a',encoding="utf-8") as newFile:
        df.to_csv("fyp2.csv",mode="a", header=False)
    newFile.close()   
    
cnbc_politics()

def cnbc_buisness():
    
    temp=[]
    links=[]
    records=[]


    url=['https://www.cnbc.com/business/']

    

    for j in url:
        for i in range(15,18):
            url=j+'?page='+str(i)
            with requests.Session() as se:
                se.encoding = "UTF-8"
                res = se.get(url) #'https://sports.ndtv.com/cricket/news'
                text = res.text
                
            soup = BeautifulSoup(text,"lxml")               # class for buisness 'ins_left_rhs'
            new = soup.find("ul",class_='stories_assetlist')   # class for cricket "post-list list-type-1"
            print(new)
            news_headline = new.find_all("a")
            
            temp.extend(news_headline)


    for link in temp:
        if link.get('href').startswith('/'):
            linkin='https://www.cnbc.com'+link.get("href")
            links.append(linkin)
        else:
            links.append(link.get("href"))
    links=Remove(links)
    
    for i in links:

        if 'https://www.cnbc.com/2019/' in i:
            r = requests.get(i)
            c = r.content
            soup = BeautifulSoup(c,"html.parser")
            topic=soup.find("h1",{"class":"title"}).text.replace("\r","").replace("\n","")
            print(topic)
            context=' '
            for content_tag in soup.find_all("p"):
                context = context+content_tag.text.replace("\r","").replace("\n","")
            context= context[18:-458]
            country ='United States'
            url2='https://www.cnbc.com/' 
            genre='Business'
            news='CNBC'
            date= soup.find("time",{"class":"datestamp"}).text.replace("\r","").replace("\n","")
            print(date)
            date= dated(date)
            records.append((news,url2,country,topic,i,genre,date,context))
            print('#####################################################################')
    df=pandas.DataFrame(records)    
    with open('fyp.csv', 'a',encoding="utf-8") as newFile:
        df.to_csv("fyp2.csv",mode="a", header=False)
    newFile.close()   
    
cnbc_buisness()






