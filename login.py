from utils import carregar, cabecalho, linha, pausar


def fazer_login():
    cabecalho("LOGIN - CLÍNICA MÉDICA")
    usuario = input("Usuário: ").strip()
    senha   = input("Senha: ").strip()

    usuarios = carregar("usuarios.json")
    for u in usuarios:
        if u["usuario"] == usuario and u["senha"] == senha:
            print(f"\nBem-vindo(a), {u['usuario']}! Perfil: {u['nivel']}")
            pausar()
            return u

    print("\nUsuário ou senha incorretos!")
    pausar()
    return None
