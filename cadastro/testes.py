import os

try:
    os.rmdir("diretorio")
except Exception as erro:
    print("Erro geral")
except OSError as error:
    print("Erro de sistema")
except FileNotFoundError as error:
    print("Diretório não encontrado")
    