import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

glevel = [20, 40, 50, 60, 70, 80]

webpage_response = requests.get("https://namu.wiki/w/%EC%9B%90%EC%8B%A0/%EB%AC%B4%EA%B8%B0/%ED%95%9C%EC%86%90%EA%B2%80")

webpage = webpage_response.content

soup = BeautifulSoup(webpage, 'html.parser')

all_names = soup.select('h3')

weapon_name_lst = []
for i in all_names:
    ele = i.get_text()
    ele = re.sub('\d+\.\d+\. ','',ele)
    weapon_name_lst.append(ele.replace('[편집]',''))

all_tables = soup.select('tr')
ascending_html_lst = []
ascending_text = []
for i in all_tables:
    text2 = []
    if '돌파 소재' in i.get_text():
        ascending_html_lst.append(i)

leveling_num = []
leveling_item = []
for i in ascending_html_lst:
    lst2 = []
    lst3 = []
    lst4 = []
    for j in i.find_all(attrs = {'style':'display:inline'}):
        lst2.append(j.get_text())
    leveling_num.append(lst2)

    for k in i.find_all(attrs = {'title':'원신/육성 아이템'}):
        lst3.append(k.get_text())
        lst4 = [i for i in lst3 if i]
    leveling_item.append(lst4)

mora = []
for i in range(len(leveling_num)):
    lst5 = []
    j = 3
    while j < len(leveling_num[i]):
        if leveling_num[i][j] == '0':
            lst5.append(int(leveling_num[i][j]))
            j += 4
        else:
            ele = leveling_num[i][j].replace(',','')
            lst5.append(int(ele))
            j += 4
    mora.append(lst5)

leveling_lst = []
for i in range(len(leveling_item)):
    inner_leveling_lst = []
    leveling_dic = {}
    j = 0
    k = 0
    while j < len(leveling_num[i]):
        if j % 4 == 3:
            j += 1
        elif k % 3 == 0:
            if k != 0:
                inner_leveling_lst.append(leveling_dic)
            leveling_dic = {}
            leveling_dic[leveling_item[i][k]] = leveling_num[i][j]
            j += 1
            k += 1
        else:
            leveling_dic[leveling_item[i][k]] = leveling_num[i][j]
            j += 1
            k += 1
    inner_leveling_lst.append(leveling_dic)
    leveling_lst.append(inner_leveling_lst)

levels = []
for i in range(len(mora)):
    inner_levels = []
    for j in range(len(mora[i])):
        inner_levels.append(glevel[j])
    levels.append(inner_levels)

data_complete_lst = []
for i in range(len(mora)):
    data_complete_dic = {}
    data_complete_dic['레벨'] = levels[i]
    data_complete_dic['소재'] = leveling_lst[i]
    data_complete_dic['모라'] = mora[i]
    data_complete_df = pd.DataFrame(data=data_complete_dic)
    data_complete_df['무기 이름'] = weapon_name_lst[i]
    data_complete_lst.append(data_complete_df)

data_complete = pd.concat(data_complete_lst)

print(data_complete)