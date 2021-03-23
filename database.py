import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

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
    main_site_response = requests.get(source)
    main_site = main_site_response.content

    main_soup = BeautifulSoup(main_site, 'html.parser')

    #all_links_html = weapon_soup.find_all('a', href = True)
    #all_links_html = weapon_soup.find_all(href = re.compile('^/w/%'))
    
    ## Goes into 캐릭터 link
    all_links_html = main_soup.find_all()

    all_links = {}
    for i in all_links_html:
        if i.string != None and i.string != '원신/등장인물':
            all_links[i.string] = 'https://namu.wiki'+i['href']
    
    lst_leveling = []
    for i in range(len(all_links)):
        leveling_df = leveling(list(all_links.values())[i])
        leveling_df['캐릭터'] = list(all_links.keys())[i]
        lst_leveling.append(leveling_df)
    
    lst_leveling_complete = pd.concat(lst_leveling)
    lst_leveling_complete['캐릭터'] = lst_leveling_complete['캐릭터'].replace('\(원신\)','',regex=True)
    return lst_leveling_complete




#weapon_types = ['Swords','Claymores','Polearms','Catalysts','Bows']
# weapon_types = ['한손검','양손검','장병기','법구','활']
# weapon_types_sites = [
#     'https://namu.wiki/w/%EB%B6%84%EB%A5%98:%EC%9B%90%EC%8B%A0/%ED%94%8C%EB%A0%88%EC%9D%B4%EC%96%B4%EB%B8%94%20%EC%BA%90%EB%A6%AD%ED%84%B0/%ED%95%9C%EC%86%90%EA%B2%80',
#     'https://namu.wiki/w/%EB%B6%84%EB%A5%98:%EC%9B%90%EC%8B%A0/%ED%94%8C%EB%A0%88%EC%9D%B4%EC%96%B4%EB%B8%94%20%EC%BA%90%EB%A6%AD%ED%84%B0/%EC%96%91%EC%86%90%EA%B2%80',
#     'https://namu.wiki/w/%EB%B6%84%EB%A5%98:%EC%9B%90%EC%8B%A0/%ED%94%8C%EB%A0%88%EC%9D%B4%EC%96%B4%EB%B8%94%20%EC%BA%90%EB%A6%AD%ED%84%B0/%EC%9E%A5%EB%B3%91%EA%B8%B0',
#     'https://namu.wiki/w/%EB%B6%84%EB%A5%98:%EC%9B%90%EC%8B%A0/%ED%94%8C%EB%A0%88%EC%9D%B4%EC%96%B4%EB%B8%94%20%EC%BA%90%EB%A6%AD%ED%84%B0/%EB%B2%95%EA%B5%AC',
#     'https://namu.wiki/w/%EB%B6%84%EB%A5%98:%EC%9B%90%EC%8B%A0/%ED%94%8C%EB%A0%88%EC%9D%B4%EC%96%B4%EB%B8%94%20%EC%BA%90%EB%A6%AD%ED%84%B0/%ED%99%9C'
# ]

# lst_all_data = []
# for i in range(len(weapon_types_sites)):
#     df_each_weapon = all_data_each_weapon(weapon_types_sites[i])
#     df_each_weapon['무기'] = weapon_types[i]
#     lst_all_data.append(df_each_weapon)

# df_all_data = pd.concat(lst_all_data, ignore_index=True)
# df_all_data = df_all_data[['무기','캐릭터','돌파 레벨','캐릭터 육성 소재','모라']]

# df_all_data.to_csv('Leveling_guide.csv')