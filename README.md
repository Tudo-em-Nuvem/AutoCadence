# AutoCadence

Este projeto é um aplicativo desktop feito com Tkinter.

## Estrutura do projeto

```
AutoCadence/
├── src/
│   ├── app.py
│   └── utils/
│       └── send_email.py
├── setup.py
├── MANIFEST.in
├── requirements.txt
├── README.md
└── .venv/
```

## Como instalar e executar

1. Crie o ambiente virtual:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Para instalar o app como pacote:
   ```bash
   pip install .
   ```
4. Para executar diretamente:
   ```bash
   python src/app.py
   ```

## Como gerar o executável para Windows

1. Instale o Python (recomendado: 3.10+).
2. Instale as dependências:
   ```bash
   python -m pip install -r requirements.txt
   ```
3. Gere o executável:
   ```bash
   pyinstaller --onefile --windowed src/app.py
   ```
   O arquivo estará em `dist/app.exe`.

- Para adicionar ícone: `--icon=icone.ico`
- Para nomear o executável: `--name AutoCadence`

## Requisitos
- Python 3.13+ (Linux) ou 3.10+ (Windows)
- Tkinter (já incluído no Python oficial)
