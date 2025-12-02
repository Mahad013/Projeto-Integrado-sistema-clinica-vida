import os
import re
import sqlite3
from collections import deque
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

# ------------------------ FILAS ------------------------
fila_consulta = deque()
fila_emergencia = deque()
pacientes_cache = []
consultas_cache = []

# ------------------------ BANCO DE DADOS ------------------------
def init_db():
    conn = sqlite3.connect("clinica.db")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            idade INTEGER,
            telefone TEXT,
            cpf TEXT UNIQUE,
            rg TEXT,
            medico TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS consultas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paciente_id INTEGER,
            tipo TEXT,
            horario TEXT,
            FOREIGN KEY(paciente_id) REFERENCES pacientes(id)
        )
    """)

    conn.commit()
    conn.close()

# ------------------------ LIMPAR TELA ------------------------
def limpar():
    os.system("cls" if os.name == "nt" else "clear")

# ------------------------ FORMATAÇÃO ------------------------
def formatar_telefone(tel):
    tel = re.sub(r'\D', '', tel)
    if len(tel) == 11:
        return f"({tel[:2]}) {tel[2:7]}-{tel[7:]}"
    elif len(tel) == 10:
        return f"({tel[:2]}) {tel[2:6]}-{tel[6:]}"
    return None

def formatar_cpf(cpf):
    cpf = re.sub(r'\D', '', cpf)
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}" if len(cpf) == 11 else None

def formatar_rg(rg):
    rg = re.sub(r'\D', '', rg)
    return f"{rg[:2]}.{rg[2:5]}.{rg[5:8]}-{rg[8:]}" if len(rg) == 9 else None

# ------------------------ VALIDAR DOCUMENTOS ------------------------
def documentos_validos(cpf, rg):
    return formatar_cpf(cpf) is not None and formatar_rg(rg) is not None

# ------------------------ OBTER PACIENTE (por CPF) ------------------------
def obter_paciente_por_cpf(cpf):
    conn = sqlite3.connect("clinica.db")
    c = conn.cursor()

    c.execute("SELECT * FROM pacientes WHERE cpf=?", (cpf,))
    dados = c.fetchone()

    conn.close()

    if dados:
        return {
            "id": dados[0],
            "nome": dados[1],
            "idade": dados[2],
            "telefone": dados[3],
            "cpf": dados[4],
            "rg": dados[5],
            "medico": dados[6]
        }

    return None

# ------------------------ VERIFICAR ATENDIMENTO ------------------------
def verificar_atendimento(p):

    print("\n--- STATUS DOS DOCUMENTOS ---")
    B = documentos_validos(p["cpf"], p["rg"])
    print("CPF válido:", "SIM" if B else "NÃO")
    print("RG válido:", "SIM" if B else "NÃO")

    if not B:
        print("\nDOCUMENTOS INVÁLIDOS! NÃO pode ser atendido.")
        input("ENTER...")
        return False

    A = input("Paciente tem agendamento? (s/n): ").lower() == "s"
    C = p["medico"] == "s"
    D = input("Pagamento em dia? (s/n): ").lower() == "s"

    if p["tipo"] == "consulta":
        return (A and B and C) or (B and C and D)
    else:
        return C and (B or D)

# ------------------------ CADASTRAR PACIENTE ------------------------
def cadastrar_paciente():
    limpar()
    print("=== CADASTRAR PACIENTE ===")

    nome = input("Nome: ")
    idade = input("Idade: ")

    # TELEFONE
    telefone = input("Telefone (somente números): ")
    tel_fmt = formatar_telefone(telefone)
    while not tel_fmt:
        print("Telefone inválido!")
        telefone = input("Digite novamente: ")
        tel_fmt = formatar_telefone(telefone)

    # CPF
    cpf = input("CPF (somente números): ")
    cpf_fmt = formatar_cpf(cpf)
    while not cpf_fmt:
        print("CPF inválido!")
        cpf = input("Digite novamente: ")
        cpf_fmt = formatar_cpf(cpf)

    # RG
    rg = input("RG (somente números): ")
    rg_fmt = formatar_rg(rg)
    while not rg_fmt:
        print("RG inválido!")
        rg = input("Digite novamente: ")
        rg_fmt = formatar_rg(rg)

    medico = input("Tem médico disponível? (s/n): ").lower()

    print("\nTipo de atendimento:")
    print("1 - Consulta")
    print("2 - Emergência")
    tipo = "consulta" if input("Escolha: ") == "1" else "emergencia"

    horario = input("Horário (HH:MM): ")
    try:
        datetime.strptime(horario, "%H:%M")
    except:
        horario = "08:00"

    conn = sqlite3.connect("clinica.db")
    c = conn.cursor()

    c.execute("""
        INSERT INTO pacientes (nome, idade, telefone, cpf, rg, medico)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (nome, idade, tel_fmt, cpf_fmt, rg_fmt, medico))

    paciente_id = c.lastrowid

    c.execute("""
        INSERT INTO consultas (paciente_id, tipo, horario)
        VALUES (?, ?, ?)
    """, (paciente_id, tipo, horario))

    conn.commit()
    conn.close()

    paciente = {
        "id": paciente_id,
        "nome": nome,
        "idade": idade,
        "telefone": tel_fmt,
        "cpf": cpf_fmt,
        "rg": rg_fmt,
        "medico": medico,
        "tipo": tipo,
        "horario": horario
    }

    print("\n✔ Cadastro concluído!")

    pode = verificar_atendimento(paciente)

    if pode:
        if tipo == "consulta":
            fila_consulta.append(paciente)
            print(f"\n➡ {nome} entrou na FILA DE CONSULTA")
        else:
            fila_emergencia.append(paciente)
            print(f"\n⚠ {nome} entrou na FILA DE EMERGÊNCIA")
    else:
        print("\nPaciente NÃO pode entrar na fila.")

    input("ENTER...")

