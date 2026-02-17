"""
RAG Engine for YouTube Transcriber Pro - Phase 2
Handles embeddings, vector storage, and conversational chat
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma

from src.logger import setup_logger

logger = setup_logger("rag_engine")

from config import (
    CHAT_MODEL,
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    EMBEDDING_MODEL,
    OPENAI_API_KEY,
    TEMPERATURE,
    TOP_K_RESULTS,
    TRANSCRIPTS_DIR,
    VECTOR_DB_DIR,
)


class RAGEngine:
    """RAG engine for semantic search and chat over transcripts"""

    def __init__(self):
        self.embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL, openai_api_key=OPENAI_API_KEY)

        self.llm = ChatOpenAI(
            model=CHAT_MODEL, temperature=TEMPERATURE, openai_api_key=OPENAI_API_KEY
        )

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP, length_function=len
        )

        self.vector_store = None
        self.conversation_chain = None
        self.memory = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True, output_key="answer"
        )

    def load_transcripts(self) -> List[Dict[str, Any]]:
        """Load all transcript JSON files"""
        transcripts = []

        if not TRANSCRIPTS_DIR.exists():
            return transcripts

        for json_file in TRANSCRIPTS_DIR.glob("*.json"):
            try:
                with open(json_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    transcripts.append(data)
            except Exception:
                logger.exception(f"Could not load transcript {json_file}")

        return transcripts

    def index_transcripts(self, progress_callback: Optional[callable] = None):
        """Create vector embeddings and index all transcripts"""
        # IMPORTANTE: Limpiar Vector DB existente primero
        import shutil

        if VECTOR_DB_DIR.exists():
            if progress_callback:
                progress_callback("🗑️ Limpiando Vector DB anterior...")
            shutil.rmtree(VECTOR_DB_DIR)
            VECTOR_DB_DIR.mkdir(parents=True, exist_ok=True)

        transcripts = self.load_transcripts()

        if not transcripts:
            raise ValueError("No transcripts found to index")

        documents = []
        metadatas = []

        for transcript in transcripts:
            # Split transcript into chunks
            chunks = self.text_splitter.split_text(transcript["transcript"])

            for i, chunk in enumerate(chunks):
                documents.append(chunk)
                metadatas.append(
                    {
                        "video_id": transcript["video_id"],
                        "title": transcript["title"],
                        "url": transcript["url"],
                        "chunk_index": i,
                        "total_chunks": len(chunks),
                    }
                )

            if progress_callback:
                progress_callback(f"Indexed: {transcript['title']}")

        # Create vector store
        self.vector_store = Chroma.from_texts(
            texts=documents,
            embedding=self.embeddings,
            metadatas=metadatas,
            persist_directory=str(VECTOR_DB_DIR),
        )

        if progress_callback:
            progress_callback(f"✅ Indexed {len(transcripts)} videos, {len(documents)} chunks")

    def load_vector_store(self):
        """Load existing vector store"""
        if not VECTOR_DB_DIR.exists() or not any(VECTOR_DB_DIR.iterdir()):
            raise ValueError("Vector store not found. Please index transcripts first.")

        self.vector_store = Chroma(
            persist_directory=str(VECTOR_DB_DIR), embedding_function=self.embeddings
        )

    def setup_conversation_chain(self):
        """Setup conversational retrieval chain"""
        if not self.vector_store:
            raise ValueError("Vector store not initialized")

        # Custom prompt template
        prompt_template = """Eres un asistente experto que ayuda a analizar transcripciones de videos de YouTube.

Contexto de los videos:
{context}

Historial de conversación:
{chat_history}

Pregunta del usuario: {question}

Instrucciones:
- Responde SOLO basándote en el contexto proporcionado
- Si no tienes información suficiente, dilo claramente
- Siempre cita la fuente (título del video) cuando respondas
- Sé conciso pero completo
- Si hay múltiples videos relevantes, menciónalos todos

Respuesta:"""

        PROMPT = PromptTemplate(
            template=prompt_template, input_variables=["context", "chat_history", "question"]
        )

        self.conversation_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.vector_store.as_retriever(search_kwargs={"k": TOP_K_RESULTS}),
            memory=self.memory,
            combine_docs_chain_kwargs={"prompt": PROMPT},
            return_source_documents=True,
        )

    def chat(self, question: str) -> Dict[str, Any]:
        """
        Ask a question and get an answer with sources

        Args:
            question: User question

        Returns:
            Dictionary with answer and source documents
        """
        if not self.conversation_chain:
            self.setup_conversation_chain()

        result = self.conversation_chain({"question": question})

        # Format sources
        sources = []
        seen_videos = set()

        for doc in result.get("source_documents", []):
            video_id = doc.metadata.get("video_id")
            if video_id not in seen_videos:
                sources.append(
                    {
                        "title": doc.metadata.get("title"),
                        "url": doc.metadata.get("url"),
                        "video_id": video_id,
                    }
                )
                seen_videos.add(video_id)

        return {
            "answer": result["answer"],
            "sources": sources,
            "source_documents": result.get("source_documents", []),
        }

    def search(self, query: str, k: int = TOP_K_RESULTS) -> List[Dict[str, Any]]:
        """
        Semantic search over transcripts

        Args:
            query: Search query
            k: Number of results to return

        Returns:
            List of relevant chunks with metadata
        """
        if not self.vector_store:
            raise ValueError("Vector store not initialized")

        results = self.vector_store.similarity_search_with_score(query, k=k)

        formatted_results = []
        for doc, score in results:
            formatted_results.append(
                {"content": doc.page_content, "score": float(score), "metadata": doc.metadata}
            )

        return formatted_results

    def reset_conversation(self):
        """Reset conversation memory"""
        self.memory.clear()
