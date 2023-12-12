import pandas as pd
import os
# sử dụng thử crawler bằng selenium, vì thế để chạy được script cần cài đặt môi trường selenium và chromeDiver hoặc firefoxDriver tương ứng với trình duyệt và phiên bản của trình duyệt đang sử dụng
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

# read excel file to get a list MaCK
listMaCK = pd.read_excel('FileBaoLoi.xlsx', sheet_name='Tai_BCTC',usecols='A')
# numMACK = listMaCK['MACK'].count()
numMACK = len(listMaCK.index)
# numMACK = listMaCK.size
i = 0
rootUrl = 'https://cafef.vn/'

def createFolder(folderName):
    path = 'MACK/'
    os.mkdir(os.path.join(path,folderName))

def searchMack(mack):
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get(rootUrl)
    # driver.maximize_window()
    # tim input nhap ma ck de search
    searchInput = driver.find_element(By.XPATH, '//div[@id="CafeF_BoxSearchNew"]//input[@id="CafeF_SearchKeyword_Company"]')
    searchInput.send_keys(mack)

    # Clicking on "Next" button
    search_button = driver.find_element(By.XPATH, '//div[@id="CafeF_BoxSearchNew"]//a[contains(@class, "s-submit")]')
    search_button.click()

    get_url = driver.current_url
    
    time.sleep(1)
    return get_url

# for maCK in listMaCK:
for i in range(numMACK):
    mack = listMaCK['MACK'][i]
    print(mack)
    # create a folder with name maCK => Done (need check if folder existed then abort)
    # createFolder(mack)

    # action search maCK on cafeF page and get url page => Doing
    urlMACK = searchMack(mack)
    print(urlMACK)    

    # f = open('MACK/linkMaCK2.csv', 'a').write(urlMACK)
    # action get urls file download => TO DO

# df = pd.DataFrame({'Ma CK': mack, 'url_mack': urlMACK})
# df.to_csv('MACK/linkMaCK.csv', index=False)