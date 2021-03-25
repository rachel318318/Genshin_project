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

    global glevel
    glevel = level

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
        leveling_df['무기 종류'] = dict_weapon_char[list(all_character_links.keys())[i]]
        lst_leveling.append(leveling_df)
    
    lst_weapon_leveling = []
    for i in range(len(all_weapon_links)):
        weapon_leveling_df = weapon_leveling(list(all_weapon_links.values())[i])
        weapon_leveling_df['무기 종류'] = list(all_weapon_links.keys())[i]
        lst_weapon_leveling.append(weapon_leveling_df)
    
    weapon_leveling_complete = pd.concat(lst_weapon_leveling)
    weapon_leveling_complete['무기 종류'] = weapon_leveling_complete['무기 종류'].replace('원신/무기/','',regex=True)

    lst_leveling_complete = pd.concat(lst_leveling)
    lst_leveling_complete['캐릭터'] = lst_leveling_complete['캐릭터'].replace('\(원신\)','',regex=True)
    return lst_leveling_complete, weapon_leveling_complete

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

def weapon_leveling(source):
    webpage_response = requests.get(source)

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
    for i in all_tables:
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

    return data_complete

def all_data(source):
    main_site_response = requests.get(source)
    main_site = main_site_response.content

    main_soup = BeautifulSoup(main_site, 'html.parser')

    character_weapon_link_html = main_soup.find_all('a', string = "캐릭터")
    character_weapon_link = 'https://namu.wiki' + character_weapon_link_html[0]['href']

    char_result, weapon_result = character_and_weapon(character_weapon_link)

    return char_result, weapon_result


df_char_all_data = all_data('https://namu.wiki/w/%EC%9B%90%EC%8B%A0')[0].reset_index()
df_char_all_data = df_char_all_data[['무기 종류','캐릭터','돌파 레벨','캐릭터 육성 소재','모라']]
df_char_all_data.to_csv('Leveling_guide.csv')

df_weapon_all_data = all_data('https://namu.wiki/w/%EC%9B%90%EC%8B%A0')[1].reset_index()
df_weapon_all_data = df_weapon_all_data[['무기 종류','무기 이름','레벨','소재','모라']]
df_weapon_all_data.to_csv('Weapon_leveling_guide.csv')

# weapon_types = ['Swords','Claymores','Polearms','Catalysts','Bows']