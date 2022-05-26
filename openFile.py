arquivo  = open("teste.txt", "r");

for linha in arquivo:
    print(repr(linha));
    
arquivo.seek(0);
conteudo = arquivo.read();

print(repr(conteudo));

arquivo.close()

