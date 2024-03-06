import os
import traceback
import sys
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup
import pandas as pd
import requests
import schedule
from IPython.display import display
from flatdict import FlatDict, FlatterDict
from Webscraping_Furnas.Bases import Bases
from Webscraping_Furnas.WebScraping import WebScraping
from Webscraping_Furnas.Debugging import Debugging
from Webscraping_Furnas.DAO import DAO
import zipfile
import shutil
from io import StringIO
import time
import tabula
from datetime import datetime, timedelta
import json
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException



# Function for ONS_Carga_Geracao_Setorizado Class
def get_dataTable_ONS_sectorized(driver, region: list) -> str:
    driver.implicitly_wait(10)
    page = BeautifulSoup(driver.page_source, 'html.parser')
    # Get Hour atualization
    data_carga_value = page.find('div', id = 'balanco_ctl00_ctl64_g_e7e5a0c7_d079_4494_a7fe_d06563f94fc5').find('h1').text.strip()
    data_carga_value = data_carga_value[20:]
    data_obtencao_value = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # realizar o acesso de hora de hora
    # Get sectorized table
    region_table = page.find('div', class_ = region)
    # Get Region
    name_table_region = region_table.find('h6').text.strip()


    consolidated_data = {}
    data_table = {
        'fonte': 'ONS',
        'regiao': '',
        'lista_consumo': {
            'data_carga': '',
            'data_obtencao': '',
        }
    }
    

    driver.implicitly_wait(5)


    # Add datas in table
    data_table['regiao'] = name_table_region
    data_table['lista_consumo']['data_carga'] = data_carga_value
    data_table['lista_consumo']['data_obtencao'] = data_obtencao_value


    # Get footer datas table
    driver.implicitly_wait(10)
    rows_content = region_table.find_all('li')
    for row in rows_content:
        key_element = row.find('p', class_ = 'total')
        value_element = row.find('p', class_ = 'total resp')

        if not key_element or not value_element:
            key_element = row.find('p')
            value_element = row.find('p', class_ = 'resp')

        if key_element and value_element:
            key = key_element.text.strip()
            value = value_element.text.strip()
            consolidated_data[key] = value

    
    data_table['lista_consumo'].update(consolidated_data)
    return data_table


# Monitor Function for ONS_Carga_Geracao_Setorizado and ONS_Carga_Geração_Geral
def monitor_element(driver, element_xpath) -> None:
    element = driver.find_element(By.XPATH, element_xpath)
    previous_element_state = element.text
    WebDriverWait(driver, 600).until(lambda driver: element_has_changed(driver, previous_element_state, element_xpath))


        
# Changed Element for ONS_Carga_Geracao_Setorizado Class
def element_has_changed(driver, previous_element_state: str, element_xpath) -> bool:
        try:
            actual_element = driver.find_element(By.XPATH, element_xpath)
            return actual_element.text != previous_element_state
        except StaleElementReferenceException:
            actual_element = driver.find_element(By.XPATH, element_xpath)  
        

        


# Page 1 -----------------------------------------------------------------------------------

