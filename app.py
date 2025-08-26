from flask import Flask, render_template, request, redirect, url_for, send_file
import pandas as pd
import os
import ast
import io
import matplotlib.pyplot as plt
from analysis.estatisticas import calcular_estatisticas
from analysis.visualizacao import (
    graficos_distribuicao_precos,
    graficos_livros_avaliacao,
    graficos_mais_caros,
    graficos_mais_baratos,
    graficos_valores_estatisticos
)
from scraping.coletor import coletar_livros

app = Flask(__name__)


##homepage
@app.route("/", methods=["GET", "POST"])
def index():
    arquivos = [f for f in os.listdir("data") if f.endswith(".csv")]
    arquivo_selecionado = []
    mensagem = ""
    estatisticas = None
    df = None

    if request.method == "POST":
        acao = request.form.get("acao")
        
        if acao == "coletar":
            return redirect(url_for("coletando"))
        elif acao == "analisar":
            arquivo_selecionado = request.form.getlist("arquivo")
            if arquivo_selecionado:
                try:
                    dfs = [pd.read_csv(os.path.join("data", arq)) for arq in arquivo_selecionado]
                    df = pd.concat(dfs)
                    estatisticas = calcular_estatisticas(df)
                except Exception as e:
                    mensagem = f"Erro ao analisar arquivos: {str(e)}"
                    print(f"Erro: {e}")  # Log para depuração
                    estatisticas = None

    estatisticas_simples = {}
    outliers_html = ""
    media_por_avaliacao_html = ""
    if estatisticas:
        estatisticas_simples = {k: v for k, v in estatisticas.items() if not hasattr(v, "to_html")}
        outliers_html = estatisticas['outliers'].to_html() if not estatisticas['outliers'].empty else "Nenhum outlier encontrado."
        media_por_avaliacao_html = estatisticas['media_por_avaliacao'].reset_index().to_html(
    index=False,
    classes="table table-striped",
    float_format="%.2f",
    header=['Avaliação', 'Preço Médio (R$)']
)

    return render_template(
        "index.html",
        estatisticas=estatisticas_simples,
        outliers_html=outliers_html,
        media_por_avaliacao_html=media_por_avaliacao_html,
        df=df,
        arquivos=arquivos,
        arquivo_selecionado=arquivo_selecionado,
        mensagem=mensagem
    )

##rota de coleta
@app.route("/coletando")
def coletando():
    prints = []
    def print_callback(msg):
        prints.append(msg)
    tabela = coletar_livros(print_callback=print_callback)
    df_coletado = pd.DataFrame(tabela)
    nome_arquivo = f"livros_{pd.Timestamp.now().strftime('%Y-%m-%d_%Hh%Mm%Ss')}.csv"
    df_coletado.to_csv(os.path.join("data", nome_arquivo), index=False)
    mensagem = "Coleta realizada e arquivo salvo!"
    return render_template("coletando.html", prints=prints, mensagem=mensagem)

# Rotas para gráficos
def plot_to_response(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    plt.close(fig)
    return send_file(buf, mimetype='image/png')

#gera os gráficos com as funções de visualizacao.py
@app.route("/grafico/<tipo>/<arquivo>")
def grafico(tipo, arquivo):
    arquivo = ast.literal_eval(arquivo)
    for arquivo_abrir in arquivo:
        caminho = os.path.join("data", arquivo_abrir)
        df = pd.read_csv(caminho)
        if tipo == "distribuicao":
            
            fig = graficos_distribuicao_precos(df, return_fig=True)
        elif tipo == "avaliacao":
            fig = graficos_livros_avaliacao(df, return_fig=True)
        elif tipo == "caros":
            fig = graficos_mais_caros(df, return_fig=True)
        elif tipo == "baratos":
            fig = graficos_mais_baratos(df, return_fig=True)
        elif tipo == "estatisticas":
            fig = graficos_valores_estatisticos(df, return_fig=True)
        else:
            return "Tipo de gráfico inválido", 400
    #retorna para rotas
    return plot_to_response(fig)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")