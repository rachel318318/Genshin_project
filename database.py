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

def character_and_weapon(source):
    character_site_response = requests.get(source)
    character_site = character_site_response.content

    character_soup = BeautifulSoup(character_site, 'html.parser')

    all_links_html = character_soup.find_all(attrs = {'class':'wiki-link-internal'})

    all_character_links = {}
    for i in all_links_html:
        all_character_links[i.attrs['title']] = 'https://namu.wiki'+i['href']
    all_character_links.pop('원신')
    all_character_links.pop('원신/등장인물')

    all_weapon_links = {}
    for key in all_character_links.keys():
        if '원신/무기/' in key:
            all_weapon_links[key] = all_character_links[key]
    
    for key in all_weapon_links.keys():
        all_character_links.pop(key)

    lst_leveling = []
    for i in range(len(all_character_links)):
        leveling_df = leveling(list(all_character_links.values())[i])
        leveling_df['캐릭터'] = list(all_character_links.keys())[i]
        leveling_df['무기'] = weapon_type(list(all_character_links.values())[i])
        lst_leveling.append(leveling_df)
        print(lst_leveling)
    
    lst_leveling_complete = pd.concat(lst_leveling)
    lst_leveling_complete['캐릭터'] = lst_leveling_complete['캐릭터'].replace('\(원신\)','',regex=True)
    return lst_leveling_complete

def weapon_type(source):
    weapon_types = ['한손검','양손검','장병기','법구','활']

    webpage_response = requests.get(source)

    webpage = webpage_response.content

    soup = BeautifulSoup(webpage, 'html.parser')

    weapon = soup.find_all(attrs = {'class':'wiki-paragraph'})

    characters_weapon = ""
    for i in weapon:
        if i.get_text() in weapon_types:
            characters_weapon = i.get_text()
            return characters_weapon


def all_data(source):
    main_site_response = requests.get(source)
    main_site = main_site_response.content

    main_soup = BeautifulSoup(main_site, 'html.parser')

    character_weapon_link_html = main_soup.find_all('a', string = "캐릭터")
    character_weapon_link = 'https://namu.wiki' + character_weapon_link_html[0]['href']

    result = character_and_weapon(character_weapon_link)

    return result


df_all_data = all_data('https://namu.wiki/w/%EC%9B%90%EC%8B%A0')

df_all_data = df_all_data[['무기','캐릭터','돌파 레벨','캐릭터 육성 소재','모라']]

df_all_data.to_csv('Leveling_guide.csv')

# weapon_types = ['Swords','Claymores','Polearms','Catalysts','Bows']