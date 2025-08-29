import sqlite3

class UsuarioRepositorio:
    def get_auth(self):
        usuario = self.obter_usuario()
        if usuario and usuario[0] and usuario[1]:
            return {
                'EMAIL_ADDRESS': usuario[0],
                'PASSWORD_EMAIL_ADDRESS': usuario[1]
            }
        return {}
    """
    Responsável por toda a persistência e recuperação de dados do usuário no banco SQLite local.
    """
    def __init__(self, caminho_db='usuario.db'):
        self.caminho_db = caminho_db
        self._criar_tabela()

    def _criar_tabela(self):
        with sqlite3.connect(self.caminho_db) as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS usuario (
                id INTEGER PRIMARY KEY,
                email TEXT,
                senha TEXT
            )''')
            conn.commit()

    def obter_usuario(self):
        with sqlite3.connect(self.caminho_db) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT email, senha FROM usuario WHERE id=1')
            return cursor.fetchone()

    def salvar_usuario(self, email, senha):
        with sqlite3.connect(self.caminho_db) as conn:
            cursor = conn.cursor()
            if self.obter_usuario():
                cursor.execute('UPDATE usuario SET email=?, senha=? WHERE id=1', (email, senha))
            else:
                cursor.execute('INSERT INTO usuario (id, email, senha) VALUES (1, ?, ?)', (email, senha))
            conn.commit()
