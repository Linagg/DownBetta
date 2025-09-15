import sys
import ctypes
import yt_dlp
import json
import os
import requests
import io
try:
    from PIL import Image
except Exception:
    Image = None
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC, TIT2, TPE1, TCON, COMM
from mutagen.id3 import ID3NoHeaderError
from mutagen.mp3 import MP3
from mutagen.flac import FLAC, Picture
from mutagen.wave import WAVE
from mutagen.aiff import AIFF
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from tkinter import ttk

# ---------- Interfaz ----------
root = tk.Tk()
root.title('DOWNBETTA')
# Oculta completamente la ventana raíz para que no aparezca
try:
    root.withdraw()
except Exception:
    pass

 

# ---------- EstÃ©tica Y2K (Keygen vibes) ----------
style = ttk.Style()
try:
    style.theme_use('clam')
except Exception:
    pass

BG = '#0b0f10'
FG = '#39ff14'  # neon green
FG2 = '#00e5ff' # neon cyan
ACCENT = '#ff00ff'  # magenta
ACCENT2 = '#faff00' # yellow

style.configure('Y2K.TFrame', background=BG, borderwidth=2, relief='ridge')
style.configure('Y2K.TLabel', background=BG, foreground=FG, font=('Consolas', 10))
style.configure('Y2K.Header.TLabel', background=BG, foreground=ACCENT2, font=('Consolas', 16, 'bold'))
style.configure('Y2K.TButton', foreground=FG, background='#101418')
style.map('Y2K.TButton', background=[('active', '#182028')], foreground=[('active', FG2)])
style.configure('Y2K.TEntry', fieldbackground='#111417', foreground=FG, insertcolor=FG)
style.configure('Y2K.TCombobox', fieldbackground='#000000', background='#000000', foreground='#ffffff')
style.map('Y2K.TCombobox', fieldbackground=[('active', '#000000')], foreground=[('active', '#ffffff')])
try:
    # Mejora contraste en la lista desplegable del Combobox
    root.option_add('*TCombobox*Listbox*foreground', '#ffffff')
    root.option_add('*TCombobox*Listbox*background', '#000000')
    root.option_add('*TCombobox*Listbox*selectForeground', '#000000')
    root.option_add('*TCombobox*Listbox*selectBackground', ACCENT2)
except Exception:
    pass
style.configure('Y2K.Horizontal.TProgressbar', background=FG, troughcolor='#111417')

