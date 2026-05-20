import os
from utils import salvar, PASTA_BD


def inicializar_arquivos():
    os.makedirs(PASTA_BD, exist_ok=True)

    arquivos = {
        "usuarios.json": [
            {"id": 1, "usuario": "admin",  "senha": "123", "nivel": "admin"},
            {"id": 2, "usuario": "recep",  "senha": "123", "nivel": "recepcionista"},
            {"id": 3, "usuario": "drjoao", "senha": "123", "nivel": "medico"}
        ],
        "medicos.json": [
            {"id": 1, "nome": "Dr. João Silva", "especialidade": "Clinico Geral", "crm": "12345"}
        ],
        "pacientes.json":   [],
        "consultas.json":   [],
        "prontuarios.json": [],
        "logs.json":        []
    }

    for arquivo, dados_padrao in arquivos.items():
        caminho = os.path.join(PASTA_BD, arquivo)
        if not os.path.exists(caminho):
            salvar(arquivo, dados_padrao)
