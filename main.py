import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import yt_dlp
import os
import re
import unicodedata

class VideoDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Descargador de Videos Platzi")
        self.root.geometry("800x500")
        
        # Variables
        self.url_var = tk.StringVar()
        self.output_path = tk.StringVar()
        self.video_name_var = tk.StringVar()
        
        # Ruta del archivo de cookies
        self.cookies_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "platzi.com_cookies.txt")
        
        self.create_widgets()
        
    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # URL input
        ttk.Label(main_frame, text="URL del video (.m3u8):").grid(row=0, column=0, sticky=tk.W, pady=5)
        url_entry = ttk.Entry(main_frame, textvariable=self.url_var, width=80)
        url_entry.grid(row=0, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Output path
        ttk.Label(main_frame, text="Carpeta de destino:").grid(row=1, column=0, sticky=tk.W, pady=5)
        output_entry = ttk.Entry(main_frame, textvariable=self.output_path, width=80)
        output_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)
        ttk.Button(main_frame, text="Buscar", command=self.browse_output).grid(row=1, column=2, padx=5)
        
        # Video name input
        ttk.Label(main_frame, text="Nombre del video (máx. 35 caracteres):").grid(row=2, column=0, sticky=tk.W, pady=5)
        name_entry = ttk.Entry(main_frame, textvariable=self.video_name_var, width=80)
        name_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # Download button
        ttk.Button(main_frame, text="Descargar Video", command=self.download_video).grid(row=3, column=1, pady=20)
        
        # Status
        self.status_label = ttk.Label(main_frame, text="")
        self.status_label.grid(row=4, column=0, columnspan=3, pady=5)
        
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
        ttk.Label(main_frame, text=instructions, wraplength=700).grid(row=5, column=0, columnspan=3, pady=10)
        
    def browse_output(self):
        directory = filedialog.askdirectory(title="Seleccionar carpeta de destino")
        if directory:
            self.output_path.set(directory)
            
    def get_next_sequence_number(self, directory):
        """Obtiene el siguiente número de secuencia basado en los archivos existentes"""
        try:
            # Lista todos los archivos .mp4 en el directorio
            existing_files = [f for f in os.listdir(directory) if f.endswith('.mp4')]
            
            # Extrae los números de secuencia de los nombres de archivo
            sequence_numbers = []
            for file in existing_files:
                match = re.match(r'^(\d+)\.', file)
                if match:
                    sequence_numbers.append(int(match.group(1)))
            
            # Retorna el siguiente número de secuencia
            next_number = max(sequence_numbers) + 1 if sequence_numbers else 1
            
            # Formatea el número con ceros adelante si es menor a 10
            return f"{next_number:02d}"
        except Exception:
            return "01"
            
    def sanitize_filename(self, filename):
        """Limpia el nombre del archivo de caracteres no permitidos"""
        # Normalizar caracteres Unicode (convertir tildes a letras base)
        normalized = unicodedata.normalize('NFKD', filename)
        ascii_text = normalized.encode('ascii', 'ignore').decode('ascii')  # Eliminar tildes
        
        # Eliminar caracteres no permitidos en Windows
        cleaned = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '_', ascii_text)
        
        # Reemplazar espacios con guiones bajos
        cleaned = re.sub(r'\s+', '_', cleaned)
        
        # Eliminar puntos y espacios al final
        cleaned = cleaned.strip('. ')
        
        # Limitar longitud máxima a 200 caracteres
        if len(cleaned) > 200:
            cleaned = cleaned[:200]
        
        return cleaned
            
    def download_video(self):
        url = self.url_var.get()
        output = self.output_path.get()
        video_name = self.video_name_var.get()
        
        if not all([url, output, video_name]):
            messagebox.showerror("Error", "Por favor complete todos los campos")
            return
            
        # Verificar longitud del nombre ingresado
        if len(video_name) > 200:
            messagebox.showerror("Error", "El nombre del video no puede exceder los 200 caracteres")
            return
            
        # Sanitiza el nombre del video
        sanitized_name = self.sanitize_filename(video_name)
        
        # Obtiene el siguiente número de secuencia
        sequence_number = self.get_next_sequence_number(output)
        
        # Construye el nombre final del archivo
        final_filename = f"{sequence_number}.{sanitized_name}.mp4"
        
        self.status_label.config(text="Iniciando descarga...")
        
        try:
            ydl_opts = {
                'cookies': self.cookies_path,
                'outtmpl': os.path.join(output, final_filename),
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
            messagebox.showinfo("Éxito", f"El video se ha descargado correctamente como: {final_filename}")
            
        except Exception as e:
            self.status_label.config(text="Error en la descarga")
            messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoDownloaderApp(root)
    root.mainloop() 