class ONS_Previsoes(WebScraping):
    def __init__(self, base: Bases, debug: Debugging) -> None:
        super().__init__(base, debug)
        self.driver = self.get_driver()

        
    def get_data(self, expiry: int = 90, simulation: bool = False) -> dict:
        self.get_content_Selenium()

        time.sleep(2)
        # self.read_pdf()
        
        return self.get_dict_status(WebScraping.STATUS_SUCCESS)
    

    def get_content_Selenium(self) -> None:
        self.debug.print_info('selenium session starting...', minLevel= Debugging.DEBUG_MAIN)
        # First site
        self.driver.get(self.base.source) 
        self.driver.implicitly_wait(10)
    
        # Button to second page
        btn_prevision = self.driver.find_element(By.XPATH, '//*[@id="pvExplorationHost"]/div/div/exploration/div/explore-canvas/div/div[2]/div/div[2]/div[2]/visual-container-repeat/visual-container[1]/transform/div') # encontrar o xpath correto 
        btn_prevision.click()
        self.driver.implicitly_wait(10)

        # PDF Button
        btn_prevision = self.driver.find_element(By.XPATH, '//*[@id="pvExplorationHost"]/div/div/exploration/div/explore-canvas/div/div[2]/div/div[2]/div[2]/visual-container-repeat/visual-container[3]/transform/div') 
        btn_prevision.click()
        self.driver.implicitly_wait(20)
    
        self.wait_for_file()

        
        self.driver.close()
        self.debug.print_info('selenium session ends', minLevel= Debugging.DEBUG_MAIN)

        

    def read_pdf(self):
        pass
        # Page 5 ----------------------------------------------------------------------------------------
        # pdf_path = 'Output\ONS\ONS_Previsoes\Apresentação_Carga 2ª Rev Quadrim_Workshop 01-08-23.pdf'

        # df_page_5 = tabula.read_pdf(pdf_path, pages='5', encoding='ISO-8859-1')
        # print(f'O tamanho da table_list é: {len(df_page_5)}')
        
        # print('\n')
        # df_page_5_table = df_page_5[1]
        # print(type(df_page_5_table))
        # display(df_page_5_table)
        # print('\n')
        

        # for coluna in df_page_5_table.columns:
        #     if df_page_5_table[coluna].dtype == 'object':
        #         df_page_5_table[coluna] = df_page_5_table[coluna].str.replace('%', '').str.replace(',', '.')


        # columns_to_convert = ['2023', '2024', '2025', '2026', '2027']
        # df_page_5_table[columns_to_convert] = df_page_5_table[columns_to_convert].apply(pd.to_numeric, errors='coerce')
        # print('\n')
        # print(type(df_page_5_table))
        # display(df_page_5_table)
        
        # print('\n')
        # list_data_page_5 = df_page_5_table.to_dict(orient='records')
        # print(type(list_data_page_5))
        # print(list_data_page_5)

        # print('\n')
        # json_data_page_5 = json.dumps(list_data_page_5)
        # print(type(json_data_page_5))
        # print(json_data_page_5)


        


        # Page 7 ----------------------------------------------------------------------------------------
        # pdf_path = 'Output\ONS\ONS_Previsoes\Apresentação_Carga 2ª Rev Quadrim_Workshop 01-08-23.pdf'

        # df_page_7 = tabula.read_pdf(pdf_path, pages='7', encoding='ISO-8859-1')
        # print(f'O tamanho da table_list é: {len(df_page_7)}')
        # print(type(df_page_7))
        # display(df_page_7)
        # print('\n')
    
        # for table in df_page_7:
        #     table.columns = table.iloc[0]
        #     table = table.drop(0)
        #     table[[2023, 2024, 2025, 2026]] = table['2023 2024 2025 2026'].str.split(' ', expand = True)
        #     table = table.drop('2023 2024 2025 2026', axis = True)
        #     table = table[['Subsistemas', 2023, 2024, 2025, 2026, 2027]]


        # table_str_json = table.to_json(orient='records')
        # list_json = json.loads(table_str_json)
        # print(type(list_json))
        # print(list_json)
        # print('\n')
        
        # for i in list_json:
        #     for value in ['2023', '2024', '2025', '2026']:
        #         i[value] = int(i[value])

        # list_json = json.dumps(list_json)
        # print(type(list_json))
        # print(list_json)

        

        # # Page 8 ----------------------------------------------------------------------------------------
        # pdf_path = 'Output\ONS\ONS_Previsoes\Apresentação_Carga 2ª Rev Quadrim_Workshop 01-08-23.pdf'

        # df_page_8 = tabula.read_pdf(pdf_path, pages='8', encoding='ISO-8859-1')
        # print('\n')
        # print(f'O tamanho da table_list é: {len(df_page_8)}')
        # print('\n')
        

        # # 3_tables
        # df_page_8_table = df_page_8[1]
        # print(type(df_page_8_table))
        # display(df_page_8_table)
        # print('\n')

        # # Table_1 --------------------------------------------------------------------------------------------------------------------
        # table_1_page_8 = df_page_8_table[0:6]
        # quadrim_table_1 = table_1_page_8.columns[0]
        # #table_1_page_8.columns = table_1_page_8.iloc[0]
        # #table_1_page_8 = table_1_page_8.drop(0, axis='index') 
        # table_1_page_8.rename(columns = {2023.0:'2023', 2024.0:'2024', 2025.0:'2025', 2026.0:'2026', 2027.0:'2027'}, inplace=True)
        # print('\n')
        # print(type(table_1_page_8))
        # display(table_1_page_8)
        # print('\n')

        
        # json_data_table_1_page_8 = table_1_page_8.to_json(orient='records')
        # print(json_data_table_1_page_8)
        # print('\n')



        # Table 2 --------------------------------------------------------------------------------------------------------------------
        #df_page_8_table.columns = df_page_8_table.iloc[0]
        # table_2_page_8 = df_page_8_table[6:13]
        # print(type(table_2_page_8))
        # display(table_2_page_8)
        # print('\n')



        # Table_3
        


       
        
    
        



