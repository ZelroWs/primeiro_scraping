#Calcular média, mediana, mínimo e máximo dos preços dos livros.
#Comparar preços por avaliação (livros com mais estrelas são mais caros?).
#Identificar livros fora do padrão de preço (outliers).

def calcular_estatisticas(df):
    estatisticas = {}
    estatisticas['media'] = round(df['preco_em_reais'].astype(float).mean(), 2)
    estatisticas['mediana'] = round(df['preco_em_reais'].astype(float).median(), 2)
    estatisticas['minimo'] = round(df['preco_em_reais'].astype(float).min(), 2)
    estatisticas['maximo'] = round(df['preco_em_reais'].astype(float).max(), 2)
    # Outliers (exemplo usando desvio padrão)
    preco = df['preco_em_reais'].astype(float)
    estatisticas['outliers'] = df[(preco < preco.mean() - 2*preco.std()) | (preco > preco.mean() + 2*preco.std())]
    # Comparação por avaliação
    estatisticas['media_por_avaliacao'] = df.groupby('avaliacao')['preco_em_reais'].mean().round(2)
    return estatisticas