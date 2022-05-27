import sqlite3 as conector

try:
    conexao = conector.connect("banco_teste.db")
    cursor = conexao.cursor()
    
    comando = '''CREATE TABLE Pessoa(
        cpf INTEGER NOT NULL, nome TEXT NOT NULL,
        nascimento DATE NOT NULL, oculos BOOLEAN NOT NULL,
        PRIMARY KEY(cpf) 
    );'''
    
    cursor.execute(comando)
    
    conexao.commit()
    
except conector.DatabaseError as error:
      
    print('Erro de Banco de Dados', error)
      
    
finally:
    cursor.close()
      
    conexao.close()