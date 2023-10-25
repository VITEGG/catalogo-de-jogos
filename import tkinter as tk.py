import tkinter as tk
from tkinter import ttk
import sqlite3

def adicionar_jogo():
    nome = nome_entry.get()
    ano = ano_entry.get()
    plataforma = plataforma_entry.get()

    if nome and ano and plataforma:
        conn = sqlite3.connect("jogos.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO jogos (nome, ano, plataforma) VALUES (?, ?, ?)", (nome, ano, plataforma))
        conn.commit()
        conn.close()
        atualizar_lista_jogos()
        nome_entry.delete(0, tk.END)
        ano_entry.delete(0, tk.END)
        plataforma_entry.delete(0, tk.END)

def editar_jogo():
    jogo_selecionado = lista_jogos.selection()
    if jogo_selecionado:
        # Obtenha as informações do jogo selecionado na lista
        jogo_selecionado = lista_jogos.item(jogo_selecionado)
        jogo_info = jogo_selecionado['values']

        # Certifique-se de que o jogo tenha todas as informações necessárias
        if len(jogo_info) == 4:
            jogo_id, nome_anterior, ano_anterior, plataforma_anterior = jogo_info

            # Obtenha as novas informações dos campos de entrada
            novo_nome = nome_entry.get()
            novo_ano = ano_entry.get()
            nova_plataforma = plataforma_entry.get()

            if novo_nome and novo_ano and nova_plataforma:
                conn = sqlite3.connect("jogos.db")
                cursor = conn.cursor()

                # Execute a atualização com base no ID do jogo
                cursor.execute("UPDATE jogos SET nome=?, ano=?, plataforma=? WHERE id=?", (novo_nome, novo_ano, nova_plataforma, jogo_id))
                conn.commit()
                conn.close()

                # Atualize a lista de jogos
                atualizar_lista_jogos()
                nome_entry.delete(0, tk.END)
                ano_entry.delete(0, tk.END)
                plataforma_entry.delete(0, tk.END)

def excluir_jogo():
    jogo_selecionado = lista_jogos.selection()
    if jogo_selecionado:
        # Obtenha o ID do jogo a ser excluído
        jogo_selecionado = lista_jogos.item(jogo_selecionado)
        jogo_info = jogo_selecionado['values']
        if len(jogo_info) > 0:
            jogo_id = jogo_info[0]

            conn = sqlite3.connect("jogos.db")
            cursor = conn.cursor()

            # Execute a exclusão com base no ID do jogo
            cursor.execute("DELETE FROM jogos WHERE id=?", (jogo_id,))
            conn.commit()
            conn.close()

            # Atualize a lista de jogos
            atualizar_lista_jogos()
            nome_entry.delete(0, tk.END)
            ano_entry.delete(0, tk.END)
            plataforma_entry.delete(0, tk.END)

def pesquisar_jogo():
    pesquisa = pesquisa_entry.get()
    conn = sqlite3.connect("jogos.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jogos WHERE nome LIKE ?", ('%' + pesquisa + '%',))
    jogos = cursor.fetchall()
    conn.close()
    atualizar_lista_jogos(jogos)

def atualizar_lista_jogos(jogos=None):
    if jogos is None:
        conn = sqlite3.connect("jogos.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM jogos")
        jogos = cursor.fetchall()
        conn.close()
    lista_jogos.delete(*lista_jogos.get_children())
    for jogo in jogos:
        lista_jogos.insert("", "end", values=jogo)

root = tk.Tk()
root.title("Catalogador de Jogos")

# Cria a tabela no banco de dados se ela não existir
conn = sqlite3.connect("jogos.db")
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS jogos (
        id INTEGER PRIMARY KEY,
        nome TEXT,
        ano INTEGER,
        plataforma TEXT
    )
''')
conn.close()

frame_adicionar = ttk.LabelFrame(root, text="Adicionar Jogo")
frame_adicionar.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

nome_label = ttk.Label(frame_adicionar, text="Nome:")
nome_label.grid(row=0, column=0, padx=5, pady=5)
nome_entry = ttk.Entry(frame_adicionar)
nome_entry.grid(row=0, column=1, padx=5, pady=5)

ano_label = ttk.Label(frame_adicionar, text="Ano:")
ano_label.grid(row=1, column=0, padx=5, pady=5)
ano_entry = ttk.Entry(frame_adicionar)
ano_entry.grid(row=1, column=1, padx=5, pady=5)

plataforma_label = ttk.Label(frame_adicionar, text="Plataforma:")
plataforma_label.grid(row=2, column=0, padx=5, pady=5)
plataforma_entry = ttk.Entry(frame_adicionar)
plataforma_entry.grid(row=2, column=1, padx=5, pady=5)

adicionar_button = ttk.Button(frame_adicionar, text="Adicionar", command=adicionar_jogo)
adicionar_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

frame_editar = ttk.LabelFrame(root, text="Editar Jogo")
frame_editar.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

editar_button = ttk.Button(frame_editar, text="Editar", command=editar_jogo)
editar_button.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

excluir_button = ttk.Button(frame_editar, text="Excluir", command=excluir_jogo)
excluir_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

frame_pesquisar = ttk.LabelFrame(root, text="Pesquisar Jogo")
frame_pesquisar.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

pesquisa_label = ttk.Label(frame_pesquisar, text="Pesquisa:")
pesquisa_label.grid(row=0, column=0, padx=5, pady=5)
pesquisa_entry = ttk.Entry(frame_pesquisar)
pesquisa_entry.grid(row=0, column=1, padx=5, pady=5)

pesquisar_button = ttk.Button(frame_pesquisar, text="Pesquisar", command=pesquisar_jogo)
pesquisar_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

frame_lista = ttk.LabelFrame(root, text="Lista de Jogos")
frame_lista.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

colunas = ("ID", "Nome", "Ano", "Plataforma")
lista_jogos = ttk.Treeview(frame_lista, columns=colunas, show="headings")
for coluna in colunas:
    lista_jogos.heading(coluna, text=coluna)
    lista_jogos.column(coluna, width=100)
lista_jogos.grid(row=0, column=0, padx=5, pady=5)

scrollbar = ttk.Scrollbar(frame_lista, orient="vertical", command=lista_jogos.yview)
scrollbar.grid(row=0, column=1, sticky="ns")
lista_jogos.configure(yscrollcommand=scrollbar.set)

atualizar_lista_jogos()

root.mainloop()
