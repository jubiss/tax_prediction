import pandas as pd
import sys,os
sys.path.append(os.getcwd())

from src.utils import static_transformations as st
from src.utils import utils
def format_raw_intern(save=False, file_name='internal_table'):

    entrada_produto = pd.read_csv('data/raw/ENTRADA_PRODUTO.csv')
    entrada = pd.read_csv('data/raw/ENTRADA.csv')
    pessoa = pd.read_csv('data/raw/PESSOA.csv')
    produto = pd.read_csv('data/raw/PRODUTO.csv')

    pessoa = pessoa[['ID', 'NOME', 'UF', 'CNPJ_CPF']].rename(columns={'ID': 'ID_PESSOA', 'NOME': 'NOME_EMPRESA'})
    entrada = entrada[entrada['DATA'] > '2021-01-01'][['ID', 'ID_PESSOA', 'NUMERO', 'FRETE']].rename(columns={'ID': 'ID_ENTRADA'})
    entrada_produto = entrada_produto[['ID_PRODUTO', 'ID_ENTRADA', 'TOTAL', 'CFOP', 'VALORIPI', 'VALORICMSSUBST']].rename(columns={'TOTAL': 'PRECO_COMPRA'})
    entrada_produto['TOTAL COM IMPOSTOS'] = entrada_produto['PRECO_COMPRA'] + entrada_produto['VALORIPI'] + entrada_produto['VALORICMSSUBST']
    produto = produto[['ID', 'NOME', 'CEST', 'CODIGONCM']].rename(columns={'ID': 'ID_PRODUTO', 'NOME': 'NOME_PRODUTO'})

    internal_processed_table = pessoa.merge(entrada, how='inner', on=['ID_PESSOA'])
    internal_processed_table = internal_processed_table.merge(entrada_produto, how='inner', on=['ID_ENTRADA'])
    internal_processed_table = internal_processed_table.merge(produto, how='inner', on=['ID_PRODUTO'])
    internal_processed_table['CEST'] = internal_processed_table['CEST'].fillna(0).astype(str)
    internal_processed_table['CNPJ_CPF'] = internal_processed_table['CNPJ_CPF'].astype(str)
    if save:
        utils.save_csv(internal_processed_table, filepath_name=f'data/processed/{file_name}.csv', save=save)
    return internal_processed_table

def format_raw_external_data(save=False, file_name='external_table'):
    fronteira_list = []
    for i in range(3,6):
        fronteira_list.append(pd.read_excel(rf'data\external\0{str(i)}-2023_extrato_fronteira_juliana.xlsx'))
    fronteira = pd.concat(fronteira_list).reset_index(drop=True)
    fronteira['VALOR DA NF'] = fronteira['VALOR DA NF'].apply(st.convert_valor_bad_format_to_float)
    fronteira['ICMS DEVIDO'] = fronteira['ICMS DEVIDO'].apply(st.convert_valor_bad_format_to_float)
    fronteira['CNPJ'] = fronteira['CNPJ EMITENTE'].apply(st.format_cnpj_to_int)
    fronteira['NOTA FISCAL'] = fronteira['NOTA FISCAL'].astype(int)
    fronteira = fronteira.drop(columns=['DATA PASSAGEM', 'REGISTRO DE NOTA', 'CNPJ EMITENTE', 'UF'])
    fronteira = fronteira.rename(columns={"NOTA FISCAL": "NUMERO", "CNPJ": "CNPJ_CPF"})
    fronteira['CNPJ_CPF'] = fronteira['CNPJ_CPF'].astype(str)
    external_processed_table = fronteira
    if save:
        utils.save_csv(external_processed_table, filepath_name=f'data/processed/{file_name}.csv', save=save)
    return external_processed_table

def merge_internal_external_data(save=False, file_name='final_table'):
    intern_data = format_raw_intern(save=save, file_name='internal_table')
    external_data = format_raw_external_data(save=save, file_name='external_table')

    int_ext_data = intern_data.merge(external_data, how='inner', on=['NUMERO', 'CNPJ_CPF'])
    int_ext_data = int_ext_data[['CEST', 'CODIGONCM', 'UF', 'ICMS DEVIDO', 'NUMERO', 
                                 'TOTAL COM IMPOSTOS', 'FRETE', 'CNPJ_CPF']]
    int_ext_data.loc[::,'CODIGONCM'] = int_ext_data['CODIGONCM'].astype(int).astype(str)

    if save:
        utils.save_csv(int_ext_data, filepath_name=f'data/processed/{file_name}.csv', save=save)
    return int_ext_data

if __name__ == '__main__':
    merge_internal_external_data(save=True, file_name='nfe_das_data')