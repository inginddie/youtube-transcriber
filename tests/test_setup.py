"""
Script de verificación rápida del setup
"""

import sys

print("=" * 60)
print("🔍 VERIFICACIÓN DEL SISTEMA")
print("=" * 60)
print()

# Test 1: Python version
print("[1/7] Verificando Python...")
print(f"✅ Python {sys.version.split()[0]}")
print()

# Test 2: Imports básicos
print("[2/7] Verificando imports básicos...")
try:
    import gradio
    import openai
    import yt_dlp
    from dotenv import load_dotenv

    print("✅ Todos los módulos importados correctamente")
except ImportError as e:
    print(f"❌ Error importando módulos: {e}")
    sys.exit(1)
print()

# Test 3: Configuración
print("[3/7] Verificando configuración...")
try:
    from config import OPENAI_API_KEY, TEMP_AUDIO_DIR, TRANSCRIPTS_DIR

    print("✅ Configuración cargada")
except Exception as e:
    print(f"❌ Error en configuración: {e}")
    sys.exit(1)
print()

# Test 4: API Key
print("[4/7] Verificando API Key...")
if OPENAI_API_KEY and not OPENAI_API_KEY.startswith("your-"):
    print(f"✅ API Key configurada: {OPENAI_API_KEY[:10]}...")
else:
    print("⚠️  API Key NO configurada")
    print("   Por favor edita el archivo .env con tu API key real")
    print("   Obtén una en: https://platform.openai.com/api-keys")
print()

# Test 5: Directorios
print("[5/7] Verificando directorios...")
if TRANSCRIPTS_DIR.exists() and TEMP_AUDIO_DIR.exists():
    print("✅ Directorios creados")
else:
    print("⚠️  Creando directorios...")
    from config import create_directories

    create_directories()
    print("✅ Directorios creados")
print()

# Test 6: Utilidades
print("[6/7] Verificando utilidades...")
try:
    from src.utils import extract_video_id, validate_url

    test_url = "https://youtu.be/dQw4w9WgXcQ"
    video_id = extract_video_id(test_url)
    is_valid = validate_url(test_url)

    if video_id == "dQw4w9WgXcQ" and is_valid:
        print("✅ Funciones de utilidad funcionando")
    else:
        print("❌ Error en funciones de utilidad")
except Exception as e:
    print(f"❌ Error: {e}")
print()

# Test 7: FFmpeg
print("[7/7] Verificando FFmpeg...")
import subprocess

try:
    result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True, timeout=5)
    if result.returncode == 0:
        version_line = result.stdout.split("\n")[0]
        print(f"✅ {version_line}")
    else:
        print("⚠️  FFmpeg instalado pero con problemas")
except FileNotFoundError:
    print("❌ FFmpeg NO encontrado")
    print("   Instala FFmpeg: winget install ffmpeg")
    print("   Luego reinicia PowerShell")
except Exception as e:
    print(f"⚠️  Error verificando FFmpeg: {e}")
print()

# Resumen
print("=" * 60)
print("📊 RESUMEN")
print("=" * 60)
print()

if OPENAI_API_KEY and not OPENAI_API_KEY.startswith("your-"):
    print("✅ Sistema listo para usar!")
    print()
    print("Comandos para empezar:")
    print("  - Interfaz Web:  python app_gradio.py")
    print("  - CLI:           python main.py https://youtu.be/VIDEO_ID")
else:
    print("⚠️  Casi listo! Falta configurar la API Key")
    print()
    print("Pasos finales:")
    print("  1. Obtén tu API key en: https://platform.openai.com/api-keys")
    print("  2. Edita el archivo .env")
    print("  3. Reemplaza el placeholder con tu clave real")
    print("  4. Ejecuta este script de nuevo: python test_setup.py")

print()
print("=" * 60)
