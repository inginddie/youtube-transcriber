"""
Script para lanzar la interfaz web de Gradio
"""
import sys

print("=" * 60)
print("🎥 YouTube Transcriber Pro - Interfaz Web")
print("=" * 60)
print()

# Verificar configuración
print("🔧 Verificando configuración...")

try:
    from config import OPENAI_API_KEY, create_directories
    
    if not OPENAI_API_KEY or OPENAI_API_KEY.startswith("your-"):
        print("❌ Error: API Key no configurada")
        print()
        print("Por favor edita el archivo .env con tu API key de OpenAI")
        print("Obtén una en: https://platform.openai.com/api-keys")
        sys.exit(1)
    
    print(f"✅ API Key configurada: {OPENAI_API_KEY[:15]}...")
    
except Exception as e:
    print(f"❌ Error en configuración: {e}")
    sys.exit(1)

# Verificar FFmpeg
print("🔧 Verificando FFmpeg...")
try:
    from src.transcriber import YouTubeTranscriber
    transcriber = YouTubeTranscriber()
    ffmpeg_location = transcriber._find_ffmpeg()
    
    if ffmpeg_location:
        print(f"✅ FFmpeg encontrado: {ffmpeg_location}")
    else:
        print("⚠️  FFmpeg no encontrado en PATH")
        print("   El sistema intentará encontrarlo automáticamente")
        
except Exception as e:
    print(f"⚠️  Advertencia: {e}")

# Crear directorios
print("🔧 Creando directorios...")
create_directories()
print("✅ Directorios listos")

print()
print("=" * 60)
print("🚀 Iniciando servidor Gradio...")
print("=" * 60)
print()
print("📍 La interfaz estará disponible en:")
print("   👉 http://localhost:7860")
print()
print("💡 Consejos:")
print("   - Usa videos cortos para probar primero")
print("   - El costo es ~$0.006 por minuto de audio")
print("   - Los archivos se guardan en la carpeta 'transcripts/'")
print()
print("⏹️  Presiona Ctrl+C para detener el servidor")
print()
print("=" * 60)
print()

# Importar y lanzar Gradio
try:
    from app_gradio import main
    main()
except KeyboardInterrupt:
    print()
    print("=" * 60)
    print("👋 Servidor detenido. ¡Hasta luego!")
    print("=" * 60)
except Exception as e:
    print()
    print("=" * 60)
    print(f"❌ Error al iniciar: {e}")
    print("=" * 60)
    sys.exit(1)
