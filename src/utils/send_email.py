import smtplib
import ssl
from email.message import EmailMessage
import imaplib
from email.utils import formatdate

def enviar_email(destinatario: str, autenticacao: object, titulo: str, mensagem: str) -> None:
    """
    Envia um e-mail usando o servidor SMTP do Gmail e salva uma cópia na pasta de enviados.
    """
    EMAIL_ADDRESS = autenticacao['EMAIL_ADDRESS']
    PASSWORD_EMAIL_ADDRESS = autenticacao['PASSWORD_EMAIL_ADDRESS']

    if not EMAIL_ADDRESS or not PASSWORD_EMAIL_ADDRESS:
        print("Erro: E-mail ou senha não configurados na aplicação.")
        return

    email = EmailMessage()
    email['Subject'] = titulo
    email['From'] = EMAIL_ADDRESS
    email['To'] = destinatario
    email['Date'] = formatdate(localtime=True)
    email.set_content(mensagem)

    contexto_ssl = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=contexto_ssl) as smtp:
            smtp.login(EMAIL_ADDRESS, PASSWORD_EMAIL_ADDRESS)
            smtp.send_message(email)
        print("E-mail enviado com sucesso!")

        try:
            mail = imaplib.IMAP4_SSL('imap.gmail.com')
            mail.login(EMAIL_ADDRESS, PASSWORD_EMAIL_ADDRESS)
            
            mail.append(
                '"[Gmail]/Sent Mail"',
                '',
                None,
                email.as_bytes()
            )

            mail.logout()
            print("E-mail salvo com sucesso na pasta de enviados.")
        except Exception as imap_erro:
            print(f"AVISO: O e-mail foi enviado, mas falhou ao salvar na pasta de enviados: {imap_erro}")

    except smtplib.SMTPAuthenticationError:
        erro_msg = "ERRO DE AUTENTICAÇÃO: E-mail ou Senha de App incorretos. Verifique as credenciais nas configurações."
        print(erro_msg)
        raise Exception(erro_msg)
    except Exception as erro:
        print(f"Erro ao enviar e-mail: {erro}")
        raise Exception("Erro ao enviar e-mail")
