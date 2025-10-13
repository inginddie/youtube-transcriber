@echo off
echo ========================================
echo YouTube Transcriber Pro - Setup Rapido
echo ========================================
echo.

REM Verificar Python
echo [1/6] Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python no encontrado. Instala Python 3.8+ desde python.org
    pause
    exit /b 1
)
echo [OK] Python encontrado
echo.

REM Verificar FFmpeg
echo [2/6] Verificando FFmpeg...
ffmpeg -version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ADVERTENCIA] FFmpeg no encontrado
    echo.
    echo Por favor instala FFmpeg:
    echo   Opcion 1: choco install ffmpeg
    echo   Opcion 2: winget install ffmpeg
    echo   Opcion 3: Descarga manual de https://www.gyan.dev/ffmpeg/builds/
    echo.
    echo Presiona cualquier tecla para continuar de todos modos...
    pause >nul
) else (
    echo [OK] FFmpeg encontrado
)
echo.

REM Crear entorno virtual
echo [3/6] Creando entorno virtual...
if exist venv (
    echo [INFO] Entorno virtual ya existe, saltando...
) else (
    python -m venv venv
    echo [OK] Entorno virtual creado
)
echo.

REM Activar entorno virtual
echo [4/6] Activando entorno virtual...
call venv\Scripts\activate.bat
echo [OK] Entorno virtual activado
echo.

REM Instalar dependencias
echo [5/6] Instalando dependencias (esto puede tardar unos minutos)...
python -m pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo [ERROR] Fallo al instalar dependencias
    pause
    exit /b 1
)
echo [OK] Dependencias instaladas
echo.

REM Crear archivo .env
echo [6/6] Configurando archivo .env...
if exist .env (
    echo [INFO] Archivo .env ya existe
) else (
    copy .env.example .env >nul
    echo [OK] Archivo .env creado
)
echo.

REM Crear directorios
echo Creando directorios necesarios...
python -c "from config import create_directories; create_directories()" 2>nul
echo [OK] Directorios creados
echo.

echo ========================================
echo SETUP COMPLETADO!
echo ========================================
echo.
echo SIGUIENTE PASO: Configurar tu API Key
echo.
echo 1. Abre el archivo .env con un editor de texto
echo 2. Reemplaza "sk-proj-your-api-key-here" con tu API key real de OpenAI
echo 3. Guarda el archivo
echo.
echo Para obtener tu API key:
echo   - Ve a: https://platform.openai.com/api-keys
echo   - Crea una nueva clave
echo   - Copiala y pegala en el archivo .env
echo.
echo COMANDOS PARA USAR:
echo   - Interfaz Web:  python app_gradio.py
echo   - Linea de comandos: python main.py https://youtu.be/VIDEO_ID
echo.
echo Presiona cualquier tecla para abrir el archivo .env...
pause >nul
notepad .env
