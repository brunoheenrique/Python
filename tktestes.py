import tkinter as tk

window = tk.TK();
btn = tk.Button(window,text="Botão Teste1", fg='blue');
btn.place(x=80,y=100);
lbl = tk.Label(window,text= "Primeiro Rótulo de teste", fg= 'red',font=('Calibri',18));
lbl.place(x=60,y=50);
txtfld = tk.Entry(window, text= "Primeiro TextBox de teste", bd= 5);
txtfld.place(x=80,y=150);
window.title("Bem vindo à Janela de Testes");
window.geomety("300x200+10+10");
window.mainloop();
