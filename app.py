from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

import librosa
import numpy as np
import os
import uuid

app = FastAPI()

# Carpeta donde se guardarán temporalmente los archivos de audio
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Carpeta de plantillas HTML
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """
    Página principal con el framework que te dieron y el formulario.
    """
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "result": None,
            "error": None,
        },
    )


@app.post("/analyze", response_class=HTMLResponse)
async def analyze_audio(request: Request, file: UploadFile = File(...)):
    """
    Recibe el archivo subido, lo guarda temporalmente,
    lo analiza y devuelve tempo y tonalidad.
    """
    if not file:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "result": None,
                "error": "No se recibió ningún archivo.",
            },
        )

    # Nombre temporal único
    file_ext = os.path.splitext(file.filename)[1]
    temp_filename = f"{uuid.uuid4().hex}{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, temp_filename)

    # Guardar archivo en disco
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    try:
        tempo, key = analyze_file(file_path)

        result = {
            "filename": file.filename,
            "tempo": round(float(tempo), 2),
            "key": key,
        }
        error = None
    except Exception as e:
        result = None
        error = f"Ocurrió un error analizando el audio: {str(e)}"
    finally:
        # Borrar archivo temporal
        if os.path.exists(file_path):
            os.remove(file_path)

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "result": result,
            "error": error,
        },
    )


def analyze_file(path: str):
    """
    Carga el audio, calcula el tempo (BPM) y estima la tonalidad.
    """
    # Cargar audio (mono, misma frecuencia de muestreo)
    y, sr = librosa.load(path, sr=None, mono=True)

    # Estimar tempo (BPM)
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)

    # Estimar tonalidad
    key = estimate_key(y, sr)

    return tempo, key


def estimate_key(y, sr):
    """
    Estima la tonalidad usando análisis de cromas
    y perfiles de Krumhansl-Schmuckler.
    """
    chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
    chroma_mean = chroma.mean(axis=1)

    major_profile = np.array(
        [6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88]
    )
    minor_profile = np.array(
        [6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17]
    )

    pitch_classes = ["C", "C#", "D", "D#", "E", "F",
                     "F#", "G", "G#", "A", "A#", "B"]

    best_index = 0
    best_mode = "major"
    best_value = -np.inf

    for i in range(12):
        major_score = np.corrcoef(chroma_mean, np.roll(major_profile, i))[0, 1]
        minor_score = np.corrcoef(chroma_mean, np.roll(minor_profile, i))[0, 1]

        if major_score > best_value:
            best_value = major_score
            best_index = i
            best_mode = "major"

        if minor_score > best_value:
            best_value = minor_score
            best_index = i
            best_mode = "minor"

    mode_name = "Mayor" if best_mode == "major" else "Menor"
    return f"{pitch_classes[best_index]} {mode_name}"
