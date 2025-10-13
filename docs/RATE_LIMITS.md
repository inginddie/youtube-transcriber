# 🚦 Rate Limits y Manejo de Errores

## ¿Qué son los Rate Limits?

OpenAI limita cuántas peticiones puedes hacer por minuto para proteger su infraestructura. Si envías demasiadas peticiones muy rápido, recibirás un error **429 - Rate limit reached**.

---

## 🔧 Cómo lo Maneja el Sistema

### 1. **Espera entre Chunks**

Cuando un video se divide en múltiples chunks, el sistema espera **5 segundos** entre cada chunk:

```
Chunk 1 → Transcribe → ✅
   ⏳ Espera 5s
Chunk 2 → Transcribe → ✅
   ⏳ Espera 5s
Chunk 3 → Transcribe → ✅
```

### 2. **Exponential Backoff**

Si detecta un error 429, el sistema espera cada vez más tiempo:

```
Intento 1 → Error 429 → Espera 6s
Intento 2 → Error 429 → Espera 12s
Intento 3 → Error 429 → Espera 24s
Intento 4 → Error 429 → Espera 48s
Intento 5 → ✅ Éxito
```

### 3. **Reintentos Automáticos**

El sistema reintenta automáticamente hasta **5 veces** antes de fallar.

---

## 📊 Límites de OpenAI

### Por Tier:

| Tier | Requests/min | Tokens/min |
|------|--------------|------------|
| Free | 3 | 40,000 |
| Tier 1 | 50 | 2,000,000 |
| Tier 2 | 100 | 4,000,000 |
| Tier 3+ | Más | Más |

**Nota**: Los límites varían según el modelo y tu tier.

### Whisper API:
- **Límite típico**: 50 requests/min (Tier 1)
- **Tamaño máximo**: 25MB por archivo
- **Costo**: $0.006 por minuto de audio

---

## 💡 Mejores Prácticas

### 1. **Procesa Videos Grandes de Uno en Uno**

En lugar de:
```
❌ Transcribir 10 videos grandes al mismo tiempo
```

Haz:
```
✅ Transcribir 1 video grande a la vez
✅ Esperar a que termine antes del siguiente
```

### 2. **Usa la Interfaz Web**

La interfaz web maneja automáticamente:
- ✅ Esperas entre chunks
- ✅ Reintentos con backoff
- ✅ Mensajes de progreso

### 3. **Monitorea tu Uso**

Verifica tu uso en: https://platform.openai.com/usage

### 4. **Actualiza tu Tier**

Si necesitas más capacidad:
1. Ve a: https://platform.openai.com/account/limits
2. Agrega más créditos
3. Tu tier aumentará automáticamente

---

## 🔍 Identificar Errores

### Error 429 - Rate Limit
```
Error code: 429 - Rate limit reached for requests
```

**Causa**: Demasiadas peticiones muy rápido  
**Solución**: El sistema espera automáticamente

### Error 429 - Quota Exceeded
```
Error code: 429 - You exceeded your current quota
```

**Causa**: Sin créditos o límite mensual alcanzado  
**Solución**: Agrega créditos en OpenAI

### Error 503 - Service Unavailable
```
Error code: 503 - The server is overloaded
```

**Causa**: OpenAI está sobrecargado  
**Solución**: Espera unos minutos y reintenta

---

## ⚙️ Configuración Avanzada

Puedes ajustar estos valores en `config.py`:

```python
# Número de reintentos
MAX_RETRIES = 5

# Tiempo base de espera (segundos)
RETRY_DELAY = 3

# El sistema usa exponential backoff:
# Intento 1: 3s
# Intento 2: 6s (3 * 2^1)
# Intento 3: 12s (3 * 2^2)
# Intento 4: 24s (3 * 2^3)
# Intento 5: 48s (3 * 2^4)
```

---

## 📈 Optimización

### Para Videos Grandes:

1. **El sistema divide automáticamente** archivos >25MB
2. **Espera 5s entre chunks** para evitar rate limits
3. **Usa exponential backoff** si detecta errores

### Para Múltiples Videos:

```python
# Procesa con delay entre videos
for url in urls:
    result = transcriber.process_video(url)
    time.sleep(10)  # Espera 10s entre videos
```

---

## 🎯 Resumen

| Situación | Acción del Sistema |
|-----------|-------------------|
| Video pequeño (<25MB) | Transcribe directamente |
| Video grande (>25MB) | Divide en chunks + espera 5s entre cada uno |
| Error 429 | Espera con exponential backoff |
| Error de red | Reintenta hasta 5 veces |
| Otros errores | Reporta y continúa con siguiente video |

---

## 🆘 Si Sigues Teniendo Problemas

1. **Verifica tu tier**: https://platform.openai.com/account/limits
2. **Revisa tu uso**: https://platform.openai.com/usage
3. **Agrega créditos**: https://platform.openai.com/account/billing
4. **Contacta soporte**: Si crees que hay un error

---

## ✅ El Sistema Está Optimizado

El sistema ya incluye:
- ✅ Rate limiting automático
- ✅ Exponential backoff
- ✅ Reintentos inteligentes
- ✅ Logging detallado
- ✅ Manejo de errores robusto

**¡Solo necesitas usarlo y el sistema se encarga del resto!** 🚀
