# 🚂 Railway Deployment Guide

Guía completa para deployar YouTube Transcriber Pro en Railway con seguridad completa.

## 🔒 Características de Seguridad

✅ **Rate Limiting**
- 5 transcripciones por hora por IP
- 20 búsquedas por minuto por IP
- 10 mensajes de chat por minuto por IP

✅ **Protección de API Keys**
- Variables de entorno seguras
- No expuestas en el código
- Rotación recomendada

✅ **Headers de Seguridad**
- X-Content-Type-Options
- X-Frame-Options
- Content-Security-Policy
- HSTS

✅ **Blacklist Automática**
- Bloqueo después de 5 intentos fallidos
- Protección contra bots

## 📋 Pre-requisitos

1. Cuenta en [Railway.app](https://railway.app)
2. OpenAI API Key
3. Repositorio en GitHub

## 🚀 Deployment Paso a Paso

### 1. Preparar el Repositorio

Asegúrate de que estos archivos estén en tu repo:
- ✅ `app_gradio_secure.py`
- ✅ `src/security.py`
- ✅ `railway.json`
- ✅ `nixpacks.toml`
- ✅ `Procfile`
- ✅ `runtime.txt`
- ✅ `requirements.txt`

### 2. Crear Proyecto en Railway

1. Ve a [railway.app](https://railway.app)
2. Click en "New Project"
3. Selecciona "Deploy from GitHub repo"
4. Autoriza Railway a acceder a tu GitHub
5. Selecciona el repositorio `youtube-transcriber`

### 3. Configurar Variables de Entorno

En Railway, ve a tu proyecto → Variables y agrega:

#### Variables Requeridas:

```bash
# OpenAI API Key (REQUERIDO)
OPENAI_API_KEY=sk-proj-tu-api-key-aqui

# Entorno
RAILWAY_ENVIRONMENT=production

# Puerto (Railway lo asigna automáticamente)
PORT=7860
```

#### Variables Opcionales de Seguridad:

```bash
# Rate Limits (valores por defecto si no se especifican)
MAX_TRANSCRIPTIONS_PER_HOUR=5
MAX_SEARCHES_PER_MINUTE=20
MAX_CHATS_PER_MINUTE=10

# Autenticación (opcional)
REQUIRE_AUTH=false
ACCESS_CODE=tu-codigo-secreto-aqui
```

#### Variables de FFmpeg:

```bash
# Railway incluye FFmpeg por defecto con nixpacks.toml
# No necesitas configurar nada adicional
```

### 4. Configurar el Build

Railway debería detectar automáticamente `nixpacks.toml`. Si no:

1. Ve a Settings → Build
2. Builder: Nixpacks
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `python app_gradio_secure.py`

### 5. Deploy

1. Railway iniciará el deployment automáticamente
2. Espera 3-5 minutos
3. Verifica los logs en la pestaña "Deployments"

### 6. Obtener la URL

1. Ve a Settings → Networking
2. Click en "Generate Domain"
3. Railway te dará una URL como: `your-app.up.railway.app`

## 🔍 Verificar el Deployment

### Checklist Post-Deployment:

- [ ] La app carga correctamente
- [ ] Puedes transcribir un video corto
- [ ] La búsqueda funciona
- [ ] El chat responde
- [ ] Los rate limits funcionan (intenta exceder el límite)
- [ ] Los logs no muestran errores

### Comandos de Verificación:

```bash
# Ver logs en tiempo real
railway logs

# Ver estado del servicio
railway status

# Conectar a la shell (si necesitas debug)
railway shell
```

## 🐛 Troubleshooting

### Error: "Module not found"

**Solución:**
```bash
# Verifica que requirements.txt esté completo
railway logs | grep "ModuleNotFoundError"
```

### Error: "FFmpeg not found"

**Solución:**
- Verifica que `nixpacks.toml` incluya `ffmpeg` en nixPkgs
- Railway debería instalarlo automáticamente

### Error: "API Key not configured"

**Solución:**
1. Ve a Variables
2. Verifica que `OPENAI_API_KEY` esté configurada
3. Redeploy: `railway up`

### Error: "Port already in use"

**Solución:**
- Railway asigna el puerto automáticamente
- No necesitas configurar PORT manualmente

### App muy lenta

**Solución:**
1. Verifica el plan de Railway (Free tier tiene límites)
2. Considera upgrade a plan Pro
3. Optimiza el código (reduce llamadas a API)

## 💰 Costos

### Railway:
- **Free Tier**: $5 de crédito mensual
- **Pro Plan**: $20/mes (recomendado para producción)

### OpenAI:
- **Whisper API**: $0.006 por minuto de audio
- **GPT-4**: ~$0.03 por 1K tokens (para chat)
- **Embeddings**: $0.0001 por 1K tokens (para búsqueda)

### Estimación mensual:
```
Railway Pro: $20
OpenAI (100 videos de 10 min): ~$6
OpenAI (1000 búsquedas): ~$1
OpenAI (500 chats): ~$15

Total estimado: ~$42/mes
```

## 🔒 Mejores Prácticas de Seguridad

### 1. Rotar API Keys Regularmente

```bash
# Cada 30-90 días
1. Genera nueva key en OpenAI
2. Actualiza en Railway Variables
3. Elimina la key antigua
```

### 2. Monitorear Uso

```bash
# Revisa logs diariamente
railway logs --tail 100

# Configura alertas en Railway
Settings → Notifications
```

### 3. Limitar Acceso

```bash
# Habilita autenticación si es necesario
REQUIRE_AUTH=true
ACCESS_CODE=un-codigo-muy-seguro-123
```

### 4. Backup Regular

```bash
# Exporta transcripciones importantes
# Railway no hace backup automático de archivos
```

## 📊 Monitoreo

### Métricas Importantes:

1. **CPU Usage**: Debería estar <80%
2. **Memory**: Debería estar <512MB
3. **Network**: Monitorea bandwidth
4. **Errors**: Revisa logs diariamente

### Configurar Alertas:

1. Railway → Settings → Notifications
2. Configura alertas para:
   - Deployment failures
   - High CPU usage
   - High memory usage
   - Crashes

## 🔄 Actualizar la App

### Método 1: Push a GitHub

```bash
git add .
git commit -m "feat: nueva funcionalidad"
git push origin main
```

Railway detectará el push y redesplegará automáticamente.

### Método 2: Railway CLI

```bash
# Instalar CLI
npm install -g @railway/cli

# Login
railway login

# Deploy
railway up
```

## 🌐 Custom Domain (Opcional)

1. Railway → Settings → Networking
2. Click "Custom Domain"
3. Agrega tu dominio (ej: transcriber.tudominio.com)
4. Configura DNS según instrucciones de Railway

## 📝 Variables de Entorno Completas

```bash
# === REQUERIDAS ===
OPENAI_API_KEY=sk-proj-...
RAILWAY_ENVIRONMENT=production
PORT=7860

# === RATE LIMITS ===
MAX_TRANSCRIPTIONS_PER_HOUR=5
MAX_SEARCHES_PER_MINUTE=20
MAX_CHATS_PER_MINUTE=10

# === AUTENTICACIÓN (Opcional) ===
REQUIRE_AUTH=false
ACCESS_CODE=

# === CONFIGURACIÓN ADICIONAL ===
WHISPER_MODEL=whisper-1
EMBEDDING_MODEL=text-embedding-ada-002
CHAT_MODEL=gpt-4-turbo-preview
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TOP_K_RESULTS=3
```

## 🎯 Checklist Final

Antes de hacer público:

- [ ] ✅ Deployment exitoso
- [ ] ✅ Variables de entorno configuradas
- [ ] ✅ Rate limits funcionando
- [ ] ✅ API key protegida
- [ ] ✅ Logs sin errores
- [ ] ✅ Todas las features funcionan
- [ ] ✅ Custom domain configurado (opcional)
- [ ] ✅ Monitoreo configurado
- [ ] ✅ Backup plan establecido

## 🆘 Soporte

Si tienes problemas:

1. **Railway Docs**: https://docs.railway.app
2. **Railway Discord**: https://discord.gg/railway
3. **GitHub Issues**: https://github.com/inginddie/youtube-transcriber/issues

## 🎉 ¡Listo!

Tu app está ahora en producción con:
- ✅ Seguridad completa
- ✅ Rate limiting
- ✅ Protección de API keys
- ✅ Monitoreo
- ✅ Escalabilidad

**URL de tu app**: `https://your-app.up.railway.app`

---

**Siguiente paso**: Comparte tu app y monitorea el uso.
