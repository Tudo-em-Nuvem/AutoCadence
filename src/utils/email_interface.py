from abc import ABC, abstractmethod

class InterfaceRemetenteEmail(ABC):
    """
    Interface para remetentes de e-mail.
    Permite abstrair o envio de e-mails para diferentes provedores.
    """
    @abstractmethod
    def enviar_email(self, destinatario: str, autenticacao: object, titulo: str, mensagem: str) -> None:
        pass
