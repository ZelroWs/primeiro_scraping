# analysis/estoque.py
import pandas as pd
def analisar_estoque(df):
    # ... conta disponíveis, relaciona com preço/avaliação ...
    livro_status = {}
    for idx, row in df.iterrows():
        # Aqui você acessa cada linha, por exemplo:
        livro_status[row['titulo_livro']] = row['estoque']
    return livro_status

    

