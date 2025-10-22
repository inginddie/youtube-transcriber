"""
Gradio UI for YouTube Transcriber Pro - Phase 1
"""
import gradio as gr
from pathlib import Path

from config import create_directories, TRANSCRIPTS_DIR, VECTOR_DB_DIR, GRADIO_PORT, GRADIO_SHARE
from src.transcriber import YouTubeTranscriber
from src.utils import parse_urls_input


def list_transcript_files():
    """List all transcript files"""
    if not TRANSCRIPTS_DIR.exists():
        return []
    
    files = []
    for ext in ['*.json', '*.txt']:
        files.extend(TRANSCRIPTS_DIR.glob(ext))
    
    # Sort by modification time (newest first)
    files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    
    return [str(f) for f in files]


def read_transcript_file(file_path: str):
    """Read and return content of a transcript file"""
    if not file_path or file_path == "":
        return "📁 No file selected. Please select a file from the dropdown above."
    
    try:
        from pathlib import Path
        path = Path(file_path)
        
        if not path.exists():
            return f"❌ File not found: {file_path}"
        
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Agregar header con info del archivo
        file_size = path.stat().st_size / 1024  # KB
        header = f"📄 File: {path.name}\n"
        header += f"📊 Size: {file_size:.2f} KB\n"
        header += f"{'='*80}\n\n"
        
        return header + content
    except Exception as e:
        return f"❌ Error reading file: {str(e)}\n\nPath: {file_path}"


def transcribe_videos(urls_text: str, skip_existing: bool, auto_index: bool, progress=gr.Progress()):
    """
    Transcribe videos from URLs
    
    Args:
        urls_text: Text containing YouTube URLs (one per line)
        skip_existing: Whether to skip already transcribed videos
        auto_index: Whether to auto-index after transcription
        progress: Gradio progress tracker
        
    Returns:
        Tuple of (status_message, file_list)
    """
    # Parse URLs
    urls = parse_urls_input(urls_text)
    
    if not urls:
        return "❌ No valid YouTube URLs found. Please enter at least one valid URL.", []
    
    # Initialize transcriber
    transcriber = YouTubeTranscriber()
    
    # Progress tracking
    results = []
    status_messages = []
    current_video = [0]  # Usar lista para poder modificar en callback
    current_step = ["Iniciando..."]
    
    def progress_callback(message: str):
        status_messages.append(message)
        
        # Detectar el paso actual
        if "PROCESSING VIDEO" in message:
            try:
                video_num = int(message.split("#")[1].split()[0])
                current_video[0] = video_num
                current_step[0] = "Preparando"
            except:
                pass
        elif "Downloading" in message or "Download" in message:
            current_step[0] = "Descargando"
        elif "Transcribing" in message or "Whisper" in message:
            current_step[0] = "Transcribiendo"
        elif "Saving" in message:
            current_step[0] = "Guardando"
        elif "COMPLETED" in message:
            current_step[0] = "Completado"
        
        # Calcular porcentaje basado en videos completados y paso actual
        completed = len(results)
        total = len(urls)
        
        # Progreso base por videos completados
        base_progress = completed / total if total > 0 else 0
        
        # Progreso adicional del video actual (estimado)
        step_progress = 0
        if current_step[0] == "Descargando":
            step_progress = 0.3
        elif current_step[0] == "Transcribiendo":
            step_progress = 0.7
        elif current_step[0] == "Guardando":
            step_progress = 0.9
        elif current_step[0] == "Completado":
            step_progress = 1.0
        
        # Progreso total
        current_video_progress = step_progress / total if total > 0 else 0
        total_progress = base_progress + current_video_progress
        total_progress = min(total_progress, 1.0)  # No exceder 100%
        
        percentage = int(total_progress * 100)
        
        # Crear mensaje de progreso mejorado con emojis
        if current_step[0] == "Descargando":
            emoji = "⬇️"
        elif current_step[0] == "Transcribiendo":
            emoji = "🎤"
        elif current_step[0] == "Guardando":
            emoji = "💾"
        elif current_step[0] == "Completado":
            emoji = "✅"
        else:
            emoji = "🔄"
        
        # Mensaje más corto y claro
        progress_msg = f"{emoji} {percentage}% | Video {current_video[0]}/{total} | {current_step[0]}"
        progress(total_progress, desc=progress_msg)
    
    # Process videos
    results = transcriber.process_multiple_videos(urls, progress_callback, skip_existing)
    
    # Generate summary
    successful = [r for r in results if r.get('success') and not r.get('skipped')]
    skipped = [r for r in results if r.get('success') and r.get('skipped')]
    failed = [r for r in results if not r.get('success')]
    
    summary = f"## 📊 Processing Summary\n\n"
    summary += f"- ✅ **Newly transcribed**: {len(successful)}\n"
    summary += f"- ⏭️  **Skipped** (already exist): {len(skipped)}\n"
    summary += f"- ❌ **Failed**: {len(failed)}\n"
    summary += f"- 📝 **Total**: {len(results)}\n\n"
    
    if successful:
        summary += "### ✅ Newly Transcribed:\n"
        for result in successful:
            summary += f"- **{result['title']}** ({result['word_count']} words)\n"
        summary += "\n"
    
    if skipped:
        summary += "### ⏭️  Skipped (Already Transcribed):\n"
        for result in skipped:
            summary += f"- **{result['title']}** (transcribed on {result.get('timestamp', 'unknown date')})\n"
        summary += "\n"
    
    if failed:
        summary += "### ❌ Failed:\n"
        for result in failed:
            summary += f"- {result['url']}: {result['error']}\n"
        summary += "\n"
    
    # Auto-index if requested and there are new transcriptions
    if auto_index and successful:
        summary += "---\n\n"
        summary += "### 🔄 Auto-Indexing for RAG...\n\n"
        
        try:
            from src.rag_engine import RAGEngine
            
            progress(0.9, desc="Indexing transcripts for RAG...")
            rag = RAGEngine()
            
            def index_progress(msg):
                summary += f"- {msg}\n"
            
            rag.index_transcripts(progress_callback=index_progress)
            
            summary += "\n✅ **Indexing complete!** You can now use the Chat and Search tabs.\n"
        except Exception as e:
            summary += f"\n⚠️ **Indexing failed:** {str(e)}\n"
            summary += "You can manually index in the 'RAG Setup' tab.\n"
    
    # Get list of transcript files and update dropdown
    transcript_files = list_transcript_files()
    
    # Return summary and updated dropdown choices
    return summary, gr.Dropdown(choices=transcript_files)


