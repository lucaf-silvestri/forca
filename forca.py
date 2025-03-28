import random
import sqlite3
import sys
import unicodedata

from tabulate import tabulate
pontos = 0
vidas = 6
palavra_atual = False
palavra_escolhida = ""
letras_escolhidas = set()
oculto = ""
letra_escolhida = ""
primeira_vez = True

def iniciar(vidas):
    if vidas == 6:
        print("\n\n           -------------------")
        print("           -                 -")
        print("           -                 -")
        print("           -               -----")
        print("           -")
        print("           -")
        print("           -")
        print("           -")
        print("           _____\n\n")
    elif vidas == 5:
        print("\n\n           -------------------")
        print("           -                 -")
        print("           -                 -")
        print("           -               -----")
        print("           -                 O")
        print("           -")
        print("           -")
        print("           -")
        print("           _____\n\n")
    elif vidas == 4:
        print("\n\n           -------------------")
        print("           -                 -")
        print("           -                 -")
        print("           -               -----")
        print("           -                 O")
        print("           -                 |")
        print("           -")
        print("           -")
        print("           _____\n\n")
    elif vidas == 3:
        print("\n\n           -------------------")
        print("           -                 -")
        print("           -                 -")
        print("           -               -----")
        print("           -                 O")
        print("           -                /|")
        print("           -")
        print("           -")
        print("           _____\n\n")
    elif vidas == 2:
        print("\n\n           -------------------")
        print("           -                 -")
        print("           -                 -")
        print("           -               -----")
        print("           -                 O")
        print("           -                /|\ ")
        print("           -")
        print("           -")
        print("           _____\n\n")
    elif vidas == 1:
        print("\n\n           -------------------")
        print("           -                 -")
        print("           -                 -")
        print("           -               -----")
        print("           -                 O")
        print("           -                /|\ ")
        print("           -                /")
        print("           -")
        print("           _____\n\n")
    else:
        global palavra_atual
        palavra_atual = False
        print("\n\n           -------------------")
        print("           -                 -")
        print("           -                 -")
        print("           -               -----")
        print("           -                 O")
        print("           -                /|\ ")
        print("           -                / \ ")
        print("           -")
        print("           _____\n")
        print(f"           Você perdeu!!\n\n           A palavra era '{palavra_escolhida}'\n")

        final()
    
    if primeira_vez == True:
        palavra(vidas)
        
def final():
    nome = input("\nSeu nome: ")
    
    conexao = sqlite3.connect("palavras.db")
    cursor = conexao.cursor()
    cursor.execute('''
            INSERT INTO recordes (nome, pontos) VALUES (?, ?)
        ''', (nome, pontos))
    conexao.commit()
    cursor.execute("SELECT nome, pontos FROM recordes ORDER BY pontos DESC LIMIT 10")
    recordes = cursor.fetchall()
    ranking = [(i + 1, nome, pontos) for i, (nome, pontos) in enumerate(recordes)]
    conexao.close()
    
    headers = ["Posição", "Nome", "Pontos"]
    print(tabulate(ranking, headers=headers, tablefmt="fancy_grid"))
    
    print(f"\nObrigado por jogar! Você finalizou com {pontos} pontos.\n")
    sys.exit()

def remover_acentos(texto):
    return ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')

def palavra(vidas):
    global primeira_vez
    primeira_vez = False
    global palavra_atual
    global palavra_escolhida
    global oculto
    global letra_escolhida
    global pontos
    
    if palavra_atual == False:
        conexao = sqlite3.connect("palavras.db")
        cursor = conexao.cursor()
        cursor.execute("SELECT palavra FROM palavras")
        palavras = [remover_acentos(palavra[0].lower()) for palavra in cursor.fetchall()]
        conexao.close()
        palavra_escolhida = random.choice(palavras)
        palavra_atual = True
        
    oculto = ["_"] * len(palavra_escolhida)
    global letras_escolhidas
    
    print(f"Palavra: {' '.join(oculto)}")
    
    while "_" in oculto:
        letra_escolhida = input("Letra: ").lower()
        
        if letra_escolhida in letras_escolhidas:
            print("\nVocê já escolheu essa letra! Tente outra.")
            continue

        letras_escolhidas.add(letra_escolhida)
        
        if letra_escolhida not in palavra_escolhida:
            vidas = vidas - 1
            pontos = pontos - 10
            print("\n- 10 pontos\n")
            iniciar(vidas) 
        else:
            pontos = pontos + 10
            print("\n+ 10 pontos")
        
        for i in range(len(palavra_escolhida)):
                if palavra_escolhida[i] == letra_escolhida:
                    oculto[i] = letra_escolhida
            
        print(f"\nPalavra: {' '.join(oculto)}") 
        
    print("\nVocê venceu!!\n+ 100 pontos")
    pontos = pontos + 100
    print(f"\nPontuação: {pontos}\n")
    palavra_atual = False
    
    loop = True
    
    while loop == True:
        novamente = int(input("Deseja jogar novamente?\n1 - Sim\n2 - Não\n"))

        if novamente == 1:
            loop = False
            primeira_vez = True
            letras_escolhidas.clear()
            
            iniciar(6)
        elif novamente == 2:
            loop = False
            letras_escolhidas.clear()
            final()
        else:
            print("Resposta inválida.\n")
        
iniciar(vidas)