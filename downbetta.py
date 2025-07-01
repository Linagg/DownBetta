import sys
import ctypes
import yt_dlp
import json
import os
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox

# ---------- Interfaz ----------
root = tk.Tk()

# Icono barra de tareas (Windows)
if sys.platform == "win32":
    try:
        myappid = 'davidbetta.soundcloud.downloader.1.0'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        root.wm_iconbitmap('davidbetta.ico')  # ← clave para que lo coja bien
    except Exception as e:
        print("Error al aplicar el icono:", e)

# 🔽 ICONO PERSONALIZADO 🔽
icono = None
try:
    icono = tk.PhotoImage(file="davidbetta.ico")
    if icono:
        root.iconphoto(False, icono)
except Exception as e:
    print(f"No se pudo cargar el icono: {e}")

root.withdraw()

playlist_url = simpledialog.askstring("URL de la playlist", "Introduce la URL de la playlist de SoundCloud (Sígueme en SoundCloud: @david-betta):")
if playlist_url is None:
    # Cerró la ventana → salir en silencio
    root.destroy()
    sys.exit()
elif playlist_url.strip() == "":
    messagebox.showerror("Error", "No se ha introducido una URL.")
    root.destroy()
    sys.exit()

download_dir = filedialog.askdirectory(title="Selecciona la carpeta de descarga")
if not download_dir:
    messagebox.showerror("Error", "No se ha seleccionado una carpeta.")
    sys.exit()

def cerrar_ventana():
    try:
        progress_window.destroy()
    except:
        pass


# ---------- Ventana de descarga ----------
progress_window = tk.Toplevel()
progress_window.title("Descargando...")
if icono:
    progress_window.iconphoto(False, icono)  # Reutilizas el mismo icono
progress_label = tk.Label(progress_window, text="Iniciando descarga...", width=60)
progress_label.pack(padx=20, pady=20)
progress_window.update()
progress_window.protocol("WM_DELETE_WINDOW", cerrar_ventana)

# ---------- Descarga y procesamiento ----------
metadata_list = []


def hook(d):
    if d['status'] == 'downloading':
        progress_label.config(text=f"Descargando: {d.get('filename', '')}")
        progress_window.update()
    elif d['status'] == 'finished':
        progress_label.config(text=f"✅ Finalizado: {os.path.basename(d['filename'])}")
        progress_window.update()

ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),
    'progress_hooks': [hook],
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

        metadata = {
            'title': title,
            'artist': artist,
            'duration': duration,
            'url': entry.get('webpage_url'),
            'thumbnail': entry.get('thumbnail') or (entry.get('thumbnails')[0]['url'] if entry.get('thumbnails') else None),
            'genre': entry.get('genre'),
            'upload_date': entry.get('upload_date'),
            'description': entry.get('description'),
        }
        metadata_list.append(metadata)

        try:
            audio = MP3(filename, ID3=EasyID3)
            audio['title'] = title
            audio['artist'] = artist
            if entry.get('genre'):
                audio['genre'] = entry.get('genre')
            audio.save()
        except Exception as e:
            print(f"❌ Error escribiendo metadata en {filename}: {e}")

# ---------- Guardar metadata ----------
with open(os.path.join(download_dir, 'metadata.json'), 'w', encoding='utf-8') as f:
    json.dump(metadata_list, f, ensure_ascii=False, indent=4)

progress_window.destroy()
messagebox.showinfo("Finalizado", "Archivos descargados con metadata embebida correctamente.")
