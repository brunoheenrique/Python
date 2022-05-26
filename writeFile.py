arquivo = open("teste.txt","a");

linhas = ["Novo teste inserindo algumas linhas no arquivo.","\nUma segunda linha representativa."]

arquivo.writelines(linhas);

arquivo.close();
