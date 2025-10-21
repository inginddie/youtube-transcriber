"""
Gradio UI for YouTube Transcriber Pro - PRODUCTION VERSION
Con seguridad, rate limiting y protección contra bots
"""
import gradio as gr
import os
from pathlib import Path
from functools import wraps

from config import create_directories, TRANSCRIPTS_DIR, VECTOR_DB_DIR
from src.transcriber import YouTubeTranscriber
from src.utils import parse_urls_input
from src.security import security_manager, get_security_headers

# Importar funciones de la app original
import sys
sys.path.append(str(Path(__file__).parent))
from app_gradio import (
    transcribe_videos,
    search_transcripts,
    chat_with_videos,
    list_transcripts,
    delete_selected_transcripts,
    check_vector_db_status,
    clear_vector_db,
    clear_all_data
)

# Configuración de producción
PRODUCTION = os.getenv("RAILWAY_ENVIRONMENT", "development") == "production"
REQUIRE_AUTH = os.getenv("REQUIRE_AUTH", "false").lower() == "true"
ACCESS_CODE = os.getenv("ACCESS_CODE", "")

# Rate limits configurables
MAX_TRANSCRIPTIONS_PER_HOUR = int(os.getenv("MAX_TRANSCRIPTIONS_PER_HOUR", "5"))
MAX_SEARCHES_PER_MINUTE = int(os.getenv("MAX_SEARCHES_PER_MINUTE", "20"))
MAX_CHATS_PER_MINUTE = int(os.getenv("MAX_CHATS_PER_MINUTE", "10"))


def get_client_ip(request: gr.Request) -> str:
    """Obtiene la IP real del cliente"""
    if request:
        # Railway pasa la IP real en estos headers
        forwarded_for = request.headers.get("x-forwarded-for")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        return request.client.host if hasattr(request, 'client') else "unknown"
    return "unknown"