def list_transcript_files():
    """
    List all transcript files in the output directory
    
    Returns:
        List of file paths
    """
    if not TRANSCRIPTS_DIR.exists():
        return []
    
    files = []
    for ext in ['*.json', '*.txt']:
        files.extend(TRANSCRIPTS_DIR.glob(ext))
    
    # Sort by modification time (newest first)
    files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    
    return [str(f) for f in files]


def read_transcript_file(file_path: str):
    """
    Read and return content of a transcript file
    
    Args:
        file_path: Path to transcript file
        
    Returns:
        File content as string
    """
    if not file_path:
        return "No file selected"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except Exception as e:
        return f"Error reading file: {str(e)}"


def index_transcripts_ui(progress=gr.Progress()):
    """
    Index all transcripts for RAG
    
    Args:
        progress: Gradio progress tracker
        
    Returns:
        Status message
    """
    try:
        from src.rag_engine import RAGEngine
        
        progress(0, desc="Initializing RAG engine...")
        rag = RAGEngine()
        
        progress(0.3, desc="Loading transcripts...")
        transcripts = rag.load_transcripts()
        
        if not transcripts:
            return "❌ No transcripts found. Please transcribe some videos first."
        
        progress(0.5, desc=f"Indexing {len(transcripts)} transcripts...")
        rag.index_transcripts(progress_callback=lambda msg: progress(0.7, desc=msg))
        
        progress(1.0, desc="Indexing complete!")
        
        return f"✅ Successfully indexed {len(transcripts)} transcripts!\n\nYou can now use the Chat tab to ask questions."
        
    except Exception as e:
        return f"❌ Error indexing transcripts: {str(e)}"


