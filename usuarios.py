from utils import carregar, salvar, proximo_id, cabecalho, linha, pausar


def listar_usuarios():
    cabecalho("LISTA DE USUÁRIOS")
    usuarios = carregar("usuarios.json")
    if not usuarios:
        print("Nenhum usuário cadastrado.")
    for u in usuarios:
        print(f"ID: {u['id']} | Usuário: {u['usuario']} | Nível: {u['nivel']}")
    pausar()


def cadastrar_usuario():
    cabecalho("CADASTRAR USUÁRIO")
    usuarios = carregar("usuarios.json")
    nome  = input("Nome de usuário: ").strip()
    senha = input("Senha: ").strip()
    print("Nível: 1-admin  2-recepcionista  3-medico")
    op    = input("Nível: ").strip()
    niveis = {"1": "admin", "2": "recepcionista", "3": "medico"}
    nivel  = niveis.get(op, "recepcionista")

    novo = {"id": proximo_id(usuarios), "usuario": nome, "senha": senha, "nivel": nivel}
    usuarios.append(novo)
    salvar("usuarios.json", usuarios)
    print("Usuário cadastrado com sucesso!")
    pausar()


def editar_usuario():
    cabecalho("EDITAR USUÁRIO")
    usuarios = carregar("usuarios.json")
    listar_usuarios()
    id_busca = input("ID do usuário para editar: ").strip()
    for u in usuarios:
        if str(u["id"]) == id_busca:
            novo_nome = input(f"Novo nome ({u['usuario']}): ").strip()
            if novo_nome:
                u["usuario"] = novo_nome
            salvar("usuarios.json", usuarios)
            print("Usuário editado!")
            pausar()
            return
    print("Usuário não encontrado.")
    pausar()


def excluir_usuario():
    cabecalho("EXCLUIR USUÁRIO")
    usuarios = carregar("usuarios.json")
    listar_usuarios()
    id_busca  = input("ID do usuário para excluir: ").strip()
    nova_lista = [u for u in usuarios if str(u["id"]) != id_busca]
    if len(nova_lista) == len(usuarios):
        print("Usuário não encontrado.")
    else:
        salvar("usuarios.json", nova_lista)
        print("Usuário excluído!")
    pausar()


def resetar_senha():
    cabecalho("RESETAR SENHA")
    usuarios = carregar("usuarios.json")
    listar_usuarios()
    id_busca = input("ID do usuário: ").strip()
    for u in usuarios:
        if str(u["id"]) == id_busca:
            nova_senha = input("Nova senha: ").strip()
            u["senha"]  = nova_senha
            salvar("usuarios.json", usuarios)
            print("Senha resetada!")
            pausar()
            return
    print("Usuário não encontrado.")
    pausar()


def menu_usuarios():
    while True:
        cabecalho("GERENCIAR USUÁRIOS")
        print("1. Listar usuários")
        print("2. Cadastrar usuário")
        print("3. Editar usuário")
        print("4. Excluir usuário")
        print("5. Resetar senha")
        print("0. Voltar")
        linha()
        opcao = input("Escolha: ").strip()

        if   opcao == "1": listar_usuarios()
        elif opcao == "2": cadastrar_usuario()
        elif opcao == "3": editar_usuario()
        elif opcao == "4": excluir_usuario()
        elif opcao == "5": resetar_senha()
        elif opcao == "0": break
        else:
            print("Opção inválida!")
            pausar()
