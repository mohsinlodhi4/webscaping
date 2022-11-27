# from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from urllib.parse import urljoin

def fetch_links(url="https://books.toscrape.com/", links=[]):

    r = requests.get(url)

    print(r.url, flush=True)

    soup = BeautifulSoup(r.text, "html.parser")

    for link in soup.select("h3 a"):

        links.append(urljoin(url, link.get("href")))

    next_page = soup.select_one("li.next a")

    if next_page:

        return fetch_links(urljoin(url, next_page.get("href"), links))

    else:

        return links

def decodeEmail(e :str):
    de = ""
    k = int(e[:2], 16)

    for i in range(2, len(e)-1, 2):
        de += chr(int(e[i:i+2], 16)^k)

    return de

def generatePagesUrl(url="https://apps.calbar.ca.gov/attorney/Licensee/Detail/", startId=10000, endId=10000):
    pages = []
    while(startId<=endId):
        u = f"{url}{startId}"
        pages.append(u)
        startId+=1
    return pages


ids=[] 
names=[] 
emails=[] 
addresses=[]
cellphones=[] 
officephones=[] 

web_url = "https://apps.calbar.ca.gov/attorney/Licensee/Detail/"
pages  = generatePagesUrl(
    url=web_url,
    startId=10000 , #should be greater or equal to 5 digits
    endId=10500 , #should be greater or equal to 5 digits
)

print('Loading...')

for page in pages:
    id = page[ page.find('Detail/')+7 : ]
    page = requests.get(page)
    content = page.text
    soup = BeautifulSoup(content, 'html.parser')
    ids.append(id)
"""    for detail in soup.find_all('li', attrs={'class':'profile-compact'}):

        # Fetching Names
        for a in detail.find_all('p', attrs={'class':'profile-name'}):
            try:
                name= a.find('a')
                if(name is not None and len(name.contents)>0):
                    names.append(name.contents[0])
            except Exception as e:
                print(name)

        # Fetching CellPhone, Addresses and Emails
        for a in detail.find_all('div', attrs={'class':'profile-contact'}):
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

                if(len(emails)<len(names)):
                    emails.append('')
                if(len(cellphones)<len(names)):
                    cellphones.append('')
                if(len(officephones)<len(names)):
                    officephones.append('')
                if(len(addresses)<len(names)):
                    addresses.append('')

            except Exception as e:
                print('error')
                print(str(e))

"""
print(ids)
# print(datetime.now())
# print(f"Names: {len(names)}")
# print(f"Emails: {len(emails)}")
# print(f"Addresses: {len(addresses)}")
# print(f"cellphones: {len(cellphones)}")
# print(f"officephones: {len(officephones)}")
# df = pd.DataFrame({'Names':names, 'Emails': emails, 'Office Phone': officephones, 'Cell Phone':cellphones, 'Address':addresses}) 
# df.to_excel('attorney-2.xlsx')