import sqlite3 as conector
class conectDB :

    def conexDB():
        try:
            conexao = conector.connect("banco_teste.db")
            cursor = conexao.cursor()
            
        # comando1 = ''' DROP TABLE Veiculo;'''
        
        # cursor.execute(comando1)
            
        #  comando2 = '''CREATE TABLE Veiculo(
        #        placa CHARACTER(7) NOT NULL,
        #        ano INTEGER NOT NULL, cor TEXT NOT NULL,
        #       motor REAL NOT NULL,
        #       proprietario INTEGER NOT NULL,
        #      marca INTEGER NOT NULL,
        #     PRIMARY KEY(placa),
            #    FOREIGN KEY(proprietario) REFERENCES Pessoa(cpf),
            #   FOREIGN KEY(marca) REFERENCES Marca(id)
        #  );'''
            
        #  cursor.execute(comando2)
            
        # conexao.commit()
            
        except conector.DatabaseError as error:
            
            print('Erro de Banco de Dados', error)
        
        finally:
            cursor.close() 
            conexao.close()