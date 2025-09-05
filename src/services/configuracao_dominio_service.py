import json
import os
import sys

class ConfiguracaoDominioService:
  """
  Gerencia a configuração de domínios permitidos, carregando a informação
  de um ficheiro embutido no executável.
  """
  def __init__(self, config_filename='dominios_permitidos.json'):
    self.dominios_permitidos = self._carregar_dominios_embutidos(config_filename)

  def _obter_caminho_config(self, filename):
    """
    Obtém o caminho para o ficheiro de configuração, quer a aplicação
    esteja a ser executada a partir do código-fonte ou de um executável PyInstaller.
    """
    if getattr(sys, 'frozen', False):
      # Se a aplicação estiver "congelada" (ou seja, a rodar a partir de um .exe)
      base_path = sys._MEIPASS
    else:
      # Se estiver a ser executada a partir do código-fonte
      base_path = os.path.dirname(os.path.abspath(__file__))
      # Volta um nível para a pasta 'src'
      base_path = os.path.join(base_path, '..')

    return os.path.join(base_path, filename)

  def _carregar_dominios_embutidos(self, config_filename) -> list[str]:
    """Carrega a lista de domínios permitidos a partir do ficheiro embutido."""
    config_path = self._obter_caminho_config(config_filename)
    
    if not os.path.exists(config_path):
      # Se o ficheiro não foi encontrado, permite todos os domínios por defeito.
      # Isto é útil para o desenvolvimento, antes da build.
      print("AVISO: Ficheiro de configuração de domínios não encontrado. A permitir todos os domínios.")
      return []
        
    try:
      with open(config_path, 'r') as f:
        config = json.load(f)
        dominios = config.get('dominios_permitidos', [])
        print(f"Domínios permitidos carregados: {dominios}")
        return dominios

    except (IOError, json.JSONDecodeError) as e:
      print(f"Erro ao carregar o ficheiro de configuração de domínios: {e}")
      return [] # Em caso de erro, permite todos os domínios.

  def verificar_dominio(self, email: str) -> bool:
    """Verifica se o domínio de um e-mail está na lista de permitidos."""
    # Se a lista de domínios estiver vazia, significa que não há restrições.
    if not self.dominios_permitidos:
      return True
        
    try:
      dominio_email = email.split('@')[-1].lower()
      return dominio_email in self.dominios_permitidos
    except IndexError:
      return False
