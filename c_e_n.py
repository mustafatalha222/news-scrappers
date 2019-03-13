#scmp(130+76+70+50+60), chinadaily(for loop), globaltimes(for loop) , c_e_n , chinatimes(for loop)
#guardian(68), express(175) ,wales(for loop) , bbc , 
#dailytimes(for loop), dawn(300), the news(99), tribune(for loop), 
#hindustan(360), indiatimes(185), indiatoday(for loop), the hindu(for loop), NDTV(for loop)


#nation hogaya ha isme nahi dala ,aur (uk ka 1 rah gaya ha bs)
import requests 
from bs4 import BeautifulSoup
from datetime import datetime
import re
records=[]


def dated(date):
    date=date.lower()
    
    tm2=re.findall('.[0-9][.|:][0-9].[:][0-9].', date)   
    if tm2:
        for i in tm2:
            date=date.replace(i,'')
   
    
    
    tm=re.findall('.[0-9][.|:][0-9].', date)    
    if tm:
        for i in tm:
            date=date.replace(i,'')
      
        
    tm3=re.findall('[0-9][.|:][0-9].', date)    
    if tm3:
        for i in tm3:
            date=date.replace(i,'')
   
    a = ['thurs','friday','fri',',','/','wednes','wed','tues','tue','thu','mon','monday','#','tuesday','wednesday','thursday','saturday','sunday','sat','sun','bst','day','  ',':','-','am','pm','updated', 'published','gmt','ist','tnn','|']     
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
    s=""
    
    
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
        print("r1 \n", r1)
        d = datetime.strptime(date, "%b %d %Y")
        date = d.strftime("%d-%m-%Y")
        print(date)
     
    elif r2: 
        print("r2 \n", r2)
        d = datetime.strptime(date, "%B %d %Y")
        date = d.strftime("%d-%m-%Y")
        print(date)
    
    elif r3: 
        print("r3 \n",r3)
        d = datetime.strptime(date, "%d %b %Y")
        date = d.strftime("%d-%m-%Y")
        print(date) 
        
    elif r4:
        print("r4 \n",r4)
        d = datetime.strptime(date, "%d %B %Y")
        date = d.strftime("%d-%m-%Y")
        print(date)
        
    elif r5: 
        print("r5 \n",r5)
        d = datetime.strptime(date, "%Y%m%d")
        date = d.strftime("%d-%m-%Y")
        print(date) 
        
    elif r6:
        print("r6 \n",r6)
        d = datetime.strptime(date, "%Y%m%d")
        date = d.strftime("%d-%m-%Y")
        print(date)

    elif r7:
        print("r7: \n",r7)
        d = datetime.strptime(date, "%d %m %Y")
        date = d.strftime("%d-%m-%Y")
        print(date)

        
    else:
        date=date
        print(date)
    return date






def c_e_n(url):   #5 page total
    print('\n')
    for i in range(4,6): 
        url_=url[:-14]
        print(url_)
        url=url[:-7]
        url=url+str(i)+'.shtml'
        print(url,'\n')
        cnt=0
        r = requests.get(url)
        html_doc = r.text
        soup = BeautifulSoup(html_doc,'html.parser')  
        genre=soup.find('div',attrs={'class':'letit'}).text
        span=soup.find_all('span',attrs={'class':'pictit'})
        for i in span:
           news='CHINA ECONOMIC NET'
           url2='http://en.ce.cn/'
           country='CHINA'
           topic=i.find('a').text
           date=i.findNext('span').text
           date=dated(date)
           ref_=i.find('a')['href']
           print(ref_)
           
           ref__=url_+ref_
           
           if '../' in ref__:
               ref=ref__.replace('../','/')
           else:
               ref=ref__.replace('./','/')
           
           
           a = ['/pick','/Entertainment','/Macro-economic','/Enterprise','/ti','/Life','/sports']     
           dlist=list(filter(lambda x:  x in ref, a))
           for i in dlist:
               ref=ref.replace(i, '').strip()
           
            
           print(ref)
                      
           r=requests.get(ref)
           soup2 = BeautifulSoup(r.text,'html.parser')
           context_=soup2.find('div',attrs={'class':'TRS_Editor'})
           if context_:
              context=context_.text.strip() 
           else:
                continue
           cnt=cnt+1
           print(cnt)
           
           records.append((news,url2,country,topic,ref,genre,date,context))
           
       




#c_e_n('http://en.ce.cn/sports/index_1.shtml')
c_e_n('http://en.ce.cn/Business/ti/index_1.shtml')
c_e_n('http://en.ce.cn/Business/Enterprise/index_1.shtml')
#c_e_n('http://en.ce.cn/Life/index_1.shtml')
c_e_n('http://en.ce.cn/Business/Macro-economic/index_1.shtml')
c_e_n('http://en.ce.cn/World/index_1.shtml')
c_e_n('http://en.ce.cn/Business/pick/index_1.shtml')


import pandas as pd
df=pd.DataFrame(records,columns=['news','url','country','topic','ref','genre','date','context'])
df.to_csv('fyp2.csv',mode='a',header=False)