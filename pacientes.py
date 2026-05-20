from utils import carregar, salvar, proximo_id, cabecalho, linha, pausar


def listar_pacientes():
    cabecalho("LISTA DE PACIENTES")
    pacientes = carregar("pacientes.json")
    if not pacientes:
        print("Nenhum paciente cadastrado.")
    for p in pacientes:
        print(f"ID: {p['id']} | Nome: {p['nome']} | CPF: {p['cpf']} | Tel: {p['telefone']}")
    pausar()


def cadastrar_paciente():
    cabecalho("CADASTRAR PACIENTE")
    pacientes = carregar("pacientes.json")
    nome      = input("Nome: ").strip()
    idade     = input("Idade: ").strip()
    cpf       = input("CPF: ").strip()
    telefone  = input("Telefone: ").strip()
    endereco  = input("Endereço: ").strip()

    novo = {
        "id":       proximo_id(pacientes),
        "nome":     nome,
        "idade":    idade,
        "cpf":      cpf,
        "telefone": telefone,
        "endereco": endereco
    }
    pacientes.append(novo)
    salvar("pacientes.json", pacientes)
    print("Paciente cadastrado com sucesso!")
    pausar()


def editar_paciente():
    cabecalho("EDITAR PACIENTE")
    pacientes = carregar("pacientes.json")
    listar_pacientes()
    id_busca  = input("ID do paciente para editar: ").strip()
    for p in pacientes:
        if str(p["id"]) == id_busca:
            novo_nome = input(f"Nome ({p['nome']}): ").strip()
            novo_tel  = input(f"Telefone ({p['telefone']}): ").strip()
            novo_end  = input(f"Endereço ({p['endereco']}): ").strip()
            if novo_nome: p["nome"]     = novo_nome
            if novo_tel:  p["telefone"] = novo_tel
            if novo_end:  p["endereco"] = novo_end
            salvar("pacientes.json", pacientes)
            print("Paciente editado!")
            pausar()
            return
    print("Paciente não encontrado.")
    pausar()


def buscar_paciente():
    cabecalho("BUSCAR PACIENTE")
    pacientes   = carregar("pacientes.json")
    nome        = input("Nome (ou parte do nome): ").strip().lower()
    encontrados = [p for p in pacientes if nome in p["nome"].lower()]
    if not encontrados:
        print("Nenhum paciente encontrado.")
    for p in encontrados:
        print(f"ID: {p['id']} | Nome: {p['nome']} | CPF: {p['cpf']} | Idade: {p['idade']} | Tel: {p['telefone']} | End: {p['endereco']}")
    pausar()


def historico_paciente():
    cabecalho("HISTÓRICO DO PACIENTE")
    pacientes = carregar("pacientes.json")
    consultas = carregar("consultas.json")
    medicos   = carregar("medicos.json")
    id_busca  = input("ID do paciente: ").strip()

    paciente = next((p for p in pacientes if str(p["id"]) == id_busca), None)
    if not paciente:
        print("Paciente não encontrado.")
        pausar()
        return

    print(f"\nPaciente: {paciente['nome']}")
    linha()
    consultas_pac = [c for c in consultas if str(c["id_paciente"]) == id_busca]
    if not consultas_pac:
        print("Nenhuma consulta encontrada.")
    for c in consultas_pac:
        medico     = next((m for m in medicos if m["id"] == c["id_medico"]), None)
        nome_medico = medico["nome"] if medico else "Desconhecido"
        print(f"Data: {c['data']} {c['hora']} | Médico: {nome_medico} | Status: {c['status']}")
    pausar()


def menu_pacientes():
    while True:
        cabecalho("PACIENTES")
        print("1. Listar todos os pacientes")
        print("2. Cadastrar paciente")
        print("3. Editar paciente")
        print("4. Buscar paciente")
        print("5. Histórico do paciente")
        print("0. Voltar")
        linha()
        opcao = input("Escolha: ").strip()

        if   opcao == "1": listar_pacientes()
        elif opcao == "2": cadastrar_paciente()
        elif opcao == "3": editar_paciente()
        elif opcao == "4": buscar_paciente()
        elif opcao == "5": historico_paciente()
        elif opcao == "0": break
        else:
            print("Opção inválida!")
            pausar()
