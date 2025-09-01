import smtplib
import ssl
from email.message import EmailMessage

def enviar_email(destinatario: str, autenticacao: object, titulo: str, mensagem: str) -> None:
    """
    Envia um e-mail usando o servidor SMTP do Gmail.
    - destinatario: e-mail do destinatário
    - autenticacao: dicionário com EMAIL_ADDRESS e PASSWORD_EMAIL_ADDRESS
    - titulo: assunto do e-mail
    - mensagem: corpo do e-mail
    """
    EMAIL_ADDRESS = autenticacao['EMAIL_ADDRESS']
    PASSWORD_EMAIL_ADDRESS = autenticacao['PASSWORD_EMAIL_ADDRESS']

    if not EMAIL_ADDRESS or not PASSWORD_EMAIL_ADDRESS:
        print("Erro: As variáveis de ambiente EMAIL_ADDRESS e PASSWORD_EMAIL_ADDRESS não foram definidas.")
        return

    # Cria o objeto do e-mail
    email = EmailMessage()
    email['Subject'] = titulo
    email['From'] = EMAIL_ADDRESS
    email['To'] = destinatario
    email.set_content(mensagem)

    # Cria um contexto SSL seguro
    contexto_ssl = ssl.create_default_context()
    try:
        # Conecta-se ao servidor do Gmail usando SSL e envia o e-mail
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=contexto_ssl) as smtp:
            smtp.login(EMAIL_ADDRESS, PASSWORD_EMAIL_ADDRESS)
            smtp.send_message(email)
        print("E-mail enviado com sucesso!")
    except Exception as erro:
        print(f"Erro ao enviar e-mail: {erro}")
        raise Exception("Erro ao enviar e-mail")
