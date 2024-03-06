"""
This file can be used to test access and make calls through the system.

If the source is not passed as a parameter, a fixed example user will be used.

For executions from other Python scripts, it is recommended to use the same
sequence presented here, but in an integrated way in the other script.
"""

from pathlib import Path
import sys
import argparse
import os
from datetime import datetime
import json
from Webscraping_Furnas.WebScraping import WebScraping
from Webscraping_Furnas.EPE import EPE_consumo_ee
from Webscraping_Furnas.INMET_clima import INMET_clima_historico
from Webscraping_Furnas.IBGE import PIB_taxa_acumulada
from Webscraping_Furnas.ONS import ONS_Previsoes
from Webscraping_Furnas.ONS import ONS_Carga_Geracao_Geral
from Webscraping_Furnas.ONS import ONS_Carga_Geracao_Setorizado
from Webscraping_Furnas.ONS import ONS_Carga_Energia_Atendida
from Webscraping_Furnas.DAO import DAO
from Webscraping_Furnas.Debugging import Debugging
import time
import logging
from Webscraping_Furnas.Bases import Bases, bases_list


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 'sim', 's', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'nao', 'n', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def main() -> None:
    start_time = time.time() 

    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--File", required=False,
                        help="File arg name. The options are: EPE_consumo_ee", type=str)
    ap.add_argument("-d", "--Debugging", type=str2bool, nargs='?', const=True, default=False,
                        help="Sets Debugging to Debugging.DEBUG_MAX")
                         
    args_, leftovers = ap.parse_known_args()
    if len(sys.argv) == 1:
        ap.print_help(sys.stderr)
        print("Using example values. Same as: ")
        print("""
                python -m MainWebScraping -f EPE_consumo_ee
            """)

    args = vars(ap.parse_args())
    file_arg_name = args['File'] if args['File'] else None
    #source = args['Source'] if args['Source'] else None

    Path("Logs").mkdir(parents=True, exist_ok=True)
    logging.basicConfig(filename='Logs/wsfurnas.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
    debugLevel = Debugging.DEBUG_MAX if args['Debugging'] else Debugging.DEBUG_MAIN
    debugging = Debugging(debugLevel)
    debugging.showBrowser = True

    if file_arg_name:
        base = [_base for _base in bases_list if _base.file_arg_name.lower() == file_arg_name.lower()][0]
   
    match base.file_arg_name.lower():
        case "epe_consumo_ee":
            scraping = EPE_consumo_ee(base, debugging)
        case "inmet_clima_historico":
            scraping = INMET_clima_historico(base, debugging)
        case "pib_taxa_acumulada":
            scraping = PIB_taxa_acumulada(base, debugging, simulation = False) 
        case "ons_previsoes":
            scraping = ONS_Previsoes(base, debugging) 
        case "ons_carga_geracao_geral":
            scraping = ONS_Carga_Geracao_Geral(base, debugging, simulation = False) 
        case "ons_carga_geracao_setorizado":
            scraping = ONS_Carga_Geracao_Setorizado(base, debugging, simulation = False)
        case "ons_carga_energia_atendida":
            scraping = ONS_Carga_Energia_Atendida(base, debugging, simulation = True)
        case "dao":
            scraping = DAO(debugging)
        case _:
            debugging.print_error(
                'file_arg_name not found: ' + str(self.base.file_arg_name))
            raise Exception("file_arg_name invalid")
    

    data = scraping.get_data()

    json_string = json.dumps(data, default=lambda x: x.__dict__,
                             sort_keys=False, indent=4)

    # Save json_string in log file `Log/wsfurnas.log` if debugging was created with at least
    # Debugging.DEBUG_MAIN. The printDefaultHandler parameter tell to debbuging print in
    # console even if debugging is created as Debugging.DEBUG_OFF.
    debugging.print_info(json_string, minLevel=Debugging.DEBUG_MAIN, printDefaultHandler=True)

    # Writes response JSON to file.
    today = datetime.now().strftime("%Y%m%d_%H%M%S")
    Path("Output/JSON").mkdir(parents=True, exist_ok=True)
    jsonOutpath = os.path.join("Output/JSON", f"{file_arg_name if file_arg_name else ''}_{str(today)}.json")
    with open(jsonOutpath, "w", encoding='utf-8') as jsonOut:
        jsonOut.write(json_string)

    print("MainWebScraping end")
    print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == '__main__':
    main()