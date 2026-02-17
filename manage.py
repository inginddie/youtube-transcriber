"""
Management CLI for YouTube Transcriber Pro
"""

import json
import shutil
import sys
from pathlib import Path

from config import TEMP_AUDIO_DIR, TRANSCRIPTS_DIR, VECTOR_DB_DIR
from src.logger import setup_logger

logger = setup_logger("manage")


def list_transcripts():
    """List all transcripts"""
    print("=" * 60)
    print("📁 TRANSCRIPCIONES DISPONIBLES")
    print("=" * 60)
    print()

    if not TRANSCRIPTS_DIR.exists():
        print("⚠️  No hay transcripciones")
        return

    json_files = list(TRANSCRIPTS_DIR.glob("*.json"))

    if not json_files:
        print("⚠️  No hay transcripciones")
        return

    print(f"Total: {len(json_files)} transcripciones\n")

    for i, json_file in enumerate(json_files, 1):
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            print(f"{i}. {data.get('title', 'Unknown')}")
            print(f"   Video ID: {data.get('video_id', 'N/A')}")
            print(f"   Palabras: {data.get('word_count', 0)}")
            print(f"   Fecha: {data.get('timestamp', 'N/A')}")
            print(f"   Archivos: {json_file.name}, {json_file.stem}.txt")
            print()
        except Exception as e:
            logger.exception(f"Error reading {json_file.name}")
            print(f"{i}. Error leyendo {json_file.name}: {e}")
            print()


def delete_transcript(video_id: str):
    """Delete a transcript by video ID"""
    print(f"🔍 Buscando transcripción con Video ID: {video_id}")

    found = False
    for json_file in TRANSCRIPTS_DIR.glob("*.json"):
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            if data.get("video_id") == video_id:
                found = True
                title = data.get("title", "Unknown")

                # Delete files
                txt_file = json_file.with_suffix(".txt")

                json_file.unlink()
                print(f"✅ Eliminado: {json_file.name}")

                if txt_file.exists():
                    txt_file.unlink()
                    print(f"✅ Eliminado: {txt_file.name}")

                print(f"\n✅ Transcripción eliminada: {title}")
                break
        except (OSError, json.JSONDecodeError) as e:
            logger.exception(f"Error processing {json_file.name}")
            continue

    if not found:
        print(f"❌ No se encontró transcripción con Video ID: {video_id}")


def check_vector_db():
    """Check vector database status"""
    print("=" * 60)
    print("🗄️ ESTADO DE LA BASE DE DATOS VECTORIAL")
    print("=" * 60)
    print()

    if not VECTOR_DB_DIR.exists():
        print("⚠️  Base de datos no inicializada")
        return

    # Calculate size
    total_size = 0
    file_count = 0

    for item in VECTOR_DB_DIR.rglob("*"):
        if item.is_file() and item.name != ".gitkeep":
            total_size += item.stat().st_size
            file_count += 1

    size_mb = total_size / (1024 * 1024)

    print(f"📍 Ubicación: {VECTOR_DB_DIR}")
    print(f"📊 Archivos: {file_count}")
    print(f"💾 Tamaño: {size_mb:.2f} MB")
    print()

    if file_count > 0:
        print("✅ Base de datos contiene datos")
    else:
        print("⚠️  Base de datos vacía o no inicializada")


def clear_vector_db():
    """Clear vector database"""
    print("🗑️  Limpiando base de datos vectorial...")

    try:
        if VECTOR_DB_DIR.exists():
            shutil.rmtree(VECTOR_DB_DIR)
            VECTOR_DB_DIR.mkdir(exist_ok=True)
            (VECTOR_DB_DIR / ".gitkeep").touch()

            print("✅ Base de datos vectorial limpiada")
            print("⚠️  Necesitarás re-indexar para usar RAG")
        else:
            print("⚠️  Base de datos no existe")

    except Exception as e:
        logger.exception("Error clearing vector DB")
        print(f"❌ Error: {e}")


def clear_temp_files():
    """Clear temporary audio files"""
    print("🗑️  Limpiando archivos temporales...")

    deleted = 0
    for file in TEMP_AUDIO_DIR.glob("*"):
        if file.name != ".gitkeep":
            try:
                file.unlink()
                deleted += 1
            except OSError as e:
                logger.warning(f"Could not delete temp file {file}: {e}")

    print(f"✅ Eliminados {deleted} archivos temporales")


