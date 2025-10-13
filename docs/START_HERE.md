# 🚀 EMPIEZA AQUÍ - Guía Rápida

## ✅ Estado Actual de la Instalación

- ✅ Python instalado
- ✅ FFmpeg instalado
- ✅ Entorno virtual creado
- ✅ Dependencias instaladas
- ✅ Directorios creados
- ⚠️  **FALTA**: Configurar API Key de OpenAI

---

## 🔑 PASO FINAL: Configurar tu API Key

### 1. Obtener API Key de OpenAI

Ve a: **https://platform.openai.com/api-keys**

- Inicia sesión o crea una cuenta
- Click en "Create new secret key"
- Dale un nombre (ej: "YouTube Transcriber")
- **COPIA LA CLAVE** (empieza con `sk-proj-...`)
- ⚠️ Guárdala ahora, no podrás verla después

### 2. Editar el archivo .env

**Opción A: Con Notepad (Recomendado)**
```
1. Abre el archivo .env con Notepad
2. Busca la línea: OPENAI_API_KEY=sk-proj-COLOCA-TU-API-KEY-AQUI
3. Reemplaza "sk-proj-COLOCA-TU-API-KEY-AQUI" con tu clave real
4. Guarda el archivo (Ctrl+S)
```

**Opción B: Con PowerShell**
```powershell
notepad .env
```

---

## 🎬 PROBAR EL SISTEMA

Una vez configurada tu API key, tienes 2 opciones:

### Opción 1: Interfaz Web (Recomendado para empezar)

```powershell
# Activar entorno virtual
.\venv\Scripts\Activate.ps1

# Iniciar la interfaz web
python app_gradio.py
```

Luego abre tu navegador en: **http://localhost:7860**

### Opción 2: Línea de Comandos

```powershell
# Activar entorno virtual
.\venv\Scripts\Activate.ps1

# Transcribir un video
python main.py https://youtu.be/dQw4w9WgXcQ
```

---

## 📝 Ejemplo de Uso (Interfaz Web)

1. **Inicia la aplicación**:
   ```powershell
   .\venv\Scripts\Activate.ps1
   python app_gradio.py
   ```

2. **Abre tu navegador**: http://localhost:7860

3. **Pega una URL de YouTube** en el cuadro de texto:
   ```
   https://youtu.be/dQw4w9WgXcQ
   ```

4. **Click en** "🚀 Transcribe Videos"

5. **Espera** a que termine (verás el progreso)

6. **Descarga** tus transcripciones en formato JSON o TXT

---

## 📁 ¿Dónde están mis archivos?

Después de transcribir, encontrarás tus archivos en:

```
youtube-transcriber/
└── transcripts/
    ├── 01_nombre_del_video.json    # Formato estructurado
    └── 01_nombre_del_video.txt     # Formato legible
```

---

## 💰 Costos Estimados

Whisper API cuesta **$0.006 por minuto** de audio:

| Duración del Video | Costo Aproximado |
|-------------------|------------------|
| 10 minutos        | $0.06 USD        |
| 30 minutos        | $0.18 USD        |
| 1 hora            | $0.36 USD        |

---

## 🆘 Solución de Problemas

### Error: "OPENAI_API_KEY not found"
**Solución**: Verifica que editaste el archivo .env correctamente

### Error: "FFmpeg not found"
**Solución**: Cierra y abre una nueva ventana de PowerShell (FFmpeg necesita reinicio)

### Error: "Module not found"
**Solución**: Asegúrate de activar el entorno virtual:
```powershell
.\venv\Scripts\Activate.ps1
```

---

## 📚 Próximos Pasos

Una vez que funcione:

1. **Lee la documentación completa**: [README.md](README.md)
2. **Explora ejemplos**: [examples/](examples/)
3. **Aprende sobre RAG**: [docs/USAGE.md](docs/USAGE.md)
4. **Despliega en producción**: [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)

---

## ✨ Comandos Útiles

```powershell
# Activar entorno virtual
.\venv\Scripts\Activate.ps1

# Interfaz web
python app_gradio.py

# CLI - Un video
python main.py https://youtu.be/VIDEO_ID

# CLI - Múltiples videos desde archivo
python main.py --file urls.txt

# Ejecutar tests
pytest

# Ver ayuda
python main.py --help
```

---

## 🎯 Resumen de Configuración

```
✅ Python 3.13.5
✅ FFmpeg instalado
✅ Entorno virtual: venv/
✅ Dependencias instaladas
✅ Directorios creados
⚠️  API Key: NECESITA CONFIGURACIÓN

SIGUIENTE PASO: Editar .env con tu API key
```

---

**¿Listo para empezar? Configura tu API key y ejecuta:**

```powershell
.\venv\Scripts\Activate.ps1
python app_gradio.py
```

**¡Disfruta transcribiendo! 🎉**
