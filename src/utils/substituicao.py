import re

def substituir_variaveis(texto: str, dados_linha: dict) -> str:
    """
    Substitui variáveis no formato {{Nome}} pelo valor correspondente no dicionário dados_linha.
    Ignora maiúsculas/minúsculas e espaços extras.
    Exemplo: "Olá {{Nome}}" -> "Olá João"
    """
    def substituir(match):
        chave = match.group(1).strip()
        for chave_dict in dados_linha.keys():
            if chave_dict.lower() == chave.lower():
                return str(dados_linha[chave_dict])
        return f'{{{{{chave}}}}}'
    return re.sub(r'\{\{\s*(.*?)\s*\}\}', substituir, texto)
