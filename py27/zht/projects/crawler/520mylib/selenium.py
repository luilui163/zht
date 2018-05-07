#-*-coding: utf-8 -*-
#author:tyhj
#selenium.py 2017/7/29 0:18
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException,NoSuchElementException,WebDriverException

import pandas as pd
import time



# chrome_options = Options()
# chrome_options.add_argument('--dns-prefetch-disable')
# driver =webdriver.Chrome(r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe',chrome_options=chrome_options)

# driver =webdriver.Chrome(r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
# driver.set_page_load_timeout(3)

driver=webdriver.Firefox(executable_path=r'C:\app\firefox\geckodriver.exe')
driver.set_page_load_timeout(3)



driver.get('http://www.520mylib.com/account/login')


username=driver.find_element_by_id('login_username')
username.send_keys()


password=driver.find_element_by_name('Password')
password.send_keys()

button=driver.find_element_by_xpath('//*[@id="loginform"]/div[6]/div/div[4]/button')
button.click()


driver.get(r'http://www.520mylib.com/db/category/4')

ul=driver.find_element_by_class_name('quick-actions')

elems=ul.find_elements_by_tag_name('a')

urls1=[]

for elem in elems:
    print elem.get_attribute('href')
    urls1.append(elem.get_attribute('href'))



wrongUrls=[]
df=pd.DataFrame(columns=['vpnUrl','username','password'])

for url1 in urls1:

    driver.get(url1)

    div=driver.find_element_by_class_name('quick-actions_homepage')

    items=div.find_elements_by_tag_name('a')

    urls2=[]
    for item in items:
        urls2.append(item.get_attribute('href'))
        print item.get_attribute('href')

    for url2 in urls2:
        try:
            driver.get(url2)
            elem=driver.find_element_by_id('link_list')#TODO
        except:
            wrongUrls.append((2,url2))
            continue

        items=elem.find_elements_by_tag_name('a')

        urls3=[]
        for item in items:
            urls3.append(item.get_attribute('href'))
            print item.get_attribute('href')

        for url3 in urls3:
            # driver.set_page_load_timeout(0.5)#TODO
            driver.get(url3)

            html=driver.page_source
            soup=BeautifulSoup(html,'html')
            form=soup.find('form')

            vpnUrl=form['action']

            inputs=form.findAll('input')
            username=inputs[0]['value']
            password=inputs[1]['value']
            df.loc[url3]=[vpnUrl,username,password]
            print url3

driver.close()


df.to_csv(r'C:\Python27\zht\crawler\520mylib\accounts.csv')
pd.DataFrame(wrongUrls).to_csv(r'C:\Python27\zht\crawler\520mylib\wrongUrls.csv')

#TODO: get the key and passwords in 520mylib  and resset






