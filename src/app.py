from services.excel_processor import ProcessadorExcel
from services.email_sender import RemetenteEmail
from tkinter import Tk, Label, Button, Frame, Text, Scrollbar, filedialog, messagebox, ttk
from repository.usuario_repositorio import RepositorioUsuario
from windows.configuracao_janela import ConfiguracaoJanela
from windows.log_janela import LogJanela
from services.processador_excel import processar_e_enviar_emails
from utils.substituicao import substituir_variaveis
import threading

class EventBinder:
  def __init__(self, app):
    self.app = app

  def bind_all(self):
    self.app.texto_entry.bind('<KeyRelease>', lambda e: self.app.atualizar_exemplo_preview())
    self.app.titulo_entry.bind('<KeyRelease>', lambda e: self.app.atualizar_estado_botao_run())
    self.app.email_col_combobox.bind('<<ComboboxSelected>>', self.app.on_email_col_selected)
    self.app.email_col_combobox.bind('<FocusOut>', self.app.atualizar_estado_botao_run)
    self.app.titulo_entry.bind('<FocusOut>', self.app.atualizar_estado_botao_run)
    self.app.texto_entry.bind('<FocusOut>', self.app.atualizar_estado_botao_run)

class LogHandler:
  def __init__(self, app):
    self.app = app
    self.log_window = None

  def open_log_window(self):
    if self.log_window is None or not self.log_window.winfo_exists():
      self.log_window = LogJanela(self.app)

  def log(self, mensagem):
    if self.log_window and self.log_window.winfo_exists():
      self.log_window.log(mensagem)

class ConfigHandler:
  def __init__(self, app, usuario_repo):
    self.app = app
    self.usuario_repo = usuario_repo
  def open_config_window(self):
    ConfiguracaoJanela(self.app, self.usuario_repo)

class ControleProcessamento:
  def __init__(self):
    self.ativo = False

