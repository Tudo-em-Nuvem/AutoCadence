import unittest
import sqlite3
import os
from src.repository.usuario_repositorio import RepositorioUsuario

class TestRepositorioUsuario(unittest.TestCase):
    """
    Testes para a classe RepositorioUsuario usando um arquivo de banco de dados temporário.
    """

    def setUp(self):
        """
        Configuração executada antes de cada teste.
        Cria um arquivo de banco de dados temporário para os testes.
        """
        self.db_path = 'test_usuario.db'
        # Garante que não exista um arquivo de um teste anterior que falhou
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        
        # Instancia o repositório, que irá criar a tabela no arquivo de teste.
        self.repositorio = RepositorioUsuario(caminho_banco=self.db_path)

    def tearDown(self):
        """
        Limpeza executada após cada teste.
        Remove o arquivo de banco de dados temporário.
        """
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_tabela_foi_criada(self):
        """
        Testa se a tabela 'usuario' foi criada corretamente no __init__.
        """
        with sqlite3.connect(self.db_path) as conexao:
            cursor = conexao.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='usuario'")
            resultado = cursor.fetchone()
            self.assertIsNotNone(resultado)
            self.assertEqual(resultado[0], 'usuario')

    def test_salvar_e_obter_usuario(self):
        """
        Testa salvar um novo usuário e depois obtê-lo do banco.
        """
        email, senha = "teste@email.com", "123456"
        self.repositorio.salvar_usuario(email, senha)

        usuario = self.repositorio.obter_usuario()
        self.assertIsNotNone(usuario)
        self.assertEqual(usuario[0], email)
        self.assertEqual(usuario[1], senha)

    def test_atualizar_usuario(self):
        """
        Testa a atualização dos dados de um usuário existente.
        """
        self.repositorio.salvar_usuario("antigo@email.com", "senha_antiga")
        novo_email, nova_senha = "novo@email.com", "senha_nova"
        self.repositorio.salvar_usuario(novo_email, nova_senha)

        usuario = self.repositorio.obter_usuario()
        self.assertEqual(usuario[0], novo_email)
        self.assertEqual(usuario[1], nova_senha)

    def test_obter_autenticacao(self):
        """
        Testa a obtenção dos dados de autenticação no formato de dicionário.
        """
        email, senha = "auth@email.com", "senha_auth"
        self.repositorio.salvar_usuario(email, senha)

        auth = self.repositorio.obter_autenticacao()
        self.assertEqual(auth['EMAIL_ADDRESS'], email)
        self.assertEqual(auth['PASSWORD_EMAIL_ADDRESS'], senha)

    def test_obter_autenticacao_sem_usuario(self):
        """
        Testa a obtenção de autenticação quando não há usuário no banco.
        Deve retornar um dicionário vazio.
        """
        auth = self.repositorio.obter_autenticacao()
        self.assertEqual(auth, {})

if __name__ == '__main__':
    unittest.main()
