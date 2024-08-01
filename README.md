# Estudo de caso vendas.csv

## Prático

Temos os dois cenários (sem otimização e otimizado) para comparação de ganhos.

<div style="background-color: #f0f0f0; padding: 10px; border-left: 5px solid #007bff;">
🚨 Atenção: Necessário disponibilizar o arquivo <b>vendas.csv</b> no diretório raiz.
</div>

Arquivo [disponível aqui](https://www.notion.so/Testes-Engenheiro-de-Dados-30dc29e69ba74e04973ab0cd903e2920?pvs=4) para download.


### Executando sem otimização

Modo bruto, não recomendado. Criado somente para comparativo.

*Uso de armazenamento que seria despejado na memória: memory usage: 2.4 Gb.*

Arquivo **vendas_estudo_caso_horse.py** pode ser executado diretamente. 

Esperado o resulado em JSON, similar a:

<details>
  <summary>Clique para expandir</summary>

```json
Início = CPU: 0.0% | Memória RAM: 86.37 MB
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 5000000 entries, 0 to 4999999
Data columns (total 14 columns):
 #   Column          Dtype  
---  ------          -----  
 0   Region          object 
 1   Country         object 
 2   Item Type       object 
 3   Sales Channel   object 
 4   Order Priority  object 
 5   Order Date      object 
 6   Order ID        int64  
 7   Ship Date       object 
 8   Units Sold      int64  
 9   Unit Price      float64
 10  Unit Cost       float64
 11  Total Revenue   float64
 12  Total Cost      float64
 13  Total Profit    float64
dtypes: float64(5), int64(2), object(7)
memory usage: 2.4 GB
```

</details>

### Executando com otimização

Arquivo **vendas_estudo_caso.py** pode ser executado diretamente. 

*Uso de armazenamento que seria despejado na memória: memory usage: 29.6 Mb.*

Esperado o resulado em JSON, similar a

<details>
  <summary>Clique para expandir</summary>

```json
Início = CPU: 0.0% | Memória RAM: 87.20 MB
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 1000000 entries, 4000000 to 4999999
Data columns (total 8 columns):
 #   Column         Non-Null Count    Dtype         
---  ------         --------------    -----         
 0   region         1000000 non-null  category      
 1   country        1000000 non-null  category      
 2   item_type      1000000 non-null  category      
 3   sales_channel  1000000 non-null  category      
 4   order_date     1000000 non-null  datetime64[ns]
 5   units_sold     1000000 non-null  int16         
 6   total_revenue  1000000 non-null  float64       
 7   year_month     1000000 non-null  period[M]     
dtypes: category(4), datetime64[ns](1), float64(1), int16(1), period[M](1)
memory usage: 29.6 MB
{
    "produto_mais_vendido_por_canal": [
        {
            "units_sold": 1044443977,
            "sales_channel": "Offline",
            "item_type": "Cereal"
        },
        {
            "units_sold": 1044143121,
            "sales_channel": "Online",
            "item_type": "Snacks"
        }
    ],
    "maior_volume_vendas_pais_regiao": {
        "0": 36343889144.909996,
        "1": "Sub-Saharan Africa",
        "2": "Rwanda"
    },
    "media_vendas_mensais_por_produto": [
        {
            "item_type": "Baby Food",
            "average_monthly_units_sold": 193798103.15503877
        },
        {
            "item_type": "Beverages",
            "average_monthly_units_sold": 193798103.15503877
        },
        {
            "item_type": "Cereal",
            "average_monthly_units_sold": 193798103.15503877
        },
        {
            "item_type": "Clothes",
            "average_monthly_units_sold": 193798103.15503877
        },
        {
            "item_type": "Cosmetics",
            "average_monthly_units_sold": 193798103.15503877
        },
        {
            "item_type": "Fruits",
            "average_monthly_units_sold": 193798103.15503877
        },
        {
            "item_type": "Household",
            "average_monthly_units_sold": 193798103.15503877
        },
        {
            "item_type": "Meat",
            "average_monthly_units_sold": 193798103.15503877
        },
        {
            "item_type": "Office Supplies",
            "average_monthly_units_sold": 193798103.15503877
        },
        {
            "item_type": "Personal Care",
            "average_monthly_units_sold": 193798103.15503877
        },
        {
            "item_type": "Snacks",
            "average_monthly_units_sold": 193798103.15503877
        },
        {
            "item_type": "Vegetables",
            "average_monthly_units_sold": 193798103.15503877
        }
    ]
}
35.77 segundos. CPU: 0.0% | Memória RAM: 113.08 MB | Uso Memória RAM: 25.88

Process finished with exit code 0
```

</details>



## Teórico

**Autor:** Helio Candido da Silva Santos  
**Posição:** Eng. De Dados  
**Requisitos registrados em:** [Notion](https://www.notion.so/Testes-Engenheiro-de-Dados-30dc29e69ba74e04973ab0cd903e2920?pvs=4)  


Caros,  
Obrigado pela oportunidade! Foi muito legal brincar com esse desafio. É claro que existem N formas de fazer, e eu segui a prática e dicas do briefing!

### Observações sobre o pedido:
1. O arquivo possui 4.999.999 linhas, com cabeçalho totaliza 5 milhões de linhas, com tamanho total de ~609Mb;
2. Na ausência da dimensão “produto” ou “product”, foi utilizado o “item type”;
3. Na vida real, seria ótimo um momento de explorar melhorar as perguntas, para chegar mais perto do desejado. Então segui minha interpretação 😊.

### Fases em resumo
1. Exploração do arquivo (técnico e conceitual);
2. Elaboração do código python não otimizado para comparar com otimizado;
3. Início da elaboração do código otimizado conforme requisitos técnicos;
4. Testes de cenários com chunksize e streaming;
5. Escolha da abordagem (chunksize escolhido pela performance);
6. Ajustes para melhores cenários;
7. Conclusão

### Abordagem
Fazer a carga por streaming não me pareceu objetivo nem produtivo, foi ótimo para testar.  
Então preferi utilizar a carga por “pacotes de linhas” com chunksize. 

### Desafio
 
O desafio está em manter o uso da memória baixa, portanto odos os cálculos foram aproveitados em chunk, para ocupar o mínimo de memória alocada.

### Estratégia
1. Criação de dicionário prévio de 1000 linhas para identificação dos tipos;
2. Ajuste de tipos de dados, para o melhor desempenho de cada coluna;
3. Seleção apenas das colunas necessárias;
4. Carregamento com chunksize de 1 milhão de linhas (demonstrou ser o equilíbrio entre velocidade e tratamento dos cálculos);
5. Resposta em JSON.