def chat_with_transcripts(message: str, history: list, progress=gr.Progress()):
    """
    Chat with transcripts using RAG
    
    Args:
        message: User message
        history: Chat history
        progress: Gradio progress tracker
        
    Returns:
        Updated history
    """
    try:
        from src.rag_engine import RAGEngine
        
        progress(0.3, desc="Loading RAG engine...")
        rag = RAGEngine()
        
        try:
            progress(0.5, desc="Loading vector store...")
            rag.load_vector_store()
        except ValueError:
            return history + [[message, "❌ Please index your transcripts first using the 'Index Transcripts' button in the RAG Setup tab."]]
        
        progress(0.7, desc="Setting up conversation...")
        rag.setup_conversation_chain()
        
        progress(0.9, desc="Generating response...")
        result = rag.chat(message)
        
        # Format response with sources
        response = result['answer']
        
        if result['sources']:
            response += "\n\n**📚 Sources:**\n"
            for i, source in enumerate(result['sources'], 1):
                response += f"{i}. [{source['title']}]({source['url']})\n"
        
        return history + [[message, response]]
        
    except Exception as e:
        return history + [[message, f"❌ Error: {str(e)}"]]


def search_transcripts(query: str, k: int = 3):
    """
    Search transcripts semantically
    
    Args:
        query: Search query
        k: Number of results
        
    Returns:
        Search results
    """
    try:
        from src.rag_engine import RAGEngine
        
        rag = RAGEngine()
        
        try:
            rag.load_vector_store()
        except ValueError:
            return "❌ Please index your transcripts first using the 'Index Transcripts' button in the RAG Setup tab."
        
        results = rag.search(query, k=k)
        
        if not results:
            return "No results found."
        
        output = f"# 🔍 Search Results for: '{query}'\n\n"
        output += f"Found {len(results)} relevant chunks:\n\n"
        
        for i, result in enumerate(results, 1):
            output += f"## Result {i} (Score: {result['score']:.4f})\n\n"
            output += f"**Video:** {result['metadata']['title']}\n\n"
            output += f"**Content:**\n{result['content'][:300]}...\n\n"
            output += f"**[Watch Video]({result['metadata']['url']})**\n\n"
            output += "---\n\n"
        
        return output
        
    except Exception as e:
        return f"❌ Error: {str(e)}"


def get_transcript_list():
    """Get list of transcripts for management"""
    import json
    
    transcripts = []
    for json_file in TRANSCRIPTS_DIR.glob("*.json"):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            label = f"{data.get('title', 'Unknown')} ({data.get('video_id', 'N/A')})"
            transcripts.append((label, str(json_file)))
        except:
            continue
    
    return transcripts


def delete_selected_transcripts(selected_files):
    """Delete selected transcript files"""
    if not selected_files:
        return "⚠️ No files selected", get_transcript_list()
    
    deleted = []
    errors = []
    
    for file_path in selected_files:
        try:
            json_path = Path(file_path)
            txt_path = json_path.with_suffix('.txt')
            
            # Delete JSON
            if json_path.exists():
                json_path.unlink()
                deleted.append(json_path.name)
            
            # Delete TXT
            if txt_path.exists():
                txt_path.unlink()
        
        except Exception as e:
            errors.append(f"{json_path.name}: {str(e)}")
    
    result = f"### 🗑️ Deletion Results\n\n"
    result += f"✅ **Deleted**: {len(deleted)} files\n\n"
    
    if deleted:
        for name in deleted:
            result += f"- {name}\n"
    
    if errors:
        result += f"\n❌ **Errors**: {len(errors)}\n\n"
        for error in errors:
            result += f"- {error}\n"
    
    result += "\n⚠️ **Note**: You may need to re-index for RAG to reflect changes."
    
    return result, get_transcript_list()


def check_vector_db_status():
    """Check vector database status"""
    import shutil
    
    if not VECTOR_DB_DIR.exists():
        return "📊 **Vector DB Status**: Not initialized"
    
    # Calculate size
    total_size = 0
    file_count = 0
    
    for item in VECTOR_DB_DIR.rglob('*'):
        if item.is_file():
            total_size += item.stat().st_size
            file_count += 1
    
    size_mb = total_size / (1024 * 1024)
    
    status = f"### 📊 Vector DB Status\n\n"
    status += f"- **Location**: `{VECTOR_DB_DIR}`\n"
    status += f"- **Files**: {file_count}\n"
    status += f"- **Size**: {size_mb:.2f} MB\n"
    
    if file_count > 0:
        status += f"\n✅ Database is initialized and contains data"
    else:
        status += f"\n⚠️ Database is empty or not initialized"
    
    return status


