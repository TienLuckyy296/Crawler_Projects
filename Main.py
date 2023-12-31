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
i=0
web = 'https://cafef.vn/'
response = requests.get(web)
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.get(web)
# soup = BeautifulSoup(response.content,"html.parser")
driver.maximize_window()
wait = WebDriverWait(driver, 100)

def createFolder(mack):
    path = os.getcwd()
    isExist = os.path.exists(os.path.join(path,mack))
    if not isExist:
        os.makedirs(os.path.join(path,mack))
    
def searchMack(mack):
    #TÌM MÃ CHỨNG KHOÁN
    input_Ma = driver.find_element(By.XPATH,"//div[@id='CafeF_BoxSearchNew']//input[@id='CafeF_SearchKeyword_Company']")
    input_Ma.send_keys(mack)
    #BẤM NÚT "TÌM KIẾM"
    find_button = driver.find_element(By.XPATH,"//div[@id='CafeF_BoxSearchNew']//a")
    find_button.click()

    get_url = driver.current_url
    time.sleep(1000)
    return get_url

for i in range(numDF):
    mack = DF['MACK'][i]
    # print(mack)

    #TẠO FOLDER TRONG VÒNG FOR
    createFolder(mack)

    #TÌM MÃ CHỨNG KHOÁN 'MACK'
    linkMack = searchMack(mack)
    # print(linkMack)

    print(' in download file : ', linkMack)
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