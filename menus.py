from datetime import date
from utils      import carregar, salvar, cabecalho, linha, pausar
from usuarios   import menu_usuarios
from medicos    import menu_medicos, listar_medicos
from pacientes  import menu_pacientes, historico_paciente
from consultas  import (menu_consultas, listar_consultas_todas,
                        listar_consultas_hoje, listar_consultas_futuras)
from prontuarios import registrar_prontuario, ver_prontuarios_paciente
from relatorios  import (menu_relatorios_admin, menu_relatorios_recepcionista,
                         menu_relatorios_medico)


# ── ADMIN ─────────────────────────────────────────────────

def menu_admin():
    while True:
        cabecalho("MENU - ADMINISTRADOR")
        print("1. Gerenciar Usuários")
        print("2. Gerenciar Médicos")
        print("3. Gerenciar Pacientes")
        print("4. Ver todas as Consultas")
        print("5. Relatórios")
        print("0. Sair")
        linha()
        opcao = input("Escolha: ").strip()

        if   opcao == "1": menu_usuarios()
        elif opcao == "2": menu_medicos()
        elif opcao == "3": menu_pacientes()
        elif opcao == "4": listar_consultas_todas()
        elif opcao == "5": menu_relatorios_admin()
        elif opcao == "0": break
        else:
            print("Opção inválida!")
            pausar()


# ── RECEPCIONISTA ─────────────────────────────────────────

def menu_recepcionista():
    while True:
        consultas = carregar("consultas.json")
        pacientes = carregar("pacientes.json")
        medicos   = carregar("medicos.json")
        hoje      = date.today().strftime("%d/%m/%Y")
        c_hoje    = [c for c in consultas if c["data"] == hoje]
        finalizadas_hoje = [c for c in c_hoje if c["status"] == "Finalizada"]
        canceladas_hoje  = [c for c in c_hoje if c["status"] == "Cancelada"]

        cabecalho("PAINEL - RECEPCIONISTA")
        print(f"  Consultas hoje:            {len(c_hoje)}")
        print(f"  Pacientes cadastrados:     {len(pacientes)}")
        print(f"  Médicos ativos:            {len(medicos)}")
        print(f"  Atendimentos finalizados:  {len(finalizadas_hoje)}")
        print(f"  Consultas canceladas hoje: {len(canceladas_hoje)}")
        linha()
        print("1. Gerenciar Pacientes")
        print("2. Gerenciar Consultas")
        print("3. Histórico do Paciente")
        print("4. Relatórios")
        print("0. Sair")
        linha()
        opcao = input("Escolha: ").strip()

        if   opcao == "1": menu_pacientes()
        elif opcao == "2": menu_consultas()
        elif opcao == "3": historico_paciente()
        elif opcao == "4": menu_relatorios_recepcionista()
        elif opcao == "0": break
        else:
            print("Opção inválida!")
            pausar()


# ── MÉDICO ────────────────────────────────────────────────

def _identificar_medico(usuario):
    medicos = carregar("medicos.json")
    for m in medicos:
        if usuario["usuario"].lower() in m["nome"].lower():
            return m
    # Se não achar automaticamente, perguntar
    print("\nMédico não identificado automaticamente.")
    listar_medicos()
    id_med = input("Qual é o seu ID de médico? ").strip()
    return next((m for m in medicos if str(m["id"]) == id_med), None)


def _iniciar_atendimento(medico):
    cabecalho("INICIAR ATENDIMENTO")
    consultas = carregar("consultas.json")
    listar_consultas_hoje()
    id_busca  = input("ID da consulta: ").strip()
    for c in consultas:
        if str(c["id"]) == id_busca and c["id_medico"] == medico["id"]:
            if c["status"] in ["Agendada", "Confirmada"]:
                c["status"] = "Em Atendimento"
                salvar("consultas.json", consultas)
                print("Atendimento iniciado!")
            else:
                print(f"Não é possível iniciar. Status: {c['status']}")
            pausar()
            return
    print("Consulta não encontrada ou não pertence a você.")
    pausar()


def _finalizar_atendimento(medico):
    cabecalho("FINALIZAR ATENDIMENTO")
    consultas = carregar("consultas.json")
    listar_consultas_hoje()
    id_busca  = input("ID da consulta: ").strip()
    for c in consultas:
        if str(c["id"]) == id_busca and c["id_medico"] == medico["id"]:
            if c["status"] == "Em Atendimento":
                c["status"] = "Finalizada"
                salvar("consultas.json", consultas)
                print("Atendimento finalizado!")
            else:
                print(f"Não é possível finalizar. Status: {c['status']}")
            pausar()
            return
    print("Consulta não encontrada ou não pertence a você.")
    pausar()


def _agenda_hoje_medico(medico):
    cabecalho(f"AGENDA DE HOJE - {medico['nome']}")
    hoje      = date.today().strftime("%d/%m/%Y")
    consultas = carregar("consultas.json")
    pacientes = carregar("pacientes.json")
    minhas    = [c for c in consultas if c["id_medico"] == medico["id"] and c["data"] == hoje]
    if not minhas:
        print("Nenhuma consulta hoje.")
    for c in minhas:
        pac = next((p for p in pacientes if p["id"] == c["id_paciente"]), None)
        print(f"ID:{c['id']} | {c['hora']} | Paciente: {pac['nome'] if pac else '?'} | Status: {c['status']}")
    pausar()


def menu_medico(usuario):
    medico_atual = _identificar_medico(usuario)
    if not medico_atual:
        print("Médico não encontrado. Encerrando.")
        pausar()
        return

    while True:
        consultas = carregar("consultas.json")
        hoje      = date.today().strftime("%d/%m/%Y")
        minhas_hoje      = [c for c in consultas if c["id_medico"] == medico_atual["id"] and c["data"] == hoje]
        finalizadas_hoje = [c for c in minhas_hoje if c["status"] == "Finalizada"]
        aguardando       = [c for c in minhas_hoje if c["status"] in ["Agendada", "Confirmada"]]
        proxima          = aguardando[0]["hora"] if aguardando else "Nenhuma"

        cabecalho(f"PAINEL - {medico_atual['nome'].upper()}")
        print(f"  Minhas consultas hoje:      {len(minhas_hoje)}")
        print(f"  Próxima consulta:           {proxima}")
        print(f"  Consultas finalizadas hoje: {len(finalizadas_hoje)}")
        print(f"  Pacientes aguardando:       {len(aguardando)}")
        linha()
        print("1. Minha agenda de hoje")
        print("2. Agenda futura")
        print("3. Iniciar atendimento")
        print("4. Finalizar atendimento")
        print("5. Registrar prontuário")
        print("6. Ver prontuários do paciente")
        print("7. Histórico do paciente")
        print("8. Relatórios")
        print("0. Sair")
        linha()
        opcao = input("Escolha: ").strip()

        if   opcao == "1": _agenda_hoje_medico(medico_atual)
        elif opcao == "2": listar_consultas_futuras()
        elif opcao == "3": _iniciar_atendimento(medico_atual)
        elif opcao == "4": _finalizar_atendimento(medico_atual)
        elif opcao == "5": registrar_prontuario(medico_atual)
        elif opcao == "6": ver_prontuarios_paciente(medico_atual)
        elif opcao == "7": historico_paciente()
        elif opcao == "8": menu_relatorios_medico(medico_atual)
        elif opcao == "0": break
        else:
            print("Opção inválida!")
            pausar()
