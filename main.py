import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk


class DownloaderApp:
	def __init__(self, root):
		self.root = root
		self.root.title("MP43 - Baixador de mídia")
		self.root.geometry("620x330")
		self.root.minsize(560, 300)

		self.url = tk.StringVar()
		self.format = tk.StringVar(value="mp4")
		self.output_dir = tk.StringVar(value=str(Path.home() / "Downloads"))
		self.status = tk.StringVar(value="Pronto para baixar")
		self.progress = tk.DoubleVar(value=0)
		self.download_button = None

		self._build_interface()

	def _build_interface(self):
		container = ttk.Frame(self.root, padding=20)
		container.pack(fill="both", expand=True)
		container.columnconfigure(1, weight=1)

		ttk.Label(container, text="MP43", font=("TkDefaultFont", 18, "bold")).grid(
			row=0, column=0, columnspan=3, sticky="w", pady=(0, 18)
		)

		ttk.Label(container, text="URL do vídeo:").grid(row=1, column=0, sticky="w", pady=6)
		url_entry = ttk.Entry(container, textvariable=self.url)
		url_entry.grid(row=1, column=1, columnspan=2, sticky="ew", padx=(12, 0), pady=6)
		url_entry.focus_set()

		ttk.Label(container, text="Formato:").grid(row=2, column=0, sticky="w", pady=6)
		format_box = ttk.Combobox(
			container,
			textvariable=self.format,
			values=("mp4", "mp3"),
			state="readonly",
			width=12,
		)
		format_box.grid(row=2, column=1, sticky="w", padx=(12, 0), pady=6)

		ttk.Label(container, text="Pasta de destino:").grid(row=3, column=0, sticky="w", pady=6)
		ttk.Entry(container, textvariable=self.output_dir).grid(
			row=3, column=1, sticky="ew", padx=(12, 8), pady=6
		)
		ttk.Button(container, text="Escolher", command=self._choose_directory).grid(
			row=3, column=2, sticky="e", pady=6
		)

		self.download_button = ttk.Button(
			container, text="Baixar", command=self.start_download
		)
		self.download_button.grid(row=4, column=0, columnspan=3, sticky="ew", pady=(20, 10))

		ttk.Progressbar(container, variable=self.progress, maximum=100).grid(
			row=5, column=0, columnspan=3, sticky="ew", pady=(4, 8)
		)
		ttk.Label(container, textvariable=self.status, wraplength=580).grid(
			row=6, column=0, columnspan=3, sticky="w"
		)

	def _choose_directory(self):
		selected = filedialog.askdirectory(initialdir=self.output_dir.get())
		if selected:
			self.output_dir.set(selected)

	def start_download(self):
		url = self.url.get().strip()
		output_dir = Path(self.output_dir.get()).expanduser()

		if not url:
			messagebox.showwarning("URL ausente", "Informe a URL do vídeo.")
			return

		self.download_button.configure(state="disabled")
		self.progress.set(0)
		self.status.set("Preparando o download...")
		threading.Thread(
			target=self._download,
			args=(url, output_dir, self.format.get()),
			daemon=True,
		).start()

	def _download(self, url, output_dir, media_format):
		try:
			import yt_dlp

			output_dir.mkdir(parents=True, exist_ok=True)
			options = {
				"outtmpl": str(output_dir / "%(title)s.%(ext)s"),
				"noplaylist": True,
				"progress_hooks": [self._progress_hook],
			}
			if media_format == "mp3":
				options.update(
					{
						"format": "bestaudio/best",
						"postprocessors": [
							{
								"key": "FFmpegExtractAudio",
								"preferredcodec": "mp3",
								"preferredquality": "192",
							}
						],
					}
				)
			else:
				options["format"] = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
				options["merge_output_format"] = "mp4"

			with yt_dlp.YoutubeDL(options) as downloader:
				downloader.download([url])
		except ImportError:
			self._finish_download(
				error="A biblioteca yt-dlp não está instalada. Execute: pip install -r requirements.txt"
			)
		except Exception as error:
			self._finish_download(error=f"Não foi possível concluir: {error}")
		else:
			self._finish_download(success=True)

	def _progress_hook(self, data):
		if data.get("status") == "downloading":
			downloaded = data.get("downloaded_bytes", 0)
			total = data.get("total_bytes") or data.get("total_bytes_estimate")
			percentage = (downloaded / total * 100) if total else 0
			self.root.after(0, self.progress.set, percentage)
			self.root.after(0, self.status.set, f"Baixando... {percentage:.1f}%")
		elif data.get("status") == "finished":
			self.root.after(0, self.progress.set, 100)
			self.root.after(0, self.status.set, "Processando o arquivo...")

	def _finish_download(self, success=False, error=None):
		def update_interface():
			self.download_button.configure(state="normal")
			if error:
				self.status.set(error)
				messagebox.showerror("Erro no download", error)
			elif success:
				self.progress.set(100)
				self.status.set("Download concluído com sucesso.")
				messagebox.showinfo("Concluído", "O arquivo foi salvo na pasta escolhida.")

		self.root.after(0, update_interface)


if __name__ == "__main__":
	root = tk.Tk()
	DownloaderApp(root)
	root.mainloop()
