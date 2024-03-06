import os
import traceback
import sys
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup
import requests
from Webscraping_Furnas.Bases import Bases
from Webscraping_Furnas.WebScraping import WebScraping
from Webscraping_Furnas.Debugging import Debugging
from datetime import datetime
import zipfile
import shutil
import time
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import glob

class PIB_taxa_acumulada(WebScraping):
    def __init__(self, base: Bases, debug: Debugging, simulation = False) -> None:
        super().__init__(base, debug)
        self.driver = self.get_driver()
        self.simulation = simulation

    def get_data(self, expiry: int = 90, simulation: bool = False) -> dict:
        self.get_content_Selenium()
        
        return self.get_dict_status(WebScraping.STATUS_SUCCESS)
    

    def get_content_Selenium(self) -> None:
        self.debug.print_info('selenium session starting...', minLevel= Debugging.DEBUG_MAIN)

        if(self.simulation):
            self.driver.get('file:///home/cenergel/Área de Trabalho/Furnas Project/webscrapingfurnas/tests/Sistema de Contas Nacionais Trimestrais _ IBGE.html')
            self.driver.implicitly_wait(20)
        else:
            self.driver.get(self.base.source)
            self.driver.implicitly_wait(20)
            

        # Selection button to downaload .pdf
        self.driver.implicitly_wait(20)
        self.driver.execute_script("window.scrollTo(0, 0);")
        select_btn = self.driver.find_element(By.XPATH, '//*[@id="evolucao-taxa"]/div[2]')
        select_btn.click()
        self.driver.implicitly_wait(20)

        btn_json_download = self.driver.find_element(By.XPATH, '//*[@id="tabelasidra201851171856341export"]/optgroup[1]/option[5]')
        btn_json_download.click()
        self.driver.implicitly_wait(20)
        
        self.wait_for_file() 

        self.driver.close()


        # Remove old files
        time.sleep(2)
        default_path = self.base.outpath
        list_arch = os.listdir(default_path)
    
        if len(list_arch) > 1:
            file_to_remove = os.path.join(default_path, list_arch[0])
            os.remove(file_to_remove)
        else:
            print('Não há arquivos suficientes para remover.')


        self.debug.print_info('selenium session ends', minLevel= Debugging.DEBUG_MAIN)


        
        