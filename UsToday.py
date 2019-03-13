import requests     
from bs4 import BeautifulSoup
import pandas
import re
from datetime import datetime
import csv    






import re
records=[]


def dated(date):
    date=date.lower()
    print(date)
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
   
    a = ['thurs','friday','fri',',','/','wednes','wed','tues','tue','thu','mon','monday','#','tuesday','wednesday','thursday','saturday','sunday','sat','sun','bst','day','  ',':','-','am','pm','a.m.','p.m.','updated', 'published','gmt','ist','tnn','|','.','et']     
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










def Remove(duplicate): 
    final_list = [] 
    for num in duplicate: 
        if num not in final_list: 
            final_list.append(num) 
    return final_list



def remover(l):
    #new list
    newlist = []
    #loop over elements
    for i in l:
        #pdb.set_trace()
        #is element a non-empty list? then call self on it
        if isinstance(i, list) and len(i) != 0:
            newlist.append(remover(i))
        #if not a list
        if not isinstance(i, list):
            newlist.append(i)
    
    #return newlist
    return newlist

def remove_empty_lists(l):
    keep_going = True
    prev_l = l
    while keep_going:
        #call remover on the list
        new_l = remover(prev_l)
        #are they identical objects?
        if new_l == prev_l:
            keep_going = False
        #set prev to new
        prev_l = new_l
    #return the result
    return new_l





def US_Today_buisness():
    
    temp=[]
    links=[]
    records=[]


    url=['https://www.usatoday.com/money/']

    

    for j in url:
        
        with requests.Session() as se:
            se.encoding = "UTF-8"
            res = se.get(j) 
            text = res.text
                
        soup = BeautifulSoup(text,"lxml")             
        new = soup.find("div",class_='card-full-width')  
        print(new)
        news_headline = new.find_all("a")
        
        temp.extend(news_headline)


    for link in temp:

        if link.get('href').startswith('/'):
            linkin='https://www.usatoday.com'+link.get("href")
            links.append(linkin)
        else:

            links.append(link.get("href"))
            

    links=Remove(links)
    links=remove_empty_lists(links)

    for i in links:
        if '2018' in i and '/usatodayhss.com' not in i and '.linkedin.com/' not in i and '/picture-gallery/' not in i and '/videos/' not in i :
            news='US Today'
            r=requests.get(i)
            print(i)
            soup2 = BeautifulSoup(r.text,'html.parser')
            if soup2.find("h1",{"class":"asset-headline speakable-headline"})==None:
                topic=''
            else:
                topic=soup2.find("h1",{"class":"asset-headline speakable-headline"}).text.replace("\r","").replace("\n","")
            

            print(topic)
            
            if soup2.find("span",{"class":"asset-metabar-time asset-metabar-item nobyline"})==None:
                date=''
            else:
                date=soup2.find("span",{"class":"asset-metabar-time asset-metabar-item nobyline"}).text.replace("\r","").replace("\n","")
                
            context=' '
            #body=soup2.find("div",{"class":"article-body"})
            for content_tag in soup2.find_all("p"):
                context = context+content_tag.text.replace("\r","").replace("\n","")              
             
            genre='Buisness'
            country='United States'
            url2='http://www.usatoday.com'
            records.append((news,url2,country,topic,i,genre,date,context))
            print('#######################################################')


    df=pandas.DataFrame(records)    
  
    with open('USToday.csv', 'a',encoding="utf-8") as newFile:
        df.to_csv(newFile, header=False)
    newFile.close()   

   
US_Today_buisness()


#sahi karna ha ye





