from abc import ABC, abstractmethod

class InterfaceRepositorioUsuario(ABC):
    """
    Interface para repositórios de usuário.
    Permite abstrair persistência e autenticação do usuário.
    """
    @abstractmethod
    def obter_autenticacao(self):
        pass

    @abstractmethod
    def obter_usuario(self):
        pass

    @abstractmethod
    def salvar_usuario(self, email, senha):
        pass
