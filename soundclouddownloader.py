import yt_dlp
import json
import os
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox

# Inicializar tkinter
root = tk.Tk()
root.withdraw()

# Pedir URL
playlist_url = simpledialog.askstring("URL de la playlist", "Introduce la URL de la playlist de SoundCloud:")

if not playlist_url:
    messagebox.showerror("Error", "No se ha introducido una URL.")
    exit()

# Selector de carpeta
download_dir = filedialog.askdirectory(title="Selecciona la carpeta de descarga")

metadata_list = []

ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

os.makedirs(download_dir, exist_ok=True)

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    playlist_info = ydl.extract_info(playlist_url, download=True)

    for entry in playlist_info['entries']:
        title = entry.get('title')
        artist = entry.get('uploader')
        duration = entry.get('duration')
        filename = os.path.join(download_dir, f"{title}.mp3")

        # Guardar metadata en lista
        metadata = {
            'title': title,
            'artist': artist,
            'duration': duration,
            'url': entry.get('webpage_url'),
            'thumbnail': entry.get('thumbnail'),
            'genre': entry.get('genre'),
            'upload_date': entry.get('upload_date'),
            'description': entry.get('description'),
        }
        metadata_list.append(metadata)

        # Escribir metadata en MP3
        try:
            audio = MP3(filename, ID3=EasyID3)
            audio['title'] = title
            audio['artist'] = artist
            if entry.get('genre'):
                audio['genre'] = entry.get('genre')
            audio.save()
        except Exception as e:
            print(f"❌ Error escribiendo metadata en {filename}: {e}")

# Guardar metadata general como JSON
with open(os.path.join(download_dir, 'metadata.json'), 'w', encoding='utf-8') as f:
    json.dump(metadata_list, f, ensure_ascii=False, indent=4)

print("\n✅ Archivos descargados con metadata embebida correctamente.")


#-------------------------------------------------
#PROGRAMADO POR EL FOCKING PUTO AMO DJ DAVIDBETTA
#-------------------------------------------------
