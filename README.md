# DOWNBETTA

Peque�a herramienta con interfaz gr�fica para descargar playlists de SoundCloud y convertirlas a audio listo para pinchar, con metadatos y portada incrustados.

- Compatible con Windows (EXE). Compilable en macOS y Linux.
- Sin publicidad. Sin trackers.

---

## Caracter�sticas

- Descarga playlists completas (yt-dlp).
- Conversi�n a: MP3, FLAC, WAV, AIFF.
- MP3 con selector de bitrate: 320, 256, 192, 160, 128.
- Metadatos: t�tulo, artista, g�nero, �lbum (t�tulo de la playlist), a�o (si disponible).
- Portada incrustada en todos los formatos (MP3/FLAC/WAV/AIFF).
- Exporta `metadata.json` con la informaci�n de todas las pistas.
- Fondo personalizable con imagen.

---

## Requisitos

- Python 3.9+ (solo si ejecutas desde c�digo).
- FFmpeg instalado en PATH (necesario para la conversi�n de audio).
- Dependencias Python: ver `requirements.txt`.

Instalaci�n de dependencias (entorno de desarrollo):

```bash
python -m venv .venv
. .venv/Scripts/activate   # Windows
# o: source .venv/bin/activate  # macOS/Linux
pip install -r dump/ScloudDownloaderExe/requirements.txt
```

---

## Uso (desde c�digo)

```bash
cd dump/ScloudDownloaderExe
python downbetta.py
```

1) Pega la URL de la playlist.
2) Elige la carpeta de destino.
3) Selecciona formato; si es MP3, elige bitrate.
4) Descarga y conversi�n autom�ticas; se incrustan metadatos y portada.

Salida:

- Archivos de audio en la carpeta elegida.
- `metadata.json` con la lista de pistas y campos b�sicos.

---

## Ejecutable (Windows)

Hay un `.spec` listo para compilar con PyInstaller (generaci�n �onedir�, arranque r�pido):

```powershell
cd dump\ScloudDownloaderExe
pyinstaller --noconfirm --clean --distpath .\out --workpath .\.build .\downbetta.spec
# Ejecuta: out\downbetta_1.1\downbetta_1.1.exe
```

Notas:
- Si quieres un �nico archivo (`onefile`), modifica el .spec o usa los flags correspondientes (arranque m�s lento).
- FFmpeg debe estar en PATH. Tambi�n puedes incluirlo como binario adicional y ajustar `PATH` en el arranque.

### Compilar en macOS / Linux

PyInstaller no hace cross-compile: compila en cada sistema.

- macOS (ejemplo onedir):
  ```bash
  pip install -U pyinstaller yt-dlp mutagen requests pillow
  pyinstaller --noconfirm --clean --windowed --onedir \
    --name downbetta_1.1 --icon davidbetta.icns \
    --add-data "davidbetta.png:." downbetta.py
  ```
- Linux (ejemplo onedir):
  ```bash
  pip install -U pyinstaller yt-dlp mutagen requests pillow
  pyinstaller --noconfirm --clean --windowed --onedir \
    --name downbetta_1.1 --icon davidbetta.png \
    --add-data "davidbetta.png:." downbetta.py
  ```

Separador de `--add-data`: macOS/Linux usa `:` y Windows `;`.

---

## Fondo personalizable

- La aplicaci�n intentar� usar, por este orden:
  1) Variable de entorno `DOWNBETTA_BG` (ruta a una imagen)
  2) La ruta absoluta indicada en el c�digo (`USER_BG_PATH`)
  3) Un archivo `Flag_of_Palestine.jpg` o `background.(jpg|jpeg|png)` junto al `.py` o `.exe`

---

## Problemas comunes

- �No aparece la portada en Windows Explorer�: pulsa F5, o abre el archivo en tu software DJ (Explorer tarda en refrescar).
- �FFmpeg no encontrado�: inst�lalo y a�ade su carpeta a `PATH`.
- �El EXE tarda en arrancar�: usa build `onedir` (m�s r�pido que `onefile`) y desactiva UPX en el `.spec`.

---

## Tecnolog�as

- yt-dlp, Mutagen, FFmpeg, Tkinter.

---

## Licencia

MIT. Agradecimientos bienvenidos.
