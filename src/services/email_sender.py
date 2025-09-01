from utils.email_interface import InterfaceRemetenteEmail
from utils.send_email import enviar_email

class RemetenteEmail(InterfaceRemetenteEmail):
    """
    Implementa o envio de e-mails usando a função utilitária enviar_email.
    Permite trocar a implementação facilmente por outra que siga a interface.
    """
    def enviar_email(self, destinatario: str, autenticacao: object, titulo: str, mensagem: str) -> None:
        enviar_email(destinatario, autenticacao, titulo, mensagem)
