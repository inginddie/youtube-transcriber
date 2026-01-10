# 🚀 Railway Quick Start - Deploy in 5 Minutes

Esta guía te llevará desde cero hasta tener la aplicación corriendo en Railway con seguridad completa.

---

## 📋 Pre-requisitos

- [ ] Cuenta de Railway (gratis en https://railway.app)
- [ ] OpenAI API Key
- [ ] Repositorio GitHub conectado a Railway

---

## 🎯 Paso 1: Preparar el Código (✅ YA COMPLETADO)

El código ya está listo en el branch: `claude/code-review-analysis-pUkeS`

**Commits incluidos:**
- ✅ Sistema de seguridad integrado
- ✅ Frontend con UI avanzada
- ✅ Documentación completa
- ✅ Scripts de deployment

---

## 🔧 Paso 2: Crear Proyecto en Railway

### 2.1 Crear Nuevo Proyecto

1. Ve a: https://railway.app/dashboard
2. Click en **"New Project"**
3. Selecciona **"Deploy from GitHub repo"**
4. Busca: `inginddie/youtube-transcriber`
5. Click en **"Deploy Now"**

### 2.2 Configurar Branch de Deploy

1. En el proyecto, click en tu servicio
2. Ve a **Settings** → **Source**
3. En **Branch**, selecciona: `claude/code-review-analysis-pUkeS`
4. Click **"Save"**

Railway detectará automáticamente el `Dockerfile` y lo usará para el build.

---

## ⚙️ Paso 3: Configurar Variables de Entorno

### 3.1 Acceder a Variables

1. En tu servicio de Railway
2. Click en la pestaña **"Variables"**
3. Click **"+ New Variable"**

### 3.2 Agregar Variables (Copia y Pega)

**Variable 1 - OpenAI API Key:**
```
Name:  OPENAI_API_KEY
Value: sk-proj-TU_API_KEY_REAL_AQUI
```

**Variable 2 - Activar Autenticación:**
```
Name:  REQUIRE_AUTH
Value: true
```

**Variable 3 - Código de Acceso:**
```
Name:  ACCESS_CODE
Value: IaAR1iW6PQIiaK8S4wn0ipBef7ucg_UX8VSrx2nVAKE
```
⚠️ **GUARDA ESTE CÓDIGO** - lo necesitarás para hacer login!

**Variable 4 - Límite de Transcripciones:**
```
Name:  MAX_TRANSCRIPTIONS_PER_HOUR
Value: 3
```

**Variable 5 - Límite de Búsquedas:**
```
Name:  MAX_SEARCHES_PER_MINUTE
Value: 10
```

**Variable 6 - Límite de Chat:**
```
Name:  MAX_CHATS_PER_MINUTE
Value: 5
```

### 3.3 Verificar Variables

Deberías ver 6 variables configuradas:

```
✅ OPENAI_API_KEY         sk-proj-*********************
✅ REQUIRE_AUTH           true
✅ ACCESS_CODE            IaAR1i*********************
✅ MAX_TRANSCRIPTIONS...  3
✅ MAX_SEARCHES_PER...    10
✅ MAX_CHATS_PER_MINUTE   5
```

---

## 🚀 Paso 4: Desplegar

### 4.1 Trigger Deployment

Railway desplegará automáticamente después de agregar las variables.

**O manualmente:**
1. Ve a **"Deployments"** tab
2. Click **"Deploy"**

### 4.2 Monitorear Build

1. Click en el deployment activo
2. Ve a **"Build Logs"**

Deberías ver:
```
Building...
Step 1/8 : FROM python:3.11-slim
Step 2/8 : RUN apt-get update && apt-get install -y ffmpeg
...
Step 8/8 : CMD ["python", "app_gradio.py"]
Successfully built
```

### 4.3 Verificar Deploy Logs

1. Ve a **"Deploy Logs"**

Deberías ver:
```
🔧 Setting up directories...
   ✓ Created: transcripts/
   ✓ Created: vector_db/
   ✓ Created: temp_audio/
🚀 Launching Gradio interface...
   ✓ Using port: 7860
   ✓ Environment: production
✅ Security manager imported successfully
   - Auth required: True
   - Access code set: Yes
Running on local URL:  http://0.0.0.0:7860
```

✅ **¡Deployment exitoso!**

---

## 🌐 Paso 5: Obtener URL y Probar

### 5.1 Obtener URL de Producción

1. En Railway dashboard, ve a **"Settings"**
2. Sección **"Domains"**
3. Click **"Generate Domain"**

Railway generará una URL como:
```
https://youtube-transcriber-production-XXXX.up.railway.app
```

**Copia esta URL** - es tu aplicación en producción!

### 5.2 Probar la Aplicación

**Test 1: Acceder a la App**
1. Abre la URL en tu navegador
2. Deberías ver: **🎥 YouTube Transcriber Pro**
3. Verás 6 pestañas en la parte superior

**Test 2: Login**
1. Ve a la pestaña **"🔐 Login"**
2. En **"Access Code"**, ingresa:
   ```
   IaAR1iW6PQIiaK8S4wn0ipBef7ucg_UX8VSrx2nVAKE
   ```
3. Click **"🔓 Login"**
4. Deberías ver:
   ```
   ✅ Login Successful!

   Welcome! You now have access to all features.

   Session ID: `IaAR1iW6PQIiaK8...`

   **You can now use all other tabs.**
   ```

**Test 3: Verificar Estado de Sesión**
1. Mira la barra superior
2. Deberías ver:
   ```
   🟢 Status: Authenticated ✅
   Session ID: `IaAR1iW6PQIiaK8...`
   Time Remaining: 59 minutes
   Rate Limits: 🎬 3/3 | 🔍 10/10 | 💬 5/5
   ```

**Test 4: Probar Transcripción**
1. Ve a **"📝 Transcribe Videos"**
2. Ingresa una URL de YouTube
3. Click **"🚀 Transcribe Videos"**
4. Debería empezar a procesar

**Test 5: Verificar Rate Limiting**
1. Intenta transcribir 4 videos seguidos (límite es 3/hora)
2. El cuarto debería mostrar:
   ```
   ⚠️ Rate Limit Exceeded

   Rate limit exceeded for transcription.
   Please wait XXX seconds.
   ```

**Test 6: Dashboard de Seguridad**
1. Ve a **"🔒 Security"** tab
2. Verás estadísticas del sistema:
   - Active Sessions: 1
   - Rate Limits configurados
   - Tu información de sesión

---

## ✅ Checklist de Deployment

Marca cada item:

**Configuración:**
- [ ] Proyecto creado en Railway
- [ ] Branch `claude/code-review-analysis-pUkeS` seleccionado
- [ ] 6 variables de entorno configuradas
- [ ] OPENAI_API_KEY con valor real
- [ ] ACCESS_CODE guardado de forma segura

**Deployment:**
- [ ] Build completado sin errores
- [ ] Deploy logs muestran app corriendo
- [ ] URL de producción generada
- [ ] URL accesible en navegador

**Testing:**
- [ ] Login funciona con ACCESS_CODE
- [ ] Session status bar muestra "Authenticated"
- [ ] Transcripción funciona correctamente
- [ ] Rate limiting activo (test con 4 videos)
- [ ] Security dashboard accesible
- [ ] Logout funciona correctamente

---

## 🎉 ¡Felicidades!

Tu aplicación está desplegada en producción con:
- ✅ Autenticación segura
- ✅ Rate limiting activo
- ✅ Session management
- ✅ Dashboard de seguridad
- ✅ UI completa y profesional

---

## 📱 Compartir con Usuarios

**Información para enviar:**

```
🎥 YouTube Transcriber Pro

URL: https://tu-app.up.railway.app
Código de Acceso: IaAR1iW6PQIiaK8S4wn0ipBef7ucg_UX8VSrx2nVAKE

Instrucciones:
1. Abre la URL
2. Ve a la pestaña "🔐 Login"
3. Ingresa el código de acceso
4. Click "Login"
5. ¡Listo! Puedes transcribir hasta 3 videos por hora

Soporte: [tu email o GitHub]
```

---

## 🔧 Troubleshooting Rápido

### Problema: Build falla

**Solución:**
1. Ve a Build Logs
2. Busca el error específico
3. Usualmente falta alguna variable de entorno

### Problema: App no inicia

**Solución:**
1. Ve a Deploy Logs
2. Verifica que `OPENAI_API_KEY` esté configurada
3. Redeploy manualmente

### Problema: Login no funciona

**Solución:**
1. Verifica que `REQUIRE_AUTH=true` (no `True` ni `TRUE`)
2. Verifica que `ACCESS_CODE` esté configurado
3. Copia el código exactamente (case-sensitive)

### Problema: Rate limiting no funciona

**Solución:**
1. Las variables deben ser números: `3`, `10`, `5`
2. NO usar comillas: `"3"` ❌, `3` ✅
3. Redeploy después de cambiar variables

---

## 📊 Monitoreo

**Métricas en Railway Dashboard:**
- **CPU**: < 50% es normal
- **Memory**: ~500MB-1GB típico
- **Network**: Picos durante transcripciones

**Logs:**
- Railway → Deployments → Deploy Logs
- Actualización en tiempo real

---

## 🔐 Seguridad Post-Deployment

### Mejores Prácticas

1. **Rota el ACCESS_CODE cada 3-6 meses**
   ```bash
   python3 -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

2. **Monitorea logs periódicamente**
   - Busca intentos de login fallidos
   - Revisa patrones sospechosos

3. **Ajusta rate limits según uso**
   - Empieza conservador
   - Aumenta gradualmente según necesidad

4. **Nunca compartas el ACCESS_CODE públicamente**
   - Usa 1Password, Bitwarden, Signal
   - NO en GitHub issues, Discord público, etc.

---

## 📈 Próximos Pasos

1. **Dominio Personalizado** (Opcional)
   - Railway Settings → Domains
   - Agrega tu dominio custom

2. **Backups**
   - Exporta transcripciones importantes
   - Railway hace backups automáticos del código

3. **Escalamiento**
   - Upgrade Railway plan si necesitas más recursos
   - Pro: $20/mes para equipos

4. **Agregar Features**
   - API REST con FastAPI
   - Frontend Next.js
   - Múltiples usuarios con DB
   - Analytics dashboard

---

**¿Necesitas ayuda?**
- 📖 Guía completa: `RAILWAY_DEPLOYMENT_GUIDE.md`
- 🔒 Seguridad: `docs/SECURITY_SETUP.md`
- 🛠️ Helper script: `./deploy_helper.sh`

---

**Deployment completado:** $(date)
**Version:** 1.0.0 (Security Integration)
