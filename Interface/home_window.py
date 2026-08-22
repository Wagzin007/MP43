#O import é essêncial para que a gente desenha a imagem na tela
import tkinter as tk

#Root tk.Tk abre a janela
root = tk.Tk()
#Define o título da mesma
root.title("MP43")
#Define o tamanho máximo e o mínimo da janela
root.geometry("1280x720")
root.minsize(640, 360)
label = tk.Label(root, text="Seja bem vindo ao MP43")
botao = tk.Button(root, text="Clique")
entrada = tk.Entry(root)
#E este faz a janela ficar aberta até ser fechada manualmente
root.mainloop()
