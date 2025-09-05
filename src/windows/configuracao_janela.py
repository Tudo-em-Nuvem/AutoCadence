from tkinter import Toplevel, Label, Entry, Button, StringVar
from services.configuracao_dominio_service import ConfiguracaoDominioService

class ConfiguracaoJanela(Toplevel):
  """
  Janela de configuração para editar/visualizar email e senha do usuário.
  """
  def __init__(self, master, usuario_repo):
    super().__init__(master)
    self.title('Configurações')
    self.geometry('390x360')
    self.configure(bg='#23272f')
    self.resizable(False, False)
    self.usuario_repo = usuario_repo


    self.dominio_service = ConfiguracaoDominioService()

    self.email_var = StringVar()
    self.senha_var = StringVar()

    usuario = self.usuario_repo.obter_usuario()
    if usuario:
        self.email_var.set(usuario[0])
        self.senha_var.set(usuario[1])

    Label(self, text='Configurações', font=('Segoe UI', 14, 'bold'), bg='#23272f', fg='#f5c518').pack(pady=(16, 8))
    Label(self, text='Email:', font=('Segoe UI', 11), bg='#23272f', fg='#b0b3b8').pack(pady=(0, 0))
    Entry(self, textvariable=self.email_var, width=30, font=('Segoe UI', 11), bg='#2c2f38', fg='#f5c518', insertbackground='#f5c518', bd=0).pack(pady=5)
    Label(self, text='Senha:', font=('Segoe UI', 11), bg='#23272f', fg='#b0b3b8').pack(pady=(10, 0))
    Entry(self, textvariable=self.senha_var, show='*', width=30, font=('Segoe UI', 11), bg='#2c2f38', fg='#f5c518', insertbackground='#f5c518', bd=0).pack(pady=5)
    Button(self, text='Setup', command=self._salvar_usuario, font=('Segoe UI', 11, 'bold'), bg='#f5c518', fg='#23272f', activebackground='#ffe066', activeforeground='#23272f', bd=0, padx=10, pady=6).pack(pady=(18, 30))
    self.mensagem_erro = Label(self, text='', font=('Segoe UI', 10), bg='#23272f', fg='#ff4d4d')
    self.mensagem_erro.pack()

    # Torna a janela modal e sempre em cima
    self.transient(master)
    self.grab_set()
    self.focus_set()

  def _salvar_usuario(self):
    email = self.email_var.get().strip()
    senha = self.senha_var.get()
    
    if not email or not senha:
      self.mensagem_erro.config(text='Email e senha não podem estar vazios.')
      return

    # Validação usando o serviço
    if not self.dominio_service.verificar_dominio(email):
      dominios_permitidos = ', '.join(self.dominio_service.dominios_permitidos)
      self.mensagem_erro.config(text=f'Domínio não cadastrado para essa aplicação.')
      return
    
    self.usuario_repo.salvar_usuario(email, senha)
    self.destroy()
