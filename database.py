import requests
from bs4 import BeautifulSoup
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
        print("Ascension materials cannot be found.")
    else:
        lst_complete = [i for i in lst if i != ' ']
        print(lst_complete)


    level = []
    materials = []
    mora = []

    #change it to while loop!!
    for i in range(len(lst_complete)):
        if '000' in lst_complete[i]:
            s = lst_complete[i].replace(',', '')
            mora.append(int(s))
        elif lst_complete[i][-1] == '0' and len(lst_complete[i]) == 2:
            level.append(int(lst_complete[i]))
            j = i+1
            dic = {}
            while lst_complete[j][-1] != '0' and len(lst_complete[j]) != 2:
                if lst_complete[j] == 'X':
                    j += 1
                else:
                    num = lst_complete[j+1].replace('×', '').replace(' ', '')
                    dic[lst_complete[j]] = int(num)
                    j += 2
            materials.append(dic)

    print(level)
    print(materials)
    print(mora)
