# Descargador de Videos Platzi

Esta es una aplicación simple para descargar videos de Platzi usando yt-dlp.

## Requisitos

- Python 3.6 o superior
- yt-dlp
- tkinter (generalmente viene incluido con Python)

## Instalación

1. Clona este repositorio o descarga los archivos
2. Crea un entorno virtual:
```bash
python -m venv venv
```

3. Activa el entorno virtual:
   - En Windows:
   ```bash
   .\venv\Scripts\activate
   ```
   - En Linux/Mac:
   ```bash
   source venv/bin/activate
   ```

4. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## Configuración del Archivo de Cookies

1. Instala la extensión "Get cookies.txt LOCALLY" en tu navegador:
   - [Chrome Web Store](https://chrome.google.com/webstore/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc)
   - [Firefox Add-ons](https://addons.mozilla.org/en-US/firefox/addon/get-cookies-txt-locally/)

2. Inicia sesión en Platzi en tu navegador

3. Ve a la página del video que quieres descargar

4. Usa la extensión para exportar las cookies:
   - Haz clic en el ícono de la extensión
   - Selecciona "Exportar cookies"
   - Guarda el archivo como `platzi.com_cookies.txt` en la carpeta del proyecto

## Uso

1. Ejecuta la aplicación:
```bash
python main.py
```

2. En la interfaz:
   - Ingresa la URL del video de Platzi (ver instrucciones abajo)
   - Selecciona la carpeta donde quieres guardar el video
   - Haz clic en "Descargar Video"

## Obtención de la URL del Video

1. Abre el video en Platzi
2. Presiona F12 para abrir las herramientas de desarrollo
3. Ve a la pestaña 'Network'
4. Busca un archivo que termine en .m3u8
5. Copia la URL completa (debe incluir todos los parámetros)

## Notas Importantes

- Asegúrate de que el archivo `platzi.com_cookies.txt` esté en la misma carpeta que `main.py`
- Las cookies tienen una duración limitada, si la descarga falla, intenta exportar las cookies nuevamente
- Algunos videos pueden tener restricciones de DRM que impidan su descarga
- El archivo de cookies contiene información sensible, no lo compartas ni lo subas a repositorios públicos

## Solución de Problemas

Si encuentras errores:
1. Verifica que las cookies sean recientes (menos de 24 horas)
2. Asegúrate de estar logueado en Platzi
3. Intenta obtener una nueva URL del video
4. Verifica que el archivo de cookies esté en el formato correcto 