def mostrar_ui_y2k(parent):
    win = tk.Toplevel(parent)
    win.title('DOWNBETTA')
    try:
        if icono:
            win.iconphoto(False, icono)
    except Exception:
        pass
    win.configure(bg=BG)
    win.resizable(False, False)
    win.grab_set()

    outer = ttk.Frame(win, style='Y2K.TFrame', padding=12)
    outer.grid(row=0, column=0, sticky='nsew')

    header = ttk.Label(outer, text=':: DOWNBETTA ::', style='Y2K.Header.TLabel')
    header.grid(row=0, column=0, columnspan=3, sticky='w')

    sub = ttk.Label(outer, text='SOUNDCLOUD PLAYLIST Ripper', style='Y2K.TLabel')
    sub.grid(row=1, column=0, columnspan=3, pady=(0,10), sticky='w')

    ttk.Label(outer, text='URL Playlist', style='Y2K.TLabel').grid(row=2, column=0, padx=(0,8), pady=6, sticky='w')
    url_var = tk.StringVar()
    url_entry = ttk.Entry(outer, textvariable=url_var, width=48, style='Y2K.TEntry')
    url_entry.grid(row=2, column=1, columnspan=2, pady=6, sticky='w')

    ttk.Label(outer, text='Carpeta destino', style='Y2K.TLabel').grid(row=3, column=0, padx=(0,8), pady=6, sticky='w')
    dir_var = tk.StringVar()
    dir_entry = ttk.Entry(outer, textvariable=dir_var, width=38, style='Y2K.TEntry')
    dir_entry.grid(row=3, column=1, pady=6, sticky='w')
    def elegir_dir():
        d = filedialog.askdirectory(title='Selecciona la carpeta de descarga')
        if d:
            dir_var.set(d)
    ttk.Button(outer, text='Elegir...', command=elegir_dir, style='Y2K.TButton').grid(row=3, column=2, padx=(8,0), pady=6, sticky='w')

    ttk.Label(outer, text='Formato', style='Y2K.TLabel').grid(row=4, column=0, padx=(0,8), pady=6, sticky='w')
    formato_var = tk.StringVar(value='mp3')
    formatos = ['mp3', 'flac', 'wav', 'aiff']
    formato_cb = ttk.Combobox(outer, textvariable=formato_var, values=formatos, state='readonly', width=10, style='Y2K.TCombobox')
    formato_cb.grid(row=4, column=1, pady=6, sticky='w')

    ttk.Label(outer, text='Bitrate (MP3)', style='Y2K.TLabel').grid(row=5, column=0, padx=(0,8), pady=6, sticky='w')
    calidad_var = tk.StringVar(value='320')
    calidades = ['320', '256', '192', '160', '128']
    calidad_cb = ttk.Combobox(outer, textvariable=calidad_var, values=calidades, state='readonly', width=10, style='Y2K.TCombobox')
    calidad_cb.grid(row=5, column=1, pady=6, sticky='w')

    def on_formato_change(event=None):
        if formato_var.get().lower() == 'mp3':
            calidad_cb.configure(state='readonly')
        else:
            calidad_cb.configure(state='disabled')
    formato_cb.bind('<<ComboboxSelected>>', on_formato_change)
    on_formato_change()

    resultado = {'ok': False, 'url': None, 'dir': None, 'codec': None, 'quality': None}

    botones = ttk.Frame(outer, style='Y2K.TFrame')
    botones.grid(row=6, column=0, columnspan=3, pady=(12,0), sticky='e')

    def cancelar():
        resultado['ok'] = False
        win.destroy()

    def aceptar():
        u = url_var.get().strip()
        d = dir_var.get().strip()
        if not u:
            messagebox.showerror('Error', 'Introduce la URL de la playlist')
            return
        if not d:
            messagebox.showerror('Error', 'Selecciona la carpeta de descarga')
            return
        resultado['ok'] = True
        resultado['url'] = u
        resultado['dir'] = d
        resultado['codec'] = formato_var.get().lower()
        resultado['quality'] = calidad_var.get() if resultado['codec'] == 'mp3' else None
        win.destroy()

    ttk.Button(botones, text='Cancelar', command=cancelar, style='Y2K.TButton').grid(row=0, column=0, padx=(0,8))
    ttk.Button(botones, text='DESCARGAR', command=aceptar, style='Y2K.TButton').grid(row=0, column=1)

    url_entry.focus_set()
    parent.wait_window(win)
    if resultado['ok']:
        return resultado['url'], resultado['dir'], resultado['codec'], resultado['quality']
    return None, None, None, None

# Obtener datos desde la UI Y2K y forzar diÃ¡logos a devolverlos
playlist_url, download_dir, selected_codec, selected_quality = mostrar_ui_y2k(root)
if not playlist_url or not download_dir or not selected_codec:
    root.destroy(); sys.exit()

selected_codec = selected_codec.lower()
# Icono barra de tareas (Windows)
if sys.platform == "win32":
    try:
        myappid = 'davidbetta.soundcloud.downloader.1.0'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        root.wm_iconbitmap('davidbetta.ico')  # â† clave para que lo coja bien
    except Exception as e:
        print("Error al aplicar el icono:", e)

# ðŸ”½ ICONO PERSONALIZADO ðŸ”½
icono = None
try:
    icono = tk.PhotoImage(file="davidbetta.ico")
    if icono:
        root.iconphoto(False, icono)
