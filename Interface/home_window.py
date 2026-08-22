#O import é essêncial para que a gente desenha a imagem na tela
import tkinter as tk

#Root tk.Tk abre a janela
root = tk.Tk()
#Define o título da mesma
appname = root.title("MP43")
#Define o tamanho máximo e o mínimo da janela
WindowSize = root.geometry("1280x720"); root.minsize(640, 360)
Saudation_text = tk.Label(root, text="Seja bem vindo ao MP43"); Saudation_text.pack()
BotãoExemplo = tk.Button(root, text="Clique"); BotãoExemplo.pack()
entrada = tk.Entry(root)
#Faz com que a janela fique aberta
root.mainloop()
