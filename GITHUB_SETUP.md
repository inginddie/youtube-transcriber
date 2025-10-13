# 🚀 GitHub Setup Guide

Guía paso a paso para subir este proyecto a GitHub.

## 📋 Pre-requisitos

- Git instalado en tu sistema
- Cuenta de GitHub
- Repositorio creado en GitHub (vacío, sin README)

## 🔧 Pasos para Subir el Proyecto

### 1. Inicializar Git (si no está inicializado)

```bash
cd youtube-transcriber
git init
```

### 2. Configurar Git (primera vez)

```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu-email@ejemplo.com"
```

### 3. Agregar Archivos

```bash
# Agregar todos los archivos (respetando .gitignore)
git add .

# Verificar qué archivos se agregarán
git status
```

### 4. Hacer el Primer Commit

```bash
git commit -m "🎉 Initial commit: YouTube Transcriber Pro with RAG and Management features"
```

### 5. Conectar con GitHub

Reemplaza `TU_USUARIO` y `TU_REPO` con tus datos:

```bash
git remote add origin https://github.com/TU_USUARIO/TU_REPO.git
```

### 6. Subir a GitHub

```bash
# Primera subida
git branch -M main
git push -u origin main
```

## 🔐 Autenticación

### Opción 1: HTTPS con Token (Recomendado)

1. Ve a GitHub → Settings → Developer settings → Personal access tokens
2. Genera un nuevo token con permisos de `repo`
3. Usa el token como contraseña cuando Git te lo pida

### Opción 2: SSH

```bash
# Generar clave SSH
ssh-keygen -t ed25519 -C "tu-email@ejemplo.com"

# Agregar a GitHub
# Copia el contenido de ~/.ssh/id_ed25519.pub
# Pégalo en GitHub → Settings → SSH and GPG keys

# Cambiar remote a SSH
git remote set-url origin git@github.com:TU_USUARIO/TU_REPO.git
```

## 📝 Comandos Útiles Post-Setup

### Actualizar el Repositorio

```bash
# Ver cambios
git status

# Agregar cambios
git add .

# Commit
git commit -m "feat: descripción del cambio"

# Subir
git push
```

### Crear Ramas

```bash
# Crear y cambiar a nueva rama
git checkout -b feature/nueva-funcionalidad

# Subir rama
git push -u origin feature/nueva-funcionalidad
```

### Sincronizar con GitHub

```bash
# Descargar cambios
git pull

# Ver ramas remotas
git branch -r

# Ver historial
git log --oneline --graph
```

## 🏷️ Crear Releases

### Opción 1: Desde GitHub UI

1. Ve a tu repositorio en GitHub
2. Click en "Releases" → "Create a new release"
3. Crea un tag (ej: `v1.0.0`)
4. Agrega título y descripción
5. Publica

### Opción 2: Desde CLI

```bash
# Crear tag
git tag -a v1.0.0 -m "Release version 1.0.0"

# Subir tag
git push origin v1.0.0

# O subir todos los tags
git push --tags
```

## 📊 Configurar GitHub Pages (Opcional)

Si quieres documentación en GitHub Pages:

1. Ve a Settings → Pages
2. Source: Deploy from a branch
3. Branch: main → /docs
4. Save

## 🔒 Configurar Secrets

Para CI/CD o deployment, agrega secrets:

1. Ve a Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Agrega:
   - `OPENAI_API_KEY` (si usas GitHub Actions)
   - Otros secrets necesarios

## ✅ Verificación Post-Setup

Verifica que todo esté correcto:

- [ ] Repositorio visible en GitHub
- [ ] README.md se muestra correctamente
- [ ] .gitignore funciona (no se subieron archivos sensibles)
- [ ] Issues y Pull Requests tienen templates
- [ ] GitHub Actions configurado (opcional)
- [ ] Descripción y topics agregados al repo

## 🎨 Personalizar el Repositorio

En GitHub, agrega:

1. **Descripción**: "YouTube video transcriber with AI-powered search and chat"
2. **Topics**: 
   - `youtube`
   - `transcription`
   - `whisper`
   - `openai`
   - `rag`
   - `gradio`
   - `python`
   - `ai`
3. **Website**: URL de demo (si tienes)
4. **Social Preview**: Imagen del proyecto

## 🚨 Problemas Comunes

### Error: "remote origin already exists"

```bash
git remote remove origin
git remote add origin https://github.com/TU_USUARIO/TU_REPO.git
```

### Error: "failed to push some refs"

```bash
# Si el repo remoto tiene commits que no tienes localmente
git pull origin main --rebase
git push
```

### Archivos Grandes

Si tienes archivos grandes (>100MB):

```bash
# Usar Git LFS
git lfs install
git lfs track "*.mp3"
git lfs track "*.wav"
git add .gitattributes
git commit -m "chore: add Git LFS"
```

### Eliminar Archivos del Historial

Si subiste algo por error:

```bash
# Eliminar archivo del historial
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch ruta/al/archivo" \
  --prune-empty --tag-name-filter cat -- --all

# Forzar push
git push origin --force --all
```

## 📚 Recursos Adicionales

- [GitHub Docs](https://docs.github.com)
- [Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)

## 🎉 ¡Listo!

Tu proyecto está ahora en GitHub. Comparte el link:

```
https://github.com/TU_USUARIO/TU_REPO
```

---

**Siguiente paso**: Actualiza el README.md con el link correcto del repositorio.
