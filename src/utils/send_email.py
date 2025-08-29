import smtplib
import ssl
from email.message import EmailMessage
def send_email(to: str, auth: object,title: str, message: str) -> None:
    """
    Envia um e-mail usando o servidor SMTP do Gmail.

    Args:
        to (str): O endereço de e-mail do destinatário.
        title (str): O assunto (título) do e-mail.
        message (str): O corpo da mensagem do e-mail.
    
    Raises:
        Exception: Se ocorrer um erro ao enviar o e-mail.
    """
    # Obtém as credenciais do e-mail a partir de variáveis de ambiente
    EMAIL_ADDRESS = auth['EMAIL_ADDRESS']
    PASSWORD_EMAIL_ADDRESS = auth['PASSWORD_EMAIL_ADDRESS']

    if not EMAIL_ADDRESS or not PASSWORD_EMAIL_ADDRESS:
        print("Erro: As variáveis de ambiente EMAIL_ADDRESS e PASSWORD_EMAIL_ADDRESS não foram definidas.")
        return

    # Cria o objeto do e-mail
    msg = EmailMessage()
    msg['Subject'] = title
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to
    msg.set_content(message)

    # Cria um contexto SSL seguro
    context = ssl.create_default_context()
    try:
        # Conecta-se ao servidor do Gmail usando SSL e envia o e-mail
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(EMAIL_ADDRESS, PASSWORD_EMAIL_ADDRESS)
            smtp.send_message(msg)
        print("E-mail enviado com sucesso!")

    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
        raise Exception("Erro ao enviar e-mail")
