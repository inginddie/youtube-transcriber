# 🧠 Guía de RAG (Retrieval-Augmented Generation)

## ¿Qué es RAG?

RAG permite **chatear con tus transcripciones** y hacer **búsquedas semánticas** inteligentes. En lugar de buscar palabras clave, el sistema entiende el **significado** de tu pregunta.

---

## 🚀 Cómo usar RAG

### Paso 1: Transcribir Videos

Primero necesitas tener al menos una transcripción:

```bash
python main.py https://youtu.be/VIDEO_ID
```

O usa la interfaz web en la pestaña "Transcribe Videos".

### Paso 2: Indexar Transcripciones

**Opción A: Interfaz Web**
1. Abre la interfaz: `python launch_web.py`
2. Ve a la pestaña "🔧 RAG Setup"
3. Click en "Index Transcripts"
4. Espera a que termine (puede tardar 1-2 minutos)

**Opción B: Script de prueba**
```bash
python test_rag.py
```

### Paso 3: Chatear o Buscar

**Chat:**
1. Ve a la pestaña "💬 Chat with Transcripts"
2. Escribe tu pregunta
3. Obtén respuestas con citaciones de fuentes

**Búsqueda:**
1. Ve a la pestaña "🔍 Search Transcripts"
2. Escribe tu consulta
3. Ve los resultados más relevantes

---

## 💡 Ejemplos de Uso

### Preguntas para el Chat

```
✅ "¿De qué trata este video?"
✅ "Resume los puntos principales"
✅ "¿Qué herramientas mencionan?"
✅ "¿Cómo se hace [algo específico]?"
✅ "¿Qué dijeron sobre [tema]?"
```

### Búsquedas Semánticas

```
✅ "crear influencer con IA"
✅ "herramientas de generación de imágenes"
✅ "monetización de contenido"
✅ "tutorial paso a paso"
```

---

## 🔧 Cómo Funciona

### 1. Indexación

```
Transcripción → Chunks → Embeddings → Vector DB
```

- **Chunks**: El texto se divide en partes de ~1000 caracteres
- **Embeddings**: Cada chunk se convierte en un vector (representación matemática)
- **Vector DB**: Se guarda en ChromaDB (local)

### 2. Búsqueda

```
Tu pregunta → Embedding → Búsqueda de similitud → Top-K resultados
```

- Tu pregunta se convierte en un vector
- Se buscan los chunks más similares
- Se devuelven los más relevantes

### 3. Chat

```
Tu pregunta → Búsqueda → Contexto → GPT-4 → Respuesta + Fuentes
```

- Se buscan los chunks relevantes
- Se envían a GPT-4 como contexto
- GPT-4 genera una respuesta basada en ese contexto
- Se incluyen las fuentes (videos) de donde vino la información

---

## 💰 Costos

### Indexación (una sola vez por transcripción)
- **Embeddings**: ~$0.0001 por 1K tokens
- **Ejemplo**: Video de 30 min (~5000 palabras) = ~$0.001

### Chat (por pregunta)
- **Búsqueda**: Gratis (local)
- **GPT-4**: ~$0.03 por 1K tokens de entrada
- **Ejemplo**: Pregunta típica = ~$0.01-0.03

### Búsqueda
- **Completamente gratis** (todo es local)

---

## 📊 Configuración Avanzada

Puedes ajustar estos parámetros en `config.py`:

```python
# Tamaño de los chunks
CHUNK_SIZE = 1000          # Caracteres por chunk
CHUNK_OVERLAP = 200        # Superposición entre chunks

# Búsqueda
TOP_K_RESULTS = 3          # Número de chunks a recuperar

# Chat
TEMPERATURE = 0.7          # Creatividad de GPT-4 (0-1)
CHAT_MODEL = "gpt-4-turbo-preview"  # Modelo a usar
```

---

## 🎯 Casos de Uso

### 1. Investigación
```
"¿Qué estudios mencionan sobre [tema]?"
"Resume las estadísticas presentadas"
```

### 2. Aprendizaje
```
"Explica el concepto de [X]"
"¿Cuáles son los pasos para [Y]?"
```

### 3. Análisis de Contenido
```
"¿Qué productos recomiendan?"
"¿Cuál es el tono del video?"
```

### 4. Extracción de Información
```
"Lista todas las herramientas mencionadas"
"¿Qué precios se mencionan?"
```

---

## 🔍 Búsqueda vs Chat

### Usa Búsqueda cuando:
- ✅ Quieres ver el texto original
- ✅ Necesitas múltiples resultados
- ✅ Quieres explorar el contenido
- ✅ No necesitas una respuesta elaborada

### Usa Chat cuando:
- ✅ Quieres una respuesta directa
- ✅ Necesitas un resumen
- ✅ Quieres hacer preguntas de seguimiento
- ✅ Necesitas análisis o interpretación

---

## 🐛 Solución de Problemas

### "Please index your transcripts first"
**Solución**: Ve a "RAG Setup" y haz click en "Index Transcripts"

### "Vector store not found"
**Solución**: Necesitas indexar primero. El vector store se crea durante la indexación.

### "No transcripts found"
**Solución**: Transcribe al menos un video primero.

### Respuestas incorrectas o irrelevantes
**Solución**: 
- Asegúrate de que la pregunta sea clara
- Verifica que el contenido esté en las transcripciones
- Intenta reformular la pregunta

### Indexación muy lenta
**Solución**: 
- Es normal para muchas transcripciones
- Solo necesitas hacerlo una vez
- Puedes cerrar y volver después

---

## 📚 Recursos Adicionales

- [Documentación de ChromaDB](https://docs.trychroma.com/)
- [Documentación de LangChain](https://python.langchain.com/)
- [OpenAI Embeddings](https://platform.openai.com/docs/guides/embeddings)
- [GPT-4 API](https://platform.openai.com/docs/models/gpt-4)

---

## 🎉 ¡Listo!

Ahora puedes:
1. ✅ Transcribir videos de YouTube
2. ✅ Indexar las transcripciones
3. ✅ Chatear con tus videos
4. ✅ Buscar semánticamente

**¡Disfruta explorando tus transcripciones con IA!** 🚀
