import unittest
from unittest.mock import MagicMock, patch, call
from datetime import datetime, timedelta

# Como estamos na pasta 'tests', precisamos garantir que o Python encontre os módulos em 'src'
# Se você seguiu a instrução de instalar o projeto com `pip install -e .`, esta linha não é estritamente necessária,
# mas é uma boa prática para garantir que o teste possa ser executado de forma independente.
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services.cadencia_manager import CadenciaManager

class TestCadenciaManager(unittest.TestCase):
  """
  Testes para a classe CadenciaManager, responsável pela lógica de
  intervalos e pausas automáticas no envio de e-mails.
  """

  def setUp(self):
    """
    Configura um ambiente de teste limpo antes de cada teste.
    """
    # Mock da função de callback para registrar as mensagens enviadas
    self.mock_callback = MagicMock()
    # Mock do controle de processamento, iniciando como ativo
    self.mock_controle = MagicMock()
    self.mock_controle.ativo = True
    # Instancia o CadenciaManager com os mocks
    self.manager = CadenciaManager(self.mock_callback, self.mock_controle)
    # Limpa as chamadas do mock que ocorrem no __init__ para não interferir nos testes
    self.mock_callback.reset_mock()

  @patch('src.services.cadencia_manager.random.randint', return_value=15)
  def test_inicializacao_define_proxima_pausa(self, mock_randint):
    """
    Testa se o __init__ configura corretamente o primeiro ciclo de trabalho.
    """
    # O setUp zera o mock, então para testar a inicialização,
    # criamos uma nova instância aqui com um mock local.
    mock_callback_local = MagicMock()
    manager = CadenciaManager(mock_callback_local, self.mock_controle)

    # Agora, verificamos o resultado da nova instância
    self.assertIsInstance(manager.horario_proxima_pausa, datetime)
    # Verifica se o horário da pausa está no futuro
    self.assertGreater(manager.horario_proxima_pausa, datetime.now())
    # Verifica se a mensagem de log inicial foi enviada para o nosso mock local
    mock_callback_local.assert_called_once()
    self.assertIn("[CADÊNCIA] Ciclo de trabalho iniciado.", mock_callback_local.call_args[0][0])

  @patch('src.services.cadencia_manager.CadenciaManager._aguardar_de_forma_interruptivel')
  @patch('src.services.cadencia_manager.datetime')
  def test_aguardar_proximo_passo_executa_intervalo_curto(self, mock_datetime, mock_aguardar):
    """
    Testa se um intervalo curto (5 a 8s) é executado quando não é hora da pausa longa.
    """
    # Garante que o tempo "agora" seja ANTES do horário da pausa programada
    mock_datetime.now.return_value = self.manager.horario_proxima_pausa - timedelta(minutes=1)

    self.manager.aguardar_proximo_passo()

    # Verifica se o método de espera foi chamado. Não podemos testar o valor exato
    # pois é aleatório, mas podemos verificar se foi chamado uma vez.
    mock_aguardar.assert_called_once()
    # Verificamos se o tempo de espera está dentro do intervalo esperado
    tempo_espera = mock_aguardar.call_args[0][0]
    self.assertGreaterEqual(tempo_espera, 5)
    self.assertLessEqual(tempo_espera, 8)

  @patch('src.services.cadencia_manager.CadenciaManager._executar_pausa_automatica')
  @patch('src.services.cadencia_manager.datetime')
  def test_aguardar_proximo_passo_executa_pausa_longa(self, mock_datetime, mock_pausa_automatica):
    """
    Testa se a pausa automática longa é acionada quando o tempo de trabalho expira.
    """
    # Garante que o tempo "agora" seja DEPOIS do horário da pausa programada
    mock_datetime.now.return_value = self.manager.horario_proxima_pausa + timedelta(seconds=1)

    self.manager.aguardar_proximo_passo()

    # Verifica se a função de pausa longa foi chamada e a de espera curta não
    mock_pausa_automatica.assert_called_once()

  @patch('src.services.cadencia_manager.time.sleep')
  def test_aguardar_de_forma_interruptivel_sem_pausa(self, mock_sleep):
    """
    Testa se a espera aguarda o tempo correto quando não há interrupção.
    """
    self.mock_controle.ativo = True
    duracao = 3 # segundos

    self.manager._aguardar_de_forma_interruptivel(duracao)

    # Verifica se time.sleep(1) foi chamado 3 vezes
    self.assertEqual(mock_sleep.call_count, duracao)
    mock_sleep.assert_has_calls([call(1), call(1), call(1)])

  @patch('src.services.cadencia_manager.time.sleep')
  def test_aguardar_de_forma_interruptivel_com_pausa_manual(self, mock_sleep):
    """
    Testa se a espera é interrompida imediatamente se o usuário pausar.
    """
    # Simula que o usuário pausou o processo
    self.mock_controle.ativo = False

    self.manager._aguardar_de_forma_interruptivel(120) # 2 minutos

    # Verifica que o time.sleep nunca foi chamado, pois a função deve retornar imediatamente
    mock_sleep.assert_not_called()

if __name__ == '__main__':
  unittest.main()
