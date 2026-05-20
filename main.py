from dados  import inicializar_arquivos
from login  import fazer_login
from menus  import menu_admin, menu_recepcionista, menu_medico

print("\n" + "=" * 50)
print("      SISTEMA DE CLÍNICA MÉDICA")
print("=" * 50)

inicializar_arquivos()

tentativas = 0
while True:
    usuario = fazer_login()

    if usuario:
        tentativas = 0
        nivel = usuario["nivel"]

        if   nivel == "admin":          menu_admin()
        elif nivel == "recepcionista":  menu_recepcionista()
        elif nivel == "medico":         menu_medico(usuario)

        print("\nSessão encerrada.")

    else:
        tentativas += 1
        if tentativas >= 3:
            print("Número máximo de tentativas atingido. Encerrando.")
            break
        print(f"Tentativa {tentativas}/3.")
