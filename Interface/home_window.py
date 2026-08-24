#O import é essêncial para que a gente desenha a imagem na tela
import tkinter as tk

#functions lib que serão exênciais durante a execução do código
#Root tk.Tk abre a janela
root = tk.Tk()
def Clicar():
    clicker = tk.Label(root, text="Botão Clicado")
    clicker.pack()
#Define o título da mesma
appname = root.title("MP43")
#Define o tamanho máximo e o mínimo da janela
WindowSize = root.geometry("1280x720"); root.minsize(640, 360)
Saudation_text = tk.Label(root, text="Seja bem vindo ao MP43"); Saudation_text.pack()
BotãoExemplo = tk.Button(root, text="Clique", command = Clicar); BotãoExemplo.pack()
entrada = tk.Entry(root); entrada.pack()
#Faz com que a janela fique aberta
root.mainloop()