# ------------------------ VER FILAS ------------------------
def ver_fila():
    limpar()
    print("=== FILAS ===\n")

    print("--- Emergência ---")
    if fila_emergencia:
        for i, p in enumerate(fila_emergencia, 1):
            print(f"{i}. {p['nome']} | {p['horario']}")
    else:
        print("Nenhum.")

    print("\n--- Consulta ---")
    if fila_consulta:
        for i, p in enumerate(fila_consulta, 1):
            print(f"{i}. {p['nome']} | {p['horario']}")
    else:
        print("Nenhum.")

    input("\nENTER...")

# ------------------------ CHAMAR PRÓXIMO ------------------------
def chamar_proximo():
    limpar()
    print("=== PRÓXIMO PACIENTE ===\n")

    if fila_emergencia:
        p = fila_emergencia.popleft()
        print(f"⚠ Chamando EMERGÊNCIA: {p['nome']}")
    elif fila_consulta:
        p = fila_consulta.popleft()
        print(f"➡ Chamando CONSULTA: {p['nome']}")
    else:
        print("Fila vazia!")

    input("ENTER...")

# ------------------------ ESTATÍSTICAS ------------------------
def estatisticas():
    limpar()
    print("=== ESTATÍSTICAS ===\n")

    conn = sqlite3.connect("clinica.db")
    c = conn.cursor()

    c.execute("SELECT idade FROM pacientes")
    idades = [row[0] for row in c.fetchall()]

    print("Total de pacientes:", len(idades))
    print("Idade média:", sum(idades) / len(idades) if idades else 0)
    print("Mais novo:", min(idades) if idades else 0)
    print("Mais velho:", max(idades) if idades else 0)

    print("\nFila Emergência:", len(fila_emergencia))
    print("Fila Consulta:", len(fila_consulta))

    conn.close()
    input("\nENTER...")

# ------------------------ BUSCAR PACIENTE ------------------------
def buscar_paciente():
    limpar()
    nome = input("Nome para buscar: ")

    conn = sqlite3.connect("clinica.db")
    c = conn.cursor()

    c.execute("SELECT * FROM pacientes WHERE nome LIKE ?", ('%' + nome + '%',))
    resultados = c.fetchall()
    conn.close()

    if not resultados:
        print("Nenhum encontrado!")
        input("ENTER...")
        return

    for p in resultados:
        print("\n--- PACIENTE ---")
        print("Nome:", p[1])
        print("Idade:", p[2])
        print("Telefone:", p[3])
        print("CPF:", p[4])
        print("RG:", p[5])
        print("Médico:", "Sim" if p[6] == "s" else "Não")

    input("ENTER...")

# ------------------------ LISTAR TODOS ------------------------
def listar_todos():
    limpar()
    print("=== TODOS OS PACIENTES ===\n")

    conn = sqlite3.connect("clinica.db")
    c = conn.cursor()

    c.execute("SELECT nome, idade, telefone, cpf, rg FROM pacientes")
    lista = c.fetchall()
    conn.close()

    if not lista:
        print("Nenhum cadastrado.")
    else:
        for p in lista:
            print("\n----------------------")
            print("Nome:", p[0])
            print("Idade:", p[1])
            print("Telefone:", p[2])
            print("CPF:", p[3])
            print("RG:", p[4])

    input("\nENTER...")

# ------------------------ GERAR RECEITA (PDF) ------------------------
def gerar_receita():
    limpar()
    print("=== GERAR RECEITA (PDF) ===\n")

    cpf = input("CPF do paciente: ")
    p = obter_paciente_por_cpf(formatar_cpf(cpf))

    if not p:
        print("Paciente não encontrado!")
        input("ENTER...")
        return

    nome_pdf = f"Receita_{p['nome'].replace(' ', '_')}.pdf"
    pdf = canvas.Canvas(nome_pdf, pagesize=A4)

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(100, 780, "Clínica Vida+ - Receita Médica")

    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, 740, f"Paciente: {p['nome']}")
    pdf.drawString(100, 720, f"CPF: {p['cpf']}")
    pdf.drawString(100, 700, f"Data: {datetime.now().strftime('%d/%m/%Y')}")

    pdf.drawString(100, 660, "Prescrição:")
    pdf.drawString(100, 640, "- Medicamento: __________________________")
    pdf.drawString(100, 620, "- Dosagem: _____________________________")
    pdf.drawString(100, 600, "- Observações: _________________________")

    pdf.save()

    print(f"\nPDF gerado: {nome_pdf}")
    input("ENTER...")

# ------------------------ MENU PRINCIPAL ------------------------
if __name__ == "__main__":
    init_db()
    while True:
        limpar()
        print("=== SISTEMA CLÍNICA VIDA+ ===")
        print("1. Cadastrar paciente")
        print("2. Ver fila de atendimento")
        print("3. Chamar próximo paciente")
        print("4. Estatísticas")
        print("5. Buscar paciente")
        print("6. Listar todos pacientes")
        print("7. Gerar receita (PDF)")
        print("8. Sair")

        op = input("\nEscolha: ")

        if op == "1":
            cadastrar_paciente()
        elif op == "2":
            ver_fila()
        elif op == "3":
            chamar_proximo()
        elif op == "4":
            estatisticas()
        elif op == "5":
            buscar_paciente()
        elif op == "6":
            listar_todos()
        elif op == "7":
            gerar_receita()
        elif op == "8":
            break
        else:
            input("Opção inválida! ENTER...")