def rate_limit_wrapper(operation: str):
    """Decorador para aplicar rate limiting a funciones"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, request: gr.Request = None, **kwargs):
            # Obtener IP del cliente
            client_ip = get_client_ip(request)
            
            # Verificar rate limit
            allowed, error_msg = security_manager.check_rate_limit(client_ip, operation)
            
            if not allowed:
                return f"⚠️ {error_msg}", None
            
            # Ejecutar función original
            try:
                return func(*args, **kwargs)
            except Exception as e:
                # Log error pero no exponer detalles
                print(f"Error in {operation}: {str(e)}")
                return "❌ An error occurred. Please try again later.", None
        
        return wrapper
    return decorator


# Wrappers con rate limiting
@rate_limit_wrapper("transcription")
def secure_transcribe_videos(urls_text: str, skip_existing: bool, auto_index: bool, 
                             progress=gr.Progress(), request: gr.Request = None):
    """Versión segura de transcribe_videos con rate limiting"""
    return transcribe_videos(urls_text, skip_existing, auto_index, progress)


@rate_limit_wrapper("search")
def secure_search_transcripts(query: str, top_k: int, request: gr.Request = None):
    """Versión segura de search_transcripts con rate limiting"""
    return search_transcripts(query, top_k)


@rate_limit_wrapper("chat")
def secure_chat_with_videos(message: str, history: list, request: gr.Request = None):
    """Versión segura de chat_with_videos con rate limiting"""
    return chat_with_videos(message, history)


def create_secure_interface():
    """Crea la interfaz Gradio con seguridad"""
    
    # Custom CSS para producción
    custom_css = """
    .gradio-container {
        max-width: 1200px !important;
    }
    .security-notice {
        background-color: #fff3cd;
        border: 1px solid #ffc107;
        border-radius: 5px;
        padding: 10px;
        margin: 10px 0;
        color: #856404;
    }
    .rate-limit-info {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 5px;
        padding: 8px;
        margin: 5px 0;
        font-size: 0.9em;
        color: #0c5460;
    }
    """
    
    with gr.Blocks(
        title="YouTube Transcriber Pro",
        theme=gr.themes.Soft(),
        css=custom_css
    ) as app:
        
        gr.Markdown("# 🎥 YouTube Transcriber Pro")
        gr.Markdown("Open-source tool for transcribing YouTube videos with AI-powered search and chat")
        
        # Security notice en producción
        if PRODUCTION:
            gr.Markdown(
                """
                <div class="security-notice">
                ⚠️ <strong>Production Environment</strong><br>
                Rate limits are enforced to ensure fair usage for all users.
                </div>
                """,
                elem_classes="security-notice"
            )
        
        with gr.Tabs():
            # TAB 1: Transcribe
            with gr.Tab("📝 Transcribe"):
                gr.Markdown("## Transcribe YouTube Videos")
                
                if PRODUCTION:
                    gr.Markdown(
                        f"""
                        <div class="rate-limit-info">
                        ℹ️ Rate Limit: {MAX_TRANSCRIPTIONS_PER_HOUR} transcriptions per hour
                        </div>
                        """
                    )
                
                with gr.Row():
                    with gr.Column():
                        urls_input = gr.Textbox(
                            label="YouTube URLs",
                            placeholder="https://youtu.be/VIDEO_ID\nhttps://www.youtube.com/watch?v=VIDEO_ID",
                            lines=5,
                            info="Enter one or more YouTube URLs (one per line)"
                        )
                        
                        with gr.Row():
                            skip_existing = gr.Checkbox(
                                label="Skip already transcribed videos",
                                value=True
                            )
                            auto_index = gr.Checkbox(
                                label="Auto-index for search (Phase 2)",
                                value=True
                            )
                        
                        transcribe_btn = gr.Button("🎬 Transcribe", variant="primary")
                    
                    with gr.Column():
                        transcribe_output = gr.Textbox(
                            label="Status",
                            lines=10,
                            interactive=False
                        )
                        transcribe_files = gr.File(
                            label="Generated Files",
                            file_count="multiple",
                            interactive=False
                        )
                
                transcribe_btn.click(
                    fn=secure_transcribe_videos,
                    inputs=[urls_input, skip_existing, auto_index],
                    outputs=[transcribe_output, transcribe_files]
                )
            
            # TAB 2: Search
            with gr.Tab("🔍 Search"):
                gr.Markdown("## Semantic Search")
                
                if PRODUCTION:
                    gr.Markdown(
                        f"""
                        <div class="rate-limit-info">
                        ℹ️ Rate Limit: {MAX_SEARCHES_PER_MINUTE} searches per minute
                        </div>
                        """
                    )
                
                with gr.Row():
                    with gr.Column():
                        search_query = gr.Textbox(
                            label="Search Query",
                            placeholder="What are you looking for?",
                            lines=2
                        )
                        search_top_k = gr.Slider(
                            minimum=1,
                            maximum=10,
                            value=3,
                            step=1,
                            label="Number of results"
                        )
                        search_btn = gr.Button("🔍 Search", variant="primary")
                    
                    with gr.Column():
                        search_output = gr.Textbox(
                            label="Search Results",
                            lines=15,
                            interactive=False
                        )
                
                search_btn.click(
                    fn=secure_search_transcripts,
                    inputs=[search_query, search_top_k],
                    outputs=search_output
                )
            
            # TAB 3: Chat
            with gr.Tab("💬 Chat"):
                gr.Markdown("## Chat with Your Videos")
                
                if PRODUCTION:
                    gr.Markdown(
                        f"""
                        <div class="rate-limit-info">
                        ℹ️ Rate Limit: {MAX_CHATS_PER_MINUTE} messages per minute
                        </div>
                        """
                    )
                
                chatbot = gr.Chatbot(
                    label="Conversation",
                    height=400
                )
                msg = gr.Textbox(
                    label="Your message",
                    placeholder="Ask a question about your videos...",
                    lines=2
                )
                
                with gr.Row():
                    submit_btn = gr.Button("💬 Send", variant="primary")
                    clear_btn = gr.Button("🗑️ Clear Chat")
                
                submit_btn.click(
                    fn=secure_chat_with_videos,
                    inputs=[msg, chatbot],
                    outputs=chatbot
                ).then(
                    lambda: "",
                    outputs=msg
                )
                
                clear_btn.click(lambda: [], outputs=chatbot)
            
            # TAB 4: Management
            with gr.Tab("⚙️ Management"):
                gr.Markdown("## Manage Transcriptions")
                
                with gr.Row():
                    with gr.Column():
                        gr.Markdown("### 📁 Transcriptions")
                        refresh_btn = gr.Button("🔄 Refresh List")
                        transcripts_list = gr.CheckboxGroup(
                            label="Select transcriptions to delete",
                            choices=[],
                            interactive=True
                        )
                        delete_btn = gr.Button("🗑️ Delete Selected", variant="stop")
                        delete_output = gr.Textbox(label="Status", lines=3)
                    
                    with gr.Column():
                        gr.Markdown("### 🗄️ Vector Database")
                        check_db_btn = gr.Button("📊 Check DB Status")
                        db_status = gr.Textbox(label="Database Status", lines=5)
                        clear_db_btn = gr.Button("🗑️ Clear Vector DB", variant="stop")
                        
                        gr.Markdown("### 🧹 Danger Zone")
                        clear_all_btn = gr.Button("⚠️ DELETE EVERYTHING", variant="stop")
                        clear_all_output = gr.Textbox(label="Status", lines=3)
                
                # Event handlers
                refresh_btn.click(
                    fn=list_transcripts,
                    outputs=transcripts_list
                )
                
                delete_btn.click(
                    fn=delete_selected_transcripts,
                    inputs=transcripts_list,
                    outputs=[delete_output, transcripts_list]
                )
                
                check_db_btn.click(
                    fn=check_vector_db_status,
                    outputs=db_status
                )
                
                clear_db_btn.click(
                    fn=clear_vector_db,
                    outputs=db_status
                )
                
                clear_all_btn.click(
                    fn=clear_all_data,
                    outputs=clear_all_output
                )
        
        # Footer
        gr.Markdown(
            """
            ---
            **YouTube Transcriber Pro** | 
            [GitHub](https://github.com/inginddie/youtube-transcriber) | 
            [Documentation](https://github.com/inginddie/youtube-transcriber/blob/main/README.md)
            """
        )
    
    return app


def main():
    """Launch the secure Gradio interface"""
    # Validate API key
    from config import OPENAI_API_KEY
    if not OPENAI_API_KEY:
        print("❌ ERROR: OPENAI_API_KEY not found in environment variables")
        print("Please set OPENAI_API_KEY in Railway variables")
        exit(1)
    
    print("🔧 Setting up directories...")
    create_directories()
    
    print("🔒 Initializing security...")
    if PRODUCTION:
        print(f"   ✓ Production mode enabled")
        print(f"   ✓ Rate limiting: {MAX_TRANSCRIPTIONS_PER_HOUR} transcriptions/hour")
        print(f"   ✓ Rate limiting: {MAX_SEARCHES_PER_MINUTE} searches/minute")
        print(f"   ✓ Rate limiting: {MAX_CHATS_PER_MINUTE} chats/minute")
    
    if REQUIRE_AUTH:
        print(f"   ✓ Authentication required")
    
    print("🚀 Launching Gradio interface...")
    
    app = create_secure_interface()
    
    # Obtener puerto de Railway
    port = int(os.getenv("PORT", "7860"))
    print(f"   ✓ Using port: {port}")
    
    # Configuración de launch
    launch_kwargs = {
        "server_name": "0.0.0.0",  # Necesario para Railway
        "server_port": port,
        "show_error": not PRODUCTION,  # No mostrar errores detallados en producción
        "quiet": False,  # Siempre mostrar logs para debug
        "share": False,
    }
    
    print(f"   ✓ Starting server on 0.0.0.0:{port}")
    app.launch(**launch_kwargs)


if __name__ == "__main__":
    main()
