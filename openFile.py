arquivo  = open("teste.txt", "r");

for linha in arquivo:
    print(repr(linha));

arquivo.close()

