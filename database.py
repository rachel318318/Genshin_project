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

    dict_weapon_char = char_to_weapon(source)

    lst_leveling = []
    for i in range(len(all_character_links)):
        leveling_df = leveling(list(all_character_links.values())[i])
        leveling_df['캐릭터'] = list(all_character_links.keys())[i]
        leveling_df['무기'] = dict_weapon_char[list(all_character_links.keys())[i]]
        lst_leveling.append(leveling_df)
    
    lst_leveling_complete = pd.concat(lst_leveling)
    lst_leveling_complete['캐릭터'] = lst_leveling_complete['캐릭터'].replace('\(원신\)','',regex=True)
    return lst_leveling_complete

def char_to_weapon(source):
    webpage_response = requests.get(source)

    webpage = webpage_response.content

    soup = BeautifulSoup(webpage, 'html.parser')

    tbody_lst = []
    for i in soup.find_all('tbody'):
        tbody_lst.append(i)

    weapon_div = None
    for i in tbody_lst:
        div = i.find_all('div')
        for j in div:
            if "무기" in j.get_text():
                weapon_div = i

    tr = weapon_div.find_all('tr')
    weapon_char_lst = []
    for i in tr[1:]:
        td = i.find_all('td')
        for j in td:
            new_lst2 = []
            a = j.find_all(attrs = {'class':'wiki-link-internal'})
            for t in a:
                if '원신/무기/' in t.attrs['title'] and t.attrs['title'] not in weapon_char_lst:
                    weapon_char_lst.append(t.attrs['title'].replace('원신/무기/', ''))
                elif t.attrs['title'] not in new_lst2:
                    new_lst2.append(t.attrs['title'])
            if new_lst2:
                weapon_char_lst.append(new_lst2)


    j = 1
    weapon_char_dict = {}
    while j < len(weapon_char_lst):
        for k in weapon_char_lst[j]:
            weapon_char_dict[k] = weapon_char_lst[j-1]
        j += 2
    
    return weapon_char_dict

def all_data(source):
    main_site_response = requests.get(source)
    main_site = main_site_response.content

    main_soup = BeautifulSoup(main_site, 'html.parser')

    character_weapon_link_html = main_soup.find_all('a', string = "캐릭터")
    character_weapon_link = 'https://namu.wiki' + character_weapon_link_html[0]['href']

    result = character_and_weapon(character_weapon_link)

    return result


df_all_data = all_data('https://namu.wiki/w/%EC%9B%90%EC%8B%A0').reset_index()

df_all_data = df_all_data[['무기','캐릭터','돌파 레벨','캐릭터 육성 소재','모라']]

df_all_data.to_csv('Leveling_guide.csv')

# weapon_types = ['Swords','Claymores','Polearms','Catalysts','Bows']