# Page 2 -----------------------------------------------------------------------------------

class ONS_Carga_Geracao_Geral(WebScraping):
    def __init__(self, base: Bases, debug: Debugging, simulation = False) -> None:
        super().__init__(base, debug)
        self.driver = self.get_driver()
        self.simulation = simulation

        
    def get_data(self, expiry: int = 90, simulation: bool = False) -> dict:
        while True:
            current_time = datetime.now().strftime("%H:%M")
            if current_time == '12:57':
                self.get_content_Selenium()
                return self.get_dict_status(WebScraping.STATUS_SUCCESS)
    
    

    def get_content_Selenium(self) -> None:
        self.debug.print_info('selenium session starting...', minLevel= Debugging.DEBUG_MAIN)

        if(self.simulation):
            self.driver.get('file:///home/cenergel/Área de Trabalho/Furnas Project/webscrapingfurnas/tests/Carga e Geração.html')
            self.driver.implicitly_wait(20)

        else:
            self.driver.get(self.base.source) 
            self.driver.implicitly_wait(20)



        while(True):
            # Close browser
            finish_browser = datetime.now().strftime("%H:%M")
            if finish_browser == '18:00':
                break


            # Get data with Beatifulsoap
            time.sleep(3)
            page = BeautifulSoup(self.driver.page_source, 'html.parser')
            charge_generation_table = page.find("div", class_="conteudo")
            rows = charge_generation_table.find_all('div', class_ = 'row')
            data_carga_value = charge_generation_table.find('h5').text.strip()
            data_obtencao_value = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            
            consolidated_data = {}
            data_table = {
                'fonte': 'ONS',
                'lista_consumo': {
                    'data_carga': '',
                    'data_obtencao': '',
                }
            }

            self.driver.implicitly_wait(20)

            data_table['lista_consumo']['data_carga'] = data_carga_value
            data_table['lista_consumo']['data_obtencao'] = data_obtencao_value

            
            for row in rows:
                key_element = row.find('span', class_ = 'p')
                value_element = row.find('span', class_ = 'r')

                if key_element and value_element:
                    key = key_element.text.strip().replace(':', '')
                    value = value_element.text.strip()
                    consolidated_data[key] = value
                    
            data_table['lista_consumo'].update(consolidated_data)

        

            element = '//*[@id="curva_ctl00_ctl64_g_2559304d_ec9c_4f80_abba_e53b97ebf8fc"]/h1/span'

            monitor_element(self.driver, element)
        
            self.wait_for_file()  

            dao = DAO(debug = Debugging)
            dao.ONS_Insert_Carga_Geracao_Nacional(data_table)
            
            self.debug.print_info('selenium session ends', minLevel= Debugging.DEBUG_MAIN)

    
        self.driver.close()


               



# Page 3 -----------------------------------------------------------------------------------

