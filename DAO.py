import os
from pathlib import Path
from datetime import datetime
from flatdict import FlatDict, FlatterDict
from Webscraping_Furnas.Bases import Bases
from Webscraping_Furnas.WebScraping import WebScraping
from Webscraping_Furnas.Debugging import Debugging
from Webscraping_Furnas.Connector_DataBase import Connector_dataBase
from datetime import datetime, timedelta
import json



class DAO:
    def __init__(self, debug: Debugging) -> None:
        self.conn = Connector_dataBase()
        self.debug = debug
        

    def insert(self, query: str) -> None:
        print(query)
        self.conn.connection_dataBase()
        try:
            #Creating a cursor object using the cursor() method
            cursor = self.conn.connection.cursor()
            # Executing the SQL command
            cursor.execute(query)

            # Commit your changes in the database
            self.conn.connection.commit()
            print('Commit da transação')

        except Exception as e:
            # Rolling back in case of error
            self.conn.connection.rollback()
            print(e)

        # Closing the connection
        cursor.close()
        self.conn.connection.close()
        print('Conexão fechada com sucesso!')


    def _consult(self, query: str) -> str:
        self.conn.connection_dataBase()
        try:
            cursor = self.conn.connection.cursor()
            cursor.execute(query)
            result = cursor.fetchone()
            obj_consult = str(result[0])
            return obj_consult
        
        except Exception as e:
            self.conn.connection.rollback()
            print(e)

        cursor.close()
        self.conn.connection.close()
        print('Conexão fechada com sucesso!')
        



    def _count(self, table: str) -> None:
        print(f"count from {table}")
        count = 0
        self.conn.connection_dataBase()
        try:
            #Creating a cursor object using the cursor() method
            cursor = self.conn.connection.cursor()
            # Executing the SQL command
            cursor.execute(f"select count(Id) from {table}")

            (count,) = cursor.fetchone()

        except Exception as e:
            print(e)

        # Closing the connection
        self.conn.connection.close()
        print('Conexão fechada com sucesso!')
        return count


    def ONS_Insert_Carga_Geracao_Nacional(self, data):
        # Query SELECT -> data_carga in BD WS_FURNAS
        sql_query = f"""
            SELECT data_carga FROM Carga_Geracao_Nacional ORDER BY data_obtencao DESC LIMIT 1;
        """
        sql_query_result = self._consult(sql_query)
        
        # data -> data_obtencao in data
        data_carga = data['lista_consumo']['data_carga']
        data_carga = datetime.strptime(data_carga, '%d/%m/%Y %H:%M').strftime('%Y-%m-%d %H:%M:00')

        print(type(data_carga))
        print(f'A data de obtencao da variável data é: {data_carga}')
        
        
        if sql_query_result != data_carga:
            energia = data['lista_consumo']

            # Datetime formatation
            data_carga_formatada = datetime.strptime(energia['data_carga'], '%d/%m/%Y %H:%M').strftime('%Y-%m-%d %H:%M:00')

            print('\n')
            print(energia)
            print('\n')

            sql_str = f"""
                INSERT INTO Carga_Geracao_Nacional(
                    data_carga,
                    data_obtencao,
                    carga_MW,
                    exportacao_MW,
                    ger_eolica_MW,
                    ger_hidraulica_MW,
                    ger_termica_MW,
                    ger_nuclear_MW,
                    ger_solar_MW,
                    importacao_MW
                )
                VALUES (
                    '{(data_carga_formatada)}',
                    '{(energia['data_obtencao'])}',
                    {(energia['Carga'][:-3]).replace(',', '.')},
                    {(energia['Exportação'][:-3]).replace(',', '.')},
                    {(energia['Ger. Eólica'][:-3]).replace(',', '.')},
                    {(energia['Ger. Hidráulica'][:-3]).replace(',', '.')},
                    {(energia['Ger. Térmica'][:-3]).replace(',', '.')},
                    {(energia['Ger. Nuclear'][:-3]).replace(',', '.')},
                    {(energia['Ger. Solar'][:-3]).replace(',', '.')},
                    {(energia['Importação'][:-3]).replace(',', '.')})
            """

            self.insert(sql_str)
            
            
        else:
            msg = 'Os dados são iguais a última captura e não serão inseridos no Banco de dados!'
            self.debug.print_info(message=msg, minLevel=Debugging.DEBUG_MAIN, printDefaultHandler=True)


        
     # -----------------------------------------------------------------------------------------------------------   


    def insert_regioes(self) -> None:
        if(self._count("Regiao") == 0):
            sql_insert_regioes = """INSERT INTO Regiao (nome) VALUES
                    ('Norte'),
                    ('Nordeste'),
                    ('Sudeste / Centro-Oeste'),
                    ('Sul')"""
            self.insert(sql_insert_regioes)


    # def ONS_Insert_Carga_Geracao_Regional(self, data):
    #     self.insert_regioes()

    #     # Query SELECT -> data_carga in BD WS_FURNAS
    #     sql_query = f"""
    #         SELECT data_carga FROM Carga_Geracao_Regional ORDER BY data_obtencao DESC LIMIT 1;
    #     """
    #     sql_query_result = self._consult(sql_query)
        
    #     # data -> data_obtencao in data
    #     data_carga = data['lista_consumo']['data_carga']
    #     data_carga = datetime.strptime(data_carga, '%d/%m/%Y %H:%M').strftime('%Y-%m-%d %H:%M:00')

    #     print(type(data_carga))
    #     print(f'A data de obtencao da variável data é: {data_carga}')
        
        
    #     if sql_query_result != data_carga:
    #         for i in range(0, len(data)):
    #             energia = data[i]['lista_consumo']

    #             # Datetime formatation
    #             data_carga_formatada = datetime.strptime(energia['data_carga'], '%d/%m/%Y %H:%M').strftime('%Y-%m-%d %H:%M:00')

    #             if (data[i]['regiao'] == 'Norte'):
    #                 sql_str_norte = f"""
    #                     INSERT INTO Carga_Geracao_Regional(
    #                         data_carga,
    #                         data_obtencao,
    #                         ger_total_MW,
    #                         ger_eolica_MW,
    #                         ger_hidraulica_MW,
    #                         ger_termica_MW,
    #                         ger_nuclear_MW,
    #                         ger_outros,
    #                         ger_solar_MW,
    #                         ger_verificada_MW,
    #                         id_regiao
    #                     )
    #                     VALUES (
    #                         '{(data_carga_formatada)}',
    #                         '{(energia['data_obtencao'])}',
    #                         {(energia['Total']).replace(',', '.')},
    #                         {(energia['Eólica']).replace(',', '.')},
    #                         {(energia['Hidráulica']).replace(',', '.')},
    #                         {(energia['Térmica']).replace(',', '.')},
    #                         NULL,
    #                         NULL,
    #                         {(energia['Solar']).replace(',', '.')},
    #                         {(energia['Verificada']).replace(',', '.')},
    #                         1
    #                     )
    #                 """
    #                 print('Regiao Norte')
    #                 self._insert(sql_str_norte)



    #             elif (data[i]['regiao'] == 'Nordeste'):
    #                 sql_str_nordeste = f"""
    #                     INSERT INTO Carga_Geracao_Regional(
    #                         data_carga,
    #                         data_obtencao,
    #                         ger_total_MW,
    #                         ger_hidraulica_MW,
    #                         ger_termica_MW,
    #                         ger_eolica_MW,
    #                         ger_solar_MW,
    #                         ger_verificada_MW,
    #                         ger_nuclear_MW,
    #                         ger_outros,
    #                         id_regiao
    #                     )
    #                     VALUES (
    #                         '{(data_carga_formatada)}',
    #                         '{(energia['data_obtencao'])}',
    #                         {(energia['Total']).replace(',', '.')},
    #                         {(energia['Hidráulica']).replace(',', '.')},
    #                         {(energia['Térmica']).replace(',', '.')},
    #                         {(energia['Eólica']).replace(',', '.')},
    #                         {(energia['Solar']).replace(',', '.')},
    #                         {(energia['Verificada']).replace(',', '.')},
    #                         NULL,
    #                         NULL,
    #                         2
    #                     )
    #                 """
    #                 print('Regiao Nordeste')
    #                 self._insert(sql_str_nordeste)


    #             elif (data[i]['regiao'] == 'Sudeste / Centro-Oeste'):
    #                 sql_str_sudeste = f"""
    #                     INSERT INTO Carga_Geracao_Regional(
    #                         data_carga,
    #                         data_obtencao,
    #                         ger_total_MW,
    #                         ger_hidraulica_MW,
    #                         ger_termica_MW,
    #                         ger_nuclear_MW,
    #                         ger_outros,
    #                         ger_solar_MW,
    #                         ger_eolica_MW,
    #                         ger_verificada_MW,
    #                         id_regiao
    #                     )
    #                     VALUES (
    #                         '{(data_carga_formatada)}',
    #                         '{(energia['data_obtencao'])}',
    #                         {(energia['Total']).replace(',', '.')},
    #                         {(energia['Hidráulica']).replace(',', '.')},
    #                         {(energia['Térmica']).replace(',', '.')},
    #                         NULL,
    #                         {(energia['Itaipu 50Hz']).replace(',', '.')},
    #                         {(energia['Solar']).replace(',', '.')},
    #                         {(energia['Eólica']).replace(',', '.')},
    #                         {(energia['Verificada']).replace(',', '.')},
    #                         3
    #                     )
    #                 """

    #                 print('Regiao Sudeste / Centro-Oeste')
    #                 self._insert(sql_str_sudeste)



    #             elif (data[i]['regiao'] == 'Sul'):
    #                 sql_str_sul = f"""
    #                     INSERT INTO Carga_Geracao_Regional(
    #                         data_carga,
    #                         data_obtencao,
    #                         ger_total_MW,
    #                         ger_hidraulica_MW,
    #                         ger_termica_MW,
    #                         ger_eolica_MW,
    #                         ger_solar_MW,
    #                         ger_verificada_MW,
    #                         ger_nuclear_MW,
    #                         ger_outros,
    #                         id_regiao
    #                     )
    #                     VALUES (
    #                         '{(data_carga_formatada)}',
    #                         '{(energia['data_obtencao'])}',
    #                         {(energia['Total']).replace(',', '.')},
    #                         {(energia['Hidráulica']).replace(',', '.')},
    #                         {(energia['Térmica']).replace(',', '.')},
    #                         {(energia['Eólica']).replace(',', '.')},
    #                         {(energia['Solar']).replace(',', '.')},
    #                         {(energia['Verificada']).replace(',', '.')},
    #                         NULL,
    #                         NULL,
    #                         4
    #                     )
    #                 """
    #                 print('Regiao Sul')
    #                 self._insert(sql_str_sul)
                    
    #         # Closing the connection
    #         self.conn.connection.close()
    #         print('Conexão fechada com sucesso!')


    #     else:
    #         msg = 'Os dados são iguais a última captura e não serão inseridos no Banco de dados!'
    #         self.debug.print_info(message=msg, minLevel=Debugging.DEBUG_MAIN, printDefaultHandler=True)





    # def IBGE_transform_PIB_taxa_acumulada(self, data):
    #     with open(data, encoding='utf-8') as f:
    #         data = json.load(f)
    #         dados_trimestrais = data['valuesMap']['Brasil']

    #         aux_year = list(dados_trimestrais.keys())
    #         year_list = []

        
    #         for i in range(0, len(aux_year), 4):
    #             year = int(aux_year[i][-4:])
    #             year_list.append(year)


    #         aux = list(dados_trimestrais.values())
    #         if len(aux) % 4 != 0:
    #             aux += ['0'] * (4 - len(aux) % 4)

    #         for i in range(0, len(aux), 4):
    #             tri_1 = aux[ i ]
    #             if (i + 1 < len(aux)):
    #                 tri_2 = aux[ i + 1]
    #             if (i + 2 < len(aux)):
    #                 tri_3 = aux[ i + 2]
    #             if (i + 3 < len(aux)):
    #                 tri_4 = aux[ i + 3]

                
    #             year = year_list[i // 4]

         
    #             sql_str = f'''
    #                 INSERT INTO PIB_Preco_Mercado(
    #                     ano,
    #                     trimestre_1,
    #                     trimestre_2,
    #                     trimestre_3,
    #                     trimestre_4
    #                 )
    #                 VALUES (
    #                     {year},
    #                     {float(tri_1.replace(',', '.'))},
    #                     {float(tri_2.replace(',', '.'))},
    #                     {float(tri_3.replace(',', '.'))},
    #                     {float(tri_4.replace(',', '.'))}
    #             )
    #             '''

    #             self._insert(sql_str)

    #         # Closing the connection
    #         self.conn.connection.close()
    #         print('Conexão fechada com sucesso!')


    # def EPE_tranform(self):
    #      pass


    # def INMET_transform(self):
    #      pass



# _____________________________________________________________________________________________________________
# TEST
# Call ONS_transform_Carga_Geracao_Nacional  
# ons_nacional = DAO(debug=Debugging)
# ons_nacional.ONS_Insert_Carga_Geracao_Nacional()
# ons_nacional.ONS_transform_Carga_Geracao_Nacional('Output\\ONS\\ONS_Carga_Geracao_Geral\\2024-01-08-09-42-43.json')

# Call ONS_transform_Carga_Geracao_Regional 
# ons_regional = Datas_to_Database()
# ons_regional.ONS_transform_Carga_Geracao_Regional('Output\\ONS\\ONS_Carga_Geracao_Setorizado\\2023-12-26-10-39-38.json')

# Call IBGE_transform_PIB_taxa_acumulada
# ibge_taxa_acumulada = Datas_to_Database()
# ibge_taxa_acumulada.IBGE_transform_PIB_taxa_acumulada('Output\\PIB_taxa_acumulada\\JSON\\20231226014153.json')