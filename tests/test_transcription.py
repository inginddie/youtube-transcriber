"""
Script de prueba rápida de transcripción
"""

from config import create_directories
from src.transcriber import YouTubeTranscriber

print("=" * 60)
print("🧪 PRUEBA DE TRANSCRIPCIÓN")
print("=" * 60)
print()

# Setup
create_directories()

# Inicializar transcriber
print("🔧 Inicializando transcriber...")
transcriber = YouTubeTranscriber()
print(f"✅ FFmpeg encontrado: {transcriber._ffmpeg_location_cache}")
print()

# URL de prueba
test_url = "https://youtu.be/WRKau5PJO4c"

print(f"📹 Video de prueba: {test_url}")
print("⏱️  Procesando...")
print()


# Callback de progreso
def progress_callback(message: str):
    print(f"   {message}")


print("🚀 Iniciando transcripción...")
print()

try:
    result = transcriber.process_video(test_url, index=1, progress_callback=progress_callback)

    print()
    print("=" * 60)

    if result["success"]:
        print("✅ TRANSCRIPCIÓN EXITOSA!")
        print("=" * 60)
        print()
        print(f"📄 Título: {result['title']}")
        print(f"📊 Palabras: {result['word_count']}")
        print(f"📁 JSON: {result['json_path']}")
        print(f"📁 TXT: {result['txt_path']}")
        print()

        # Mostrar un preview del contenido
        import json

        with open(result["json_path"], "r", encoding="utf-8") as f:
            data = json.load(f)

        print("📝 Preview de la transcripción:")
        print("-" * 60)
        preview = data["transcript"][:200]
        print(preview + "..." if len(data["transcript"]) > 200 else preview)
        print("-" * 60)
        print()
        print("✨ ¡Prueba completada con éxito!")
        print()
        print("Ahora puedes:")
        print("  1. Ver los archivos en la carpeta 'transcripts/'")
        print("  2. Usar la interfaz web: python launch_web.py")
        print("  3. Transcribir más videos: python main.py <URL>")

    else:
        print("❌ TRANSCRIPCIÓN FALLIDA")
        print("=" * 60)
        print(f"Error: {result['error']}")

except Exception as e:
    print()
    print("=" * 60)
    print("❌ ERROR")
    print("=" * 60)
    print(f"Error: {str(e)}")
    print()
    import traceback

    traceback.print_exc()

print()
print("=" * 60)
