"""
Script de prueba para detección de duplicados
"""

from config import create_directories
from src.transcriber import YouTubeTranscriber

print("=" * 60)
print("🧪 PRUEBA DE DETECCIÓN DE DUPLICADOS")
print("=" * 60)
print()

# Setup
create_directories()
transcriber = YouTubeTranscriber()

# URL de prueba (usa un video que ya hayas transcrito)
test_url = "https://youtu.be/WRKau5PJO4c"

print("📝 Escenario 1: Intentar transcribir video existente")
print("-" * 60)
print(f"URL: {test_url}")
print()

# Intento 1: Con detección de duplicados (por defecto)
print("🔍 Intento 1: Con detección de duplicados activada")
result1 = transcriber.process_video(test_url, index=1, skip_if_exists=True)

if result1.get("skipped"):
    print(f"✅ Video detectado como duplicado y saltado")
    print(f"   Título: {result1['title']}")
    print(f"   Archivo: {result1['json_path']}")
else:
    print(f"⚠️  Video no detectado como duplicado (puede ser nuevo)")

print()
print("=" * 60)
print()

# Intento 2: Forzar re-transcripción
print("🔍 Intento 2: Forzar re-transcripción (skip_if_exists=False)")
print("⚠️  ADVERTENCIA: Esto usará créditos de API si el video existe")
print()

respuesta = input("¿Quieres continuar con la re-transcripción? (y/n): ")

if respuesta.lower() == "y":
    result2 = transcriber.process_video(test_url, index=1, skip_if_exists=False)

    if result2.get("success"):
        print(f"✅ Video re-transcrito exitosamente")
        print(f"   Título: {result2['title']}")
        print(f"   Palabras: {result2['word_count']}")
    else:
        print(f"❌ Error: {result2.get('error')}")
else:
    print("⏭️  Re-transcripción cancelada")

print()
print("=" * 60)
print()

# Escenario 2: Lista con duplicados
print("📝 Escenario 2: Lista con URLs duplicadas")
print("-" * 60)

urls_con_duplicados = [
    "https://youtu.be/WRKau5PJO4c",
    "https://www.youtube.com/watch?v=WRKau5PJO4c",  # Mismo video, URL diferente
    "https://youtu.be/WRKau5PJO4c?si=abc123",  # Mismo video con parámetros
]

print(f"URLs en la lista: {len(urls_con_duplicados)}")
for i, url in enumerate(urls_con_duplicados, 1):
    print(f"  {i}. {url}")

print()
print("🔍 Procesando lista...")
print()

results = transcriber.process_multiple_videos(urls_con_duplicados, skip_if_exists=True)

print()
print("📊 Resultados:")
print(f"   Total en lista: {len(urls_con_duplicados)}")
print(f"   Procesados: {len(results)}")
print(f"   Duplicados removidos: {len(urls_con_duplicados) - len(results)}")

print()
print("=" * 60)
print("✅ PRUEBA COMPLETADA")
print("=" * 60)
print()
print("Conclusiones:")
print("  1. El sistema detecta videos ya transcritos")
print("  2. Puedes forzar re-transcripción con skip_if_exists=False")
print("  3. Los duplicados en la lista se detectan automáticamente")
print("  4. Esto ahorra tiempo y dinero")
