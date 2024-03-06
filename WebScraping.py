import os
from bs4 import BeautifulSoup
import requests
import time
import json
from Webscraping_Furnas.Debugging import Debugging
from Webscraping_Furnas.Bases import Bases
from datetime import datetime
from pathlib import Path
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager, ChromeType
from webdriver_manager.firefox import GeckoDriverManager
from Webscraping_Furnas.Connector_DataBase import Connector_dataBase



class WebScraping:
    STATUS_NO_ACTION = 'no action needed'
    STATUS_SUCCESS = 'success'
    STATUS_FAIL = 'fail'
    
    def __init__(self, base: Bases, debug: Debugging) -> None:
        self.base = base
        self.debug = debug
        msg = ''.join(
            ("\n" * 2, '=' * 50, 'Beginning of scraping object', '=' * 50, "\n" * 2))
        self.debug.print_info(msg, minLevel=Debugging.DEBUG_MAIN)
        self.debug.print_info(
            "\n" + str(self.base.fileFriendlyName), minLevel=Debugging.DEBUG_MAIN)

    def modification_date(self) -> datetime:
        if self.base.outpath:
            if os.path.isfile(self.base.outpath):
                t = os.path.getmtime(self.base.outpath)
                return datetime.fromtimestamp(t)
            else:
                folder_stat = os.stat(self.base.outpath)
                modification_timestamp = folder_stat.st_mtime
                return datetime.fromtimestamp(modification_timestamp)
        return None
    
    def outdated_file(self, expiry_date_in_days: int = 31) -> bool:
        current_date = datetime.now()
        file_date = self.modification_date()
        timedelta = current_date - file_date
        return timedelta.days >= expiry_date_in_days and expiry_date_in_days > 0

    def file_exists(self) -> bool:
        if os.path.isfile(self.base.outpath):
            self.debug.print_info(
                    "File already downloaded.", 
                    minLevel=Debugging.DEBUG_MAIN)
            return True
        return False

    def get_dict_status(self, status: str) -> dict:
        return {
                'status': status,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'baseSource': self.base.source,
                'basefile_arg_name': self.base.file_arg_name,
                'filepath': self.base.outpath,
                'modificationDate': str(self.modification_date())
            }

    def need_update(self, expiry: int, simulation: bool) -> bool:
        if self.file_exists():
            if self.outdated_file(expiry_date_in_days=expiry):
                self.debug.print_info(
                    "Outdated file. A new one will be downloaded.", 
                    minLevel=Debugging.DEBUG_MAIN)
                if not simulation:
                    os.remove(self.base.outpath)
            else: 
                return False #self.get_dict_status(WebScraping.STATUS_NO_ACTION)
        return True

    def filepath_without_extension(self, filepath):
        return os.path.splitext(filepath)[0]

    def get_driver(self, browser: str = 'chrome') -> webdriver:        
        abspath = os.path.abspath(self.base.outpath)
        
        if browser.lower() in ('chrome', 'chromium'):
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_experimental_option("prefs", {
                "profile.default_content_setting_values.automatic_downloads": 1,
                "download.default_directory": abspath,
                "download.prompt_for_download": False,
                "plugins.always_open_pdf_externally": True,
                "start-maximized": False,
            })
            if not self.debug.showBrowser:
                chrome_options.add_argument('--headless')
                chrome_options.headless = True
            
       
            if browser.lower() == 'chrome':
                driver = webdriver.Chrome(options=chrome_options, service=ChromeService(ChromeDriverManager().install()))
            elif browser.lower() == 'chromium':
                ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
                driver = webdriver.Chrome(options=chrome_options)
        else:
            profile = webdriver.FirefoxProfile()
            profile.set_preference('browser.download.folderList', 2)
            profile.set_preference('browser.download.manager.showWhenStarting', False)
            profile.set_preference('browser.download.dir', abspath)
            profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/csv')
            driver = webdriver.Firefox(firefox_profile=profile, executable_path=GeckoDriverManager().install())
        #driver.maximize_window()
        return driver

    def get_content_Selenium(self) -> None:
        pass

    def wait_for_file(self):
        def pdf_exists(*xargs): #keep *xargs even without use it
            today = datetime.now().strftime("%Y%m%d_%H%M%S")
            if os.path.isfile(self.base.outpath):
                return True
            return False
        self.wait_for(pdf_exists, timeout=7, raiseExp=False)

    def wait_for(self, condition_function, timeout=8, xpathStr=None, expt_message='', raiseExp=True):
        start_time = time.time()
        found = False
        while time.time() < start_time + timeout and not found:
            if condition_function():
                found = True
            else:
                time.sleep(0.1)
        if raiseExp and not found:
            raise Exception(
                f'Timeout waiting for self.wait_for. Message: {expt_message}'
            )
        return found
    

