import psutil
import pandas as pd
import time
import json
import os
from collections import defaultdict


# Funcoes opcionais para estudo

def get_resource_usage():
    """
    Mede o uso de CPU e memória do processo atual.

    Esta função usa a biblioteca `psutil` para medir o uso de CPU e memória
    do processo Python em execução. O uso de CPU é medido ao longo de um
    intervalo de 1 segundo, e o uso de memória é convertido para megabytes (MB).

    Returns:
        tuple: Uma tupla contendo:
            - cpu_usage (float): O uso de CPU em porcentagem.
            - memory_usage (float): O uso de memória em megabytes (MB).
    """
    process = psutil.Process()
    cpu_usage = process.cpu_percent(interval=1)
    memory_info = process.memory_info()
    memory_usage = memory_info.rss / (1024 ** 2)  # Convertendo para MB
    return cpu_usage, memory_usage


# Funcoes da solucao


def rename_columns(df):
    """
    Renomeia as colunas de um DataFrame, convertendo todas para minúsculas e substituindo espaços por underscores.

    Esta função toma um DataFrame como entrada e aplica duas transformações nas suas colunas:
    1. Converte todos os caracteres das colunas para minúsculas.
    2. Substitui espaços em branco nas colunas por underscores (_).

    Args:
        df (pd.DataFrame): DataFrame cujas colunas serão renomeadas.

    Returns:
        pd.DataFrame: O DataFrame com as colunas renomeadas.
    """
    df.columns = df.columns.str.lower().str.replace(' ', '_')
    return df


