import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def graficos_distribuicao_precos(df, return_fig=False):
    fig, ax = plt.subplots(figsize=(13,5))
    sns.histplot(df['preco_em_reais'].astype(float), bins=20, kde=True, ax=ax)
    ax.set_title('Distribuição dos Preços dos Livros')
    ax.set_xlabel('Preço (R$)')
    ax.set_ylabel('Quantidade')
    for p in ax.patches:
        ax.annotate(f'{int(p.get_height())}R$', 
                    (p.get_x() + p.get_width() / 2, p.get_height()), 
                    ha='center', va='bottom', fontsize=10, color='black')
    if return_fig:
        return fig
    plt.show()

def graficos_livros_avaliacao(df, return_fig=False):
    fig, ax = plt.subplots(figsize=(8,5))
    sns.countplot(x='avaliacao', data=df, ax=ax)
    ax.set_title('Quantidade de Livros por Avaliação')
    ax.set_xlabel('Avaliação (estrelas)')
    ax.set_ylabel('Quantidade')
    for p in ax.patches:
        ax.annotate(f'{int(p.get_height())}', 
                    (p.get_x() + p.get_width() / 2, p.get_height()), 
                    ha='center', va='bottom', fontsize=10, color='black')
    if return_fig:
        return fig
    plt.show()

def graficos_mais_caros(df, return_fig=False):
    df_sorted = df.sort_values(by='preco_em_reais', ascending=False)
    top_livros = df_sorted.head(5)
    fig, ax = plt.subplots(figsize=(10,5))
    sns.barplot(x='preco_em_reais', y='titulo_livro', data=top_livros, palette='Reds_r', ax=ax)
    ax.set_title('Top 5 Livros Mais Caros')
    ax.set_xlabel('Preço (R$)')
    ax.set_ylabel('Título do Livro')
    for i, v in enumerate(top_livros['preco_em_reais']):
        ax.text(v, i, f'R${v}', va='center', ha='left', fontsize=10, color='black')
    if return_fig:
        return fig
    plt.show()

def graficos_mais_baratos(df, return_fig=False):
    df_sorted = df.sort_values(by='preco_em_reais', ascending=False)
    bottom_livros = df_sorted.tail(5)
    fig, ax = plt.subplots(figsize=(10,5))
    sns.barplot(x='preco_em_reais', y='titulo_livro', data=bottom_livros, palette='Blues', ax=ax)
    ax.set_title('Top 5 Livros Mais Baratos')
    ax.set_xlabel('Preço (R$)')
    ax.set_ylabel('Título do Livro')
    for i, v in enumerate(bottom_livros['preco_em_reais']):
        ax.text(v, i, f'R${v}', va='center', ha='left', fontsize=10, color='black')
    if return_fig:
        return fig
    plt.show()

def graficos_valores_estatisticos(df, return_fig=False):
    preco_float = df['preco_em_reais'].astype(float)
    estatisticas = {
        'Média': preco_float.mean(),
        'Mediana': preco_float.median(),
        'Mínimo': preco_float.min(),
        'Máximo': preco_float.max()
    }
    fig, ax = plt.subplots(figsize=(8,5))
    sns.barplot(x=list(estatisticas.keys()), y=list(estatisticas.values()), palette='viridis', ax=ax)
    ax.set_title('Estatísticas dos Preços dos Livros')
    ax.set_ylabel('Preço (R$)')
    for i, v in enumerate(estatisticas.values()):
        ax.text(i, v, f'R${v:.2f}', ha='center', va='bottom', fontsize=10, color='black')
    if return_fig:
        return fig
    plt.show()