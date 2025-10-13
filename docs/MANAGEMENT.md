# ⚙️ Guía de Gestión de Archivos

## 🎯 Funcionalidades de Gestión

El sistema ahora incluye herramientas completas para gestionar tus transcripciones y la base de datos vectorial.

---

## 🖥️ Interfaz Web - Pestaña "Management"

### 1. 📁 Gestión de Transcripciones

#### Ver Transcripciones
- Click en "🔄 Actualizar Lista"
- Verás todas tus transcripciones con:
  - Título del video
  - Video ID
  - Fecha de transcripción

#### Eliminar Transcripciones Seleccionadas
1. Marca las transcripciones que quieres eliminar
2. Click en "🗑️ Eliminar Seleccionadas"
3. Confirma la operación

**Qué se elimina:**
- ✅ Archivo JSON
- ✅ Archivo TXT
- ⚠️ La entrada en Vector DB (necesitas re-indexar)

### 2. 🗄️ Gestión de Base de Datos Vectorial

#### Ver Estado de la DB
- Click en "📊 Ver Estado de DB"
- Verás:
  - Ubicación de la DB
  - Número de archivos
  - Tamaño en MB
  - Estado (inicializada o vacía)

#### Vaciar Vector DB
- Click en "🗑️ Vaciar Vector DB"
- Esto elimina todos los índices vectoriales
- **Necesitarás re-indexar** para usar RAG de nuevo

**Cuándo vaciar:**
- ✅ Eliminaste muchas transcripciones
- ✅ Quieres empezar de cero con RAG
- ✅ La DB está corrupta

### 3. 🧹 Limpieza Completa

#### Eliminar TODO
- Click en "🗑️ ELIMINAR TODO"
- Esto elimina:
  - ✅ Todas las transcripciones (JSON + TXT)
  - ✅ Toda la base de datos vectorial
  - ✅ Archivos temporales

**⚠️ ADVERTENCIA**: Esta acción es **irreversible**

**Cuándo usar:**
- Quieres empezar completamente de cero
- Estás haciendo pruebas
- Quieres liberar espacio

---

## 💻 CLI - Script de Gestión

### Comandos Disponibles

```bash
# Ver ayuda
python manage.py

# Listar transcripciones
python manage.py --list

# Ver estadísticas
python manage.py --stats

# Eliminar una transcripción
python manage.py --delete VIDEO_ID

# Ver estado de Vector DB
python manage.py --check-db

# Limpiar Vector DB
python manage.py --clear-db

# Limpiar archivos temporales
python manage.py --clean-temp

# Eliminar TODO
python manage.py --clear-all
```

### Ejemplos de Uso

#### Listar Transcripciones
```bash
python manage.py --list
```

Output:
```
📁 TRANSCRIPCIONES DISPONIBLES
============================================================

Total: 5 transcripciones

1. How to create an AI Influencer
   Video ID: 6g_f2XxwSRA
   Palabras: 2,547
   Fecha: 2025-10-12T20:55:11
   Archivos: 01_How_to_create_an_AI_Influencer.json, .txt

2. ...
```

#### Ver Estadísticas
```bash
python manage.py --stats
```

Output:
```
📊 ESTADÍSTICAS
============================================================

📝 Transcripciones: 5
📊 Total de palabras: 12,547
📈 Promedio por video: 2,509 palabras

🗄️  Vector DB: 15.43 MB

✅ Sin archivos temporales
```

#### Eliminar una Transcripción
```bash
python manage.py --delete 6g_f2XxwSRA
```

Output:
```
🔍 Buscando transcripción con Video ID: 6g_f2XxwSRA
✅ Eliminado: 01_How_to_create_an_AI_Influencer.json
✅ Eliminado: 01_How_to_create_an_AI_Influencer.txt

✅ Transcripción eliminada: How to create an AI Influencer
```

#### Limpiar Vector DB
```bash
python manage.py --clear-db
```

Output:
```
🗑️  Limpiando base de datos vectorial...
✅ Base de datos vectorial limpiada
⚠️  Necesitarás re-indexar para usar RAG
```

#### Limpieza Completa
```bash
python manage.py --clear-all
```

