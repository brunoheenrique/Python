import tkinter as tk

window = tk.Tk();
btn = tk.Button(window,text="Botão Teste1", fg='blue');
btn.place(x=80,y=100);
lbl = tk.Label(window,text= "Primeiro Rótulo de teste", fg= 'red',font=('Calibri',16));
lbl.place(x=60,y=0);
txtfld = tk.Entry(window, text= "Primeiro TextBox de teste", bd= 4);
txtfld.place(x=80,y=150);
mnu = tk.Menu(window,activebackground='blue',title="Menuzão");
mnubtn = tk.Menubutton(window,text="Botão Menu",fg='black');
mnubtn.place(x=80,y=200);
window.title("Bem vindo à Janela de Testes");
window.geometry("320x320+10+10");
window.mainloop();