except Exception as e:
    print(f"No se pudo cargar el icono: {e}")

# Asegura que la raíz permanezca oculta
try:
    root.withdraw()
except Exception:
    pass

# Inputs ya capturados por la UI Y2K
if not selected_codec:
    sys.exit()

def cerrar_ventana():
    try:
        progress_window.destroy()
    except:
        pass


# ---------- Ventana de descarga ----------
progress_window = tk.Toplevel()
progress_window.title("Descargando...")
try:
    if icono:
        progress_window.iconphoto(False, icono)
except Exception:
    pass
progress_window.configure(bg=BG)
progress_label = tk.Label(progress_window, text="Iniciando descarga...", width=60, bg=BG, fg=FG, font=("Consolas", 10))
progress_label.pack(padx=20, pady=(20,10))
try:
    pb = ttk.Progressbar(progress_window, mode='indeterminate', length=360, style='Y2K.Horizontal.TProgressbar')
    pb.pack(padx=20, pady=(0,16))
    pb.start(12)
except Exception:
    pass
progress_window.update()
progress_window.protocol("WM_DELETE_WINDOW", cerrar_ventana)

# ---------- Descarga y procesamiento ----------
metadata_list = []


def hook(d):
    if d['status'] == 'downloading':
        progress_label.config(text=f"Descargando: {d.get('filename', '')}")
        progress_window.update()
    elif d['status'] == 'finished':
        progress_label.config(text=f"âœ… Finalizado: {os.path.basename(d['filename'])}")
        progress_window.update()

postprocessors = [{
    'key': 'FFmpegExtractAudio',
    'preferredcodec': selected_codec,
}]
if selected_codec == 'mp3' and selected_quality:
    postprocessors[0]['preferredquality'] = selected_quality

# Nota: para formatos sin pÃ©rdida (flac/wav/aiff) el bitrate no aplica.

ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),
    'progress_hooks': [hook],
    'postprocessors': postprocessors,
}

