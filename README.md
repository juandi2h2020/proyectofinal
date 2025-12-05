# Analizador de Audio (FastAPI + Librosa)

Proyecto desarrollado por **Juan Diego Hidrobo**.

Esta es una aplicación web sencilla hecha en **Python** usando **FastAPI**, que permite:

- Subir archivos de audio (por ejemplo `.mp3`, `.wav`).
- Analizar el audio en el servidor.
- Mostrar en la página:
  - El tempo estimado (BPM – beats por minuto).
  - La tonalidad estimada (key) de la canción.

El frontend usa **HTML + Bootstrap** (a través de una plantilla) y el backend usa **FastAPI + Librosa** para el análisis de audio.

---

## 👤 Autor

- **Nombre:** Juan Diego Hidrobo  
- **Tecnologías usadas:** Python, FastAPI, Librosa, Bootstrap, Jinja2  
- **Objetivo del proyecto:** Practicar desarrollo web con Python y análisis básico de audio.

---

## 🚀 Requisitos

Antes de ejecutar el proyecto necesitas:

- **Python 3.11 o 3.12**  
  > ⚠️ Versiones muy nuevas como 3.14 pueden causar problemas de compatibilidad con `librosa` y `numba`.
- **pip** (gestor de paquetes de Python).
- (Opcional pero recomendado) **Virtualenv / venv** para crear un entorno virtual.
- **Git** si quieres clonar el proyecto desde GitHub.

---

## 📂 Estructura del proyecto

La estructura básica del proyecto es:

```text
audio-analyzer/
├─ app.py
├─ requirements.txt
├─ templates/
│  └─ index.html
├─ uploads/
└─ venv/              # (opcional, no se sube a GitHub)
