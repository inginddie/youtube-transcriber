@echo off
REM Script de inicio rápido para YouTube Transcriber Pro

echo ========================================
echo YouTube Transcriber Pro
echo ========================================
echo.

REM Agregar FFmpeg al PATH
set "FFMPEG_PATH=C:\Users\Diego\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0-full_build\bin"
set "PATH=%PATH%;%FFMPEG_PATH%"

REM Activar entorno virtual
call venv\Scripts\activate.bat

REM Mostrar menú
echo Selecciona una opcion:
echo.
echo 1. Iniciar Interfaz Web (Gradio)
echo 2. Transcribir un video (CLI)
echo 3. Ejecutar tests
echo 4. Verificar sistema
echo 5. Salir
echo.

set /p choice="Opcion (1-5): "

if "%choice%"=="1" goto web
if "%choice%"=="2" goto cli
if "%choice%"=="3" goto tests
if "%choice%"=="4" goto verify
if "%choice%"=="5" goto end

:web
echo.
echo Iniciando interfaz web...
echo Abre tu navegador en: http://localhost:7860
echo Presiona Ctrl+C para detener
echo.
python app_gradio.py
goto end

:cli
echo.
set /p url="Ingresa la URL del video de YouTube: "
echo.
echo Transcribiendo...
python main.py %url%
echo.
pause
goto end

:tests
echo.
echo Ejecutando tests...
pytest -v
echo.
pause
goto end

:verify
echo.
python test_setup.py
echo.
pause
goto end

:end
echo.
echo Gracias por usar YouTube Transcriber Pro!
