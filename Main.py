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

# driver.maximize_window()
wait = WebDriverWait(driver, 10)

def createFolder(mack):
    path = os.getcwd()
    isExist = os.path.exists(os.path.join(path,mack))
    
    if not isExist:
        os.makedirs(os.path.join(path,mack))

    dir_path = os.path.join(path,mack)
    return dir_path    

def searchMack(mack):
    input_Ma = driver.find_element(By.XPATH,"//div[@id='CafeF_BoxSearchNew']//input[@id='CafeF_SearchKeyword_Company']")
    input_Ma.send_keys(mack)
    
    find_button = driver.find_element(By.XPATH,"//div[@id='CafeF_BoxSearchNew']//a[@class='bt_search sprite s-submit']")
    find_button.click()

def findFiles():
    find_BCTC_box = driver.find_element(By.XPATH,"//li[@id='liTabCongTy5CT']//a")
    find_BCTC_box.click()
    
    xpathLinks = (By.XPATH, "//div[@id='divDocument']//div[@class='treeview']//table//tbody//tr//td//a")
    urls = wait.until(EC.visibility_of_all_elements_located(xpathLinks))
    return urls   

def nameCut():
    for urlBCTC in findFiles():
        print('urlBCTC ============= ',urlBCTC)
        # link_BCTC = urlBCTC.get_attribute("href")
        orginal_file_name_2 = driver.find_element(By.XPATH,"//div[@id='divDocument']//div[@class='treeview']//table//tbody//tr[position()>1]//td[1]//text()")
        # orginal_file_name_1 = link_BCTC.split('/')[7]
        print('orginal_file_name_2 : ',orginal_file_name_2)
        response = requests.get(orginal_file_name_2)

        with open(os.path.join(createFolder(mack),orginal_file_name_2), "wb") as pdfFile:
            pdfFile.write(response.content)

def return_to_Homepage():
    home_button = driver.find_element(By.XPATH,"//div[@id='menu_wrap']//li[@class='bt_home active']//a")
    home_button.click()

for i in range(numDF):
    mack = DF['MACK'][i]
    # print(mack)

    #TẠO FOLDER TRONG VÒNG FOR
    createFolder(mack)

    #TÌM MÃ CHỨNG KHOÁN 'MACK'
    linkMack = searchMack(mack)
    # print(linkMack)

    findFiles()

    nameCut()

    return_to_Homepage()