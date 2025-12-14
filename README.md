📌 Projeto Integrado – Sistema da Clínica Vida+
Introdução

A cidade de São Lucas está crescendo rapidamente, aumentando a demanda por serviços médicos de qualidade. A Clínica Vida+, especializada em atendimentos médicos e exames laboratoriais, enfrenta dificuldades para gerenciar suas rotinas. Atualmente, os agendamentos são feitos manualmente, os médicos não conseguem acessar rapidamente o histórico completo dos pacientes e erros de cobrança e de relatórios são comuns.

Para resolver essas questões, a diretora Sra. Helena contratou o desenvolvimento de um sistema informatizado que organize o atendimento, melhore o controle de informações e facilite o trabalho administrativo da clínica.

Objetivos do Sistema

O sistema deve oferecer funcionalidades que permitam:

Cadastro de pacientes, médicos e exames;

Agendamento de consultas e exames com controle de horários disponíveis;

Registro detalhado de atendimentos, incluindo evolução do paciente;

Geração de relatórios mensais para acompanhamento administrativo.

A ideia é aplicar conhecimentos de análise, planejamento, modelagem e implementação de soluções de TI para resolver os problemas apresentados.

Estrutura do Projeto
1️⃣ Planejamento no Trello

Criar um quadro Scrum com as seguintes listas:

Backlog

Sprint Atual

Em Progresso

Concluído

Definir objetivos e duração de cada sprint;

Atualizar as tarefas conforme o andamento;

Entrega: prints do quadro e relatório final de cada sprint.

2️⃣ Sistema em Python

O sistema deve permitir:

Cadastrar pacientes (nome, idade, telefone);

Exibir estatísticas:

Total de pacientes;

Idade média;

Paciente mais jovem e mais velho;

Buscar pacientes pelo nome;

Listar todos os pacientes cadastrados;

Menu interativo, que permite navegar até a saída do sistema.

Entrega: código funcional em Python.

3️⃣ Controle de Acesso (Lógica Booleana)

Criar expressões lógicas para:

Consulta Normal

Emergência

Construir tabelas verdade com 16 linhas cada;

Analisar situações em que o paciente será atendido;

Testar cenários práticos.

Entrega: expressões lógicas, tabelas verdade e opcionalmente Python para gerar as tabelas automaticamente.

4️⃣ Algoritmo de Fila (FIFO)

Inserir 3 pacientes em uma fila (nome + CPF);

Remover o primeiro paciente atendido;

Exibir os pacientes restantes.

Entrega: pseudocódigo ou implementação em Python.

5️⃣ Diagrama de Casos de Uso

Criar diagrama UML para o sistema:

Atores: Secretária, Médico e Paciente;

Funcionalidades: cadastro de paciente, agendamento, confirmação, cancelamento de consultas, geração e impressão de receitas.

Entrega: imagem do diagrama UML.

Demonstração do Sistema feito em um atendimento completo!!
=== SISTEMA CLÍNICA VIDA+ ===
1. Cadastrar paciente
2. Ver fila de atendimento
3. Chamar próximo paciente
4. Estatísticas
5. Buscar paciente
6. Listar todos os pacientes
7. Gerar receita (PDF)
8. Sair
Escolha uma opção: 1
Nome do paciente: Pedro Lima
Idade: 27
Telefone: (11) 98888-1234
Paciente cadastrado com sucesso!

Checklist de Entregas
Passo	Tipo	Status
Trello	Documentação	⬜
Sistema Python	Programação	⬛
Lógica Booleana	Programação/Documentação	⬛
Algoritmo FIFO	Pseudocódigo/Python	⬛
Diagrama UML	Modelagem	⬜
Lógica Booleana

Expressões:

Consulta Normal: (A ∧ B ∧ C) ∨ (B ∧ C ∧ D)
Emergência: C ∧ (B ∨ D)


Implementação em Python:

def consulta_normal(a,b,c,d):
    return (a and b and c) or (b and c and d)

def emergencia(b,c,d):
    return c and (b or d)

Tabela Verdade (Python)
from itertools import product

print("| A | B | C | D | Consulta Normal | Emergência |")
for a, b, c, d in product([True, False], repeat=4):
    cn = consulta_normal(a,b,c,d)
    em = emergencia(b,c,d)
    conv = lambda x: "V" if x else "F"
    print(f"| {conv(a)} | {conv(b)} | {conv(c)} | {conv(d)} | {conv(cn)} | {conv(em)} |")

Algoritmo FIFO – Pseudocódigo
INÍCIO
    CRIAR fila_vazia

    PARA i = 1 ATÉ 3
        LER nome, CPF
        ADICIONAR (nome, CPF) NA fila_vazia
    FIM_PARA

    REMOVER primeiro paciente da fila
    MOSTRAR paciente_atendido

    PARA CADA paciente EM fila_vazia
        MOSTRAR paciente
    FIM_PARA
FIM


Implementação em Python:

fila = []

for i in range(3):
    nome = input("Digite o nome do paciente: ")
    cpf = input("Digite o CPF do paciente: ")
    fila.append((nome, cpf))

paciente = fila.pop(0)
print("Paciente atendido:", paciente)

print("Pacientes restantes na fila:")
for p in fila:
    print(p)

Diagrama UML

Diagrama feito no aplicativo: https://www.visual-paradigm.com



