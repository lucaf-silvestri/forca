import sqlite3
from tabulate import tabulate
import pandas as pd

DB_NAME = "palavras.db"

def initialize_db():
    conn = sqlite3.connect('palavras.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS palavras (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            palavra TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recordes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            pontos INTERGER NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

# Função para cadastrar uma palavra
def add_printer(palavra):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO palavras (palavra) VALUES (?)
        ''', (palavra,))
        conn.commit()
        print(f"Palavra adicionada com sucesso.")
    except sqlite3.IntegrityError:
        print(f"Erro: Já existe uma palavra com esse IP.")
    except Exception as e:
        print(f"Erro ao adicionar palavra: {e}")
    finally:
        conn.close()

# Função para buscar todas as palavras
def get_all_palavras():
    """
    Retorna uma lista de todas as palavras no banco de dados.
    :return: Lista de dicionários com as informações das palavras
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT palavra FROM palavras')
    palavras = cursor.fetchall()
    conn.close()
    
    headers = ["Palavra"]
    return tabulate(palavras, headers=headers, tablefmt="fancy_grid")

def verRecordes():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM recordes')
    recordes = cursor.fetchall()
    conn.close()
    
    headers = ["ID", "Nome", "Pontos"]
    return tabulate(recordes, headers=headers, tablefmt="fancy_grid")

def cadastrar_excel():
    try:
        df = pd.read_excel('palavras.xlsx')
    except Exception as e:
        print(f"Erro ao ler a planilha: {e}")
        return
    
    # Verifica se as colunas necessárias estão presentes
    colunas_necessarias = {'palavra'}
    if not colunas_necessarias.issubset(df.columns):
        print(f"A planilha deve conter as seguintes colunas: {colunas_necessarias}")
        return
    
    # Conecta ao banco de dados
    conn = sqlite3.connect('palavras.db')
    cursor = conn.cursor()

    # Insere as palavras na tabela
    for _, row in df.iterrows():
        try:
            cursor.execute('''
                INSERT INTO palavras (palavra) VALUES (?)
            ''', (row['palavra'],))
        except Exception as e:
            print(f"Erro ao inserir a palavra {row['palavra']}: {e}")
    
    conn.commit()
    conn.close()
    print("Palavras cadastradas com sucesso!")

def apagarRecorde():
    conexao = sqlite3.connect("palavras.db")
    cursor = conexao.cursor()
    
    # Mostrar os recordes antes de apagar
    cursor.execute("SELECT id, nome, pontos FROM recordes")
    recordes = cursor.fetchall()

    if not recordes:
        print("\nNenhum recorde encontrado.")
        conexao.close()
        return

    print("\nRecordes disponíveis para exclusão:")
    for rec in recordes:
        print(f"ID: {rec[0]} | Nome: {rec[1]} | Pontos: {rec[2]}")
    
    # Pedir ao usuário o ID do recorde que deseja excluir
    try:
        id_escolhido = int(input("\nDigite o ID do recorde que deseja apagar: "))
        
        cursor.execute("DELETE FROM recordes WHERE id = ?", (id_escolhido,))
        conexao.commit()

        if cursor.rowcount > 0:
            print("\nRecorde apagado com sucesso!")
        else:
            print("\nNenhum recorde encontrado com esse ID.")

    except ValueError:
        print("\nID inválido! Digite um número válido.")

    conexao.close()

def apagarRecordes():
    conexao = sqlite3.connect("palavras.db")
    cursor = conexao.cursor()
    
    confirmacao = input("\nTem certeza que deseja apagar TODOS os recordes? (S/N): ").strip().lower()
    
    if confirmacao == "s":
        cursor.execute("DELETE FROM recordes")
        conexao.commit()
        print("\nTodos os recordes foram apagados com sucesso!")
    else:
        print("\nAção cancelada. Nenhum recorde foi apagado.")
    
    conexao.close()

sair = False

while sair == False:
    resposta = int(input("\nO que deseja fazer?\n1 - Buscar todas as palavras cadastradas\n2 - Cadastrar uma palavra\n3 - Cadastrar palavras através de planilha Excel\n4 - Buscar todos os recordes cadastrados\n5 - Deletar um recorde\n6 - Deletar todos os recordes\n7 - Sair\n"))
    
    if resposta == 1:
        print(get_all_palavras())
    elif resposta == 2:
        initialize_db()
        palavra = input("\nDigite a palavra: ")
        
        add_printer(palavra)
    elif resposta == 3:
        initialize_db()
        cadastrar_excel()
    elif resposta == 4:
        print(verRecordes())
    elif resposta == 5:
        apagarRecorde()
    elif resposta == 6:
        apagarRecordes()
    elif resposta == 7:
        sair = True
    else:
        print("Resposta inválida")

