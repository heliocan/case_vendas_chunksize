import psutil
import pandas as pd
import time
import os


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


def read_horse(filename):
    """
    Lê arquivo sem pudor.

    Args:
        filename (str): O caminho para o arquivo CSV.
    """
    # Carregar uma amostra para inferir tipos de dados
    data = pd.read_csv(filename)
    data.info(memory_usage='deep')

    return data

def check_file_exists(file_path):
    """
    Verifica se o arquivo especificado existe no diretório atual.

    Args:
        file_path (str): O caminho do arquivo a ser verificado.

    Returns:
        bool: Retorna True se o arquivo existir, False caso contrário.
    """
    return os.path.isfile(file_path)

def main_hourse():
    file_path = 'vendas.csv'

    # Verifica se o arquivo existe
    if not check_file_exists(file_path):
        print("Raiz: Arquivo não encontrado. Arquivo vendas.csv deve estar no diretório raiz do projeto.")
        return

    # Métricas de uso
    cpu_before, mem_before = get_resource_usage()
    print(f"Início = CPU: {cpu_before}% | Memória RAM: {mem_before:.2f} MB")

    start_time = time.time()
    read_horse(file_path)
    end_time = time.time()

    cpu_after, mem_after = get_resource_usage()
    elapsed_time = end_time - start_time
    print(f"{elapsed_time:.2f} segundos. CPU: {cpu_after}% | Memória RAM: {mem_after:.2f} MB | Uso Memória RAM:"
          f" {mem_after - mem_before:.2f}")

# Chamada sem otimização
main_hourse()