def read_csv_to_df(filename):
    """
    Lê um arquivo CSV em chunks, infere tipos de dados, filtra colunas necessárias e otimiza o uso de memória.
    Durante o carregamento dos chunks, calcula os seguintes resultados:
    1. Produto mais vendido em termos de quantidade e canal.
    2. País e região com o maior volume de vendas (em valor).
    3. Média de vendas mensais por produto.

    Args:
        filename (str): O caminho para o arquivo CSV.

    Returns:
        dict: Dicionário com os resultados das três perguntas em formato JSON.
    """
    # Colunas necessárias para as perguntas do desafio

    colunas_necessarias = ['Item Type', 'Units Sold', 'Sales Channel', 'Country', 'Region', 'Total Revenue',
                           'Order Date']

    # Carregar uma amostra para inferir tipos de dados
    flat_file = pd.read_csv(filename, low_memory=False, nrows=1000)
    types = flat_file.dtypes
    types = types.apply(str)

    dict_types = types.to_dict()

    # Inicializando estruturas para armazenar resultados intermediários
    vendas_por_produto_canal = defaultdict(int)
    vendas_por_pais_regiao = defaultdict(float)
    vendas_mensais_produto = defaultdict(lambda: defaultdict(int))

    for chunk in pd.read_csv(filename, low_memory=False, dtype=dict_types, chunksize=1000000,
                             usecols=colunas_necessarias):
        # Renomeando colunas
        chunk = rename_columns(chunk)

        # Convertendo 'order_date' para datetime
        chunk['order_date'] = pd.to_datetime(chunk['order_date'])

        # Otimizar inteiros
        ints = chunk.select_dtypes(include=['int64', 'int32', 'int16']).columns
        chunk[ints] = chunk[ints].apply(pd.to_numeric, downcast='integer')

        # Otimizar floats
        floats = chunk.select_dtypes(include=['float']).columns
        chunk[floats] = chunk[floats].apply(pd.to_numeric, downcast='float')

        # Otimizar objetos
        objects = chunk.select_dtypes('object').columns
        chunk[objects] = chunk[objects].apply(lambda x: x.astype('category'))

        # Atualizando vendas por produto e canal
        grouped_produto_canal = chunk.groupby(['sales_channel', 'item_type'], observed=True)['units_sold'].sum()
        for (sales_channel, item_type), units_sold in grouped_produto_canal.items():
            vendas_por_produto_canal[(sales_channel, item_type)] += units_sold

        # Atualizando vendas por país e região
        grouped_pais_regiao = chunk.groupby(['region', 'country'], observed=True)['total_revenue'].sum()
        for (region, country), total_revenue in grouped_pais_regiao.items():
            vendas_por_pais_regiao[(region, country)] += total_revenue

        # Atualizando vendas mensais por produto
        chunk['year_month'] = chunk['order_date'].dt.to_period('M')
        grouped_mensal_produto = chunk.groupby(['year_month', 'item_type'], observed=True)['units_sold'].sum()
        for (year_month, item_type), units_sold in grouped_mensal_produto.items():
            vendas_mensais_produto[year_month][item_type] += units_sold

    # Convertendo resultados para DataFrames
    df_vendas_por_produto_canal = pd.DataFrame.from_dict(vendas_por_produto_canal, orient='index',
                                                         columns=['units_sold']).reset_index()
    df_vendas_por_produto_canal[['sales_channel', 'item_type']] = pd.DataFrame(
        df_vendas_por_produto_canal['index'].tolist(), index=df_vendas_por_produto_canal.index)
    df_vendas_por_produto_canal = df_vendas_por_produto_canal.drop(columns=['index'])
    idx = df_vendas_por_produto_canal.groupby('sales_channel', observed=True)['units_sold'].idxmax()
    produto_mais_vendido_por_canal = df_vendas_por_produto_canal.loc[idx].reset_index(drop=True)

    df_vendas_por_pais_regiao = pd.DataFrame.from_dict(vendas_por_pais_regiao, orient='index',
                                                       columns=['total_revenue']).reset_index()
    df_vendas_por_pais_regiao[['region', 'country']] = pd.DataFrame(df_vendas_por_pais_regiao['index'].tolist(),
                                                                    index=df_vendas_por_pais_regiao.index)
    df_vendas_por_pais_regiao = df_vendas_por_pais_regiao.drop(columns=['index'])
    idx = df_vendas_por_pais_regiao['total_revenue'].idxmax()
    maior_volume_vendas_pais_regiao = df_vendas_por_pais_regiao.loc[idx].reset_index(drop=True)

    df_vendas_mensais_produto = pd.DataFrame(
        [(key, item_type, sum(units_sold.values())) for key, units_sold in vendas_mensais_produto.items() for item_type
         in units_sold.keys()], columns=['year_month', 'item_type', 'units_sold'])
    media_vendas_mensais_por_produto = df_vendas_mensais_produto.groupby('item_type')['units_sold'].mean().reset_index()
    media_vendas_mensais_por_produto.columns = ['item_type', 'average_monthly_units_sold']

    # Preparando os resultados para JSON
    resultados = {"produto_mais_vendido_por_canal": produto_mais_vendido_por_canal.to_dict(orient='records'),
        "maior_volume_vendas_pais_regiao": maior_volume_vendas_pais_regiao.to_dict(),
        "media_vendas_mensais_por_produto": media_vendas_mensais_por_produto.to_dict(orient='records')}

    chunk.info(memory_usage='deep')

    return json.dumps(resultados, indent=4)

def check_file_exists(file_path):
    """
    Verifica se o arquivo especificado existe no diretório atual.

    Args:
        file_path (str): O caminho do arquivo a ser verificado.

    Returns:
        bool: Retorna True se o arquivo existir, False caso contrário.
    """
    return os.path.isfile(file_path)

def main():
    file_path = 'vendas.csv'

    # Verifica se o arquivo existe
    if not check_file_exists(file_path):
        print("Raiz: Arquivo não encontrado. Arquivo vendas.csv deve estar no diretório raiz do projeto.")
        return

    # metricas de uso
    cpu_before, mem_before = get_resource_usage()
    print(f"Início = CPU: {cpu_before}% | Memória RAM: {mem_before:.2f} MB")

    start_time = time.time()

    resultados_json = read_csv_to_df(file_path)
    print(resultados_json)

    end_time = time.time()

    cpu_after, mem_after = get_resource_usage()
    elapsed_time = end_time - start_time
    print(f"{elapsed_time:.2f} segundos. CPU: {cpu_after}% | Memória RAM: {mem_after:.2f} MB | Uso Memória RAM:"
          f" {mem_after - mem_before:.2f}")


## Chamada com otimizacao

main()
