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

def generatePagesUrl(url="https://www.floridabar.org/directories/find-mbr/", startPage=1, endPage=1, pageSize=50):
    queryStartIndex = url.find("?")
    queryEndIndex = url.find("pageNumber=")
    if(queryStartIndex==-1):
        return [url]

    pages = []
    query = url[queryStartIndex:queryEndIndex]
    web_url = url[:queryStartIndex]
    while(startPage<=endPage):
        u = f"{web_url}{query}{'' if query[-1]=='&' else '&'}pageNumber={startPage}&pageSize={pageSize}"
        pages.append(u)
        startPage+=1
    return pages


names=[] 
emails=[] 
addresses=[]
cellphones=[] 
officephones=[] 
start_page = 1
end_page = 1
filter_url = ""
pageSize = 50
web_url = "https://www.floridabar.org/directories/find-mbr/"
pages  = generatePagesUrl(
    url="https://www.floridabar.org/directories/find-mbr/?locType=T&locValue=miami+dade&sdx=N&eligible=N&deceased=N&pageNumber=1000&pageSize=50",
    startPage=1 ,
    endPage=100 ,
    pageSize=50 ,
)
# page = requests.get("https://www.floridabar.org/directories/find-mbr/?fName=a&sdx=N&eligible=N&deceased=N&pageNumber=1&pageSize=10")
print('Loading...')

for page in pages:
    page = requests.get(page)
    content = page.text
    soup = BeautifulSoup(content, 'html.parser')

    for detail in soup.find_all('li', attrs={'class':'profile-compact'}):

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
                print('line')
                print(str(e))


print(f"Names: {len(names)}")
print(f"Emails: {len(emails)}")
print(f"Addresses: {len(addresses)}")
print(f"cellphones: {len(cellphones)}")
print(f"officephones: {len(officephones)}")
df = pd.DataFrame({'Names':names, 'Emails': emails, 'Office Phone': officephones, 'Cell Phone':cellphones, 'Address':addresses}) 
# df.to_csv('attorneys.csv', index=False, encoding='utf-8')
df.to_excel('attorneys.xlsx')