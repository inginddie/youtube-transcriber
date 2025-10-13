# ⚡ Quick Start Guide

Guía rápida de 5 minutos para empezar a usar YouTube Transcriber Pro.

## 🚀 Instalación Rápida

### 1. Clonar el Repositorio

```bash
git clone https://github.com/TU_USUARIO/youtube-transcriber.git
cd youtube-transcriber
```

### 2. Crear Entorno Virtual

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar API Key

```bash
# Copiar archivo de ejemplo
copy .env.example .env    # Windows
cp .env.example .env      # Mac/Linux

# Editar .env y agregar tu API key
# OPENAI_API_KEY=sk-proj-tu-api-key-aqui
```

Obtén tu API key en: https://platform.openai.com/api-keys

### 5. Instalar FFmpeg

**Windows (con winget):**
```bash
winget install ffmpeg
```

**Mac (con Homebrew):**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install ffmpeg
```

### 6. Verificar Instalación

```bash
python tests/test_setup.py
```

## 🎯 Uso Básico

### Interfaz Web (Recomendado)

```bash
python app_gradio.py
```

Abre tu navegador en: http://localhost:7860

### Línea de Comandos

```bash
# Un video
python main.py https://youtu.be/VIDEO_ID

# Múltiples videos
python main.py https://youtu.be/VIDEO1 https://youtu.be/VIDEO2

# Desde archivo
python main.py --file urls.txt
```

## 📋 Funcionalidades Principales

### 1. Transcribir Videos

1. Abre la interfaz web
2. Ve a la pestaña "📝 Transcribe"
3. Pega la URL del video
4. Click en "🎬 Transcribir"

### 2. Buscar en Transcripciones

1. Ve a la pestaña "🔍 Search"
2. Escribe tu consulta
3. Obtén resultados relevantes con contexto

### 3. Chat con tus Videos

1. Ve a la pestaña "💬 Chat"
2. Haz preguntas sobre el contenido
3. Obtén respuestas con fuentes citadas

### 4. Gestionar Transcripciones

**Interfaz Web:**
1. Ve a la pestaña "⚙️ Management"
2. Ver, seleccionar y eliminar transcripciones
3. Gestionar Vector DB

**CLI:**
```bash
# Ver todas las transcripciones
python manage.py --list

# Ver estadísticas
python manage.py --stats

# Eliminar una transcripción
python manage.py --delete VIDEO_ID

# Limpiar archivos temporales
python manage.py --clean-temp
```

## 💰 Costos

Whisper API: **$0.006 por minuto**

| Duración | Costo Aprox. |
|----------|--------------|
| 10 min   | $0.06        |
| 30 min   | $0.18        |
| 1 hora   | $0.36        |

## 📁 Archivos Generados

```
transcripts/
├── 01_Titulo_del_Video.json    # Para RAG
└── 01_Titulo_del_Video.txt     # Para lectura
```

## 🆘 Problemas Comunes

### Error: "API Key not configured"

Edita el archivo `.env` y agrega tu API key:
```
OPENAI_API_KEY=sk-proj-tu-api-key-aqui
```

### Error: "FFmpeg not found"

Instala FFmpeg y reinicia tu terminal:
```bash
# Windows
winget install ffmpeg

# Mac
brew install ffmpeg

# Linux
sudo apt install ffmpeg
```

### Error: "Module not found"

Asegúrate de estar en el entorno virtual:
```bash
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

# Reinstalar dependencias
pip install -r requirements.txt
```

### Videos muy largos

Para videos largos (>1 hora):
- Considera el costo (~$0.36 por hora)
- El proceso puede tardar varios minutos
- Asegúrate de tener buena conexión

## 📚 Más Información

- **Documentación Completa**: [DOCUMENTATION.md](DOCUMENTATION.md)
- **Guía de Uso**: [docs/USAGE.md](docs/USAGE.md)
- **Guía de Gestión**: [docs/MANAGEMENT.md](docs/MANAGEMENT.md)
- **Guía RAG**: [docs/RAG_GUIDE.md](docs/RAG_GUIDE.md)

## 🤝 Contribuir

¿Quieres contribuir? Lee [CONTRIBUTING.md](CONTRIBUTING.md)

## 📧 Soporte

- **Issues**: https://github.com/TU_USUARIO/youtube-transcriber/issues
- **Discussions**: https://github.com/TU_USUARIO/youtube-transcriber/discussions

---

¡Listo para transcribir! 🎉
