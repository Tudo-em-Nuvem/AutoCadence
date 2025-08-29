import re

def substituir_variaveis_no_texto(texto, linha):
    """
    Substitui variáveis no formato {{Nome}} pelo valor correspondente no dicionário linha.
    Ignora case e espaços extras.
    """
    def substituir(match):
        chave = match.group(1).strip()
        for k in linha.keys():
            if k.lower() == chave.lower():
                return str(linha[k])
        return f'{{{{{chave}}}}}'
    return re.sub(r'\{\{\s*(.*?)\s*\}\}', substituir, texto)
