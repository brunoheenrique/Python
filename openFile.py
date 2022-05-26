arquivo  = open("teste.txt", "r");

conteudo = arquivo.readline();
conteudo2 = arquivo.readline();
conteudo3 = arquivo.readline();

print(repr(conteudo));
print(repr(conteudo2));
print(repr(conteudo3));

arquivo.close()

