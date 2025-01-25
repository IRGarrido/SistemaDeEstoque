from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = '12345'

def conectar_produto_db():
    conectar = sqlite3.connect('produtos.db')
    return conectar


def conectar_tipoProduto_db():
    conectar = sqlite3.connect('tipoProdutos.db')
    return conectar


def criar_tabela_produto():
    conectar = conectar_produto_db()
    cursor = conectar.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            Cod_Produto INTEGER PRIMARY KEY AUTOINCREMENT,
            Nome_Produto TEXT NOT NULL UNIQUE,
            EstoqueMinimo INTEGER NOT NULL,
            EstoqueAtual INTEGER NOT NULL,
            ValorVenda FLOAT NOT NULL,
            Cod_TipoProduto INTEGER,
            FOREIGN KEY (Cod_TipoProduto) REFERENCES tipoProdutos(Cod_TipoProduto)
        )      
    ''')
    conectar.commit()
    conectar.close()

def criar_tabela_tipoProduto():
    conectar = conectar_tipoProduto_db()
    cursor = conectar.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tipoProdutos (
            Cod_TipoProduto INTEGER PRIMARY KEY AUTOINCREMENT,
            Nome_TipoProduto TEXT NOT NULL UNIQUE
        );
    ''')

    cursor.execute('SELECT COUNT(*) FROM tipoProdutos')
    tamanhoTabela = cursor.fetchone()[0]
    
    if tamanhoTabela == 0:
        produtos = ['Higiene', 'Alimento','Bebida','Eletrônico','Papelaria']

        for produto in produtos:
            cursor.execute("INSERT INTO tipoProdutos (Nome_TipoProduto) VALUES (?) ", (produto,))

    conectar.commit()
    conectar.close()


@app.route('/')
def index():
    conectar = conectar_tipoProduto_db()
    cursor = conectar.cursor()
    cursor.execute('SELECT * FROM tipoProdutos ORDER BY (Nome_TipoProduto)')
    tiposProdutos = cursor.fetchall()
    conectar.close()
    return render_template('index.html', tiposProdutos=tiposProdutos)

@app.route('/adicionar_produto', methods=['POST'])
def adicionar_produto():
    if request.method == 'POST':
        nome = request.form['nomeProduto']
        estoqueMin = request.form['estoqueMinimo']
        estoqueAtual = 0
        valorVenda = request.form['valorVenda']
        tipoProduto = request.form['tipoProduto']

        conectar = conectar_produto_db()
        cursor = conectar.cursor()
        try:
            cursor.execute(
                'INSERT INTO produtos (Nome_Produto, EstoqueMinimo, EstoqueAtual, ValorVenda, Cod_TipoProduto) VALUES (?, ?, ?, ?, ?)', (nome, estoqueMin, estoqueAtual, valorVenda, tipoProduto)
            )

            conectar.commit()
            conectar.close()
            flash('Produto adicionado com sucesso!', 'sucess')
        except:
         flash('Produto inválido!', 'error')

        return redirect(url_for('index'))

@app.route('/tipoProduto')
def cadastroTipoDeProduto():
    return render_template('tipoProduto.html')

@app.route('/adicionar_tipoProduto', methods=['POST'])
def adicionar_tipoProduto():
    if request.method == 'POST':
        nome = request.form['nomeTipoProduto']
        conectar = conectar_tipoProduto_db()
        cursor = conectar.cursor()
        try:
            cursor.execute(
                'INSERT INTO tipoProdutos (Nome_TipoProduto) VALUES (?)', (nome,)
            )

            conectar.commit()
            conectar.close()
            flash('Tipo de produto adicionado com sucesso!', 'sucess')
        except:
            flash('Tipo de produto inválido!', 'error')

        return redirect(url_for('index'))


if __name__ == '__main__':
    criar_tabela_produto()
    criar_tabela_tipoProduto()
    app.run(debug=True)