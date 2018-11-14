import requests
from bs4 import BeautifulSoup

url = 'https://www.hindustantimes.com/'
page = requests.get(url)
page = page.content

soup = BeautifulSoup(page, 'html.parser')

#list of all the classes which contain headlines
headline_class_list = ['big-story-h2', 'big-story-mid-h3', 'subhead4', 'subhead4 pt-10', 'top-thumb-rgt', 'media-heading heading4', 'headingfour', 'media-heading headingfive', 'headingfive', 'random-heading', 'para-txt']
headline_div_class = soup.find_all('div', attrs={'class':[headline_class_list]})

#getting text
news_list=[]
for i in headline_div_class:
    news_list.append(i.get_text())
import re
for i in range (len(news_list)):
    news_list[i]=re.sub('\s+',' ', news_list[i])
    
#removing small sentences which are not headlines like  select city, know more etc.
processed_news_list=[]
for i in range (len(news_list)):
    z=news_list[i].split()
    if (len(z)>=4):
        processed_news_list.append(news_list[i])
        
#translating Punjabi to English
import langdetect
from translate import Translator
for i in range(len(processed_news_list)):
    if(langdetect.detect(processed_news_list[i]) == 'pa'):
        translator = Translator(from_lang='pa', to_lang='en')
        processed_news_list[i] = translator.translate(processed_news_list[i])

#writing the headlines row-wise
import csv
with open('headline.csv', 'w', newline='') as f:
    wr = csv.writer(f)
    for i in processed_news_list:
        wr.writerow([i])