class ONS_Carga_Geracao_Setorizado(WebScraping):
    def __init__(self, base: Bases, debug: Debugging, simulation = False) -> None:
        super().__init__(base, debug)
        self.driver = self.get_driver()
        self.simulation = simulation


        
    def get_data(self, expiry: int = 90, simulation: bool = False) -> dict:
        while True:
            current_time = datetime.now().strftime("%H:%M")
            if current_time == '13:29': #14:22
                self.get_content_Selenium()
                time.sleep(3)
                return self.get_dict_status(WebScraping.STATUS_SUCCESS) 
       
                    
 

    def get_content_Selenium(self) -> None:
        self.debug.print_info('selenium session starting...', minLevel= Debugging.DEBUG_MAIN)

        if(self.simulation):
            self.driver.get('file:///home/cenergel/Área de Trabalho/Furnas Project/webscrapingfurnas/tests/Balanço de Energia.html')
            self.driver.implicitly_wait(20)

        else:
            self.driver.get(self.base.source)
            self.driver.implicitly_wait(20)


        
        data_table_final = []
        # current_date_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        # default_path = os.path.join(self.base.outpath, f'{current_date_time}.json')
    
        time.sleep(3)

        while(True):
            finish_browser = datetime.now().strftime("%H:%M")
            if finish_browser == '18:00':
                break
                           
            region = ['norte', 'nordeste', 'sudeste', 'sul']
            for i in range(0, len(region)):
                data_table_final.append(get_dataTable_ONS_sectorized(self.driver, region[i]))
                
            element = '//*[@id="balanco_ctl00_ctl64_g_e7e5a0c7_d079_4494_a7fe_d06563f94fc5"]/h1'
            monitor_element(self.driver, element)

                    
            self.wait_for_file()

            self.debug.print_info('selenium session ends', minLevel= Debugging.DEBUG_MAIN)

            # default for production = 60
            capture_time = 3

            if int(datetime.now().strftime("%M")) % capture_time == 0:
                # dao = DAO(debug = Debugging)
                # dao.ONS_Insert_Carga_Geracao_Regional(data_table_final)
                # chamar a classe DAO aqui pra mandar pro banco
                print(data_table_final)


        
        self.driver.close()



# Page 4 -----------------------------------------------------------------------------------
        
class ONS_Carga_Energia_Atendida(WebScraping):
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
            self.driver.get('file:///home/cenergel/furnas_project/webscrapingfurnas/tests/Páginas - Histórico da Operação.html')
            time.sleep(20)

        else:
            self.driver.get(self.base.source) 
            self.driver.implicitly_wait(20)


        # data_table_final = []


        # while(True):
        #     # Get data with Beatifulsoap
        #     time.sleep(3)
        #     page = BeautifulSoup(self.driver.page_source, 'html.parser')
        #     charge_generation_table = page.find("div", class_="conteudo")
        #     rows = charge_generation_table.find_all('div', class_ = 'row')
        #     data_carga_value = charge_generation_table.find('h5').text.strip()
        #     data_obtencao_value = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            
        #     consolidated_data = {}
        #     data_table = {
        #         'fonte': 'ONS',
        #         'lista_consumo': {
        #             'data_carga': '',
        #             'data_obtencao': '',
        #         }
        #     }

        #     self.driver.implicitly_wait(20)

        #     data_table['lista_consumo']['data_carga'] = data_carga_value
        #     data_table['lista_consumo']['data_obtencao'] = data_obtencao_value

            
        #     for row in rows:
        #         key_element = row.find('span', class_ = 'p')
        #         value_element = row.find('span', class_ = 'r')

        #         if key_element and value_element:
        #             key = key_element.text.strip().replace(':', '')
        #             value = value_element.text.strip()
        #             consolidated_data[key] = value
                    
        #     data_table['lista_consumo'].update(consolidated_data)

        #     data_table_final.append(data_table)

        #     element = '//*[@id="curva_ctl00_ctl64_g_2559304d_ec9c_4f80_abba_e53b97ebf8fc"]/h1/span'
        
        #     monitor_element(self.driver, element)
        
        #     self.wait_for_file()  


        #     current_date_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        #     default_path = os.path.join(self.base.outpath, f'{current_date_time}.json') #f'{self.base.outpath}/{current_date_time}.json'
        #     save_json(data_table_final, default_path)
    

        #     #self.driver.close()
        #     self.debug.print_info('selenium session ends', minLevel= Debugging.DEBUG_MAIN)


