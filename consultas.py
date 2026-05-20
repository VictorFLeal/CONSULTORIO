from datetime import date, datetime
from utils import carregar, salvar, proximo_id, cabecalho, linha, pausar
from pacientes import listar_pacientes
from medicos import listar_medicos


def _info_consulta(c, pacientes, medicos):
    pac = next((p for p in pacientes if p["id"] == c["id_paciente"]), None)
    med = next((m for m in medicos  if m["id"] == c["id_medico"]),   None)
    nome_pac = pac["nome"] if pac else "?"
    nome_med = med["nome"] if med else "?"
    return nome_pac, nome_med


def listar_consultas_todas():
    cabecalho("TODAS AS CONSULTAS")
    consultas = carregar("consultas.json")
    pacientes = carregar("pacientes.json")
    medicos   = carregar("medicos.json")
    if not consultas:
        print("Nenhuma consulta cadastrada.")
    for c in consultas:
        pac, med = _info_consulta(c, pacientes, medicos)
        print(f"ID:{c['id']} | {c['data']} {c['hora']} | Pac: {pac} | Med: {med} | Status: {c['status']}")
    pausar()


def listar_consultas_hoje():
    cabecalho("CONSULTAS DE HOJE")
    hoje      = date.today().strftime("%d/%m/%Y")
    consultas = carregar("consultas.json")
    pacientes = carregar("pacientes.json")
    medicos   = carregar("medicos.json")
    hoje_list = [c for c in consultas if c["data"] == hoje]
    if not hoje_list:
        print("Nenhuma consulta para hoje.")
    for c in hoje_list:
        pac, med = _info_consulta(c, pacientes, medicos)
        print(f"ID:{c['id']} | {c['hora']} | Pac: {pac} | Med: {med} | Status: {c['status']}")
    pausar()


def listar_consultas_futuras():
    cabecalho("CONSULTAS FUTURAS")
    hoje      = datetime.today()
    consultas = carregar("consultas.json")
    pacientes = carregar("pacientes.json")
    medicos   = carregar("medicos.json")
    futuras   = []
    for c in consultas:
        try:
            data_c = datetime.strptime(c["data"], "%d/%m/%Y")
            if data_c >= hoje and c["status"] not in ["Cancelada", "Finalizada"]:
                futuras.append(c)
        except:
            pass
    if not futuras:
        print("Nenhuma consulta futura.")
    for c in futuras:
        pac, med = _info_consulta(c, pacientes, medicos)
        print(f"ID:{c['id']} | {c['data']} {c['hora']} | Pac: {pac} | Med: {med} | Status: {c['status']}")
    pausar()


def marcar_consulta():
    cabecalho("MARCAR CONSULTA")
    pacientes = carregar("pacientes.json")
    medicos   = carregar("medicos.json")
    consultas = carregar("consultas.json")

    listar_pacientes()
    id_pac  = input("ID do paciente: ").strip()
    paciente = next((p for p in pacientes if str(p["id"]) == id_pac), None)
    if not paciente:
        print("Paciente não encontrado.")
        pausar()
        return

    listar_medicos()
    id_med = input("ID do médico: ").strip()
    medico = next((m for m in medicos if str(m["id"]) == id_med), None)
    if not medico:
        print("Médico não encontrado.")
        pausar()
        return

    data = input("Data (DD/MM/AAAA): ").strip()
    hora = input("Hora (HH:MM): ").strip()

    for c in consultas:
        if (str(c["id_medico"]) == id_med and c["data"] == data
                and c["hora"] == hora and c["status"] != "Cancelada"):
            print("Já existe uma consulta marcada para este médico neste horário!")
            pausar()
            return

    nova = {
        "id":          proximo_id(consultas),
        "id_paciente": int(id_pac),
        "id_medico":   int(id_med),
        "data":        data,
        "hora":        hora,
        "status":      "Agendada"
    }
    consultas.append(nova)
    salvar("consultas.json", consultas)
    print("Consulta marcada com sucesso!")
    pausar()


def reagendar_consulta():
    cabecalho("REAGENDAR CONSULTA")
    consultas = carregar("consultas.json")
    listar_consultas_todas()
    id_busca  = input("ID da consulta: ").strip()
    for c in consultas:
        if str(c["id"]) == id_busca:
            nova_data = input(f"Nova data ({c['data']}): ").strip()
            nova_hora = input(f"Nova hora ({c['hora']}): ").strip()
            if nova_data: c["data"] = nova_data
            if nova_hora: c["hora"] = nova_hora
            salvar("consultas.json", consultas)
            print("Consulta reagendada!")
            pausar()
            return
    print("Consulta não encontrada.")
    pausar()


def cancelar_consulta():
    cabecalho("CANCELAR CONSULTA")
    consultas = carregar("consultas.json")
    listar_consultas_todas()
    id_busca  = input("ID da consulta: ").strip()
    for c in consultas:
        if str(c["id"]) == id_busca:
            c["status"] = "Cancelada"
            salvar("consultas.json", consultas)
            print("Consulta cancelada!")
            pausar()
            return
    print("Consulta não encontrada.")
    pausar()


def confirmar_presenca():
    cabecalho("CONFIRMAR PRESENÇA")
    consultas = carregar("consultas.json")
    listar_consultas_hoje()
    id_busca  = input("ID da consulta: ").strip()
    for c in consultas:
        if str(c["id"]) == id_busca:
            if c["status"] == "Agendada":
                c["status"] = "Confirmada"
                salvar("consultas.json", consultas)
                print("Presença confirmada!")
            else:
                print(f"Status atual: {c['status']}. Não é possível confirmar.")
            pausar()
            return
    print("Consulta não encontrada.")
    pausar()


def menu_consultas():
    while True:
        cabecalho("CONSULTAS")
        print("1. Marcar consulta")
        print("2. Reagendar consulta")
        print("3. Cancelar consulta")
        print("4. Confirmar presença")
        print("5. Consultas de hoje")
        print("6. Consultas futuras")
        print("7. Todas as consultas")
        print("0. Voltar")
        linha()
        opcao = input("Escolha: ").strip()

        if   opcao == "1": marcar_consulta()
        elif opcao == "2": reagendar_consulta()
        elif opcao == "3": cancelar_consulta()
        elif opcao == "4": confirmar_presenca()
        elif opcao == "5": listar_consultas_hoje()
        elif opcao == "6": listar_consultas_futuras()
        elif opcao == "7": listar_consultas_todas()
        elif opcao == "0": break
        else:
            print("Opção inválida!")
            pausar()
