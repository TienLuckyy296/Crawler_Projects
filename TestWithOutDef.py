from selenium import webdriver
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import time 
import requests
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

driver.maximize_window()
wait = WebDriverWait(driver, 1000)

for i in range(numDF):
    mack = DF['MACK'][i]

    #TẠO FOLDER TRONG VÒNG FOR
    path = os.getcwd()
    isExist = os.path.exists(os.path.join(path,mack))
    
    if not isExist:
        os.makedirs(os.path.join(path,mack))

    dir_path = os.path.join(path,mack)

    #TÌM MÃ CHỨNG KHOÁN 'MACK'
    input_Ma = driver.find_element(By.XPATH,"//div[@id='CafeF_BoxSearchNew']//input[@id='CafeF_SearchKeyword_Company']")
    input_Ma.send_keys(mack)

    #BẤM NÚT "TÌM KIẾM"
    find_button = driver.find_element(By.XPATH,"//div[@id='CafeF_BoxSearchNew']//a[@class='bt_search sprite s-submit']")
    find_button.click()
    
    #TÌM VỊ TRÍ CHỨA BCTC
    find_BCTC_box = driver.find_element(By.XPATH,"//li[@id='liTabCongTy5CT']//a")
    find_BCTC_box.click()
    
    xpathLinks = (By.XPATH, "//div[@id='divDocument']//div[@class='treeview']//table//tbody//tr//td//a")
    urls = wait.until(EC.visibility_of_all_elements_located(xpathLinks))

    for urlBCTC in urls:
        link_BCTC = urlBCTC.get_attribute("href")
        # print(link_BCTC)
        orginal_file_name = link_BCTC.split('/')[7]
        print('downloaded : ',orginal_file_name)
        response = requests.get(link_BCTC)

        with open(os.path.join(dir_path,orginal_file_name), "wb") as pdfFile:
            pdfFile.write(response.content)
        
    # RETURN_TO_HOMEPAGE
    home_button = driver.find_element(By.XPATH,"//div[@id='menu_wrap']//li[@class='bt_home active']//a")
    home_button.click()        