import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import time 

DF = pd.read_excel("FileBaoLoi.xlsx",sheet_name="test",usecols='A')
numDF = len(DF.index)
i=0
web = 'https://cafef.vn/'
#path = 'C:/Users//TienLN//Downloads//chromedriver-win64'

def createFolder(folderName):
    path = 'C:/Users/TienLN/cafef/'
    os.mkdir(os.path.join(path,folderName))
    
def searchMack(mack):
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get(web)
    #driver.maximize_window()

    #TÌM MÃ CHỨNG KHOÁN
    input_Ma = driver.find_element(By.XPATH,"//div[@id='CafeF_BoxSearchNew']//input[@id='CafeF_SearchKeyword_Company']")
    input_Ma.send_keys(mack)

    #BẤM NÚT "TÌM KIẾM"
    find_button = driver.find_element(By.XPATH,"//div[@id='CafeF_BoxSearchNew']//a")
    find_button.click()
 
    time.sleep(2)

for i in range(numDF):
    mack = DF['MACK'][i]
    print(mack)

    #TẠO FOLDER TRONG VÒNG FOR
    #createFolder(mack)

    #TÌM MÃ CHỨNG KHOÁN 'MACK'
    linkMack = searchMack(mack)
    print(linkMack)