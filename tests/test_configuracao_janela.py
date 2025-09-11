import unittest
import os

from src.services.configuracao_dominio_service import ConfiguracaoDominioService

class TestConfiguracaoDominioService(unittest.TestCase):
    """
    Testes para a classe ConfiguracaoDominioService.
    """
    def setUp(self):
        """
        Configura um ficheiro de teste temporário antes de cada teste.
        """
        self.config_filepath = 'test_dominios.json'
        self.service = ConfiguracaoDominioService(config_file=self.config_filepath)

    def tearDown(self):
        """
        Remove o ficheiro de teste temporário após cada teste.
        """
        if os.path.exists(self.config_filepath):
            os.remove(self.config_filepath)

    def test_configuracao_nao_existe_inicialmente(self):
        """
        Verifica se o ficheiro de configuração não existe antes de ser criado.
        """
        self.assertFalse(self.service.configuracao_existe())

    def test_salvar_e_carregar_dominios(self):
        """
        Testa se a lista de domínios é salva e carregada corretamente.
        """
        dominios_para_salvar = ['empresa.com', 'negocio.pt']
        self.service.salvar_dominios(dominios_para_salvar)

        # Verifica se o ficheiro foi criado
        self.assertTrue(self.service.configuracao_existe())

        # Carrega os domínios e verifica se são os mesmos
        dominios_carregados = self.service.carregar_dominios()
        self.assertEqual(dominios_carregados, dominios_para_salvar)

    def test_verificar_dominio_permitido(self):
        """
        Testa a verificação de um e-mail com um domínio permitido.
        """
        self.service.salvar_dominios(['exemplo.com'])
        self.assertTrue(self.service.verificar_dominio('contato@exemplo.com'))

    def test_verificar_dominio_nao_permitido(self):
        """
        Testa a verificação de um e-mail com um domínio não permitido.
        """
        self.service.salvar_dominios(['autorizado.com'])
        self.assertFalse(self.service.verificar_dominio('teste@naoautorizado.com'))

    def test_verificar_dominio_com_lista_vazia(self):
        """
        Testa se a verificação permite qualquer domínio quando a lista de permitidos está vazia.
        """
        self.service.salvar_dominios([])
        self.assertTrue(self.service.verificar_dominio('qualquercoisa@qualquerlugar.com'))

    def test_verificar_dominio_sem_ficheiro_config(self):
        """
        Testa se a verificação permite qualquer domínio se o ficheiro de configuração não existir.
        """
        # Garante que o ficheiro não existe
        if os.path.exists(self.config_filepath):
            os.remove(self.config_filepath)
        
        self.assertTrue(self.service.verificar_dominio('teste@livre.com'))
        
    def test_verificar_email_invalido(self):
        """
        Testa o comportamento ao verificar um e-mail sem '@'.
        """
        self.service.salvar_dominios(['dominio.com'])
        self.assertFalse(self.service.verificar_dominio('emailinvalido'))

if __name__ == '__main__':
    unittest.main()