Output:
```
🗑️  LIMPIEZA COMPLETA
============================================================

⚠️  ¿Estás seguro? Esto eliminará TODO (y/n): y

✅ Eliminadas 5 transcripciones
✅ Base de datos vectorial limpiada
✅ Eliminados 0 archivos temporales

✅ Limpieza completa finalizada
```

---

## 🔄 Flujos de Gestión

### Flujo 1: Eliminar Videos Específicos

```
1. Listar transcripciones
   python manage.py --list

2. Identificar Video ID del que quieres eliminar

3. Eliminar
   python manage.py --delete VIDEO_ID

4. Re-indexar (si usas RAG)
   Interfaz Web → RAG Setup → Index Transcripts
```

### Flujo 2: Limpiar y Empezar de Cero

```
1. Eliminar todo
   python manage.py --clear-all

2. Transcribir nuevos videos
   python main.py --file new_urls.txt

3. Indexar
   Interfaz Web → RAG Setup → Index Transcripts
```

### Flujo 3: Mantenimiento Regular

```
1. Ver estadísticas
   python manage.py --stats

2. Limpiar archivos temporales
   python manage.py --clean-temp

3. Verificar Vector DB
   python manage.py --check-db
```

---

## 💡 Mejores Prácticas

### ✅ Hacer:

1. **Backup antes de eliminar**
   ```bash
   # Copiar carpeta transcripts
   cp -r transcripts transcripts_backup
   ```

2. **Limpiar archivos temporales regularmente**
   ```bash
   python manage.py --clean-temp
   ```

3. **Re-indexar después de eliminar transcripciones**
   - Si usas RAG
   - Para mantener sincronizado

4. **Ver estadísticas periódicamente**
   ```bash
   python manage.py --stats
   ```

### ❌ Evitar:

1. **Eliminar sin backup** si son importantes
2. **Vaciar Vector DB** sin razón
3. **Eliminar TODO** sin confirmar
4. **Olvidar re-indexar** después de cambios

---

## 🔒 Seguridad

### Confirmaciones

- ✅ `--clear-all` pide confirmación
- ✅ Interfaz web muestra advertencias
- ✅ Operaciones son registradas en logs

### Recuperación

**Si eliminaste por error:**

1. **Transcripciones**: No hay recuperación (re-transcribir)
2. **Vector DB**: Re-indexar las transcripciones existentes
3. **Temp files**: No importa (se regeneran)

**Prevención:**

```bash
# Hacer backup antes de limpiar
tar -czf backup_$(date +%Y%m%d).tar.gz transcripts/ vector_db/
```

---

## 📊 Monitoreo

### Ver Uso de Espacio

```bash
# Windows
python manage.py --stats

# O manualmente
dir transcripts /s
dir vector_db /s
```

### Logs de Operaciones

Todas las operaciones se registran en:
```
logs/transcriber_YYYYMMDD.log
```

---

## 🆘 Troubleshooting

### "Permission denied" al eliminar

**Solución:**
- Cierra cualquier programa que esté usando los archivos
- Ejecuta como administrador

### "Vector DB corrupta"

**Solución:**
```bash
python manage.py --clear-db
# Luego re-indexar en la interfaz web
```

### "Archivos temporales ocupan mucho espacio"

**Solución:**
```bash
python manage.py --clean-temp
```

---

## 🎯 Comandos Rápidos

```bash
# Ver qué tienes
python manage.py --list
python manage.py --stats

# Limpiar
python manage.py --clean-temp        # Solo temporales
python manage.py --clear-db          # Solo Vector DB
python manage.py --delete VIDEO_ID   # Una transcripción
python manage.py --clear-all         # TODO

# Verificar
python manage.py --check-db          # Estado de DB
```

---

## ✅ Resumen

| Operación | Interfaz Web | CLI |
|-----------|--------------|-----|
| Listar | ✅ Pestaña Management | `--list` |
| Eliminar seleccionadas | ✅ Checkbox + botón | `--delete` |
| Ver DB | ✅ Botón "Ver Estado" | `--check-db` |
| Limpiar DB | ✅ Botón "Vaciar DB" | `--clear-db` |
| Eliminar todo | ✅ Botón "ELIMINAR TODO" | `--clear-all` |
| Estadísticas | ❌ | `--stats` |
| Limpiar temp | ❌ | `--clean-temp` |

---

**¡Gestiona tus transcripciones de forma fácil y segura!** 🚀
