import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

webpage_response = requests.get("https://namu.wiki/w/%EC%9B%90%EC%8B%A0/%EB%AC%B4%EA%B8%B0/%ED%95%9C%EC%86%90%EA%B2%80")

webpage = webpage_response.content

soup = BeautifulSoup(webpage, 'html.parser')

all_tables = soup.select('h3')

weapon_name_lst = []
for i in all_tables:
    ele = i.get_text()
    ele = re.sub('\d+\.\d+\. ','',ele)
    weapon_name_lst.append(ele.replace('[편집]',''))

