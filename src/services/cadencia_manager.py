import time
import random
from datetime import datetime, timedelta

class CadenciaManager:
  """
  Gerencia a cadência de envio de e-mails, introduzindo pausas automáticas
  e intervalos variáveis para simular um comportamento mais humano e evitar bloqueios.
  """

  def __init__(self, funcao_callback, controle_processamento):
    """
    Inicializa o gerenciador de cadência.
 
    Args:
      funcao_callback (function): Função para enviar mensagens de log para a UI.
      controle_processamento (ControleProcessamento): Objeto para verificar o estado (ativo/pausado) do processo.
    """
    self.funcao_callback = funcao_callback
    self.controle_processamento = controle_processamento
    self._reiniciar_ciclo_trabalho()

  def _reiniciar_ciclo_trabalho(self):
    """Define e informa um novo ciclo de trabalho com duração aleatória."""
    minutos_trabalho = random.randint(10, 20)
    self.horario_proxima_pausa = datetime.now() + timedelta(minutes=minutos_trabalho)
    self.funcao_callback(
      f"[CADÊNCIA] Ciclo de trabalho iniciado. Próxima pausa automática programada para as {self.horario_proxima_pausa.strftime('%H:%M:%S')}."
    )

  def _executar_pausa_automatica(self):
    """Executa uma pausa automática com duração aleatória, permitindo interrupção manual."""
    minutos_pausa = random.randint(3, 15)
    horario_retorno = datetime.now() + timedelta(minutes=minutos_pausa)
    self.funcao_callback(
        f"[CADÊNCIA] Pausa automática iniciada. Duração: {minutos_pausa} minutos. Retorno previsto para as {horario_retorno.strftime('%H:%M:%S')}."
    )

    self._aguardar_de_forma_interruptivel(minutos_pausa * 60)

    # Se o processo não foi pausado manualmente durante a espera
    if self.controle_processamento.ativo:
      self.funcao_callback("[CADÊNCIA] Pausa automática finalizada. Retomando envios.")
      self._reiniciar_ciclo_trabalho()

  def _aguardar_de_forma_interruptivel(self, duracao_segundos: int):
    """
    Aguarda por um determinado tempo, mas verifica o controle de pausa
    a cada segundo para permitir que o usuário interrompa a espera.
    """
    for _ in range(duracao_segundos):
      if not self.controle_processamento.ativo:
        # Interrompe a espera se o usuário pausou manualmente
        return
      time.sleep(1)

  def aguardar_proximo_passo(self):
    """
    Método principal que gerencia o tempo entre os envios.
    Ele decide se é hora de uma pausa longa ou de um intervalo curto.
    """
    # Primeiro, verifica se um ciclo de trabalho terminou e uma pausa longa é necessária.
    if datetime.now() >= self.horario_proxima_pausa:
      self._executar_pausa_automatica()
      # Após uma pausa longa, não é necessário um intervalo curto adicional.
      return

    # Se não for hora de uma pausa longa, aguarda um intervalo curto e aleatório.
    intervalo_curto_segundos = random.randint(5, 8)
    self._aguardar_de_forma_interruptivel(intervalo_curto_segundos)
