# from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import pandas as pd

def decodeEmail(e :str):
    de = ""
    k = int(e[:2], 16)

    for i in range(2, len(e)-1, 2):
        de += chr(int(e[i:i+2], 16)^k)

    return de

names=[] 
emails=[] 
addresses=[]
cellphones=[] 
officephones=[] 
page = requests.get("https://www.floridabar.org/directories/find-mbr/?fName=a&sdx=N&eligible=N&deceased=N&pageNumber=1&pageSize=10")

content = page.text
soup = BeautifulSoup(content, 'html.parser')

# Fetching Names
for a in soup.find_all('p', attrs={'class':'profile-name'}):
    try:
        name= a.find('a')
        if(name is not None and len(name.contents)>0):
            names.append(name.contents[0])
        # print(name.string)
        # names.append(name.text)
    except Exception as e:
        print(name)

# Fetching Emails
# for a in soup.find_all('a', attrs={'class':'icon-email', 'style': 'word-wrap: break-word;'}):
#     try:
#         if(a is not None):
#             email = decodeEmail(a.contents[0].get('data-cfemail'))
#             emails.append(email)
#     except Exception as e:
#         print()

# Fetching CellPhone, Addresses and Emails
for a in soup.find_all('div', attrs={'class':'profile-contact'}):
    try:
        i=0
        for b in a.find_all('p'):
            if(i==0):
                cell= b
                newc = [x for x in cell.contents if x!='<br/>' ]
                addr =' '.join(map(str,newc)).replace('<br/>','')
                addresses.append(addr)
            else:
                j=0
                for tel in b.find_all('a'):
                    if(tel.get('href').find('tel:')!=-1):
                        if(j==1):
                            officephones.append(tel.get('href').replace('tel:',''))
                        else:
                            cellphones.append(tel.get('href').replace('tel:',''))
                    j+=1
                for tel in b.find_all('a'):
                    if(len(cellphones)<len(officephones)):
                        cellphones.append('')
                    elif(len(cellphones)>len(officephones)):
                        officephones.append('')



            i+=1
        emailTag = a.find('a', attrs={'class':'icon-email'})
        if(emailTag is not None):
            email = decodeEmail(emailTag.contents[0].get('data-cfemail'))
            emails.append(email)
        else:
            emails.append('')
    except Exception as e:
        print(e)

# print(len(names))
# print(len(emails))
# print(len(addresses))
# print(len(cellphones))
# print(len(officephones))
df = pd.DataFrame({'Names':names, 'Emails': emails, 'Office Phone': officephones, 'Cell Phone':cellphones, 'Address':addresses}) 
# df.to_csv('attorneys.csv', index=False, encoding='utf-8')
df.to_excel('attorneys.xlsx')