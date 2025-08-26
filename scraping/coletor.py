from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv
import os
import re
import pandas as pd
from datetime import datetime




#define o agent
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'

#define o header
#partes de uma requisição ou resposta HTTP que transmitem informações adicionais
#sobre a interação entre o cliente (por exemplo, o scraper) e o servidor web
headers = {'User-Agent': user_agent}


#usa a api economia da AwesomeAPI para converter o euro em real
def conversor_euro():
    load_dotenv()
    api_key = os.getenv("MINHA_API_KEY")
    api_moeda = f'https://economia.awesomeapi.com.br/last/EUR-BRL?token={api_key}'
    valor_euro = requests.get(api_moeda)
    if valor_euro.status_code != 200:
        print(f"Erro {valor_euro.status_code}: {valor_euro.text}")
        return None
    return float(valor_euro.json()['EURBRL']['bid'])


#Crealiza o Web Scraping
def coletar_livros(print_callback=None):
    #URL do site que será acessado
    url = 'https://books.toscrape.com/'
    valor_euro = conversor_euro()
    #faz uma requisição HTTP GET para o site especificado na URL
    #e passa os headers definidos anteriormente
    page = requests.request('GET', url = url, headers = headers)

    #verifica o status da requisição
    if page.status_code != 200:
        print(f"Erro {page.status_code}: {page.text}")
        return None

    #cria um objeto BeautifulSoup a partir do conteúdo da página
    #e especifica o parser "analisador" HTML a ser usado ('html.parser')
    soup_page = BeautifulSoup(page.text, 'html.parser')
    #descobre quantas páginas de livros o site tem
    quantidade_paginas = soup_page.find('li', attrs={'class': 'current'})
    match = re.search(r'of (\d+)', quantidade_paginas.text)
    if match:
        total_paginas = int(match.group(1))
    else:
        print("Não foi possível encontrar o total de páginas.")
        return None
    
    tabela_de_livros = []
    #passa por todas as páginas do site de acordo com a variavel quantidade_paginas 
    for i in range(total_paginas):
        msg = f'Página verificada: https://books.toscrape.com/catalogue/page-{i+1}.html'
        print(msg)
        #passa as páginas acessadas para o front
        if print_callback:
            print_callback(msg)
        page = requests.request('GET', url = f'https://books.toscrape.com/catalogue/page-{i+1}.html', headers = headers)
        #gera a soup da página
        soup_page = BeautifulSoup(page.text, 'html.parser')
        #gera a tabela soup dos livros encontrados
        tabela_de_livros_soup = soup_page.find('ol', attrs={'class': 'row'})
        #coleta as variaveis de cada livro e armazena na tabela_de_livros
        for element in tabela_de_livros_soup.find_all('li'):
            titulo_livro = element.h3.a['title']

            avaliacao = element.p['class'][1]
            word_to_num = {
            'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5,
            }
            avaliacao_num = word_to_num[avaliacao]
            preco_euro = element.find_all('p')[1].string
            # Remove todos os caracteres não numéricos, exceto vírgula e ponto
            preco_euro_tratado = float(re.sub(r'[^\d.]', '', preco_euro))
            preco = preco_euro_tratado * valor_euro
            preco_formatado = "%.2f" % preco

            estoque = element.find_all('p')[2].get_text(strip=True)

            livro = {
                'titulo_livro': titulo_livro,
                'avaliacao': avaliacao_num,
                'preco_em_reais': preco_formatado,
                'estoque': estoque
            }
            tabela_de_livros.append(livro)


    return tabela_de_livros

#função que cria os arquivos .csv de cada analise, com a data de quando foi executada
def salvar_csv(tabela_de_livros):
    data = datetime.now().strftime('%Y-%m-%d_%Hh%Mm%Ss')
    df = pd.DataFrame(tabela_de_livros)
    df.to_csv(f'data/livros_{data}.csv', index=False)