class App(Tk):
  _last_instance = None
  def __init__(self):
    App._last_instance = self
    super().__init__()
    self.title('AutoCadence App')
    self.geometry('700x500')
    self.configure(bg='#23272f')
    self.resizable(True, True)
    self.usuario_repo = RepositorioUsuario()
    self.controle = ControleProcessamento()
    self.caminho_excel = None
    self.df = None
    self.total_linhas = 0
    self.linha_atual = 0
    self.excel_processor = None
    self.email_sender = RemetenteEmail()
    self.event_binder = EventBinder(self)
    self.log_handler = LogHandler(self)
    self.config_handler = ConfigHandler(self, self.usuario_repo)
    card = Frame(self, bg='#2c2f38', bd=2, relief='groove')
    card.pack(pady=10, padx=20, fill='both', expand=True)
    frame_botoes = Frame(card, bg='#2c2f38')
    frame_botoes.pack(side='top', fill='x', pady=(10, 0))
    self.btn_excel = Button(frame_botoes, text='Selecionar arquivo Excel', font=('Segoe UI', 12), command=self.selecionar_arquivo_excel, bg='#f5c518', fg='#23272f', activebackground='#ffe066', activeforeground='#23272f', bd=0, padx=10, pady=8)
    self.btn_excel.pack(side='left', padx=10)
    self.btn_run = Button(frame_botoes, text='▶️', font=('Segoe UI Symbol', 16), command=self.alternar_estado_processamento, state='disabled', bg='#23272f', fg='#f5c518', activebackground='#23272f', activeforeground='#ffe066', bd=0, padx=10, pady=8)
    self.btn_run.pack(side='left', padx=10)
    self.btn_config = Button(frame_botoes, text='⚙️', font=('Segoe UI Symbol', 16), command=self.abrir_janela_configuracoes, bg='#23272f', fg='#b0b3b8', activebackground='#23272f', activeforeground='#f5c518', bd=0, padx=10, pady=8)
    self.btn_config.pack(side='right', padx=10)
    Button(frame_botoes, text='Fechar', command=self.destroy, font=('Segoe UI', 12), bg='#23272f', fg='#b0b3b8', activebackground='#23272f', activeforeground='#f5c518', bd=0, padx=10, pady=8).pack(side='right', padx=10)
    self.label_progresso = Label(card, text='Progresso: 0/0', font=('Segoe UI', 11), bg='#2c2f38', fg='#f5c518')
    self.label_progresso.pack(side='top', anchor='w', padx=10, pady=(0, 5))
    frame_texto = Frame(card, bg='#2c2f38')
    frame_texto.pack(side='top', fill='both', expand=True, padx=10, pady=(10, 10))
    self.email_col_label = Label(frame_texto, text='Selecione a coluna de e-mail:', font=('Segoe UI', 11), bg='#2c2f38', fg='#b0b3b8')
    self.email_col_label.pack_forget()
    self.email_col_combobox = ttk.Combobox(frame_texto, state='readonly', font=('Segoe UI', 11))
    self.email_col_combobox.pack_forget()
    self.coluna_email_selecionada = None
    self.titulo_label = Label(frame_texto, text='Título do e-mail:', font=('Segoe UI', 11), bg='#2c2f38', fg='#b0b3b8')
    self.titulo_label.pack(anchor='w', pady=(0,2))
    self.titulo_entry = Text(frame_texto, height=2, font=('Segoe UI', 11), bg='#23272f', fg='#f5c518', insertbackground='#f5c518', bd=0, wrap='word')
    self.titulo_entry.pack(fill='both', expand=False, pady=(0,8))
    self.texto_label = Label(frame_texto, text='Corpo do e-mail:', font=('Segoe UI', 11), bg='#2c2f38', fg='#b0b3b8')
    self.texto_label.pack(anchor='w', pady=(0,2)) 
    self.texto_entry = Text(frame_texto, height=5, font=('Segoe UI', 11), bg='#23272f', fg='#f5c518', insertbackground='#f5c518', bd=0, wrap='word')
    self.texto_entry.pack(fill='both', expand=True, pady=(0,8))
    exemplo_frame = Frame(frame_texto, bg='#2c2f38')
    exemplo_frame.pack(fill='both', expand=True, pady=(0,8))
    self.exemplo_text = Text(exemplo_frame, height=5, font=('Segoe UI', 10), bg='#23272f', fg='#ffe066', wrap='word', bd=0, state='disabled')
    self.exemplo_text.pack(side='left', fill='both', expand=True)
    exemplo_scroll = Scrollbar(exemplo_frame, command=self.exemplo_text.yview)
    exemplo_scroll.pack(side='right', fill='y')
    self.exemplo_text.config(yscrollcommand=exemplo_scroll.set)

  def selecionar_arquivo_excel(self):
    file_path = filedialog.askopenfilename(
      title='Selecione um arquivo Excel',
      filetypes=[('Excel Files', '*.xlsx *.xls')]
    )

    if file_path:
      self.caminho_excel = file_path
      messagebox.showinfo('Arquivo selecionado', f'Arquivo selecionado:\n{file_path}')
      self.btn_run.config(state='disabled')

      try:
        self.excel_processor = ProcessadorExcel(file_path)
        self.df = self.excel_processor.carregar()
        self.total_linhas = self.excel_processor.obter_total_linhas()
        self.linha_atual = 0
        colunas = self.excel_processor.obter_colunas()
        self.email_col_combobox['values'] = colunas 
        self.email_col_combobox.set('')
        self.email_col_label.pack_forget()
        self.email_col_combobox.pack_forget()
        self.email_col_label.pack(anchor='w', pady=(0,2), before=self.titulo_label)
        self.email_col_combobox.pack(fill='x', pady=(0,8), before=self.titulo_label)
      except Exception as e:
        messagebox.showerror("Erro ao Carregar", f"Ocorreu um erro ao carregar o arquivo Excel: {e}")
        self.df = None
        self.total_linhas = 0
        self.linha_atual = 0
        self.email_col_label.pack_forget()
        self.email_col_combobox.pack_forget()

    self.atualizar_exemplo_preview()
    self.atualizar_contador_progresso()
    self.atualizar_estado_botao_run()

  def on_email_col_selected(self, event=None):
    """
    Chamado quando o usuário seleciona a coluna de e-mail.
    Remove duplicados e atualiza a UI.
    """
    coluna_selecionada = self.email_col_combobox.get()
    
    if not coluna_selecionada or self.excel_processor is None:
      return

    try:
      removidos = self.excel_processor.remover_duplicados(coluna_selecionada)
      if removidos > 0:
        messagebox.showinfo(
          "Limpeza de Duplicados",
          f"{removidos} e-mail(s) duplicado(s) foram removidos da lista."
        )
        self.total_linhas = self.excel_processor.obter_total_linhas()
        self.atualizar_contador_progresso()
        self.atualizar_exemplo_preview()
    except Exception as e:
      messagebox.showerror("Erro ao Limpar", f"Ocorreu um erro ao remover e-mails duplicados: {e}")

    self.atualizar_estado_botao_run()

  def on_text_fields_changed(self, event):
    self.atualizar_estado_botao_run()

  def atualizar_estado_botao_run(self, event=None):
    titulo = self.titulo_entry.get('1.0', 'end').strip()
    corpo = self.texto_entry.get('1.0', 'end').strip()
    coluna_email = self.email_col_combobox.get().strip()
    auth = self.usuario_repo.obter_autenticacao() if hasattr(self.usuario_repo, 'obter_autenticacao') else {}

    coluna_email_ok = bool(coluna_email)
    if self.df is not None and hasattr(self.df, 'columns'):
      coluna_email_ok = coluna_email in self.df.columns

    auth_ok = auth and 'EMAIL_ADDRESS' in auth and 'PASSWORD_EMAIL_ADDRESS' in auth and auth['EMAIL_ADDRESS'] and auth['PASSWORD_EMAIL_ADDRESS']

    if coluna_email_ok and titulo and corpo and auth_ok:
      self.btn_run.config(state='normal')
    else:
      self.btn_run.config(state='disabled')

  def alternar_estado_processamento(self):
    titulo = self.titulo_entry.get('1.0', 'end').strip()
    corpo = self.texto_entry.get('1.0', 'end').strip()

    auth = self.usuario_repo.obter_autenticacao() if hasattr(self.usuario_repo, 'obter_autenticacao') else {}
    if not titulo or not corpo or not auth or not auth.get('EMAIL_ADDRESS') or not auth.get('PASSWORD_EMAIL_ADDRESS'):
      messagebox.showwarning('Campos obrigatórios', 'Preencha título, corpo e configure e-mail/senha antes de enviar!')
      return
    
    if not self.controle.ativo:
      self.controle.ativo = True
      self.btn_run.config(text='⏸️')
      self.abrir_janela_log()
      self.iniciar_processo_envio()
    else:
      self.controle.ativo = False
      self.btn_run.config(text='▶️')

  def atualizar_contador_progresso(self):
    self.label_progresso.config(text=f'Progresso: {self.linha_atual}/{self.total_linhas}')

  def atualizar_exemplo_preview(self):
    texto = self.texto_entry.get('1.0', 'end').strip()
    if hasattr(self, 'df') and self.df is not None and not self.df.empty and texto:
      linha = self.df.sample(1).iloc[0].to_dict()
      exemplo = self.substituir_variaveis(texto, linha)
      self.exemplo_text.config(state='normal')
      self.exemplo_text.delete('1.0', 'end')
      self.exemplo_text.insert('end', f'Exemplo: {exemplo}')
      self.exemplo_text.config(state='disabled')
    else:
      self.exemplo_text.config(state='normal')
      self.exemplo_text.delete('1.0', 'end')
      self.exemplo_text.config(state='disabled')

  def substituir_variaveis(self, texto, linha):
    return substituir_variaveis(texto, linha)

  def abrir_janela_log(self):
    self.log_handler.open_log_window()

  def registrar_log(self, mensagem):
    self.log_handler.log(mensagem)

  def iniciar_processo_envio(self):
    titulo = self.titulo_entry.get('1.0', 'end').strip()
    corpo = self.texto_entry.get('1.0', 'end').strip()
    auth = self.usuario_repo.obter_autenticacao() if hasattr(self.usuario_repo, 'obter_autenticacao') else {}
    texto = corpo
    coluna_email = self.email_col_combobox.get().strip()

    def processar():
      def callback_linha(mensagem, linha_idx=None):
        if linha_idx is not None:
          self.linha_atual = linha_idx + 1
          self.after(0, self.atualizar_contador_progresso)
        self.after(0, lambda: self.registrar_log(mensagem))

      processar_e_enviar_emails(
        self.excel_processor,
        callback_linha,
        self.controle,
        texto,
        self.linha_atual,
        titulo,
        auth,
        remetente_email=self.email_sender,
        nome_coluna_email=coluna_email
      )

    threading.Thread(target=processar, daemon=True).start()

  def abrir_janela_configuracoes(self):
    self.config_handler.open_config_window()

  def configurar_eventos(self):
    self.texto_entry.bind('<KeyRelease>', lambda e: self.atualizar_exemplo_preview())

if __name__ == '__main__':
  app = App()
  app.event_binder.bind_all()
  app.mainloop()

