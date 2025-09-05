import pandas as pd

class ProcessadorExcel:
  """
  Classe responsável por carregar e manipular dados de um arquivo Excel.
  Permite obter linhas, colunas e total de registros para processamento.
  """
  def __init__(self, caminho_arquivo):
    self.caminho_arquivo = caminho_arquivo
    self.dataframe = None

  def carregar(self):
    """Carrega o arquivo Excel e armazena o DataFrame interno."""
    self.dataframe = pd.read_excel(self.caminho_arquivo)
    return self.dataframe

  def obter_total_linhas(self):
    """Retorna o total de linhas do DataFrame carregado."""
    if self.dataframe is not None:
      return len(self.dataframe)
    return 0

  def obter_linha(self, indice):
    """Retorna o dicionário da linha pelo índice."""
    if self.dataframe is not None and 0 <= indice < len(self.dataframe):
      return self.dataframe.iloc[indice].to_dict()
    return None

  def obter_colunas(self):
    """Retorna a lista de colunas do DataFrame carregado."""
    if self.dataframe is not None:
      return list(self.dataframe.columns)
    return []

  def remover_duplicados(self, nome_coluna_email: str) -> int:
    """
    Remove linhas duplicadas com base na coluna de e-mail especificada.
    A remoção é feita diretamente no DataFrame interno da classe.

    Args:
      nome_coluna_email (str): O nome da coluna a ser verificada para duplicatas.

    Returns:
      int: O número de linhas duplicadas que foram removidas.
    """
    if self.dataframe is None or nome_coluna_email not in self.dataframe.columns:
      return 0
    
    linhas_originais = len(self.dataframe)
    # Remove duplicatas baseadas na coluna de e-mail, mantendo a primeira ocorrência.
    # A opção inplace=True modifica o dataframe diretamente.
    self.dataframe.drop_duplicates(subset=[nome_coluna_email], keep='first', inplace=True)
    linhas_finais = len(self.dataframe)
    
    return linhas_originais - linhas_finais
