# Benchmark RAPIDS

Objetivo deste projeto é realizar testes com diferentes engines de processamento de dados em **Python**, comparando suas performances em relação ao tempo de execução.

## Setup

Máquina
- Processandor: Ryzen 9 7900
- Memória RAM: 64G
- Placa de Vídeo: RTX 4080 Super ProArt (16G)

Ambiente
- Python: 3.12.8
- RAPIDS: 24.12
- Cuda: 12.4
- NVidia Driver: 550.120

- Arquivos para leitura:
    - csv     (8,2G / 81.672.501 de linhas)
    - parquet (3,4G / 81.672.501 de linhas)*

*para arquivos parquet fizemos outros testes, considerando arquivos de 1 milhão à 115 milhões.

## Método

### Testes
- pandas
- cudf.pandas

### Passos
1. Ler arquivo;
2. Realizar `groupby` da chave primária contando linhas;

### Análise

Foram executadas 12 medições de tempo de execução para cara configuração, sem concorrência entre as execuções.

Após a apuração dos valores, para cada experimento, removemos o maior e menor tempo, considerando os demais 10 valores.

Assim, calculamos a média, mediana e desvio padrão:

Isto é:

|Tipo Engine   | Tipo Arquivo   |   Média |   Desvio Padrão |   Mediana |    Rate |
|:------------:|:--------------:|--------:|----------------:|----------:|--------:|
|cudf-pandas   | parquet        |  1.0649 |          0.0058 |    1.0630 |  1.0000 |
|cudf-pandas   | csv            |  7.4592 |          0.0058 |    7.4590 |  7.0045 |
|pandas        | parquet        | 12.7809 |          0.2217 |   12.7336 | 12.0018 |
|pandas        | csv            | 63.5371 |          1.6020 |   63.7970 | 59.6640 |

Uma representação gráfica que pode ajudar na visualização dessas diferenças:

<img src="barplot.png" alt="Gráfico de barras comparando experimentos de performence em tempo">

Este resultado nos deixaram curiosos em relação ao o que acontece com diferentes tamanhos de arquivos. Isto é: será que a performance vai ser degradada de forma linear?

Neste momento refizemos o exeperimento, considerando apenas arquivos `parquet`, com diferentes números de linhas.

<img src="lineplot.png" alt="Gráfico de linhas comparando engine des processamento e quantidade de linhas" width=620px>

Notamos que com `pandas` a performance é degradada muito mais rapidamente, de formar linear. O mesmo não acontece com o `cudf-pandas`.

Vale dizer ainda que percebemos mais um evento interessante. Conforme o tamanho dos arquivos crescem, chega um momento que nossa GPU não comporta alocar todos dados em sua memória. Nesse momento, um degrau de degradação surge. Nossa hipótese é que neste ponto, a GPU começa a realizar trocas mais frequentes com a memória RAM, alocando chunks para conseguir processar todo volume necessário.

Ou seja, havendo uma maior quantidade de recursos disponíveis (VRAM), é provável que a performance seguira na mesma tendência. Ou seja, não começaria a degradar em passos exponenciais, como podemos observar quadno nos aproximamos de 100 milhões.


## Próximos passos

Adicionar novas engines de processamento, como:
- duckdb
- polars
- Apache Spark