def clear_all():
    """Clear everything"""
    print("=" * 60)
    print("🗑️  LIMPIEZA COMPLETA")
    print("=" * 60)
    print()

    confirm = input("⚠️  ¿Estás seguro? Esto eliminará TODO (y/n): ")

    if confirm.lower() != "y":
        print("❌ Operación cancelada")
        return

    # Delete transcripts
    deleted_transcripts = 0
    for json_file in TRANSCRIPTS_DIR.glob("*.json"):
        try:
            txt_file = json_file.with_suffix(".txt")
            json_file.unlink()
            if txt_file.exists():
                txt_file.unlink()
            deleted_transcripts += 1
        except OSError as e:
            logger.warning(f"Could not delete transcript {json_file}: {e}")

    print(f"✅ Eliminadas {deleted_transcripts} transcripciones")

    # Clear vector DB
    clear_vector_db()

    # Clear temp files
    clear_temp_files()

    print()
    print("✅ Limpieza completa finalizada")


def show_stats():
    """Show statistics"""
    print("=" * 60)
    print("📊 ESTADÍSTICAS")
    print("=" * 60)
    print()

    # Transcripts
    json_files = list(TRANSCRIPTS_DIR.glob("*.json"))
    total_words = 0

    for json_file in json_files:
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                total_words += data.get("word_count", 0)
        except (OSError, json.JSONDecodeError) as e:
            logger.warning(f"Could not read stats from {json_file}: {e}")

    print(f"📝 Transcripciones: {len(json_files)}")
    print(f"📊 Total de palabras: {total_words:,}")
    if json_files:
        print(f"📈 Promedio por video: {total_words // len(json_files):,} palabras")
    print()

    # Vector DB
    if VECTOR_DB_DIR.exists():
        total_size = sum(f.stat().st_size for f in VECTOR_DB_DIR.rglob("*") if f.is_file())
        size_mb = total_size / (1024 * 1024)
        print(f"🗄️  Vector DB: {size_mb:.2f} MB")
    else:
        print(f"🗄️  Vector DB: No inicializada")
    print()

    # Temp files
    temp_files = [f for f in TEMP_AUDIO_DIR.glob("*") if f.name != ".gitkeep"]
    if temp_files:
        temp_size = sum(f.stat().st_size for f in temp_files) / (1024 * 1024)
        print(f"⚠️  Archivos temporales: {len(temp_files)} ({temp_size:.2f} MB)")
        print(f"   Ejecuta: python manage.py --clean-temp")
    else:
        print(f"✅ Sin archivos temporales")


def main():
    """Main CLI"""
    if len(sys.argv) < 2:
        print("YouTube Transcriber Pro - Management CLI")
        print()
        print("Uso:")
        print("  python manage.py --list              # Listar transcripciones")
        print("  python manage.py --delete VIDEO_ID   # Eliminar transcripción")
        print("  python manage.py --check-db          # Ver estado de Vector DB")
        print("  python manage.py --clear-db          # Limpiar Vector DB")
        print("  python manage.py --clean-temp        # Limpiar archivos temporales")
        print("  python manage.py --clear-all         # Eliminar TODO")
        print("  python manage.py --stats             # Ver estadísticas")
        sys.exit(0)

    command = sys.argv[1]

    if command == "--list":
        list_transcripts()

    elif command == "--delete":
        if len(sys.argv) < 3:
            print("❌ Error: Especifica el Video ID")
            print("Uso: python manage.py --delete VIDEO_ID")
            sys.exit(1)
        delete_transcript(sys.argv[2])

    elif command == "--check-db":
        check_vector_db()

    elif command == "--clear-db":
        clear_vector_db()

    elif command == "--clean-temp":
        clear_temp_files()

    elif command == "--clear-all":
        clear_all()

    elif command == "--stats":
        show_stats()

    else:
        print(f"❌ Comando desconocido: {command}")
        print("Usa: python manage.py (sin argumentos) para ver ayuda")
        sys.exit(1)


if __name__ == "__main__":
    main()
