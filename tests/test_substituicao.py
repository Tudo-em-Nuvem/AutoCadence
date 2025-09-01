import unittest
import sys
import os

# Adiciona o diretório raiz do projeto ao sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils.substituicao import substituir_variaveis

class TestSubstituicao(unittest.TestCase):
  """
  Testes para o módulo de substituição de variáveis.
  """

  def test_substituir_variaveis_simples(self):
    """
    Testa a substituição de uma única variável no texto.
    """
    texto = "Olá {{nome}}, tudo bem?"
    dados_linha = {"nome": "João"}
    resultado = substituir_variaveis(texto, dados_linha)
    self.assertEqual(resultado, "Olá João, tudo bem?")

  def test_substituir_multiplas_variaveis(self):
    """
    Testa a substituição de múltiplas variáveis no mesmo texto.
    """
    texto = "O produto {{produto}} custa R$ {{preco}}."
    dados_linha = {"produto": "Caneta", "preco": "2.50"}
    resultado = substituir_variaveis(texto, dados_linha)
    self.assertEqual(resultado, "O produto Caneta custa R$ 2.50.")

  def test_variavel_nao_encontrada(self):
    """
    Testa o comportamento quando uma variável no texto não existe nos dados.
    A variável deve ser mantida no formato original.
    """
    texto = "Olá {{nome}}, seu email é {{email}}."
    dados_linha = {"nome": "Maria"}
    resultado = substituir_variaveis(texto, dados_linha)
    self.assertEqual(resultado, "Olá Maria, seu email é {{email}}.")

  def test_substituicao_case_insensitive(self):
    """
    Testa se a substituição ignora maiúsculas/minúsculas no nome da variável.
    """
    texto = "Olá {{  NoMe  }}, seja bem-vindo."
    dados_linha = {"nome": "Carlos"}
    resultado = substituir_variaveis(texto, dados_linha)
    self.assertEqual(resultado, "Olá Carlos, seja bem-vindo.")

  def test_texto_sem_variaveis(self):
    """
    Testa um texto que não contém variáveis.
    O texto original deve ser retornado.
    """
    texto = "Este é um texto simples sem variáveis."
    dados_linha = {"nome": "Teste"}
    resultado = substituir_variaveis(texto, dados_linha)
    self.assertEqual(resultado, texto)

if __name__ == '__main__':
  unittest.main()