import os
import json
import subprocess
import sys

# Define o nome do ficheiro de configuração que será embutido.
CONFIG_FILENAME = 'dominios_permitidos.json'
# Define o caminho onde o ficheiro será salvo, dentro da estrutura do projeto.
CONFIG_FILEPATH = os.path.join('src', CONFIG_FILENAME)

def solicitar_dominios():
  """Solicita ao desenvolvedor a lista de domínios permitidos."""
  print("--- Configuração de Build do AutoCadence ---")
  print("Insira os domínios de e-mail que serão permitidos nesta build.")
  print("Separe múltiplos domínios por vírgula (ex: empresa.com, negocio.pt)")
  
  dominios_str = input("Domínios permitidos: ").strip()
  
  if not dominios_str:
    print("Nenhum domínio inserido. A build permitirá qualquer domínio.")
    return []
      
  # Limpa e formata a lista de domínios
  dominios_lista = [d.strip().lower() for d in dominios_str.split(',')]
  return dominios_lista

def criar_arquivo_config(dominios):
  """Cria o ficheiro de configuração JSON com a lista de domínios."""
  config_data = {'dominios_permitidos': dominios}
  try:
    with open(CONFIG_FILEPATH, 'w') as f:
      json.dump(config_data, f, indent=4)
    print(f"'{CONFIG_FILEPATH}' criado com sucesso.")
    return True
  except IOError as e:
    print(f"ERRO: Não foi possível criar o ficheiro de configuração: {e}")
    return False

def executar_pyinstaller():
  """Executa o PyInstaller para criar o executável."""
  print("\n--- A iniciar o processo de build com PyInstaller ---")
  
  # Comando para o PyInstaller
  # --add-data: Inclui o nosso ficheiro de configuração dentro do .exe
  # No Windows, o separador de caminhos é ';', no Linux/macOS é ':'
  path_separator = ';' if sys.platform == 'win32' else ':'
  
  command = [
    'pyinstaller',
    'src/app.py',
    '--name=AutoCadence',
    '--onefile',
    '--windowed',
    f'--add-data={CONFIG_FILEPATH}{path_separator}.'
  ]
  
  try:
    subprocess.run(command, check=True)
    print("\n--- Build concluída com sucesso! ---")
    print(f"O executável 'AutoCadence.exe' encontra-se na pasta 'dist'.")
  except subprocess.CalledProcessError as e:
    print(f"\nERRO: O PyInstaller falhou com o código de saída {e.returncode}.")
    print("Verifique as mensagens de erro acima.")
  except FileNotFoundError:
    print("\nERRO: O comando 'pyinstaller' não foi encontrado.")
    print("Certifique-se de que o PyInstaller está instalado no seu ambiente virtual ('pip install pyinstaller').")

def limpar_arquivo_config():
    """Remove o ficheiro de configuração após a build para não o enviar para o Git."""
    if os.path.exists(CONFIG_FILEPATH):
      os.remove(CONFIG_FILEPATH)
      print(f"'{CONFIG_FILEPATH}' removido.")

if __name__ == '__main__':
    dominios_permitidos = solicitar_dominios()
    
    if criar_arquivo_config(dominios_permitidos):
      executar_pyinstaller()
    
    # A limpeza ocorre sempre, mesmo que a build falhe.
    limpar_arquivo_config()
