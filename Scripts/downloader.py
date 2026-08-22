# Importa a classe Path da biblioteca pathlib.
# Ela será usada para trabalhar com caminhos de arquivos e pastas.
from pathlib import Path
import yt_dlp

# Cria a função responsável por realizar o download.
# url representa o endereço do vídeo.
# formato representa o tipo do arquivo: mp3 ou mp4.
# pasta_destino representa o local onde o arquivo será salvo.
def baixar(url, formato, pasta_destino):

    # Mostra a URL recebida pela função.
    print(f"URL: {url}")

    # Mostra o formato escolhido pelo usuário.
    print(f"Formato: {formato}")

    # Mostra a pasta escolhida para salvar o arquivo.
    print(f"Pasta: {pasta_destino}")

    opcoes = {
        # Salva o arquivo dentro da pasta escolhida.
        # %(title)s usa o titulo do video como nome.
        # %(ext) s usa a extensao do arquivo
        #outtmpl= out template = modelo de saída
        "outtmpl": str(Path(pasta_destino) / "%(title)s.%(ext)s"),
        "noplaylist": True,
    }
    if formato == "mp3":
        #Escolhe o melhor audio disponivel.
        opcoes["format"] = "bestaudio/best"
    else:
        #Escolho o melhor video disponivel.
        opcoes ["format"] = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best"

    #Cria um baixador usando as opçoes definidas acima
    with yt_dlp.YoutubeDL(opcoes) as baixador:
        #Inicia o Download usando a URL recebida.
        baixador.download([url])
    

    return "Donwload concluido com sucesso."
    
