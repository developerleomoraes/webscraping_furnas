import json
import os
from pathlib import Path

class Bases:
    def __init__(self, fileFriendlyName: str = None, file_arg_name: str = None, 
                 source: str = None, baseURL: str = None,
                 outpath: str = None) -> None:
        self.fileFriendlyName = fileFriendlyName
        self.file_arg_name = file_arg_name
        if baseURL:
            self.baseURL = baseURL
        if source:
            self.source = source
        self.outpath = outpath
        # if not os.path.exists(outpath):
        #     os.makedirs(outpath)
            
    def toJSON(self) -> str:
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def __str__(self) -> str:
        return self.toJSON()

EPE_consumo_ee = Bases(
    fileFriendlyName='EPE consumo energia elétrica', 
    file_arg_name='EPE_consumo_ee',
    source='https://www.epe.gov.br/pt/publicacoes-dados-abertos/publicacoes/consumo-de-energia-eletrica',
    baseURL='https://www.epe.gov.br',
    outpath='Output/EPE_consumo_ee.xls'
)

INMET_clima_historico = Bases(
    fileFriendlyName='INMET clima - dados históricos',
    file_arg_name='INMET_clima_historico',
    source='https://portal.inmet.gov.br/uploads/dadoshistoricos/',
    baseURL='https://portal.inmet.gov.br/dadoshistoricos',
    outpath='Output/INMET_historico/'
)

PIB_taxa_acumulada = Bases(
    fileFriendlyName="IBGE PIB - taxa acumulada",
    file_arg_name='PIB_taxa_acumulada',
    source='https://www.ibge.gov.br/estatisticas/economicas/contas-nacionais/9300-contas-nacionais-trimestrais.html?=&t=series-historicas&utm_source=landing&utm_medium=explica&utm_campaign=pib#evolucao-taxa',
    baseURL='https://www.ibge.gov.br/pt/inicio.html',
    outpath='Output/PIB_taxa_acumulada'
)

ONS_Previsoes = Bases(
    fileFriendlyName="ONS - previsoes",
    file_arg_name='ONS_Previsoes',
    source='https://app.powerbi.com/view?r=eyJrIjoiZmZhOWE0NTYtYjc2NC00ZTAxLWJmZTEtNDYyZGE0ZjdlZWVlIiwidCI6IjNhZGVlNWZjLTkzM2UtNDkxMS1hZTFiLTljMmZlN2I4NDQ0OCIsImMiOjR9',
    baseURL='https://www.ons.org.br/',
    outpath='Output/ONS/ONS_Previsoes'
)

ONS_Carga_Geracao_Geral = Bases(
    fileFriendlyName="ONS - Carga e Geracao Geral",
    file_arg_name='ONS_Carga_Geracao_Geral',
    source='https://www.ons.org.br/paginas/energia-agora/carga-e-geracao',
    baseURL='https://www.ons.org.br/',
    outpath='Output/ONS/ONS_Carga_Geracao_Geral'
)

ONS_Carga_Geracao_Setorizado = Bases(
    fileFriendlyName="ONS - Carga e Geracao Setorizado",
    file_arg_name='ONS_Carga_Geracao_Setorizado',
    source='https://www.ons.org.br/paginas/energia-agora/balanco-de-energia',
    baseURL='https://www.ons.org.br/',
    outpath='Output/ONS/ONS_Carga_Geracao_Setorizado' 
)

ONS_Carga_Energia_Atendida = Bases(
    fileFriendlyName="ONS - Carga e Energia Atendida",
    file_arg_name='ONS_Carga_Energia_Atendida',
    source='https://www.ons.org.br/Paginas/resultados-da-operacao/historico-da-operacao/carga_energia.aspx',
    baseURL='https://www.ons.org.br/',
    outpath='Output/ONS/ONS_Carga_Energia_Atendida' 
)

bases_list = [
    EPE_consumo_ee,
    INMET_clima_historico, 
    PIB_taxa_acumulada,
    ONS_Previsoes,
    ONS_Carga_Geracao_Geral,
    ONS_Carga_Geracao_Setorizado,
    ONS_Carga_Energia_Atendida
]


"""
Array with all valid bases
"""
