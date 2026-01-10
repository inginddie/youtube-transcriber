# 🚀 Railway Deployment Guide - YouTube Transcriber Pro

Esta guía te ayudará a desplegar tu aplicación con el sistema de seguridad integrado en Railway.

---

## 📋 Pre-requisitos

- [ ] Cuenta de Railway (https://railway.app)
- [ ] Repositorio GitHub conectado a Railway
- [ ] OpenAI API Key
- [ ] Código de acceso elegido para producción

---

## 🔄 Paso 1: Push del Código

El código ya está pusheado al branch `claude/code-review-analysis-pUkeS`. Ahora necesitas:

### Opción A: Merge a Main (Recomendado)

```bash
# Cambia a main
git checkout main

# Merge del branch de desarrollo
git merge claude/code-review-analysis-pUkeS

# Push a main
git push origin main
```

### Opción B: Deploy desde Branch Directamente

Railway puede desplegar desde cualquier branch. Configura esto en el dashboard.

---

## ⚙️ Paso 2: Configurar Variables de Entorno en Railway

### 2.1 Accede a tu proyecto en Railway

1. Ve a https://railway.app/dashboard
2. Selecciona tu proyecto `youtube-transcriber`
3. Click en tu servicio
4. Click en la pestaña **"Variables"**

### 2.2 Agrega las Variables de Entorno

#### Variables Requeridas ✅

```bash
# OpenAI API Key (CRÍTICO)
OPENAI_API_KEY=sk-proj-tu-api-key-real-aqui

# Autenticación de Producción
REQUIRE_AUTH=true
ACCESS_CODE=tu_codigo_super_secreto_minimo_20_caracteres

# Rate Limiting para Producción (conservador)
MAX_TRANSCRIPTIONS_PER_HOUR=3
MAX_SEARCHES_PER_MINUTE=10
MAX_CHATS_PER_MINUTE=5
```

#### Variables Opcionales (con valores por defecto)

```bash
# Modelos de OpenAI (opcional, usa defaults si no se especifica)
WHISPER_MODEL=whisper-1
EMBEDDING_MODEL=text-embedding-ada-002
CHAT_MODEL=gpt-4-turbo-preview

# Puerto (Railway lo asigna automáticamente)
# No necesitas configurar PORT, Railway lo hace por ti
```

### 2.3 Generar un Código de Acceso Seguro

Usa este comando para generar un código fuerte:

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

Ejemplo de output:
```
Xk9_mP2nQ7-wL4zR8vC3hT6yB1dF5sA0eG9uH2jK7lM3
```

**Copia este código y úsalo como tu ACCESS_CODE**

---

## 🎯 Paso 3: Configuración Paso a Paso en Railway Dashboard

### 3.1 Agregar Variables una por una:

1. Click en **"+ New Variable"**
2. **Variable 1:**
   - Name: `OPENAI_API_KEY`
   - Value: `sk-proj-...` (tu API key real)
   - Click **"Add"**

3. **Variable 2:**
   - Name: `REQUIRE_AUTH`
   - Value: `true`
   - Click **"Add"**

4. **Variable 3:**
   - Name: `ACCESS_CODE`
   - Value: (el código generado arriba)
   - Click **"Add"**

5. **Variable 4:**
   - Name: `MAX_TRANSCRIPTIONS_PER_HOUR`
   - Value: `3`
   - Click **"Add"**

6. **Variable 5:**
   - Name: `MAX_SEARCHES_PER_MINUTE`
   - Value: `10`
   - Click **"Add"**

7. **Variable 6:**
   - Name: `MAX_CHATS_PER_MINUTE`
   - Value: `5`
   - Click **"Add"**

### 3.2 Verificar Variables

Deberías ver algo como:

```
OPENAI_API_KEY         sk-proj-*********************
REQUIRE_AUTH           true
ACCESS_CODE            Xk9_*********************
MAX_TRANSCRIPTIONS...  3
MAX_SEARCHES_PER...    10
MAX_CHATS_PER_MINUTE   5
```

---

## 🚀 Paso 4: Desplegar

### 4.1 Trigger Deployment

Después de agregar las variables:

1. Railway detectará los cambios automáticamente
2. **O** haz un nuevo commit:
   ```bash
   git commit --allow-empty -m "chore: trigger Railway deployment"
   git push origin main
   ```

### 4.2 Monitorear Deployment

1. En Railway dashboard, ve a la pestaña **"Deployments"**
2. Verás el build en progreso
3. Espera a que muestre **"Success"** (toma ~3-5 minutos)

### 4.3 Logs de Deployment

Para ver el progreso:
1. Click en el deployment activo
2. Ve a **"Build Logs"** para ver la construcción del Docker
3. Ve a **"Deploy Logs"** para ver el inicio de la app

Deberías ver:
```
🔧 Setting up directories...
🚀 Launching Gradio interface...
   ✓ Using port: 7860
   ✓ Environment: production
Running on local URL:  http://0.0.0.0:7860
```

---

## 🔗 Paso 5: Obtener URL de Producción

1. En Railway dashboard, busca el dominio generado
2. Formato: `https://tu-app-production.up.railway.app`
3. **O** configura un dominio personalizado en **Settings > Domains**

---

## 🧪 Paso 6: Probar el Deployment

### 6.1 Acceder a la Aplicación

1. Abre la URL de Railway en tu navegador
2. Deberías ver la aplicación con 6 pestañas
3. La pestaña **"🔐 Login"** debería ser visible

### 6.2 Probar Autenticación

1. Ve a la pestaña **"🔐 Login"**
2. Ingresa el ACCESS_CODE que configuraste
3. Click **"🔓 Login"**
4. Deberías ver:
   ```
   ✅ Login Successful!

   Welcome! You now have access to all features.

   Session ID: `Xk9_mP2nQ7-wL4zR...`

   **You can now use all other tabs.**
   ```

### 6.3 Probar Rate Limiting

**Test de Transcripción:**
1. Ve a **"📝 Transcribe Videos"**
2. Intenta transcribir 4 videos seguidos (límite es 3/hora)
3. El cuarto debería mostrar:
   ```
   ⚠️ Rate Limit Exceeded

   Rate limit exceeded for transcription.
   Please wait 3542 seconds.
   Remaining requests: 0
   ```

**Test de Chat:**
1. Indexa algunas transcripciones primero
2. Ve a **"💬 Chat"**
3. Envía 6 mensajes rápidamente (límite es 5/minuto)
4. El sexto debería mostrar error de rate limit

### 6.4 Probar sin Login

1. Abre la app en una ventana privada (incognito)
2. Intenta usar **"📝 Transcribe Videos"** sin hacer login
3. Deberías ver:
   ```
   🔒 Authentication Required

   Your session has expired or is invalid. Please log in again.
   ```

---

## ✅ Checklist de Verificación

Marca cada item cuando lo completes:

- [ ] Variables de entorno configuradas en Railway
- [ ] `REQUIRE_AUTH=true` está activo
- [ ] `ACCESS_CODE` es fuerte (20+ caracteres)
- [ ] Rate limits configurados para producción
- [ ] Deployment exitoso en Railway
- [ ] URL de producción accesible
- [ ] Login funciona correctamente
- [ ] Rate limiting funciona en transcripción
- [ ] Rate limiting funciona en chat/search
- [ ] Autenticación bloquea acceso sin login
- [ ] Sesión expira después de 1 hora (opcional, test largo)

---

## 🔧 Troubleshooting

### Problema: "OPENAI_API_KEY not found"

**Solución:**
1. Verifica que agregaste `OPENAI_API_KEY` en Railway Variables
2. El valor debe empezar con `sk-proj-` o `sk-`
3. No debe tener espacios al inicio/final
4. Redeploy después de agregar la variable

### Problema: Login no funciona

**Solución:**
1. Verifica que `REQUIRE_AUTH=true` (no `True` ni `TRUE`)
2. Verifica que `ACCESS_CODE` está configurado
3. Intenta el código exactamente como lo copiaste (case-sensitive)
4. Revisa logs en Railway para ver errores

### Problema: Rate limiting no funciona

**Solución:**
1. Las variables deben ser números: `3`, `10`, `5` (no `"3"`)
2. Redeploy después de cambiar variables
3. Espera 1 minuto para que tome efecto

### Problema: Deployment falla

**Solución 1 - Build Error:**
```bash
# Verifica que requirements.txt existe
ls requirements.txt

# Verifica sintaxis de Python localmente
python -m py_compile app_gradio.py
```

**Solución 2 - Runtime Error:**
1. Ve a Deploy Logs en Railway
2. Busca el error específico
3. Comúnmente: falta variable de entorno

### Problema: App corre pero no responde

**Solución:**
1. Verifica que el puerto es correcto (Railway asigna automáticamente)
2. En `app_gradio.py` tenemos:
   ```python
   port = int(os.getenv("PORT", GRADIO_PORT))
   ```
   Esto debería funcionar automáticamente

---

## 📊 Monitoreo de Producción

### Ver Logs en Tiempo Real

1. Railway Dashboard > Tu Servicio > **"Deployments"**
2. Click en deployment activo
3. **"Deploy Logs"** tab
4. Verás logs en tiempo real:
   ```
   🔧 Setting up directories...
   🚀 Launching Gradio interface...
   ✅ Security manager imported successfully
   ```

### Métricas

Railway dashboard muestra:
- **CPU Usage**: Debería estar <50% normalmente
- **Memory**: ~500MB-1GB para esta app
- **Network**: Picos durante transcripciones

---

## 🔐 Seguridad Post-Deployment

### Mejores Prácticas

1. **Nunca compartas el ACCESS_CODE públicamente**
   - No lo pongas en issues de GitHub
   - No lo compartas en Discord/Slack públicos
   - Usa 1Password, Bitwarden, etc. para compartir de forma segura

2. **Rotación de Códigos**
   - Cambia el ACCESS_CODE cada 3-6 meses
   - Genera uno nuevo: `python3 -c "import secrets; print(secrets.token_urlsafe(32))"`
   - Actualiza en Railway Variables
   - Notifica a usuarios autorizados

3. **Monitoreo de Uso**
   - Revisa logs periódicamente para actividad sospechosa
   - Busca patrones de múltiples intentos fallidos
   - Considera agregar alertas (futuro)

4. **Backups**
   - Railway hace backups automáticos
   - Considera exportar transcripciones importantes regularmente
   - Git es tu backup para código

---

## 📈 Escalamiento

### Si necesitas más capacidad:

1. **Aumentar Rate Limits**
   ```bash
   MAX_TRANSCRIPTIONS_PER_HOUR=10  # Era 3
   MAX_SEARCHES_PER_MINUTE=30      # Era 10
   MAX_CHATS_PER_MINUTE=15         # Era 5
   ```

2. **Upgrade Railway Plan**
   - Hobby: $5/mes (suficiente para uso personal)
   - Pro: $20/mes (para equipos pequeños)

3. **Monitorear Costos de OpenAI**
   - Transcripción: ~$0.006/minuto de audio
   - Embedding: ~$0.0001/1K tokens
   - Chat (GPT-4): ~$0.03/1K tokens

---

## 🎉 ¡Deployment Exitoso!

Si llegaste aquí, tu aplicación está:
- ✅ Desplegada en Railway
- ✅ Protegida con autenticación
- ✅ Rate limiting activo
- ✅ Lista para uso en producción

### Próximos Pasos

1. **Comparte la URL** con usuarios autorizados
2. **Envía el ACCESS_CODE** de forma segura (Signal, 1Password, etc.)
3. **Monitorea el uso** en las primeras semanas
4. **Ajusta rate limits** según necesidad real
5. **Considera agregar**:
   - Dominio personalizado
   - Múltiples usuarios con DB
   - Dashboard de analytics
   - Webhooks para notificaciones

---

## 📞 Soporte

- **Issues**: https://github.com/inginddie/youtube-transcriber/issues
- **Railway Docs**: https://docs.railway.app
- **Railway Discord**: https://discord.gg/railway

---

**Última actualización**: 2026-01-09
**Versión**: 1.0.0 (Security Integration)
