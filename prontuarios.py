from utils import carregar, salvar, proximo_id, cabecalho, linha, pausar


def registrar_prontuario(medico):
    cabecalho("REGISTRAR PRONTUÁRIO")
    consultas   = carregar("consultas.json")
    pacientes   = carregar("pacientes.json")
    prontuarios = carregar("prontuarios.json")

    em_atendimento = [c for c in consultas
                      if c["id_medico"] == medico["id"] and c["status"] == "Em Atendimento"]
    if not em_atendimento:
        print("Nenhuma consulta em atendimento no momento.")
        pausar()
        return

    for c in em_atendimento:
        pac = next((p for p in pacientes if p["id"] == c["id_paciente"]), None)
        print(f"ID:{c['id']} | Paciente: {pac['nome'] if pac else '?'}")

    id_busca = input("ID da consulta: ").strip()
    consulta = next((c for c in em_atendimento if str(c["id"]) == id_busca), None)
    if not consulta:
        print("Consulta não encontrada.")
        pausar()
        return

    pac = next((p for p in pacientes if p["id"] == consulta["id_paciente"]), None)
    print(f"\nPaciente: {pac['nome'] if pac else '?'}")

    diagnostico  = input("Diagnóstico: ").strip()
    receita      = input("Receita médica: ").strip()
    observacoes  = input("Observações: ").strip()
    retorno      = input("Retorno recomendado (opcional): ").strip()

    prontuario = {
        "id":          proximo_id(prontuarios),
        "id_consulta": consulta["id"],
        "id_paciente": consulta["id_paciente"],
        "id_medico":   medico["id"],
        "data":        consulta["data"],
        "diagnostico": diagnostico,
        "receita":     receita,
        "observacoes": observacoes,
        "retorno":     retorno
    }
    prontuarios.append(prontuario)
    salvar("prontuarios.json", prontuarios)
    print("Prontuário registrado com sucesso!")
    pausar()


def ver_prontuarios_paciente(medico):
    cabecalho("PRONTUÁRIOS DO PACIENTE")
    prontuarios = carregar("prontuarios.json")
    pacientes   = carregar("pacientes.json")
    id_busca    = input("ID do paciente: ").strip()

    paciente = next((p for p in pacientes if str(p["id"]) == id_busca), None)
    if not paciente:
        print("Paciente não encontrado.")
        pausar()
        return

    registros = [pr for pr in prontuarios
                 if pr["id_paciente"] == int(id_busca) and pr["id_medico"] == medico["id"]]
    if not registros:
        print("Nenhum prontuário encontrado.")
    for pr in registros:
        linha()
        print(f"Data:        {pr['data']}")
        print(f"Diagnóstico: {pr['diagnostico']}")
        print(f"Receita:     {pr['receita']}")
        print(f"Observações: {pr['observacoes']}")
        print(f"Retorno:     {pr['retorno']}")
    pausar()
