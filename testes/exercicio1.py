with open('exercicio1.txt',"r") as arquivo:
    conteudo = arquivo.read().split(",");
    
with open('resultado1.txt',"w") as resultado:
    for item in conteudo:
        texto = f"Novo conteudo {item.strip()}\n";
        resultado.write(texto);
