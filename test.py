import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

webpage_response = requests.get("https://namu.wiki/w/%EA%B0%90%EC%9A%B0")

webpage = webpage_response.content

soup = BeautifulSoup(webpage, 'html.parser')

all_tables = soup.select('.wiki-table')

lst = []
for i in all_tables:
    if '돌파 레벨' in i.get_text():
        lst = i.get_text('|').split("|")

lst_complete = []
if not lst:
    pass
else:
    lst_complete = [i for i in lst if i != ' ']

level_lst = [i for i in lst_complete if i[-1] == '0' and len(i) == 2]

level = []
materials = []
mora = []

i = 0
while i < len(lst_complete):
    if '000' in lst_complete[i]:
        s = lst_complete[i].replace(',', '')
        mora.append(int(s))
        i += 1
    elif lst_complete[i] in level_lst:
        level.append(int(lst_complete[i]))
        i += 1
        dic = {}
        while lst_complete[i] not in level_lst and '000' not in lst_complete[i]:
            if lst_complete[i] == 'X':
                i += 1
            else:
                num = lst_complete[i+1].replace('×', '').replace(' ', '')
                dic[lst_complete[i]] = int(num)
                i += 2
        materials.append(dic)
    else:
        i += 1

d = {}
d[lst_complete[0]] = level
d[lst_complete[1]] = materials
d[lst_complete[2]] = mora

df_leveling = pd.DataFrame(data=d)

print(df_leveling)