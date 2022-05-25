from tkinter import *

def donothing():
   filewin = Toplevel(root);
   button = Button(filewin, text="Do nothing button");
   button.pack();
   
root = Tk();
menubar = Menu(root);

filemenu = Menu(menubar, tearoff=0);
menubar.add_cascade(label="File", menu=filemenu);

filemenu.add_command(label="New", command=donothing);
filemenu.add_command(label="Open", command=donothing);
filemenu.add_command(label="Save", command=donothing);
filemenu.add_command(label="Save as...", command=donothing);
filemenu.add_command(label="Close", command=donothing);
filemenu.add_separator();
filemenu.add_command(label="Exit", command=root.quit);

editmenu = Menu(menubar, tearoff=0);
menubar.add_cascade(label="Edit", menu=editmenu);

editmenu.add_command(label="Undo", command=donothing);
editmenu.add_separator();
editmenu.add_command(label="Cut", command=donothing);
editmenu.add_command(label="Copy", command=donothing);
editmenu.add_command(label="Paste", command=donothing);
editmenu.add_command(label="Delete", command=donothing);
editmenu.add_command(label="Select All", command=donothing);

helpmenu = Menu(menubar, tearoff=0);
menubar.add_cascade(label="Help", menu=helpmenu);

helpmenu.add_command(label="Help Index", command=donothing);
helpmenu.add_command(label="About...", command=donothing);

titulo = Label(root,text="Testes Form de Python",fg='red',font=('Arial',18));
titulo.place(x=60,y=0);

botao= Button(root,text="Inserir",fg="red",bd=5,width= 7, height= 1);
botao.place(x=12,y=180);

root.title("Bem Vindo Menu TkInter")
root.geometry("300x220+10+10");
root.config(menu=menubar);
root.mainloop();