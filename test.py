import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

weapon_types = ['한손검','양손검','장병기','법구','활']

webpage_response = requests.get("https://namu.wiki/w/%EC%97%AC%ED%96%89%EC%9E%90(%EC%9B%90%EC%8B%A0)")

webpage = webpage_response.content

soup = BeautifulSoup(webpage, 'html.parser')

lst = []
for child in soup.td.children:
    lst.append(child)

print(lst)

characters_weapon = ""
# for i in weapon:
#     if i.get_text() in weapon_types:
#         characters_weapon = i.get_text()