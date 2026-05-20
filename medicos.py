from utils import carregar, salvar, proximo_id, cabecalho, linha, pausar


def listar_medicos():
    cabecalho("LISTA DE MÉDICOS")
    medicos = carregar("medicos.json")
    if not medicos:
        print("Nenhum médico cadastrado.")
    for m in medicos:
        print(f"ID: {m['id']} | Nome: {m['nome']} | Especialidade: {m['especialidade']} | CRM: {m['crm']}")
    pausar()


def cadastrar_medico():
    cabecalho("CADASTRAR MÉDICO")
    medicos       = carregar("medicos.json")
    nome          = input("Nome: ").strip()
    especialidade = input("Especialidade: ").strip()
    crm           = input("CRM: ").strip()

    novo = {"id": proximo_id(medicos), "nome": nome, "especialidade": especialidade, "crm": crm}
    medicos.append(novo)
    salvar("medicos.json", medicos)
    print("Médico cadastrado com sucesso!")
    pausar()


def editar_medico():
    cabecalho("EDITAR MÉDICO")
    medicos  = carregar("medicos.json")
    listar_medicos()
    id_busca = input("ID do médico para editar: ").strip()
    for m in medicos:
        if str(m["id"]) == id_busca:
            novo_nome = input(f"Nome ({m['nome']}): ").strip()
            nova_esp  = input(f"Especialidade ({m['especialidade']}): ").strip()
            if novo_nome: m["nome"]          = novo_nome
            if nova_esp:  m["especialidade"] = nova_esp
            salvar("medicos.json", medicos)
            print("Médico editado!")
            pausar()
            return
    print("Médico não encontrado.")
    pausar()


def excluir_medico():
    cabecalho("EXCLUIR MÉDICO")
    medicos    = carregar("medicos.json")
    listar_medicos()
    id_busca   = input("ID do médico para excluir: ").strip()
    nova_lista = [m for m in medicos if str(m["id"]) != id_busca]
    if len(nova_lista) == len(medicos):
        print("Médico não encontrado.")
    else:
        salvar("medicos.json", nova_lista)
        print("Médico excluído!")
    pausar()


def menu_medicos():
    while True:
        cabecalho("GERENCIAR MÉDICOS")
        print("1. Listar médicos")
        print("2. Cadastrar médico")
        print("3. Editar médico")
        print("4. Excluir médico")
        print("0. Voltar")
        linha()
        opcao = input("Escolha: ").strip()

        if   opcao == "1": listar_medicos()
        elif opcao == "2": cadastrar_medico()
        elif opcao == "3": editar_medico()
        elif opcao == "4": excluir_medico()
        elif opcao == "0": break
        else:
            print("Opção inválida!")
            pausar()
