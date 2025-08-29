from tkinter import Toplevel, Text, Scrollbar

class LogJanela(Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title('Log de Processamento')
        self.geometry('400x300')
        self.configure(bg='#23272f')
        self.log_text = Text(self, state='normal', bg='#2c2f38', fg='#f5c518', font=('Segoe UI', 11), bd=0, insertbackground='#f5c518')
        self.log_text.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        scrollbar = Scrollbar(self, command=self.log_text.yview, bg='#23272f', troughcolor='#23272f', bd=0)
        scrollbar.pack(side='right', fill='y', padx=(0,10), pady=10)
        self.log_text.config(yscrollcommand=scrollbar.set)

    def log(self, mensagem):
        self.log_text.insert('end', mensagem + '\n')
        self.log_text.see('end')
