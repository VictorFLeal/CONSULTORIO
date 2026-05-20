import json
import os

PASTA_BD = os.path.join(os.path.dirname(__file__), "Banco de dados")


def _caminho(arquivo):
    return os.path.join(PASTA_BD, arquivo)


def carregar(arquivo):
    caminho = _caminho(arquivo)
    if not os.path.exists(caminho):
        return []
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)


def salvar(arquivo, dados):
    caminho = _caminho(arquivo)
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)


def proximo_id(lista):
    if not lista:
        return 1
    return max(item["id"] for item in lista) + 1


def linha():
    print("-" * 50)


def cabecalho(titulo):
    linha()
    print(f"  {titulo}")
    linha()


def pausar():
    input("\nPressione ENTER para continuar...")
