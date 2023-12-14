from selenium import webdriver
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import time 
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

web = 'https://cafef.vn/'
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.get(web)
response = requests.get(web)
soup = BeautifulSoup(response.content,"html.parser")
driver.maximize_window()

find_box = driver.find_element(By.XPATH,"//div[@id='CafeF_BoxSearchNew']")
input_Ma = find_box.find_element(By.XPATH,".//input[@id='CafeF_SearchKeyword_Company']")

input_Ma.send_keys("AAT")

find_button = driver.find_element(By.XPATH,"//div[@id='CafeF_BoxSearchNew']//a")
find_button.click()

find_BCTC_box = driver.find_element(By.XPATH,"//li[@id='liTabCongTy5CT']//a[@href]")
find_BCTC_box.click()

find_BCTC_board = driver.find_elements(By.XPATH,"//div[@id='divDocument']//div[@class='treeview']//table//tbody//tr//td//a[@href]")
# time.sleep(10)

urls = WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.XPATH, "//div[@id='divDocument']//div[@class='treeview']//table//tbody//tr//td//a[@href]")))
for urlBCTC in urls:
    link_BCTC = urlBCTC.get_attribute("href")
    #print(urlBCTC.get_attribute("href"))
    for link in link_BCTC:
        response = requests.get(link_BCTC)

        with open("download.pdf", "wb") as pdfFile:
            pdfFile.write(response.content)
    
#time.sleep(1000)