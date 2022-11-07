from bs4 import BeautifulSoup
import requests
import json
import re
import traceback

alphabets = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

base_url = "http://www.homeoint.org/books/boericmm"

url_s = [f"{base_url}/{alph}.htm" for alph in alphabets]

medicines = {}

errors = {}

for url in url_s:
    res  = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')

    contents = (soup.find_all('p'))[4]

    x   = str(contents).replace('<font size="2">',"").replace("<p>","").replace("</p>","")
    arr = filter(lambda x: x.find("<a href")>-1, x.split("<br/>"))

    for tag in arr:
        medicine_link       = tag[tag.find("href")+6:tag.find("htm")+3]
        medicine_short_name = tag[tag.find("_top")+6:tag.find('</a>')]
        print(medicine_short_name)
        medicine_long_name = (tag.split('&gt;')[1]).replace("\n","").replace("  "," ").strip().replace("   "," ")
        medicines[medicine_short_name] = {
            "short_name":medicine_short_name,
            "long_name":medicine_long_name,
            "link":medicine_link
        }

        medicine_url = base_url + "/" + medicine_link

        res  = requests.get(medicine_url)
        soup = BeautifulSoup(res.text,'html.parser')

        try:

            name_and_other_meta = soup.find_all("p")[3]
            common_name = (str(name_and_other_meta).split("<br/>"))[2].replace("</font>","").replace("</b>","").replace("</p>","")

            print(common_name)

            medicines[medicine_short_name]['symptoms'] = {}
            arr = res.text.split('<p align="justify">')
            for i in range(1,len(arr)):
                arr[i] = arr[i].replace('<font color="#ff0000"><b>','').replace('</p>','').replace("\n","")
                arr[i] = re.sub(' +', ' ', arr[i])
                if arr[i].find(".--") >= 0:
                    if arr[i].find("Dose.--") >= 0:
                        medicines[medicine_short_name]['dose'] = arr[i].replace("Dose.--","")
                    elif arr[i].find("Relationship.--") >= 0:
                        medicines[medicine_short_name]['relationship'] = arr[i].replace("Relationship.--","")
                    else:
                        symp_category = arr[i].split(".--")[0]
                        symp_category = symp_category.lower()
                        medicines[medicine_short_name]['symptoms'][symp_category] = arr[i].split(".--")[1]
                else:
                    medicines[medicine_short_name]['description'] = arr[i]

        except Exception as e:
            print("\n-----\nERROR\n-----")
            print(medicine_short_name)
            print(medicine_long_name)
            print("--",end="")
            print("-"*(len(medicine_long_name)+2))
            errors[medicine_short_name] = {}
            errors[medicine_short_name]['traceback'] = {}
            errors[medicine_short_name]['traceback'] = traceback.format_exc()
            errors[medicine_short_name]['error'] = {}
            errors[medicine_short_name]['error'] = str(e)
            





with open("medicines2.json",'w') as f:
    json.dump(medicines,f)

with open("errors.json",'w') as f:
    json.dump(errors,f)


# print(list(filter(lambda x: x != "",medicine_links)))

# soup = BeautifulSoup( x, 'html.parser')
# print(soup.prettify())

# for a_tag in soup.find_all("a"):
#     print("--------------------")
#     print(a_tag)
#     print(a_tag['href'])
#     print(a_tag.contents)
#     print("--------------------")