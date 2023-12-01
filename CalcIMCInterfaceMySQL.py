import tkinter as tk

import mysql.connector

# Função para conectar ao banco de dados e criar uma tabela se não existir
def conectar_bd():
    try:
        conexao = mysql.connector.connect(
            host="seu_host",
            user="seu_usuario",
            password="sua_senha",
            database="seu_banco_de_dados",
            port="sua_porta"
        )

        cursor = conexao.cursor()

        # Criar tabela se não existir
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS dados_pacientes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(255),
                endereco VARCHAR(255),
                altura FLOAT,
                peso FLOAT,
                imc FLOAT
            )
        """)

        conexao.commit()
        return conexao, cursor
    except mysql.connector.Error as err:
        print(f"Erro ao conectar ao banco de dados: {err}")
        return None, None

# Função para salvar os dados no banco de dados
def salvar_dados(nome, endereco, altura, peso, imc):
    conexao, cursor = conectar_bd()
    if conexao and cursor:
        try:
            # Inserir dados na tabela
            cursor.execute("""
                INSERT INTO dados_pacientes (nome, endereco, altura, peso, imc)
                VALUES (%s, %s, %s, %s, %s)
            """, (nome, endereco, altura, peso, imc))
            
            conexao.commit()
            print("Dados salvos no banco de dados.")
        except mysql.connector.Error as err:
            print(f"Erro ao salvar dados no banco de dados: {err}")
        finally:
            cursor.close()
            conexao.close()


def calcular_imc():
    try:
        altura = float(entry_altura.get()) / 100  # Convertendo a altura para metros
        peso = float(entry_peso.get())
        imc = peso / (altura ** 2)

        if imc < 17:
            resultado.set(f"IMC: {imc:.2f} - Muito abaixo do peso")
        elif 17 <= imc < 18.5:
            resultado.set(f"IMC: {imc:.2f} - Abaixo do peso")
        elif 18.5 <= imc < 25:
            resultado.set(f"IMC: {imc:.2f} - Peso normal")
        elif 25 <= imc < 30:
            resultado.set(f"IMC: {imc:.2f} - Acima do peso")
        elif 30 <= imc < 35:
            resultado.set(f"IMC: {imc:.2f} - Obesidade I")
        elif 35 <= imc < 40:
            resultado.set(f"IMC: {imc:.2f} - Obesidade II (severa)")
        else:
            resultado.set(f"IMC: {imc:.2f} - Obesidade III (mórbida)")
    except ValueError:
        resultado.set("Por favor, insira valores válidos.")


def reiniciar():
    entry_nome.delete(0, tk.END)
    entry_endereco.delete(0, tk.END)
    entry_altura.delete(0, tk.END)
    entry_peso.delete(0, tk.END)
    resultado.set("IMC: ")


def sair():
    root.quit()


root = tk.Tk()
root.geometry('450x200')
root.title("Cálculo de IMC - Índice de Massa Corporal")

# Labels e Entradas
tk.Label(root, text="Nome do paciente:").grid(row=0, column=0, sticky="w")
entry_nome = tk.Entry(root, width=45)
entry_nome.grid(row=0, column=1)

tk.Label(root, text="Endereço completo:").grid(row=1, column=0, sticky="w")
entry_endereco = tk.Entry(root, width=45)
entry_endereco.grid(row=1, column=1)

tk.Label(root, text="Altura (cm):").grid(row=2, column=0, sticky="w")
entry_altura = tk.Entry(root, width=45)
entry_altura.grid(row=2, column=1)

tk.Label(root, text="Peso (kg):").grid(row=3, column=0, sticky="w")
entry_peso = tk.Entry(root, width=45)
entry_peso.grid(row=3, column=1)

resultado = tk.StringVar()

resultado.set(" ")
tk.Entry(root, textvariable=resultado, state='readonly', width=45).grid(row=5, column=1)

# Botões
tk.Button(root, text="Calcular IMC", command=calcular_imc).grid(row=4, column=0, pady=10)
tk.Button(root, text="Reiniciar", command=reiniciar).grid(row=4, column=1, pady=10)
tk.Button(root, text="Sair", command=sair).grid(row=4, column=2, pady=10)

root.mainloop()