# 🪟 Instalación en Windows - Guía Paso a Paso

## Paso 1: Instalar FFmpeg

### Opción A: Con Chocolatey (Recomendado)

Si tienes Chocolatey instalado:
```powershell
choco install ffmpeg
```

### Opción B: Instalación Manual

1. **Descargar FFmpeg:**
   - Ve a: https://www.gyan.dev/ffmpeg/builds/
   - Descarga: `ffmpeg-release-essentials.zip`

2. **Extraer:**
   - Extrae el archivo ZIP a `C:\ffmpeg`

3. **Agregar al PATH:**
   - Presiona `Win + X` → "Sistema"
   - Click en "Configuración avanzada del sistema"
   - Click en "Variables de entorno"
   - En "Variables del sistema", busca "Path"
   - Click "Editar" → "Nuevo"
   - Agrega: `C:\ffmpeg\bin`
   - Click "Aceptar" en todas las ventanas

4. **Verificar:**
   - Abre una **nueva** ventana de PowerShell
   - Ejecuta: `ffmpeg -version`

### Opción C: Con winget (Windows 10/11)

```powershell
winget install ffmpeg
```

## Paso 2: Verificar Python

```powershell
python --version
# Debe mostrar: Python 3.8 o superior
```

## Paso 3: Obtener API Key de OpenAI

1. Ve a: https://platform.openai.com/api-keys
2. Inicia sesión o crea una cuenta
3. Click en "Create new secret key"
4. Copia la clave (empieza con `sk-proj-...`)
5. **¡Guárdala! No podrás verla de nuevo**

## ¡Listo para continuar!

Una vez completados estos pasos, continúa con la configuración del proyecto.
