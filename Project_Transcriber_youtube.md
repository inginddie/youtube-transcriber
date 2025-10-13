# 🎥 YouTube Transcriber Pro - Master Plan

## 📋 Tabla de Contenidos
1. [Visión del Proyecto](#visión-del-proyecto)
2. [Arquitectura Técnica](#arquitectura-técnica)
3. [Estructura de Archivos](#estructura-de-archivos)
4. [Stack Tecnológico](#stack-tecnológico)
5. [Configuración Inicial](#configuración-inicial)
6. [Fase 1: MVP - Transcriptor](#fase-1-mvp---transcriptor)
7. [Fase 2: RAG + Chat](#fase-2-rag--chat)
8. [Uso CLI (Alternativo)](#uso-cli-alternativo)
9. [Deployment](#deployment)
10. [Roadmap](#roadmap)

---

## 🎯 Visión del Proyecto

**YouTube Transcriber Pro** es una herramienta open-source para transcribir videos de YouTube usando OpenAI Whisper, con capacidades de búsqueda semántica y chat conversacional sobre el contenido.

### Casos de Uso:
- Investigadores analizando contenido educativo
- Estudiantes creando notas de clases
- Creadores de contenido analizando competencia
- Profesionales extrayendo insights de conferencias

### Diferenciadores:
- ✅ Multiidioma automático (Whisper)
- ✅ Output en JSON + TXT (RAG-ready)
- ✅ UI accesible (Gradio)
- ✅ Chat conversacional sobre transcripciones
- ✅ 100% open source

---

## 🏗️ Arquitectura Técnica

### Fase 1: Transcriptor
```
┌─────────────────┐
│   Gradio UI     │
│  - URL Input    │
│  - Progress     │
│  - File Viewer  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Core Engine    │
│  - yt-dlp       │ ─→ Descarga audio MP3
│  - OpenAI API   │ ─→ Transcribe con Whisper
│  - File Manager │ ─→ Guarda JSON + TXT
└─────────────────┘
         │
         ▼
┌─────────────────┐
│  Outputs        │
│  - JSON (RAG)   │
│  - TXT (legible)│
└─────────────────┘
```

### Fase 2: RAG + Chat
```
┌─────────────────┐
│   Gradio UI     │
│  + Chat Box     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  RAG Pipeline   │
│  - Embeddings   │ ─→ text-embedding-ada-002 (OpenAI)
│  - Vector DB    │ ─→ ChromaDB (local)
│  - Retriever    │ ─→ Similarity search
│  - LLM Chat     │ ─→ GPT-4 (OpenAI)
└─────────────────┘
```

---

## 📁 Estructura de Archivos

```
youtube-transcriber/
│
├── .env                      # API keys (NO subir a Git)
├── .gitignore               # Protección de secretos
├── requirements.txt         # Dependencias Python
├── config.py               # Configuración central
├── README.md               # Documentación de usuario
├── MASTER_PLAN.md          # Este archivo
│
├── main.py                 # Script CLI (Fase 1)
├── app_gradio.py           # UI Gradio (Fase 1)
│
├── src/                    # Código modular
│   ├── __init__.py
│   ├── transcriber.py     # Lógica de transcripción
│   ├── rag_engine.py      # RAG + embeddings (Fase 2)
│   └── utils.py           # Funciones auxiliares
│
├── transcripts/           # Outputs generados
│   ├── 01_video_title.json
│   ├── 01_video_title.txt
│   ├── 02_another_video.json
│   └── 02_another_video.txt
│
├── temp_audio/            # Archivos temporales (auto-limpieza)
│   └── .gitkeep
│
├── vector_db/             # ChromaDB storage (Fase 2)
│   └── .gitkeep
│
└── tests/                 # Unit tests (futuro)
    └── test_transcriber.py
```

---

## 🛠️ Stack Tecnológico

### Core:
- **Python**: 3.8+
- **OpenAI API**: Whisper (transcripción) + GPT-4 (chat Fase 2)
- **yt-dlp**: Descarga de audio de YouTube
- **Gradio**: Interfaz de usuario

### Fase 2 adicionales:
- **ChromaDB**: Vector database local
- **LangChain**: Orquestación RAG
- **OpenAI Embeddings**: text-embedding-ada-002

### Deployment:
- **Hugging Face Spaces**: Hosting gratuito
- **Docker**: Containerización (opcional)

---

## ⚙️ Configuración Inicial

### 1. Requisitos del Sistema
- **Python**: 3.8 o superior
- **FFmpeg**: Requerido por yt-dlp
  ```bash
  # Windows (con Chocolatey)
  choco install ffmpeg
  
  # O descargar de: https://ffmpeg.org/download.html
  ```
- **OpenAI API Key**: https://platform.openai.com/api-keys

### 2. Instalación

```bash
# Clonar o crear el proyecto
git clone <repo-url>
cd youtube-transcriber

# Crear entorno virtual (recomendado)
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Instalar dependencias
pip install -r requirements.txt
```

### 3. Configurar .env

```env
# .env
OPENAI_API_KEY=sk-proj-tu-api-key-aqui
```

### 4. Verificar instalación

```bash
python -c "import yt_dlp; import openai; print('✅ Todo listo')"
```

---

## 🚀 Fase 1: MVP - Transcriptor

### Objetivo:
Sistema funcional de transcripción con UI Gradio.

### Features:
- ✅ Input múltiples URLs
- ✅ Progress bar en tiempo real
- ✅ Output JSON + TXT
- ✅ Visor de archivos generados
- ✅ Descarga de transcripciones

### Archivos clave:
1. **config.py** - Configuración
2. **main.py** - Lógica core
3. **app_gradio.py** - Interfaz Gradio

### Flujo de datos:

```
Usuario ingresa URLs
         ↓
Gradio valida y parsea
         ↓
Para cada URL:
  1. Descargar audio (MP3)
  2. Enviar a Whisper API
  3. Recibir transcripción
  4. Guardar JSON + TXT
  5. Actualizar progress bar
  6. Limpiar archivos temporales
         ↓
Mostrar archivos generados
         ↓
Permitir descarga
```

### Estructura JSON de output:

```json
{
  "video_id": "6g_f2XxwSRA",
  "url": "https://youtu.be/6g_f2XxwSRA",
  "title": "Video Title Here",
  "language": null,
  "transcript": "Full transcription text...",
  "timestamp": "2025-10-12T14:30:00",
  "index": 1,
  "word_count": 2547
}
```

### Estimación de costos:

| Duración video | Costo aproximado |
|----------------|------------------|
| 10 minutos     | $0.06 USD        |
| 30 minutos     | $0.18 USD        |
| 1 hora         | $0.36 USD        |
| 2 horas        | $0.72 USD        |

**Nota**: Basado en Whisper API ($0.006/minuto)

---

## 🧠 Fase 2: RAG + Chat

### Objetivo:
Chat conversacional sobre transcripciones usando RAG.

### Nuevas features:
- ✅ Índice vectorial de transcripciones
- ✅ Búsqueda semántica
- ✅ Chat interface en Gradio
- ✅ Citación de fuentes (video + timestamp)

### Arquitectura RAG:

```
Usuario hace pregunta
         ↓
Convertir pregunta a embedding
         ↓
Buscar en ChromaDB (similarity search)
         ↓
Recuperar top-k chunks relevantes
         ↓
Construir prompt con contexto
         ↓
Enviar a GPT-4
         ↓
Respuesta + citaciones
```

### Nuevas dependencias (requirements.txt):

```txt
# Fase 2
chromadb>=0.4.0
langchain>=0.1.0
langchain-openai>=0.0.5
tiktoken>=0.5.0
```

### Configuración adicional:

```python
# config.py - Fase 2
EMBEDDING_MODEL = "text-embedding-ada-002"
CHAT_MODEL = "gpt-4-turbo-preview"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
TOP_K_RESULTS = 3
```

### Flujo de indexación:

```python
# Pseudo-código
for json_file in transcripts_folder:
    # 1. Leer transcripción
    data = load_json(json_file)
    
    # 2. Dividir en chunks
    chunks = text_splitter.split(data['transcript'])
    
    # 3. Crear embeddings
    embeddings = openai.embed(chunks)
    
    # 4. Guardar en ChromaDB con metadata
    vector_db.add(
        embeddings=embeddings,
        texts=chunks,
        metadata={
            'video_id': data['video_id'],
            'title': data['title'],
            'url': data['url']
        }
    )
```

### Chat prompt template:

```
Eres un asistente que ayuda a analizar transcripciones de videos de YouTube.

Contexto relevante:
{retrieved_chunks}

Videos de origen:
{source_videos}

Pregunta del usuario: {question}

Responde basándote SOLO en el contexto proporcionado. 
Si no tienes información suficiente, dilo claramente.
Siempre cita la fuente (título del video).
```

---

## 💻 Uso CLI (Alternativo)

### Opción 1: URLs hardcodeadas

Editar `main.py`:

```python
if __name__ == "__main__":
    create_directories()
    
    urls = [
        "https://youtu.be/6g_f2XxwSRA",
        "https://youtu.be/z7zZ_MiB_IU",
        # ... más URLs
    ]
    
    for i, url in enumerate(urls, 1):
        success = process_video(url, i)
        if success:
            print(f"✅ Video {i} completado")
```

Ejecutar:
```bash
python main.py
```

### Opción 2: Archivo de entrada

Crear `urls.txt`:
```
https://youtu.be/6g_f2XxwSRA
https://youtu.be/z7zZ_MiB_IU
https://youtu.be/bdploS_8Q1A
```

Modificar `main.py`:

```python
if __name__ == "__main__":
    create_directories()
    
    with open('urls.txt', 'r') as f:
        urls = [line.strip() for line in f if line.strip()]
    
    for i, url in enumerate(urls, 1):
        process_video(url, i)
```

### Opción 3: Argumentos de línea de comandos

```bash
python main.py https://youtu.be/VIDEO_ID
python main.py --file urls.txt
python main.py --batch urls1.txt urls2.txt
```

Implementación con `argparse`:

```python
import argparse

parser = argparse.ArgumentParser(description='Transcribe YouTube videos')
parser.add_argument('urls', nargs='*', help='YouTube URLs')
parser.add_argument('--file', help='File with URLs (one per line)')
args = parser.parse_args()

if args.file:
    with open(args.file) as f:
        urls = [line.strip() for line in f]
else:
    urls = args.urls
```

---

## 🌐 Deployment

### Opción 1: Hugging Face Spaces (Recomendado - GRATIS)

1. **Crear Space en HF**:
   - Ir a https://huggingface.co/spaces
   - New Space → Gradio → SDK
   - Nombre: `youtube-transcriber-pro`

2. **Estructura requerida**:
   ```
   Space/
   ├── app.py              # Renombrar app_gradio.py
   ├── requirements.txt
   └── README.md
   ```

3. **Configurar Secrets**:
   - Settings → Repository Secrets
   - Agregar: `OPENAI_API_KEY`

4. **README.md del Space**:
   ```markdown
   ---
   title: YouTube Transcriber Pro
   emoji: 🎥
   colorFrom: blue
   colorTo: purple
   sdk: gradio
   sdk_version: 4.0.0
   app_file: app.py
   pinned: false
   ---
   ```

### Opción 2: Local + ngrok (Desarrollo)

```bash
# Instalar ngrok
choco install ngrok

# Ejecutar Gradio
python app_gradio.py

# En otra terminal
ngrok http 7860
```

### Opción 3: Docker (Producción)

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y ffmpeg

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app_gradio.py"]
```

```bash
docker build -t youtube-transcriber .
docker run -p 7860:7860 -e OPENAI_API_KEY=sk-... youtube-transcriber
```

---

## 🗺️ Roadmap

### ✅ Completado:
- [x] Arquitectura base
- [x] Transcripción core
- [x] Output JSON + TXT

### 🔨 En progreso (Fase 1):
- [ ] UI Gradio básica
- [ ] Progress tracking
- [ ] File viewer
- [ ] Error handling robusto

### 📅 Planeado (Fase 2):
- [ ] Vector database setup
- [ ] Embedding pipeline
- [ ] RAG retrieval
- [ ] Chat interface
- [ ] Timestamp extraction
- [ ] Multi-video search

### 🌟 Features futuras:
- [ ] Batch processing paralelo
- [ ] Resumen automático por video
- [ ] Export a PDF/Markdown
- [ ] Soporte para playlists completas
- [ ] Detección de speakers
- [ ] Traducción automática
- [ ] Integración con Notion/Obsidian

---

## 📊 Métricas de éxito

### Fase 1:
- [ ] Transcribir 100% de URLs sin errores
- [ ] Tiempo promedio < 2x duración del video
- [ ] UI funcional en < 3 clicks
- [ ] 10+ usuarios beta testing

### Fase 2:
- [ ] Chat responde en < 3 segundos
- [ ] 90%+ precisión en citaciones
- [ ] Top-3 retrieval relevante en 80%+ queries
- [ ] 100+ usuarios activos

---

## 🤝 Contribuciones

### Áreas donde se necesita ayuda:
1. **Testing**: Unit tests y edge cases
2. **UI/UX**: Mejoras de diseño Gradio
3. **Optimización**: Procesamiento paralelo
4. **Documentación**: Tutoriales en video
5. **Internacionalización**: Traducciones UI

---

## 📝 Notas técnicas

### Limitaciones conocidas:
- **Whisper API**: Límite 25MB por archivo
- **Rate limits**: 50 requests/min (tier 1)
- **ChromaDB**: Máximo ~1M documentos en local
- **Gradio**: No state persistence entre reinicios

### Alternativas evaluadas:

| Componente | Elegido | Alternativas | Razón |
|------------|---------|--------------|-------|
| Transcripción | Whisper API | Whisper local, AssemblyAI | Balance costo/calidad |
| UI | Gradio | Streamlit, Flask | Rapidez desarrollo |
| Vector DB | ChromaDB | Pinecone, Weaviate | Simplicidad + local |
| LLM | GPT-4 | Claude, Llama | Disponibilidad API |

### Consideraciones de seguridad:
- ⚠️ NUNCA commitear `.env`
- ⚠️ Validar URLs para evitar inyección
- ⚠️ Sanitizar nombres de archivo
- ⚠️ Rate limiting en producción
- ⚠️ Logs sin API keys

---

## 📚 Referencias

### Documentación:
- [OpenAI Whisper API](https://platform.openai.com/docs/guides/speech-to-text)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [Gradio](https://www.gradio.app/docs/)
- [ChromaDB](https://docs.trychroma.com/)
- [LangChain](https://python.langchain.com/docs/get_started/introduction)

### Tutoriales relacionados:
- Building RAG systems with LangChain
- Gradio Advanced Features
- Vector Database Optimization

---

## 🎯 Comandos rápidos

```bash
# Setup inicial
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Ejecutar CLI
python main.py

# Ejecutar Gradio
python app_gradio.py

# Ejecutar tests
pytest tests/

# Limpiar archivos temporales
python -c "import shutil; shutil.rmtree('temp_audio', ignore_errors=True)"

# Ver espacio usado
python -c "import os; print(sum(os.path.getsize(f'transcripts/{f}') for f in os.listdir('transcripts')))"
```

---

**Última actualización**: 2025-10-12  
**Versión del plan**: 1.0  
**Mantenedor**: @inginddie  
**Licencia**: MIT (pendiente)