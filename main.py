from flask import Flask, render_template, jsonify, request
import pandas as pd
import psycopg2
import matplotlib.pyplot as plt

app = Flask(__name__)

# Configurações do banco de dados
DB_CONFIG = {
    'dbname': 'seu_banco',        # Altere para o nome do seu banco
    'user': 'seu_usuario',        # Altere para seu usuário
    'password': 'sua_senha',      # Altere para sua senha
    'host': 'localhost',           # ou o endereço do seu servidor
    'port': '5432'                 # porta padrão do PostgreSQL
}


def get_data(filtro=None):
    conn = psycopg2.connect(**DB_CONFIG)
    query = "SELECT * FROM produtos"

    # Adiciona filtro à consulta, se presente
    if filtro:
        query += " WHERE nome ILIKE %s"  # ILIKE para case insensitive
        df = pd.read_sql_query(query, conn, params=(f'%{filtro}%',))
    else:
        df = pd.read_sql_query(query, conn)

    conn.close()
    return df

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/grafico')
def grafico():
    df = get_data()
    plt.figure()
    df.plot(kind='bar', x='nome', y='quantidade', legend=False)
    plt.title('Quantidade de Produtos')
    plt.xlabel('Produtos')
    plt.ylabel('Quantidade')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('static/grafico.png')  # Salva a imagem na pasta static
    plt.close()
    return jsonify({'url': 'static/grafico.png'})

@app.route('/produtos')
def lista_produtos():
    filtro = request.args.get('filtro', '')
    df = get_data(filtro)
    produtos = df.to_dict(orient='records')
    return render_template('produtos.html', produtos=produtos, filtro=filtro)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
