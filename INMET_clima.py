import os
import traceback
import sys
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup
import requests
from Webscraping_Furnas.WebScraping import WebScraping
from Webscraping_Furnas.Debugging import Debugging
from Webscraping_Furnas.Bases import Bases
from datetime import datetime
import zipfile
import shutil

class INMET_clima_historico(WebScraping):
    START_YEAR = 2000
    def __init__(self, base: Bases, debug: Debugging) -> None:
        super().__init__(base, debug)
        self.zip_year = str(INMET_clima_historico.START_YEAR)+'.zip'
        self.current_year = datetime.now().year
        Path(self.base.outpath).mkdir(parents=True, exist_ok=True)

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

    def file_exists(self) -> bool:
        f = os.path.join(self.base.outpath, self.zip_year)
        directory = self.filepath_without_extension(f)
        if os.path.isfile(f) or os.path.isdir(directory):
            self.debug.print_info(
                    "File already downloaded.", 
                    minLevel=Debugging.DEBUG_MAIN)
            return True
        return False

    def extract_zip_content(self, path: str, year: int, remove: bool) -> None:
        with zipfile.ZipFile(path, 'r') as z:
            for item in z.namelist():
                z.extract(item)
                if os.path.isfile(item):
                    year_dir = os.path.join(self.base.outpath, str(year))
                    Path(year_dir).mkdir(parents=True, exist_ok=True)
                    shutil.move(item, year_dir)
        if remove:
            os.remove(path)

    def get_data(self, expiry: int = 31, simulation: bool = False) -> dict:
        for year in range(INMET_clima_historico.START_YEAR, self.current_year + 1):
            self.zip_year = str(year)+'.zip'
            aux_expiry = -1 if year < self.current_year else expiry
            if self.need_update(aux_expiry, simulation) and not simulation:
                try:
                    href = os.path.join(self.base.source, self.zip_year)
                    self.debug.print_info(
                    'Request to ' + href, minLevel=Debugging.DEBUG_MAIN)
                    r = requests.get(href, allow_redirects=True)
                    aux_outpath = os.path.join(self.base.outpath, self.zip_year)
                    with open(aux_outpath, 'wb') as f:
                        f.write(r.content)
                    self.extract_zip_content(aux_outpath, year, False)
                except Exception:
                    print(traceback.format_exc())
                    return self.get_dict_status(WebScraping.STATUS_FAIL)
                self.debug.print_info(
                    'File downloaded to ' + aux_outpath, minLevel=Debugging.DEBUG_MAIN)
        return self.get_dict_status(WebScraping.STATUS_SUCCESS)