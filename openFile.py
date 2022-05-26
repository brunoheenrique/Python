arquivo  = open("teste.txt");

arquivo2 = open("C:/Dev/WebDesign/Webdesign/teste2.txt")

conteudo = arquivo.readline();
conteudo2 = arquivo.readline();
conteudo3 = arquivo.readline();

print(repr(conteudo));
print(repr(conteudo2));
print(repr(conteudo3));

arquivo.close()

arquivo2.close()
