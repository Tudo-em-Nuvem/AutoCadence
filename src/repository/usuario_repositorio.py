import sqlite3

class RepositorioUsuario:
    """
    Responsável por toda a persistência e recuperação de dados do usuário no banco SQLite local.
    Permite obter, salvar e autenticar usuário para envio de e-mails.
    """
    def __init__(self, caminho_banco='usuario.db'):
        # Caminho do banco de dados SQLite
        self.caminho_banco = caminho_banco
        self._criar_tabela()

    def _criar_tabela(self):
        """Cria a tabela de usuário se não existir."""
        with sqlite3.connect(self.caminho_banco) as conexao:
            cursor = conexao.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS usuario (
                id INTEGER PRIMARY KEY,
                email TEXT,
                senha TEXT
            )''')
            conexao.commit()

    def obter_usuario(self):
        """Obtém o e-mail e senha do usuário cadastrado."""
        with sqlite3.connect(self.caminho_banco) as conexao:
            cursor = conexao.cursor()
            cursor.execute('SELECT email, senha FROM usuario WHERE id=1')
            return cursor.fetchone()

    def salvar_usuario(self, email, senha):
        """Salva ou atualiza o e-mail e senha do usuário."""
        with sqlite3.connect(self.caminho_banco) as conexao:
            cursor = conexao.cursor()
            if self.obter_usuario():
                cursor.execute('UPDATE usuario SET email=?, senha=? WHERE id=1', (email, senha))
            else:
                cursor.execute('INSERT INTO usuario (id, email, senha) VALUES (1, ?, ?)', (email, senha))
            conexao.commit()

    def obter_autenticacao(self):
        """Retorna o dicionário de autenticação para envio de e-mails."""
        usuario = self.obter_usuario()
        if usuario and usuario[0] and usuario[1]:
            return {
                'EMAIL_ADDRESS': usuario[0],
                'PASSWORD_EMAIL_ADDRESS': usuario[1]
            }
        return {}
