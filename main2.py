import requests
from bs4 import BeautifulSoup
import re

res = requests.get("http://www.homeoint.org/books/boericmm/c/con-m.htm")

soup = BeautifulSoup(res.text,'html.parser')
# print(soup.prettify())
name_and_other_meta = soup.find_all("p")
# [3]

for i in name_and_other_meta:
    print("-------------------------------------------------------")
    print(i)
    print("-------------------------------------------------------")
    
# print(name_and_other_meta)
# common_name = (str(name_and_other_meta).split("<br/>"))[2].replace("</font>","").replace("</b>","").replace("</p>","")

# print(common_name)


exit()

arr = res.text.split('<p align="justify">')
for i in range(1,len(arr)):
    print("-------------------------------------------------------")
    arr[i] = arr[i].replace('<font color="#ff0000"><b>','').replace('</p>','').replace("\n","")
    arr[i] = re.sub(' +', ' ', arr[i])
    if arr[i].find(".--") >= 0 :
        print("symptoms")
        print(arr[i])
    else:
        print("gen")
        print(arr[i])
    # print(aa)
    print("-------------------------------------------------------")