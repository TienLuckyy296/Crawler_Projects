from selenium import webdriver
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import time 
import requests
# from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os

DF = pd.read_excel("FileBaoLoi.xlsx",sheet_name="test",usecols='A')
numDF = len(DF.index)
i = int
web = 'https://cafef.vn/'
response = requests.get(web)
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.get(web)
# soup = BeautifulSoup(response.content,"html.parser")
driver.maximize_window()
wait = WebDriverWait(driver, 100)

#TÌM MÃ CHỨNG KHOÁN (HOMEPAGE)
input_Ma_1 = driver.find_element(By.XPATH,"//div[@id='CafeF_BoxSearchNew']//input[@id='CafeF_SearchKeyword_Company']")
input_Ma_1.send_keys("AAA")

find_button = driver.find_element(By.XPATH,"//div[@id='CafeF_BoxSearchNew']//a")
find_button.click()
# print(linkMack)

for i in range(numDF):
    mack = DF['MACK'][i]
    # print(mack)
    print(i) 
    #TẠO FOLDER TRONG VÒNG FOR
    path = os.getcwd()
    isExist = os.path.exists(os.path.join(path,mack))
    if not isExist:
        os.makedirs(os.path.join(path,mack))


    #TÌM MÃ CHỨNG KHOÁN 'MACK'
    input_Ma_2 = driver.find_element(By.XPATH,"//div[@id='CafeF_BoxSearch']//input[@id='CafeF_SearchKeyword_Company']")
    input_Ma_2.send_keys(mack)
    #BẤM NÚT "TÌM KIẾM"
    find_button = driver.find_element(By.XPATH,"//div[@id='CafeF_BoxSearch']//input[@class='s-submit']")
    find_button.click()
    
     
    #TÌM VỊ TRÍ CHỨA BCTC
    find_BCTC_box = driver.find_element(By.XPATH,"//li[@id='liTabCongTy5CT']//a[@href]")
    find_BCTC_box.click()
    
    xpathLinks = (By.XPATH, "//div[@id='divDocument']//div[@class='treeview']//table//tbody//tr//td//a[@href]")
    urls = wait.until(EC.visibility_of_all_elements_located(xpathLinks))
    print(urls)
    for urlBCTC in urls:
        link_BCTC = urlBCTC.get_attribute("href")
        # print(link_BCTC)
        orginal_file_name = link_BCTC.split('/')[7]
        print(orginal_file_name)
        response = requests.get(link_BCTC)

        with open(orginal_file_name, "wb") as pdfFile:
            pdfFile.write(response.content)
    i=i+1        