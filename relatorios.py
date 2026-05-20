from datetime import date, datetime
from utils import carregar, cabecalho, linha, pausar


# ── RELATÓRIOS ADMINISTRADOR ──────────────────────────────

def relatorio_consultas_por_status(status):
    consultas = carregar("consultas.json")
    total     = len([c for c in consultas if c["status"] == status])
    print(f"\nConsultas com status '{status}': {total}")
    pausar()


def relatorio_total_pacientes():
    pacientes = carregar("pacientes.json")
    print(f"\nTotal de pacientes cadastrados: {len(pacientes)}")
    pausar()


def relatorio_total_medicos():
    medicos = carregar("medicos.json")
    print(f"\nTotal de médicos ativos: {len(medicos)}")
    pausar()


def relatorio_consultas_por_medico():
    cabecalho("CONSULTAS POR MÉDICO")
    consultas = carregar("consultas.json")
    medicos   = carregar("medicos.json")
    for m in medicos:
        total = len([c for c in consultas if c["id_medico"] == m["id"]])
        print(f"{m['nome']}: {total} consulta(s)")
    pausar()


def relatorio_pacientes_mais_atendidos():
    cabecalho("PACIENTES MAIS ATENDIDOS")
    consultas = carregar("consultas.json")
    pacientes = carregar("pacientes.json")
    contagem  = {}
    for c in consultas:
        if c["status"] == "Finalizada":
            id_p = c["id_paciente"]
            contagem[id_p] = contagem.get(id_p, 0) + 1
    if not contagem:
        print("Nenhum atendimento finalizado.")
        pausar()
        return
    ordenado = sorted(contagem.items(), key=lambda x: x[1], reverse=True)
    for id_p, total in ordenado:
        pac  = next((p for p in pacientes if p["id"] == id_p), None)
        nome = pac["nome"] if pac else "?"
        print(f"{nome}: {total} atendimento(s)")
    pausar()


def menu_relatorios_admin():
    while True:
        cabecalho("RELATÓRIOS - ADMIN")
        print("1. Consultas realizadas (Finalizadas)")
        print("2. Consultas canceladas")
        print("3. Total de pacientes")
        print("4. Total de médicos")
        print("5. Consultas por médico")
        print("6. Pacientes mais atendidos")
        print("0. Voltar")
        linha()
        opcao = input("Escolha: ").strip()

        if   opcao == "1": relatorio_consultas_por_status("Finalizada")
        elif opcao == "2": relatorio_consultas_por_status("Cancelada")
        elif opcao == "3": relatorio_total_pacientes()
        elif opcao == "4": relatorio_total_medicos()
        elif opcao == "5": relatorio_consultas_por_medico()
        elif opcao == "6": relatorio_pacientes_mais_atendidos()
        elif opcao == "0": break
        else:
            print("Opção inválida!")
            pausar()


# ── RELATÓRIOS RECEPCIONISTA ──────────────────────────────

def relatorio_consultas_por_data():
    cabecalho("CONSULTAS POR DATA")
    data      = input("Data (DD/MM/AAAA): ").strip()
    consultas = carregar("consultas.json")
    pacientes = carregar("pacientes.json")
    medicos   = carregar("medicos.json")
    filtradas = [c for c in consultas if c["data"] == data]
    if not filtradas:
        print("Nenhuma consulta nesta data.")
    for c in filtradas:
        pac = next((p for p in pacientes if p["id"] == c["id_paciente"]), None)
        med = next((m for m in medicos   if m["id"] == c["id_medico"]),   None)
        print(f"ID:{c['id']} | {c['hora']} | Pac: {pac['nome'] if pac else '?'} | Med: {med['nome'] if med else '?'} | Status: {c['status']}")
    pausar()


def relatorio_pacientes_atendidos_hoje():
    cabecalho("PACIENTES ATENDIDOS HOJE")
    hoje      = date.today().strftime("%d/%m/%Y")
    consultas = carregar("consultas.json")
    pacientes = carregar("pacientes.json")
    finalizadas = [c for c in consultas if c["data"] == hoje and c["status"] == "Finalizada"]
    if not finalizadas:
        print("Nenhum paciente atendido hoje.")
    for c in finalizadas:
        pac = next((p for p in pacientes if p["id"] == c["id_paciente"]), None)
        print(f"Paciente: {pac['nome'] if pac else '?'} | Hora: {c['hora']}")
    pausar()


def menu_relatorios_recepcionista():
    while True:
        cabecalho("RELATÓRIOS - RECEPCIONISTA")
        print("1. Consultas de hoje")
        print("2. Consultas por data")
        print("3. Consultas canceladas")
        print("4. Pacientes atendidos hoje")
        print("0. Voltar")
        linha()
        opcao = input("Escolha: ").strip()

        if   opcao == "1":
            from consultas import listar_consultas_hoje
            listar_consultas_hoje()
        elif opcao == "2": relatorio_consultas_por_data()
        elif opcao == "3": relatorio_consultas_por_status("Cancelada")
        elif opcao == "4": relatorio_pacientes_atendidos_hoje()
        elif opcao == "0": break
        else:
            print("Opção inválida!")
            pausar()


# ── RELATÓRIOS MÉDICO ─────────────────────────────────────

def relatorio_total_atendimentos_medico(medico):
    consultas = carregar("consultas.json")
    total     = len([c for c in consultas if c["id_medico"] == medico["id"] and c["status"] == "Finalizada"])
    print(f"\nTotal de atendimentos realizados: {total}")
    pausar()


def relatorio_pacientes_mes_medico(medico):
    cabecalho("PACIENTES ATENDIDOS NO MÊS")
    mes_atual   = datetime.today().strftime("%m/%Y")
    consultas   = carregar("consultas.json")
    pacientes   = carregar("pacientes.json")
    atendimentos = []
    for c in consultas:
        if c["id_medico"] == medico["id"] and c["status"] == "Finalizada":
            try:
                mes_c = datetime.strptime(c["data"], "%d/%m/%Y").strftime("%m/%Y")
                if mes_c == mes_atual:
                    atendimentos.append(c)
            except:
                pass
    print(f"Atendimentos em {mes_atual}: {len(atendimentos)}")
    for c in atendimentos:
        pac = next((p for p in pacientes if p["id"] == c["id_paciente"]), None)
        print(f"  - {pac['nome'] if pac else '?'} | {c['data']}")
    pausar()


def relatorio_pendentes_medico(medico):
    consultas = carregar("consultas.json")
    pendentes = [c for c in consultas if c["id_medico"] == medico["id"] and c["status"] in ["Agendada", "Confirmada"]]
    print(f"\nConsultas pendentes: {len(pendentes)}")
    pausar()


def menu_relatorios_medico(medico):
    while True:
        cabecalho("RELATÓRIOS - MÉDICO")
        print("1. Total de atendimentos realizados")
        print("2. Pacientes atendidos no mês")
        print("3. Consultas pendentes")
        print("0. Voltar")
        linha()
        opcao = input("Escolha: ").strip()

        if   opcao == "1": relatorio_total_atendimentos_medico(medico)
        elif opcao == "2": relatorio_pacientes_mes_medico(medico)
        elif opcao == "3": relatorio_pendentes_medico(medico)
        elif opcao == "0": break
        else:
            print("Opção inválida!")
            pausar()
