import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import yt_dlp
import os

class VideoDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Descargador de Videos Platzi")
        self.root.geometry("800x400")  # Aumentamos el tamaño para la URL larga
        
        # Variables
        self.url_var = tk.StringVar()
        self.output_path = tk.StringVar()
        
        # Ruta del archivo de cookies
        self.cookies_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "platzi.com_cookies.txt")
        
        self.create_widgets()
        
    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # URL input
        ttk.Label(main_frame, text="URL del video (.m3u8):").grid(row=0, column=0, sticky=tk.W, pady=5)
        url_entry = ttk.Entry(main_frame, textvariable=self.url_var, width=80)  # Aumentamos el ancho
        url_entry.grid(row=0, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Output path
        ttk.Label(main_frame, text="Carpeta de destino:").grid(row=1, column=0, sticky=tk.W, pady=5)
        output_entry = ttk.Entry(main_frame, textvariable=self.output_path, width=80)
        output_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)
        ttk.Button(main_frame, text="Buscar", command=self.browse_output).grid(row=1, column=2, padx=5)
        
        # Download button
        ttk.Button(main_frame, text="Descargar Video", command=self.download_video).grid(row=2, column=1, pady=20)
        
        # Status
        self.status_label = ttk.Label(main_frame, text="")
        self.status_label.grid(row=3, column=0, columnspan=3, pady=5)
        
        # Instrucciones
        instructions = """
        Instrucciones para obtener la URL:
        1. Abre el video en Platzi
        2. Presiona F12 para abrir las herramientas de desarrollo
        3. Ve a la pestaña 'Network'
        4. Busca un archivo que termine en .m3u8
        5. Copia la URL completa (debe incluir todos los parámetros)
        6. Asegúrate de que el archivo platzi.com_cookies.txt esté en la misma carpeta
        """
        ttk.Label(main_frame, text=instructions, wraplength=700).grid(row=4, column=0, columnspan=3, pady=10)
        
    def browse_output(self):
        directory = filedialog.askdirectory(title="Seleccionar carpeta de destino")
        if directory:
            self.output_path.set(directory)
            
    def download_video(self):
        url = self.url_var.get()
        output = self.output_path.get()
        
        if not all([url, output]):
            messagebox.showerror("Error", "Por favor complete todos los campos")
            return
            
        self.status_label.config(text="Iniciando descarga...")
        
        try:
            ydl_opts = {
                'cookies': self.cookies_path,
                'outtmpl': os.path.join(output, '%(title)s.%(ext)s'),
                'format': 'best',
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    'Accept': '*/*',
                    'Accept-Language': 'en-US,en;q=0.9',
                    'Origin': 'https://platzi.com',
                    'Referer': 'https://platzi.com/',
                },
                'no_check_certificate': True,
                'verbose': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                
            self.status_label.config(text="¡Descarga completada!")
            messagebox.showinfo("Éxito", "El video se ha descargado correctamente")
            
        except Exception as e:
            self.status_label.config(text="Error en la descarga")
            messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoDownloaderApp(root)
    root.mainloop() 