
import time
from utils.substituicao import substituir_variaveis
from services.excel_processor import ProcessadorExcel

def processar_e_enviar_emails(caminho_arquivo_excel, funcao_callback, controle_processamento, corpo_email, linha_inicial=0, titulo_email='', autenticacao=None, remetente_email=None, nome_coluna_email=None):
    """
    Processa o arquivo Excel linha a linha e envia e-mails personalizados para cada destinatário.
    - caminho_arquivo_excel: caminho do arquivo Excel a ser processado
    - funcao_callback: função chamada para atualizar status/log
    - controle_processamento: objeto para pausar ou parar processamento
    - corpo_email: texto do corpo do e-mail, pode conter variáveis
    - linha_inicial: linha de início do processamento
    - titulo_email: título do e-mail, pode conter variáveis
    - autenticacao: dados de autenticação do remetente
    - remetente_email: objeto responsável por enviar e-mails
    - nome_coluna_email: nome da coluna que contém os e-mails dos destinatários
    """
    excel = ProcessadorExcel(caminho_arquivo_excel)
    excel.carregar()
    total_linhas = excel.obter_total_linhas()

    for indice in range(linha_inicial, total_linhas):
        linha = excel.obter_linha(indice)
        if not controle_processamento.ativo:
            funcao_callback('Processamento pausado.', indice-1 if indice > 0 else 0)
            break

        funcao_callback(f'Tratando linha: {linha}', indice)

        # Recupera o destinatário do e-mail
        destinatario = None
        if nome_coluna_email and nome_coluna_email in linha:
            destinatario = linha[nome_coluna_email]
        else:
            for nome in ['email', 'Email', 'E-mail']:
                if nome in linha:
                    destinatario = linha[nome]
                    break

        # Valida se o destinatário é um e-mail válido
        if not destinatario or not isinstance(destinatario, str) or '@' not in destinatario:
            funcao_callback(f'[ERRO] Nenhum e-mail válido encontrado na linha {indice+1}.', indice)
            continue

        # Substitui variáveis no corpo e título do e-mail
        corpo_personalizado = substituir_variaveis(corpo_email, linha) if corpo_email else corpo_email
        titulo_personalizado = substituir_variaveis(titulo_email, linha) if titulo_email else titulo_email

        if not titulo_personalizado:
            funcao_callback(f'[AVISO] Título do e-mail está vazio na linha {indice+1}.', indice)
        if not corpo_personalizado:
            funcao_callback(f'[AVISO] Corpo do e-mail está vazio na linha {indice+1}.', indice)
        if not autenticacao or 'EMAIL_ADDRESS' not in autenticacao or 'PASSWORD_EMAIL_ADDRESS' not in autenticacao:
            funcao_callback(f'[ERRO] Dados de autenticação incompletos: {autenticacao}', indice)

        funcao_callback(f'Enviando para: {destinatario} | Título: {titulo_personalizado} | Corpo: {corpo_personalizado} | Auth: {autenticacao}', indice)
        try:
            # Envia o e-mail usando o remetente injetado
            if remetente_email:
                remetente_email.enviar_email(destinatario, autenticacao, titulo_personalizado, corpo_personalizado)
            funcao_callback(f'[OK] E-mail enviado com sucesso para: {destinatario}', indice)
        except Exception as erro:
            funcao_callback(f'[ERRO] Falha ao enviar para {destinatario}: {erro}', indice)

        # Aguarda 2 segundos entre envios para evitar bloqueios
        time.sleep(2)

    # Informa que o processamento foi concluído
    funcao_callback('Processamento concluído! Todos os e-mails foram enviados.', total_linhas)
