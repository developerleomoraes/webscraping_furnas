import os
import traceback
import sys
from bs4 import BeautifulSoup
import requests
from Webscraping_Furnas.WebScraping import WebScraping
from Webscraping_Furnas.Debugging import Debugging
from Webscraping_Furnas.Bases import Bases
from datetime import datetime

class EPE_consumo_ee(WebScraping):
    def __init__(self, base: Bases, debug: Debugging) -> None:
        super().__init__(base, debug)

    def get_data(self, expiry: int = 31, simulation: bool = False) -> dict:
        if self.need_update(expiry, simulation) and not simulation:
            try:
                soup = BeautifulSoup(requests.get(
                    self.base.source, allow_redirects=True).content, "html.parser")
                for a_tag in soup.findAll("a"):
                    href = self.base.baseURL + a_tag.attrs.get("href")
                    if href.endswith(('.xls', '.xlsx', '.csv')):
                        break
                self.debug.print_info(
                    'Request to ' + href, minLevel=Debugging.DEBUG_MAIN)
                r = requests.get(href, allow_redirects=True)
                with open(self.base.outpath, 'wb') as f:
                    f.write(r.content)
            except Exception:
                print(traceback.format_exc())
                return self.get_dict_status(WebScraping.STATUS_FAIL)
        self.debug.print_info(
            'File downloaded to ' + str(self.base.outpath), minLevel=Debugging.DEBUG_MAIN)
        return self.get_dict_status(WebScraping.STATUS_SUCCESS)