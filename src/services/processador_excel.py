import pandas as pd
import time
from utils.substituicao import substituir_variaveis_no_texto
from utils.send_email import send_email
import inspect

def processar_excel(caminho_arquivo, callback, controle, texto, linha_inicial=0, titulo='', auth=None):
    """
    Carrega o arquivo Excel e percorre as linhas, chamando callback para cada linha.
    O controle é um objeto com atributo 'ativo' para pausar/parar.
    Permite retomar do ponto pausado.
    """
    df = pd.read_excel(caminho_arquivo)
    total = len(df)
    coluna_email = None

    # Descobre a coluna de e-mail selecionada pelo usuário
    if 'coluna_email' in globals():
        coluna_email = globals()['coluna_email']
    
    args = inspect.getfullargspec(processar_excel).args
    # Se vierem como argumentos extras
    def get_arg(idx, default=None):
        try:
            return inspect.stack()[1].frame.f_locals.get(args[idx], default)
        except Exception:
            return default
    # Recebe titulo e auth do caller
    try:
        titulo = get_arg(5, '')
        auth = get_arg(6, {})
    except Exception:
        titulo = ''
        auth = {}

    for idx in range(linha_inicial, total):
        row = df.iloc[idx]
        if not controle.ativo:
            callback('Processamento pausado.', idx-1 if idx > 0 else 0)
            break

        callback(f'Tratando linha: {dict(row)}', idx)

        # Recupera destinatário
        to = None
        if coluna_email and coluna_email in row:
            to = row[coluna_email]
        else:
            for col in ['email', 'Email', 'E-mail']:
                if col in row:
                    to = row[col]
                    break

        if not to or not isinstance(to, str) or '@' not in to:
            callback(f'[ERRO] Nenhum e-mail válido encontrado na linha {idx+1}.', idx)
            continue

        # Substitui variáveis do corpo/título usando função utilitária
        corpo = substituir_variaveis_no_texto(texto, row.to_dict()) if texto else texto
        titulo_final = substituir_variaveis_no_texto(titulo, row.to_dict()) if titulo else titulo

        if not titulo_final:
            callback(f'[AVISO] Título do e-mail está vazio na linha {idx+1}.', idx)
        if not corpo:
            callback(f'[AVISO] Corpo do e-mail está vazio na linha {idx+1}.', idx)
        if not auth or 'EMAIL_ADDRESS' not in auth or 'PASSWORD_EMAIL_ADDRESS' not in auth:
            callback(f'[ERRO] Dados de autenticação incompletos: {auth}', idx)

        callback(f'Enviando para: {to} | Título: {titulo_final} | Corpo: {corpo} | Auth: {auth}', idx)
        try:
            send_email(to, auth, titulo_final, corpo)
            callback(f'[OK] E-mail enviado com sucesso para: {to}', idx)
        except Exception as e:
            callback(f'[ERRO] Falha ao enviar para {to}: {e}', idx)

        time.sleep(2)

    # Aviso de conclusão ao final do processamento
    callback('Processamento concluído! Todos os e-mails foram enviados.', total)
