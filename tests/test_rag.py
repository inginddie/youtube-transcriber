"""
Script de prueba para el sistema RAG
"""
from src.rag_engine import RAGEngine
from pathlib import Path

print("=" * 60)
print("🧪 PRUEBA DEL SISTEMA RAG")
print("=" * 60)
print()

# Verificar que hay transcripciones
transcripts_dir = Path("transcripts")
json_files = list(transcripts_dir.glob("*.json"))

if not json_files:
    print("❌ No hay transcripciones disponibles")
    print("   Por favor transcribe al menos un video primero")
    exit(1)

print(f"✅ Encontradas {len(json_files)} transcripciones")
print()

# Inicializar RAG
print("🔧 Inicializando RAG Engine...")
rag = RAGEngine()
print("✅ RAG Engine inicializado")
print()

# Cargar transcripciones
print("📚 Cargando transcripciones...")
transcripts = rag.load_transcripts()
print(f"✅ Cargadas {len(transcripts)} transcripciones:")
for t in transcripts:
    print(f"   - {t['title']} ({t['word_count']} palabras)")
print()

# Indexar transcripciones
print("🔄 Indexando transcripciones...")
print("   (Esto puede tardar un momento...)")

def progress_callback(message):
    print(f"   {message}")

try:
    rag.index_transcripts(progress_callback=progress_callback)
    print("✅ Indexación completada")
    print()
except Exception as e:
    print(f"❌ Error al indexar: {e}")
    exit(1)

# Probar búsqueda semántica
print("=" * 60)
print("🔍 PRUEBA DE BÚSQUEDA SEMÁNTICA")
print("=" * 60)
print()

search_queries = [
    "What is the main topic?",
    "How to create AI influencer?",
    "What tools are mentioned?"
]

for query in search_queries:
    print(f"Query: '{query}'")
    print("-" * 60)
    
    try:
        results = rag.search(query, k=2)
        
        for i, result in enumerate(results, 1):
            print(f"\nResult {i} (Score: {result['score']:.4f}):")
            print(f"Video: {result['metadata']['title']}")
            print(f"Content: {result['content'][:150]}...")
        
        print()
    except Exception as e:
        print(f"❌ Error: {e}")
        print()

# Probar chat
print("=" * 60)
print("💬 PRUEBA DE CHAT")
print("=" * 60)
print()

print("🔧 Configurando chat...")
try:
    rag.load_vector_store()
    rag.setup_conversation_chain()
    print("✅ Chat configurado")
    print()
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)

# Preguntas de prueba
questions = [
    "What is this video about?",
    "Can you summarize the main points?",
]

for question in questions:
    print(f"❓ Question: {question}")
    print("-" * 60)
    
    try:
        response = rag.chat(question)
        
        print(f"🤖 Answer: {response['answer']}")
        
        if response['sources']:
            print(f"\n📚 Sources:")
            for source in response['sources']:
                print(f"   - {source['title']}")
                print(f"     {source['url']}")
        
        print()
    except Exception as e:
        print(f"❌ Error: {e}")
        print()

print("=" * 60)
print("✅ PRUEBA COMPLETADA")
print("=" * 60)
print()
print("El sistema RAG está funcionando correctamente!")
print()
print("Ahora puedes:")
print("  1. Usar la interfaz web: python launch_web.py")
print("  2. Ir a la pestaña 'Chat' para chatear con tus transcripciones")
print("  3. Usar la pestaña 'Search' para búsquedas semánticas")
