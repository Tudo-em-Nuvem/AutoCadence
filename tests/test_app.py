import unittest
from unittest.mock import patch, MagicMock
from src.app import App

class TestApp(unittest.TestCase):
  """
  Testes para a classe principal da aplicação, App.
  """
  @patch('src.app.Tk')
  def setUp(self, mock_tk):
    """
    Configuração inicial dos testes para a classe App.
    Usa mocks para evitar a criação de uma janela Tkinter real.
    """
    self.app = App()
    # Mock dos componentes da UI para que possamos simular interações
    self.app.titulo_entry = MagicMock()
    self.app.texto_entry = MagicMock()
    self.app.email_col_combobox = MagicMock()
    self.app.btn_run = MagicMock()
    self.app.usuario_repo = MagicMock()
    self.app.df = MagicMock()
    self.app.exemplo_text = MagicMock()

  def test_atualizar_estado_botao_run_habilitado(self):
    """
    Testa se o botão 'run' é habilitado quando todas as condições são atendidas.
    """
    self.app.titulo_entry.get.return_value = "Título Teste"
    self.app.texto_entry.get.return_value = "Corpo do e-mail."
    self.app.email_col_combobox.get.return_value = "email"
    self.app.usuario_repo.obter_autenticacao.return_value = {
      'EMAIL_ADDRESS': 'user@teste.com',
      'PASSWORD_EMAIL_ADDRESS': 'senha'
    }
    self.app.df.columns = ["nome", "email"]
    self.app.atualizar_estado_botao_run()
    self.app.btn_run.config.assert_called_with(state='normal')

  def test_atualizar_estado_botao_run_desabilitado(self):
    """
    Testa se o botão 'run' permanece desabilitado se alguma condição não for atendida.
    """
    # CORREÇÃO: O erro de digitação estava aqui.
    self.app.titulo_entry.get.return_value = "" # Título vazio
    self.app.texto_entry.get.return_value = "Corpo do e-mail."
    self.app.email_col_combobox.get.return_value = "email"
    self.app.usuario_repo.obter_autenticacao.return_value = {
      'EMAIL_ADDRESS': 'user@teste.com', 'PASSWORD_EMAIL_ADDRESS': 'senha'
    }
    self.app.df.columns = ["nome", "email"]
    self.app.atualizar_estado_botao_run()
    self.app.btn_run.config.assert_called_with(state='disabled')

  @patch('src.app.substituir_variaveis')
  def test_atualizar_exemplo_preview(self, mock_substituir):
    """
    Testa a atualização do preview do e-mail.
    """
    mock_df = MagicMock()
    mock_df.empty = False
    linha_amostra = {'Nome': 'Exemplo', 'email': 'ex@mp.lo'}
    mock_df.sample.return_value.iloc[0].to_dict.return_value = linha_amostra
    self.app.df = mock_df

    texto_corpo = "Olá {{Nome}}!"
    self.app.texto_entry.get.return_value = texto_corpo
    mock_substituir.return_value = "Olá Exemplo!"
    self.app.atualizar_exemplo_preview()
    mock_substituir.assert_called_with(texto_corpo, linha_amostra)
    self.app.exemplo_text.insert.assert_called_with('end', 'Exemplo: Olá Exemplo!')

if __name__ == '__main__':
  unittest.main()