def clear_vector_db():
    """Clear vector database"""
    import shutil
    
    try:
        if VECTOR_DB_DIR.exists():
            shutil.rmtree(VECTOR_DB_DIR)
            VECTOR_DB_DIR.mkdir(exist_ok=True)
            (VECTOR_DB_DIR / ".gitkeep").touch()
            
            return "✅ **Vector DB cleared successfully**\n\nYou'll need to re-index your transcripts to use RAG features again."
        else:
            return "⚠️ Vector DB directory doesn't exist"
    
    except Exception as e:
        return f"❌ Error clearing Vector DB: {str(e)}"


def clear_all_data():
    """Clear all transcripts and vector database"""
    import shutil
    
    try:
        deleted_transcripts = 0
        deleted_db = False
        
        # Delete all transcripts
        for json_file in TRANSCRIPTS_DIR.glob("*.json"):
            try:
                txt_file = json_file.with_suffix('.txt')
                json_file.unlink()
                if txt_file.exists():
                    txt_file.unlink()
                deleted_transcripts += 1
            except:
                pass
        
        # Clear vector DB
        if VECTOR_DB_DIR.exists():
            shutil.rmtree(VECTOR_DB_DIR)
            VECTOR_DB_DIR.mkdir(exist_ok=True)
            (VECTOR_DB_DIR / ".gitkeep").touch()
            deleted_db = True
        
        result = "### 🗑️ Complete Cleanup Results\n\n"
        result += f"✅ **Transcripts deleted**: {deleted_transcripts}\n"
        result += f"✅ **Vector DB cleared**: {'Yes' if deleted_db else 'No'}\n\n"
        result += "🎉 **All data has been cleared!**\n\n"
        result += "You can start fresh by transcribing new videos."
        
        return result, get_transcript_list()
    
    except Exception as e:
        return f"❌ Error during cleanup: {str(e)}", get_transcript_list()


