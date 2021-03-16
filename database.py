import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd


def leveling(source):
    webpage_response = requests.get(source)

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
        print(lst_complete)


    level = []
    materials = []
    mora = []
    
    i = 0
    while i < len(lst_complete):
        if '000' in lst_complete[i]:
            s = lst_complete[i].replace(',', '')
            mora.append(int(s))
            i += 1
        elif lst_complete[i][-1] == '0' and len(lst_complete[i]) == 2:
            level.append(int(lst_complete[i]))
            i += 1
            dic = {}
            while lst_complete[i][-1] != '0' and len(lst_complete[i]) != 2:
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
    return df_leveling

def all_data(source):
    claymore_site_response = requests.get(source)
    claymore_site = claymore_site_response.content

    claymore_soup = BeautifulSoup(claymore_site, 'html.parser')

    all_links_html = claymore_soup.find_all('a', href = True)

    all_links = []
    for i in all_links_html:
        if '/w/%' in i['href']:
            all_links.append('https://namu.wiki'+i['href'])

    for i in all_links:
        try:
            print(leveling(all_links[0]))
        except IndexError:
            pass


weapon_types = ['Swords','Claymores','Polearms','Catalysts','Bows']
weapon_types_sites = [
    'https://namu.wiki/w/%EB%B6%84%EB%A5%98:%EC%9B%90%EC%8B%A0/%ED%94%8C%EB%A0%88%EC%9D%B4%EC%96%B4%EB%B8%94%20%EC%BA%90%EB%A6%AD%ED%84%B0/%ED%95%9C%EC%86%90%EA%B2%80',
    'https://namu.wiki/w/%EB%B6%84%EB%A5%98:%EC%9B%90%EC%8B%A0/%ED%94%8C%EB%A0%88%EC%9D%B4%EC%96%B4%EB%B8%94%20%EC%BA%90%EB%A6%AD%ED%84%B0/%EC%96%91%EC%86%90%EA%B2%80',
    'https://namu.wiki/w/%EB%B6%84%EB%A5%98:%EC%9B%90%EC%8B%A0/%ED%94%8C%EB%A0%88%EC%9D%B4%EC%96%B4%EB%B8%94%20%EC%BA%90%EB%A6%AD%ED%84%B0/%EC%9E%A5%EB%B3%91%EA%B8%B0',
    'https://namu.wiki/w/%EB%B6%84%EB%A5%98:%EC%9B%90%EC%8B%A0/%ED%94%8C%EB%A0%88%EC%9D%B4%EC%96%B4%EB%B8%94%20%EC%BA%90%EB%A6%AD%ED%84%B0/%EB%B2%95%EA%B5%AC',
    'https://namu.wiki/w/%EB%B6%84%EB%A5%98:%EC%9B%90%EC%8B%A0/%ED%94%8C%EB%A0%88%EC%9D%B4%EC%96%B4%EB%B8%94%20%EC%BA%90%EB%A6%AD%ED%84%B0/%ED%99%9C'
]

for i in weapon_types_sites:
    all_data(i)