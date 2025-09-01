import pandas as pd

class ProcessadorExcel:
  """
  Classe responsável por carregar e manipular dados de um arquivo Excel.
  Permite obter linhas, colunas e total de registros para processamento.
  """
  def __init__(self, caminho_arquivo):
    # Salva o caminho do arquivo Excel
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
