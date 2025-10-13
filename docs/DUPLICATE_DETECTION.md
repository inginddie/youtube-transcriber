# 🔍 Detección de Duplicados

## ¿Qué es?

El sistema ahora **detecta automáticamente** si un video ya fue transcrito y te permite:
- ✅ **Saltarlo** (por defecto) - Ahorra tiempo y dinero
- ✅ **Re-transcribirlo** (opcional) - Si quieres actualizar

---

## 🎯 Cómo Funciona

### 1. Detección por Video ID

Cuando intentas transcribir un video, el sistema:

```
1. Extrae el Video ID de la URL
2. Busca en la carpeta transcripts/
3. Compara con transcripciones existentes
4. Si encuentra coincidencia → Salta o pregunta
```

### 2. Detección de Duplicados en la Lista

Si ingresas la misma URL múltiples veces:

```
Input:
https://youtu.be/VIDEO_1
https://youtu.be/VIDEO_2
https://youtu.be/VIDEO_1  ← Duplicado!

Output:
✅ Procesando VIDEO_1
✅ Procesando VIDEO_2
⏭️  VIDEO_1 duplicado removido
```

---

## 🖥️ Uso en Interfaz Web

### Opción 1: Saltar Duplicados (Por Defecto)

1. Ingresa tus URLs
2. Deja marcado "Skip already transcribed videos"
3. Click en "Transcribe Videos"
4. El sistema saltará videos ya transcritos

**Resultado:**
```
📊 Processing Summary
- ✅ Newly transcribed: 2
- ⏭️  Skipped (already exist): 1
- ❌ Failed: 0
```

### Opción 2: Forzar Re-transcripción

1. Ingresa tus URLs
2. **Desmarca** "Skip already transcribed videos"
3. Click en "Transcribe Videos"
4. El sistema re-transcribirá todo

**Cuándo usar:**
- Quieres actualizar una transcripción antigua
- El video fue editado/actualizado
- La transcripción anterior tiene errores

---

## 💻 Uso en CLI

### Saltar Duplicados (Por Defecto)

```bash
python main.py https://youtu.be/VIDEO_ID
```

Si el video ya existe:
```
🔍 Checking for existing transcript...
⏭️  VIDEO ALREADY TRANSCRIBED - SKIPPING
📄 Title: Video Title
📅 Transcribed: 2025-10-12T21:00:00
```

### Forzar Re-transcripción

```bash
python main.py --force https://youtu.be/VIDEO_ID
```

Esto **siempre** transcribirá, incluso si ya existe.

### Desde Archivo

```bash
# Saltar duplicados
python main.py --file urls.txt

# Forzar re-transcripción
python main.py --file urls.txt --force
```

---

## 📊 Información Mostrada

Cuando se detecta un duplicado, verás:

### En Logs:
```
🔍 Checking for existing transcript...
⏭️  VIDEO ALREADY TRANSCRIBED - SKIPPING
📄 Title: How to create an AI Influencer
📅 Transcribed: 2025-10-12T21:04:29
📁 JSON: transcripts/01_How_to_create_an_AI_Influencer.json
📁 TXT: transcripts/01_How_to_create_an_AI_Influencer.txt
```

### En Resumen:
```
📊 PROCESSING SUMMARY
✅ Newly transcribed: 2
⏭️  Skipped (already exist): 1
❌ Failed: 0
📝 Total processed: 3
```

---

## 💰 Ahorro de Costos

### Sin Detección de Duplicados:
```
Video 1 (30 min) → $0.18
Video 2 (30 min) → $0.18
Video 1 (duplicado) → $0.18  ← Desperdicio!
Total: $0.54
```

### Con Detección de Duplicados:
```
Video 1 (30 min) → $0.18
Video 2 (30 min) → $0.18
Video 1 (duplicado) → $0.00  ← Saltado!
Total: $0.36
Ahorro: $0.18 (33%)
```

---

## 🔧 Casos de Uso

### 1. Procesar Playlist con Videos Repetidos

```bash
# URLs con duplicados
python main.py --file playlist.txt

# El sistema automáticamente:
# - Detecta duplicados en la lista
# - Detecta videos ya transcritos
# - Solo procesa los nuevos
```

### 2. Actualizar Transcripciones Antiguas

```bash
# Re-transcribir todo
python main.py --force --file old_videos.txt
```

### 3. Continuar Proceso Interrumpido

Si un proceso se interrumpió:

```bash
# Simplemente vuelve a ejecutar
python main.py --file urls.txt

# Solo procesará los que faltan
```

---

## 🎯 Ventajas

### ✅ Ahorro de Tiempo
- No esperas por videos ya procesados
- Proceso más rápido

### ✅ Ahorro de Dinero
- No pagas por re-transcribir
- Optimiza uso de API

### ✅ Evita Rate Limits
- Menos peticiones a la API
- Menos probabilidad de error 429

### ✅ Organización
- Sabe qué videos ya tienes
- Fácil continuar procesos

---

## 🔍 Cómo se Detecta

El sistema busca por **Video ID**, no por URL. Esto significa que estas URLs se detectan como el mismo video:

```
✅ https://youtu.be/VIDEO_ID
✅ https://www.youtube.com/watch?v=VIDEO_ID
✅ https://www.youtube.com/watch?v=VIDEO_ID&t=10s
✅ https://youtu.be/VIDEO_ID?si=abc123

Todas tienen el mismo Video ID → Se detectan como duplicados
```

---

## ⚙️ Configuración

### Por Defecto:
- ✅ Saltar duplicados: **Activado**
- ✅ Detección en lista: **Siempre activa**
- ✅ Logging detallado: **Activado**

### Cambiar Comportamiento:

**Interfaz Web:**
- Desmarca "Skip already transcribed videos"

**CLI:**
- Usa flag `--force`

**Programático:**
```python
transcriber = YouTubeTranscriber()

# Saltar duplicados
result = transcriber.process_video(url, skip_if_exists=True)

# Forzar re-transcripción
result = transcriber.process_video(url, skip_if_exists=False)
```

---

## 📝 Estructura de Respuesta

Cuando se salta un video:

```python
{
    "success": True,
    "skipped": True,  # ← Indica que fue saltado
    "video_id": "VIDEO_ID",
    "title": "Video Title",
    "json_path": "path/to/file.json",
    "txt_path": "path/to/file.txt",
    "word_count": 1234,
    "message": "Video already transcribed"
}
```

---

## 🐛 Solución de Problemas

### "Video no se detecta como duplicado"

**Posibles causas:**
1. El archivo JSON fue movido/renombrado
2. El Video ID en el JSON es diferente
3. El archivo JSON está corrupto

**Solución:**
- Verifica que el archivo JSON existe
- Abre el JSON y verifica el campo `video_id`

### "Quiero re-transcribir pero se salta"

**Solución:**
- Usa `--force` en CLI
- Desmarca "Skip already transcribed" en UI

### "Duplicados no se detectan en la lista"

**Esto es normal si:**
- Las URLs son diferentes pero apuntan al mismo video
- El sistema las detectará y removerá automáticamente

---

## ✨ Resumen

| Característica | Estado |
|----------------|--------|
| Detección por Video ID | ✅ |
| Detección en lista | ✅ |
| Saltar automáticamente | ✅ |
| Forzar re-transcripción | ✅ |
| Logging detallado | ✅ |
| Resumen de duplicados | ✅ |
| Ahorro de costos | ✅ |

**¡El sistema está optimizado para evitar trabajo duplicado!** 🚀