def create_ui():
    """Create Gradio interface"""
    
    # CSS personalizado simplificado y compatible
    custom_css = """
    /* Mejorar visibilidad general */
    .gradio-container {
        font-family: 'Inter', sans-serif;
    }
    
    /* Barra de progreso más visible */
    .progress-bar {
        min-height: 30px !important;
    }
    """
    
    with gr.Blocks(
        title="YouTube Transcriber Pro", 
        theme=gr.themes.Soft(),
        css=custom_css
    ) as app:
        gr.Markdown("""
        # 🎥 YouTube Transcriber Pro
        
        Transcribe YouTube videos and chat with your transcripts using AI
        """)
        
        with gr.Tabs():
            # Tab 1: Transcription
            with gr.Tab("📝 Transcribe Videos"):
                gr.Markdown("""
                ### How to use:
                1. Enter YouTube URLs (one per line)
                2. Click "Transcribe Videos"
                3. Wait for processing to complete
                4. View and download your transcripts
                """)
                
                with gr.Row():
                    with gr.Column(scale=2):
                        urls_input = gr.Textbox(
                            label="YouTube URLs",
                            placeholder="https://youtu.be/VIDEO_ID\nhttps://youtu.be/ANOTHER_ID\n...",
                            lines=10,
                            info="Enter one URL per line"
                        )
                        
                        with gr.Row():
                            skip_existing = gr.Checkbox(
                                label="Skip already transcribed videos",
                                value=True,
                                info="Uncheck to force re-transcription"
                            )
                            auto_index = gr.Checkbox(
                                label="Auto-index after transcription",
                                value=False,
                                info="Automatically index for RAG after transcribing"
                            )
                        
                        transcribe_btn = gr.Button("🚀 Transcribe Videos", variant="primary", size="lg")
                        
                        status_output = gr.Markdown(label="Status")
                    
                    with gr.Column(scale=1):
                        gr.Markdown("### 📁 Generated Files")
                        
                        refresh_btn = gr.Button("🔄 Refresh File List")
                        
                        file_list = gr.Dropdown(
                            label="Select a file to view",
                            choices=list_transcript_files(),
                            interactive=True,
                            allow_custom_value=True  # Permite valores que no están en la lista inicial
                        )
                        
                        file_content = gr.Textbox(
                            label="File Content",
                            lines=15,
                            max_lines=20,
                            interactive=False
                        )
                        
                        download_btn = gr.File(label="Download File", interactive=False)
            
            # Tab 2: RAG Setup
            with gr.Tab("🔧 RAG Setup"):
                gr.Markdown("""
                ### Setup RAG (Retrieval-Augmented Generation)
                
                Before you can chat with your transcripts, you need to index them:
                
                1. Make sure you have transcribed at least one video
                2. Click "Index Transcripts" below
                3. Wait for indexing to complete
                4. Go to the "Chat" or "Search" tabs
                """)
                
                index_btn = gr.Button("🔄 Index Transcripts", variant="primary", size="lg")
                index_status = gr.Markdown()
                
                gr.Markdown("""
                ### 💡 What is RAG?
                
                RAG (Retrieval-Augmented Generation) allows you to:
                - **Search** semantically through your transcripts
                - **Chat** with an AI about your video content
                - **Get answers** with source citations
                
                The system will:
                1. Split transcripts into chunks
                2. Create embeddings (vector representations)
                3. Store them in a local database (ChromaDB)
                4. Enable semantic search and chat
                """)
            
            # Tab 3: Chat
            with gr.Tab("💬 Chat with Transcripts"):
                gr.Markdown("""
                ### Chat with your transcripts
                
                Ask questions about your transcribed videos and get AI-powered answers with source citations.
                
                **Example questions:**
                - "What are the main topics discussed?"
                - "Summarize the key points"
                - "What did they say about [topic]?"
                """)
                
                chatbot = gr.Chatbot(
                    label="Chat",
                    height=500,
                    show_label=True
                )
                
                with gr.Row():
                    msg = gr.Textbox(
                        label="Your question",
                        placeholder="Ask a question about your transcripts...",
                        scale=4
                    )
                    send_btn = gr.Button("Send", variant="primary", scale=1)
                
                clear_btn = gr.Button("🗑️ Clear Chat")
                
                gr.Markdown("""
                **Note:** Make sure you've indexed your transcripts in the "RAG Setup" tab first!
                """)
            
            # Tab 4: Search
            with gr.Tab("🔍 Search Transcripts"):
                gr.Markdown("""
                ### Semantic Search
                
                Search through your transcripts using natural language.
                The system will find the most relevant content based on meaning, not just keywords.
                """)
                
                with gr.Row():
                    search_query = gr.Textbox(
                        label="Search Query",
                        placeholder="What are you looking for?",
                        scale=3
                    )
                    search_k = gr.Slider(
                        minimum=1,
                        maximum=10,
                        value=3,
                        step=1,
                        label="Number of Results",
                        scale=1
                    )
                
                search_btn = gr.Button("🔍 Search", variant="primary", size="lg")
                search_results = gr.Markdown(label="Search Results")
            
            # Tab 5: Management
            with gr.Tab("⚙️ Management"):
                gr.Markdown("""
                ### Gestión de Archivos y Base de Datos
                
                Administra tus transcripciones y la base de datos vectorial.
                
                ⚠️ **Advertencia**: Las operaciones de eliminación son permanentes.
                """)
                
                with gr.Row():
                    with gr.Column():
                        gr.Markdown("### 📁 Gestión de Transcripciones")
                        
                        transcript_list = gr.CheckboxGroup(
                            label="Selecciona transcripciones para eliminar",
                            choices=[],
                            interactive=True
                        )
                        
                        with gr.Row():
                            refresh_transcripts_btn = gr.Button("🔄 Actualizar Lista", size="sm")
                            delete_selected_btn = gr.Button("🗑️ Eliminar Seleccionadas", variant="stop")
                        
                        delete_status = gr.Markdown()
                    
                    with gr.Column():
                        gr.Markdown("### 🗄️ Gestión de Base de Datos Vectorial")
                        
                        db_info = gr.Markdown()
                        
                        with gr.Row():
                            check_db_btn = gr.Button("📊 Ver Estado de DB", size="sm")
                            clear_db_btn = gr.Button("🗑️ Vaciar Vector DB", variant="stop")
                        
                        db_status = gr.Markdown()
                        
                        gr.Markdown("""
                        ### 🧹 Limpieza Completa
                        
                        Elimina TODAS las transcripciones y la base de datos vectorial.
                        
                        ⚠️ **Esta acción es irreversible**
                        """)
                        
                        clear_all_btn = gr.Button("🗑️ ELIMINAR TODO", variant="stop", size="lg")
                        clear_all_status = gr.Markdown()
        
        # Event handlers - Transcription Tab
        transcribe_btn.click(
            fn=transcribe_videos,
            inputs=[urls_input, skip_existing, auto_index],
            outputs=[status_output, file_list]
        )
        
        refresh_btn.click(
            fn=lambda: gr.Dropdown(choices=list_transcript_files()),
            inputs=[],
            outputs=[file_list]
        )
        
        file_list.change(
            fn=read_transcript_file,
            inputs=[file_list],
            outputs=[file_content]
        )
        
        file_list.change(
            fn=lambda x: x if x else None,
            inputs=[file_list],
            outputs=[download_btn]
        )
        
        # Event handlers - RAG Setup Tab
        index_btn.click(
            fn=index_transcripts_ui,
            inputs=[],
            outputs=[index_status]
        )
        
        # Event handlers - Chat Tab
        msg.submit(
            fn=chat_with_transcripts,
            inputs=[msg, chatbot],
            outputs=[chatbot]
        ).then(
            fn=lambda: "",
            inputs=[],
            outputs=[msg]
        )
        
        send_btn.click(
            fn=chat_with_transcripts,
            inputs=[msg, chatbot],
            outputs=[chatbot]
        ).then(
            fn=lambda: "",
            inputs=[],
            outputs=[msg]
        )
        
        clear_btn.click(
            fn=lambda: [],
            inputs=[],
            outputs=[chatbot]
        )
        
        # Event handlers - Search Tab
        search_btn.click(
            fn=search_transcripts,
            inputs=[search_query, search_k],
            outputs=[search_results]
        )
        
        # Event handlers - Management Tab
        refresh_transcripts_btn.click(
            fn=get_transcript_list,
            inputs=[],
            outputs=[transcript_list]
        )
        
        delete_selected_btn.click(
            fn=delete_selected_transcripts,
            inputs=[transcript_list],
            outputs=[delete_status, transcript_list]
        )
        
        check_db_btn.click(
            fn=check_vector_db_status,
            inputs=[],
            outputs=[db_info]
        )
        
        clear_db_btn.click(
            fn=clear_vector_db,
            inputs=[],
            outputs=[db_status]
        )
        
        clear_all_btn.click(
            fn=clear_all_data,
            inputs=[],
            outputs=[clear_all_status, transcript_list]
        )
        
        # Load transcript list on tab load
        app.load(
            fn=get_transcript_list,
            inputs=[],
            outputs=[transcript_list]
        )
        
        gr.Markdown("""
        ---
        ### 💡 Tips:
        - **Transcription**: ~$0.006 per minute of audio
        - **Embeddings**: ~$0.0001 per 1K tokens (for RAG)
        - **Chat**: ~$0.03 per 1K tokens (GPT-4)
        - Maximum file size: 25MB (automatically split if larger)
        - Supports all languages that Whisper can transcribe
        
        ### 📊 Features:
        - **Transcribe**: Convert YouTube videos to text
        - **RAG Setup**: Index transcripts for semantic search
        - **Chat**: Ask questions about your videos
        - **Search**: Find relevant content across all transcripts
        
        ### 🔒 Privacy:
        - All processing uses OpenAI API
        - Vector database stored locally (ChromaDB)
        - No data shared with third parties
        """)
    
    return app


def main():
    """Launch Gradio app"""
    import os
    
    # Validate API key
    from config import OPENAI_API_KEY
    if not OPENAI_API_KEY:
        print("❌ ERROR: OPENAI_API_KEY not found in environment variables")
        print("Please set OPENAI_API_KEY in Railway variables")
        exit(1)
    
    # Setup
    print("🔧 Setting up directories...")
    create_directories()
    
    # Create and launch UI
    print("🚀 Launching Gradio interface...")
    
    # Get port from environment (Railway) or use default
    port = int(os.getenv("PORT", GRADIO_PORT))
    is_production = os.getenv("RAILWAY_ENVIRONMENT") == "production"
    
    print(f"   ✓ Using port: {port}")
    print(f"   ✓ Environment: {'production' if is_production else 'development'}")
    
    app = create_ui()
    app.launch(
        server_name="0.0.0.0",  # Required for Railway
        server_port=port,
        share=False,  # Don't share in production
        show_error=not is_production
    )


if __name__ == "__main__":
    main()
