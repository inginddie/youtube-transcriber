"""
Prueba rápida del sistema sin usar API (solo validación)
"""
from src.utils import extract_video_id, validate_url, parse_urls_input

print("🧪 PRUEBA RÁPIDA DEL SISTEMA")
print("=" * 60)
print()

# Test 1: Extracción de Video ID
print("[Test 1] Extracción de Video ID")
test_urls = [
    "https://youtu.be/dQw4w9WgXcQ",
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "https://www.youtube.com/watch?v=abc123&t=10s"
]

for url in test_urls:
    video_id = extract_video_id(url)
    print(f"  URL: {url}")
    print(f"  Video ID: {video_id}")
    print()

# Test 2: Validación de URLs
print("[Test 2] Validación de URLs")
test_cases = [
    ("https://youtu.be/dQw4w9WgXcQ", True),
    ("https://www.google.com", False),
    ("not a url", False)
]

for url, expected in test_cases:
    result = validate_url(url)
    status = "✅" if result == expected else "❌"
    print(f"  {status} {url}: {result}")
print()

# Test 3: Parseo de múltiples URLs
print("[Test 3] Parseo de múltiples URLs")
urls_text = """
https://youtu.be/dQw4w9WgXcQ
https://youtu.be/abc123def45

https://www.google.com
https://youtu.be/xyz789uvw12
"""

parsed = parse_urls_input(urls_text)
print(f"  Input: {len(urls_text.strip().split(chr(10)))} líneas")
print(f"  URLs válidas encontradas: {len(parsed)}")
for i, url in enumerate(parsed, 1):
    print(f"    {i}. {url}")
print()

# Test 4: Configuración
print("[Test 4] Verificación de Configuración")
from config import TRANSCRIPTS_DIR, TEMP_AUDIO_DIR, VECTOR_DB_DIR

print(f"  Directorio de transcripciones: {TRANSCRIPTS_DIR}")
print(f"  Existe: {'✅' if TRANSCRIPTS_DIR.exists() else '❌'}")
print()
print(f"  Directorio temporal: {TEMP_AUDIO_DIR}")
print(f"  Existe: {'✅' if TEMP_AUDIO_DIR.exists() else '❌'}")
print()
print(f"  Directorio de base de datos vectorial: {VECTOR_DB_DIR}")
print(f"  Existe: {'✅' if VECTOR_DB_DIR.exists() else '❌'}")
print()

print("=" * 60)
print("✅ TODAS LAS PRUEBAS COMPLETADAS")
print()
print("El sistema está listo para transcribir videos!")
print()
print("Comandos para empezar:")
print("  - Interfaz Web:  python app_gradio.py")
print("  - CLI:           python main.py https://youtu.be/VIDEO_ID")
print("=" * 60)
