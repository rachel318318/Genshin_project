import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

webpage_response = requests.get("https://namu.wiki/w/%ED%8B%80:%EC%9B%90%EC%8B%A0%20%ED%94%8C%EB%A0%88%EC%9D%B4%EC%96%B4%EB%B8%94%20%EC%BA%90%EB%A6%AD%ED%84%B0")

webpage = webpage_response.content

soup = BeautifulSoup(webpage, 'html.parser')

lst = []
for i in soup.find_all('tbody'):
    lst.append(i)

new = None
for i in lst:
    div = i.find_all('div')
    for j in div:
        if "무기" in j.get_text():
            new = i

tr = new.find_all('tr')
new_lst = []
for i in tr[1:]:
    td = i.find_all('td')
    for j in td:
        new_lst2 = []
        a = j.find_all(attrs = {'class':'wiki-link-internal'})
        for t in a:
            if '원신/무기/' in t.attrs['title'] and t.attrs['title'] not in new_lst:
                new_lst.append(t.attrs['title'].replace('원신/무기/', ''))
            elif t.attrs['title'] not in new_lst2:
                new_lst2.append(t.attrs['title'])
        if new_lst2:
            new_lst.append(new_lst2)


j = 1
new_dict = {}
while j < len(new_lst):
    for k in new_lst[j]:
        new_dict[k] = new_lst[j-1]
    j += 2

characters_weapon = ""
# for i in weapon:
#     if i.get_text() in weapon_types:
#         characters_weapon = i.get_text()