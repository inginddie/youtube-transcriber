"""
Unit tests for RAG engine module
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import json
import tempfile

from src.rag_engine import RAGEngine


class TestRAGEngine:
    """Tests for RAGEngine class"""
    
    @pytest.fixture
    def rag_engine(self):
        """Create RAG engine instance for testing"""
        with patch('src.rag_engine.OpenAIEmbeddings'), \
             patch('src.rag_engine.ChatOpenAI'):
            return RAGEngine()
    
    @pytest.fixture
    def sample_transcripts(self):
        """Sample transcript data"""
        return [
            {
                "video_id": "test1",
                "title": "Test Video 1",
                "url": "https://youtu.be/test1",
                "transcript": "This is a test transcript about machine learning.",
                "word_count": 8
            },
            {
                "video_id": "test2",
                "title": "Test Video 2",
                "url": "https://youtu.be/test2",
                "transcript": "Another test transcript about artificial intelligence.",
                "word_count": 7
            }
        ]
    
    def test_initialization(self, rag_engine):
        """Test RAG engine initializes correctly"""
        assert rag_engine.embeddings is not None
        assert rag_engine.llm is not None
        assert rag_engine.text_splitter is not None
        assert rag_engine.vector_store is None
        assert rag_engine.conversation_chain is None
    
    def test_load_transcripts_empty_directory(self, rag_engine):
        """Test loading transcripts from empty directory"""
        with patch('src.rag_engine.TRANSCRIPTS_DIR') as mock_dir:
            mock_dir.exists.return_value = False
            
            transcripts = rag_engine.load_transcripts()
            
            assert transcripts == []
    
    def test_load_transcripts_with_files(self, rag_engine, sample_transcripts):
        """Test loading transcripts from directory with files"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            
            # Create sample JSON files
            for i, transcript in enumerate(sample_transcripts):
                json_path = tmpdir_path / f"test_{i}.json"
                with open(json_path, 'w') as f:
                    json.dump(transcript, f)
            
            with patch('src.rag_engine.TRANSCRIPTS_DIR', tmpdir_path):
                transcripts = rag_engine.load_transcripts()
                
                assert len(transcripts) == 2
                assert transcripts[0]['video_id'] in ['test1', 'test2']
    
    @patch('src.rag_engine.Chroma')
    def test_index_transcripts_no_transcripts(self, mock_chroma, rag_engine):
        """Test indexing with no transcripts raises error"""
        with patch.object(rag_engine, 'load_transcripts', return_value=[]):
            with pytest.raises(ValueError, match="No transcripts found"):
                rag_engine.index_transcripts()
    
    @patch('src.rag_engine.Chroma')
    def test_index_transcripts_success(
        self, 
        mock_chroma, 
        rag_engine, 
        sample_transcripts
    ):
        """Test successful transcript indexing"""
        with patch.object(rag_engine, 'load_transcripts', return_value=sample_transcripts):
            mock_vector_store = MagicMock()
            mock_chroma.from_texts.return_value = mock_vector_store
            
            rag_engine.index_transcripts()
            
            assert rag_engine.vector_store is not None
            mock_chroma.from_texts.assert_called_once()
    
    @patch('src.rag_engine.Chroma')
    def test_load_vector_store_not_found(self, mock_chroma, rag_engine):
        """Test loading non-existent vector store"""
        with patch('src.rag_engine.VECTOR_DB_DIR') as mock_dir:
            mock_dir.exists.return_value = False
            
            with pytest.raises(ValueError, match="Vector store not found"):
                rag_engine.load_vector_store()
    
    @patch('src.rag_engine.Chroma')
    def test_load_vector_store_success(self, mock_chroma, rag_engine):
        """Test successful vector store loading"""
        with patch('src.rag_engine.VECTOR_DB_DIR') as mock_dir:
            mock_dir.exists.return_value = True
            mock_dir.iterdir.return_value = [Path("test_file")]
            
            mock_vector_store = MagicMock()
            mock_chroma.return_value = mock_vector_store
            
            rag_engine.load_vector_store()
            
            assert rag_engine.vector_store is not None
    
    def test_setup_conversation_chain_no_vector_store(self, rag_engine):
        """Test setting up conversation chain without vector store"""
        with pytest.raises(ValueError, match="Vector store not initialized"):
            rag_engine.setup_conversation_chain()
    
    @patch('src.rag_engine.ConversationalRetrievalChain')
    def test_setup_conversation_chain_success(self, mock_chain, rag_engine):
        """Test successful conversation chain setup"""
        rag_engine.vector_store = MagicMock()
        
        mock_chain_instance = MagicMock()
        mock_chain.from_llm.return_value = mock_chain_instance
        
        rag_engine.setup_conversation_chain()
        
        assert rag_engine.conversation_chain is not None
        mock_chain.from_llm.assert_called_once()
    
    def test_chat_without_chain(self, rag_engine):
        """Test chat without initialized chain"""
        rag_engine.vector_store = MagicMock()
        
        with patch.object(rag_engine, 'setup_conversation_chain'):
            with patch.object(
                rag_engine, 
                'conversation_chain', 
                MagicMock(return_value={
                    'answer': 'Test answer',
                    'source_documents': []
                })
            ):
                result = rag_engine.chat("Test question")
                
                assert 'answer' in result
                assert 'sources' in result
    
    def test_search_without_vector_store(self, rag_engine):
        """Test search without initialized vector store"""
        with pytest.raises(ValueError, match="Vector store not initialized"):
            rag_engine.search("test query")
    
    def test_search_success(self, rag_engine):
        """Test successful semantic search"""
        mock_vector_store = MagicMock()
        mock_doc = MagicMock()
        mock_doc.page_content = "Test content"
        mock_doc.metadata = {'video_id': 'test1', 'title': 'Test'}
        
        mock_vector_store.similarity_search_with_score.return_value = [
            (mock_doc, 0.95)
        ]
        
        rag_engine.vector_store = mock_vector_store
        
        results = rag_engine.search("test query", k=1)
        
        assert len(results) == 1
        assert results[0]['content'] == "Test content"
        assert results[0]['score'] == 0.95
        assert 'metadata' in results[0]
    
    def test_reset_conversation(self, rag_engine):
        """Test conversation memory reset"""
        rag_engine.memory = MagicMock()
        
        rag_engine.reset_conversation()
        
        rag_engine.memory.clear.assert_called_once()


class TestRAGIntegration:
    """Integration tests for RAG workflow"""
    
    @pytest.mark.integration
    def test_full_rag_workflow(self):
        """Test complete RAG workflow"""
        # This would be an integration test with real data
        # Skipped in unit tests
        pass
