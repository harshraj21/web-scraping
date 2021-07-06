from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.keys import Keys
import re
import logging
from selenium.webdriver.remote.remote_connection import LOGGER
from selenium.webdriver.common.action_chains import ActionChains
import os.path
import requests
import random
import string
import sys
from os import path
import pickle

LOGGER.setLevel(logging.WARNING)
def randomString(stringLength=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

print('\t\tVideo Fetcher And Downloader\n\nEnter Details:\n')
# username = input('Username-> ')
# password = input('Password-> ')
username = "harsh"
password = "harsh123"
website = "http://example.com/"
# website = "https://web.whatsapp.com"
col = 1
links = []
names = []
print("Started Capturing Links on: "+website)
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_argument('--disable-gpu')
options.add_argument('log-level=3')
# options.add_argument("user-data-dir=/home/harsh/.config/google-chrome")
driver = webdriver.Chrome(options=options)
try:
    cookies = pickle.load(open("cookies.pkl", "rb"))
    i=0
    while 1==1:
        try:
            print("added "+str(i))
            driver.add_cookie(cookies[i])
            i += 1
        except:
            i = 0
            break
except:
    print("Failed To Open Cookie File!!")
driver.maximize_window()
driver.get(website)
driver.find_element_by_xpath('//*[@id="AppFormNo"]').send_keys(username)
driver.find_element_by_xpath('//*[@id="Password"]').send_keys(password)
driver.execute_script("$('#fvpp-close').click();")
# driver.execute_script("$('#recaptcha-anchor > div.recaptcha-checkbox-border').click()")
input('Complete Captch Then Send Any Key To Continue: ')
driver.execute_script("alert('Getting Focus :)');")
driver.switch_to.alert.accept()
pickle.dump( driver.get_cookies() , open("cookies.pkl","ab"))
driver.find_element_by_xpath('/html/body/div[2]/div/div/div[2]/div[1]/form/div/div/button').click()
currentPageUrl = driver.current_url
try:
    syskey_request_token = re.findall('token=.*', currentPageUrl)[0]
    print("Catured "+syskey_request_token)
except:
    print("Token Not Found!")
    exit(0)
driver.execute_script("$('#fvpp-close').click();")
driver.find_element_by_xpath('//*[@id="sidebar-menu"]/li[6]/a').click()
i=1
uri = ''
htm = ''
driver.execute_script("$('#fvpp-close').click();")
print("Note: Row No Starts With >1< Count Accordingly")
row = input('Enter The Row No-> ')
row = int(row) + 1
row = str(row)
driver.execute_script("alert('Getting Focus :)');")
driver.switch_to.alert.accept()
while 1==1:
    try:
        driver.execute_script("$('#fvpp-close').click();")
        driver.find_element_by_xpath('//*[@id="page-content"]/div/div['+row+']/div/div/div[1]/div['+str(col)+']/div/a').click()
        while 1==1:
            try:
                driver.execute_script("$('#fvpp-close').click();")
                htm = driver.find_element_by_xpath('//*[@id="page-content"]/div/div[2]/div/div/div/div[2]/div/div[2]/a['+str(i)+']').get_attribute('innerHTML')
                uri = driver.find_element_by_xpath('//*[@id="my-video_html5_api"]').get_attribute('innerHTML')
                links.append(uri)
                names.append(htm)
                i += 1
                driver.find_element_by_xpath('//*[@id="page-content"]/div/div[2]/div/div/div/div[2]/div/div[2]/a['+str(i)+']').click()
            except:
                i = 1
                break
        col += 1
        driver.find_element_by_xpath('//*[@id="sidebar-menu"]/li[6]/a').click()
    except:
        break

#Logging Out
driver.find_element_by_xpath('//*[@id="header-nav-left"]/div/a/i').click()
time.sleep(1)
driver.find_element_by_xpath('//*[@id="header-nav-left"]/div/div/div/div[3]/a').click()
time.sleep(3)
pickle.dump( driver.get_cookies() , open("cookies.pkl","ab"))
driver.close()
print('Done Fetching Links')

print('Parsing Links And Names...')
i=0
while 1==1:
    try:
        names[i] = names[i].replace(" ","")
        names[i] = names[i].replace("\n","")
        names[i] = names[i].replace("<iclass=\"glyph-iconicon-arrow-right\">","")
        names[i] = names[i].replace("</i>"," ")
        try:
            links[i] = re.findall('https.*\.mp4', links[i])[0]
        except:
            links[i] = re.findall('https.*\.MP4', links[i])[0]
        if "&amp;" in links[i]:
            links[i] = links[i].replace("&amp;","&")
        i += 1
    except:
        break

print('Done')
print('Please Confirm Fetched Values...')
i=0
l = len(links)
while i<l:
    print((str(i+1))+' : '+names[i])
    i += 1

while 1==1:
    print("\nConfirm Download?\n1: Yes\n2: No")
    x = input('Enter Your Choice: ')
    if int(x) == 1:
        while 1==1:
            print("\nDownload All At Once?\n1: Yes\n2: Ask")
            y = input('Enter Your Choice: ')
            if int(y) == 1:
                break
            elif int(y) == 2:
                break
            else:
                print('\nInvalid Choice Try Again\n')
        break
    elif int(x) == 2:
        break
    else:
        print("\nInvalid Choice Try Again!\n")
i=0
name = ''
if int(x) == 1: #Yes
    if int(y) == 1: #All
        while i<l:
            name = names[i]+".mp4"
            if path.exists(name):
                nname = name.replace(".mp4","")
                nname = nname + "[" + randomString() + "]"
                nname = nname + ".mp4"
                name = nname
                print("File With Same Name Already Exist Renaming to: {}".format(name))
            try:
                with open(name, "wb") as f:
                    r = requests.get(links[i], stream=True)
                    total_length = r.headers.get('content-length')
                    if total_length is None: 
                        print("Error in getting the length of the file\n")
                    else:
                        print("\nDownloading " + name)
                        dl = 0
                        total_length = int(total_length)
                        for data in r.iter_content(chunk_size=4096):
                            dl += len(data)
                            f.write(data)
                            done = int(50 * dl / total_length)
                            sys.stdout.write("\r[%d%c][%s%s]" % (done*2,'%','#' * done, '.' * (50-done)))    
                            sys.stdout.flush()
                        print("\nDownloaded Successfully!\n")
            except:
                print("Error While Downloading File!\n")
            i += 1
    else: #Ask
        while i<l:
            print("\nToppic Name: {}\n".format(names[i]))
            ch = input('Download? 1: Yes | 2: No\nYour Choice: ')
            ch = int(ch)
            if ch == 1:
                name = names[i]+".mp4"
                if path.exists(name):
                    nname = name.replace(".mp4","")
                    nname = nname + "[" + randomString() + "]"
                    nname = nname + ".mp4"
                    name = nname
                    print("File With Same Name Already Exist Renaming to: {}".format(name))
                try:
                    with open(name, "wb") as f:
                        r = requests.get(links[i], stream=True)
                        total_length = r.headers.get('content-length')
                        if total_length is None: 
                            print("Error in getting the length of the file\n")
                        else:
                            print("\nDownloading " + name)
                            dl = 0
                            total_length = int(total_length)
                            for data in r.iter_content(chunk_size=4096):
                                dl += len(data)
                                f.write(data)
                                done = int(50 * dl / total_length)
                                sys.stdout.write("\r[%d%c][%s%s]" % (done*2,'%','#' * done, '.' * (50-done)))    
                                sys.stdout.flush()
                            print("\nDownloaded Sucessfully!\n")
                except:
                    print("Error While Downloading File!\n")
                i += 1
            elif ch == 2:
                print("\nSkipping This File Upon Your Request!")
                i += 1
            else:
                print("Invalid Choice! Try Again\n")
else: #NO
    print("OK! Not Downloading UpOn Your Request! Thanks For Using\n")
    exit(0)
