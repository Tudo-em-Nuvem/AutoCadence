import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import sys
import os

# Adiciona o diretório raiz do projeto ao sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services.excel_processor import ProcessadorExcel

class TestProcessadorExcel(unittest.TestCase):
  """
  Testes para a classe ProcessadorExcel.
  """

  @patch('pandas.read_excel')
  def test_carregar_arquivo(self, mock_read_excel):
    """
    Testa se o método carregar chama a função read_excel do pandas
    e armazena o DataFrame.
    """
    # Cria um DataFrame de exemplo
    dados_fake = {'Nome': ['Ana', 'Bruno'], 'Email': ['ana@teste.com', 'bruno@teste.com']}
    df_fake = pd.DataFrame(dados_fake)
    mock_read_excel.return_value = df_fake

    # Instancia o processador e carrega o arquivo
    processador = ProcessadorExcel('caminho/fake/arquivo.xlsx')
    df_carregado = processador.carregar()

    # Verifica se o DataFrame foi carregado corretamente
    self.assertIsNotNone(df_carregado)
    self.assertEqual(len(df_carregado), 2)
    pd.testing.assert_frame_equal(df_carregado, df_fake)

  def setUp(self):
    """
    Configuração inicial para os testes. Cria um ProcessadorExcel
    com um DataFrame fake.
    """
    dados_fake = {'Nome': ['Carlos', 'Daniela'], 'Idade': [30, 25]}
    self.df_fake = pd.DataFrame(dados_fake)
    self.processador = ProcessadorExcel('caminho/fake')
    self.processador.dataframe = self.df_fake

  def test_obter_total_linhas(self):
    """
    Testa se o total de linhas do DataFrame é retornado corretamente.
    """
    total = self.processador.obter_total_linhas()
    self.assertEqual(total, 2)

  def test_obter_linha_existente(self):
    """
    Testa a obtenção de uma linha por um índice válido.
    """
    linha = self.processador.obter_linha(0)
    self.assertEqual(linha, {'Nome': 'Carlos', 'Idade': 30})

  def test_obter_linha_inexistente(self):
    """
    Testa a obtenção de uma linha por um índice inválido.
    Deve retornar None.
    """
    linha = self.processador.obter_linha(5)
    self.assertIsNone(linha)

  def test_obter_colunas(self):
    """
    Testa se a lista de colunas do DataFrame é retornada corretamente.
    """
    colunas = self.processador.obter_colunas()
    self.assertEqual(colunas, ['Nome', 'Idade'])

if __name__ == '__main__':
  unittest.main()