os.makedirs(download_dir, exist_ok=True)

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    playlist_info = ydl.extract_info(playlist_url, download=True)
    album_title = None
    try:
        if isinstance(playlist_info, dict):
            album_title = playlist_info.get('title')
    except Exception:
        album_title = None

    for entry in playlist_info['entries']:
        title = entry.get('title')
        artist = entry.get('uploader')
        duration = entry.get('duration')
        # Construye filename con extensiÃ³n segÃºn codec elegido
        ext = 'mp3' if selected_codec == 'mp3' else selected_codec
        filename = os.path.join(download_dir, f"{title}.{ext}")

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
        # Build and embed tags + cover for all formats
        # Common fields
        title = entry.get('title')
        artist = entry.get('uploader')
        genre = entry.get('genre')
        upload_date = entry.get('upload_date')
        year = upload_date[:4] if isinstance(upload_date, str) and len(upload_date) >= 4 else None
        thumb_url = entry.get('thumbnail') or (entry.get('thumbnails')[0]['url'] if entry.get('thumbnails') else None)

        try:
            if selected_codec == 'mp3':
                audio = MP3(filename, ID3=EasyID3)
                if title: audio['title'] = title
                if artist: audio['artist'] = artist
                if album_title: audio['album'] = album_title
                if genre: audio['genre'] = genre
                if year:
                    try: audio['date'] = year
                    except Exception: pass
                audio.save(v2_version=3)

                # Cover: normalize to JPEG if Pillow available
                if thumb_url:
                    resp = requests.get(thumb_url, timeout=20)
                    img_bytes = resp.content
                    mime = 'image/jpeg'
                    try:
                        if Image is not None:
                            im = Image.open(io.BytesIO(img_bytes))
                            rgb = im.convert('RGB')
                            buf = io.BytesIO()
                            rgb.save(buf, format='JPEG', quality=90)
                            img_bytes = buf.getvalue()
                            mime = 'image/jpeg'
                        else:
                            ctype = resp.headers.get('Content-Type','')
                            if 'png' in ctype or (thumb_url and thumb_url.lower().endswith('.png')):
                                mime = 'image/png'
                    except Exception:
                        ctype = resp.headers.get('Content-Type','')
                        if 'png' in ctype or (thumb_url and thumb_url.lower().endswith('.png')):
                            mime = 'image/png'
                    try:
                        try:
                            tags = ID3(filename)
                        except ID3NoHeaderError:
                            tags = ID3(); tags.save(filename); tags = ID3(filename)
                        for k in list(tags.keys()):
                            if str(k).startswith('APIC'):
                                del tags[k]
                        tags.add(APIC(encoding=3, mime=mime, type=3, desc='Cover', data=img_bytes))
                        tags.save(v2_version=3)
                    except Exception as e:
                        print(f"Error añadiendo portada a {filename}: {e}")

            elif selected_codec == 'flac':
                audio_f = FLAC(filename)
                if title: audio_f['title'] = [title]
                if artist: audio_f['artist'] = [artist]
                if album_title: audio_f['album'] = [album_title]
                if genre: audio_f['genre'] = [genre]
                if year: audio_f['date'] = [year]
                if thumb_url:
                    try:
                        r = requests.get(thumb_url, timeout=20)
                        pic = Picture(); pic.type = 3
                        ctype = r.headers.get('Content-Type','')
                        pic.mime = 'image/jpeg'
                        if 'png' in ctype or (thumb_url and thumb_url.lower().endswith('.png')):
                            pic.mime = 'image/png'
                        pic.desc = 'Cover'; pic.data = r.content
                        audio_f.add_picture(pic)
                    except Exception:
                        pass
                audio_f.save()

            elif selected_codec == 'wav':
                audio_w = WAVE(filename)
                if audio_w.tags is None: audio_w.add_tags()
                tags = audio_w.tags
                if title: tags.add(TIT2(encoding=3, text=title))
                if artist: tags.add(TPE1(encoding=3, text=artist))
                if genre: tags.add(TCON(encoding=3, text=genre))
                if thumb_url:
                    try:
                        r = requests.get(thumb_url, timeout=20)
                        ctype = r.headers.get('Content-Type','')
                        mime = 'image/jpeg'
                        if 'png' in ctype or (thumb_url and thumb_url.lower().endswith('.png')):
                            mime = 'image/png'
                        tags.add(APIC(encoding=3, mime=mime, type=3, desc='Cover', data=r.content))
                    except Exception:
                        pass
                try: tags.save(filename, v2_version=3)
                except Exception: tags.save(filename)

            elif selected_codec == 'aiff':
                audio_a = AIFF(filename)
                if audio_a.tags is None: audio_a.add_tags()
                tags = audio_a.tags
                if title: tags.add(TIT2(encoding=3, text=title))
                if artist: tags.add(TPE1(encoding=3, text=artist))
                if genre: tags.add(TCON(encoding=3, text=genre))
                if thumb_url:
                    try:
                        r = requests.get(thumb_url, timeout=20)
                        ctype = r.headers.get('Content-Type','')
                        mime = 'image/jpeg'
                        if 'png' in ctype or (thumb_url and thumb_url.lower().endswith('.png')):
                            mime = 'image/png'
                        tags.add(APIC(encoding=3, mime=mime, type=3, desc='Cover', data=r.content))
                    except Exception:
                        pass
                try: tags.save(filename, v2_version=3)
                except Exception: tags.save(filename)

        except Exception as e:
            print(f"Error escribiendo metadata/portada en {filename}: {e}")

# ---------- Guardar metadata ----------
with open(os.path.join(download_dir, 'metadata.json'), 'w', encoding='utf-8') as f:
    json.dump(metadata_list, f, ensure_ascii=False, indent=4)

progress_window.destroy()
messagebox.showinfo("Finalizado", "Archivos descargados con metadata embebida correctamente.")
try:
    root.destroy()
except Exception:
    pass





