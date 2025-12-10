import os
from typing import List, Dict, Any
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import TextLoader, DirectoryLoader, PythonLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from core.config import settings

class RAGService:
    """
    Production-grade RAG service using ChromaDB and HuggingFace Embeddings.
    Handles ingestion of code repositories and semantic retrieval.
    """
    
    def __init__(self):
        self.persist_directory = os.path.join(settings.WORKSPACE_DIR, "chroma_db")
        
        # Use a robust local embedding model
        self.embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'}
        )
        
        self.vector_store = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings,
            collection_name="github_agent_memory"
        )
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )

    def ingest_repository(self, repo_path: str) -> int:
        """
        Ingests a local repository into the vector store.
        Returns the number of chunks added.
        """
        print(f"[RAG] Ingesting repository from {repo_path}...")
        
        # Load Python files (can be expanded to other types)
        loader = DirectoryLoader(
            repo_path, 
            glob="**/*.py", 
            loader_cls=PythonLoader,
            use_multithreading=True
        )
        documents = loader.load()
        
        if not documents:
            print("[RAG] No documents found to ingest.")
            return 0
            
        # Split documents
        chunks = self.text_splitter.split_documents(documents)
        
        # Add metadata
        for chunk in chunks:
            chunk.metadata["source_repo"] = repo_path
            
        # Index chunks
        self.vector_store.add_documents(chunks)
        self.vector_store.persist()
        
        print(f"[RAG] Successfully indexed {len(chunks)} code chunks.")
        return len(chunks)

    def retrieve_context(self, query: str, k: int = 5) -> List[str]:
        """
        Retrieves relevant code snippets based on semantic similarity.
        """
        docs = self.vector_store.similarity_search(query, k=k)
        return [doc.page_content for doc in docs]

    def clear_memory(self):
        """
        Clears the vector store.
        """
        self.vector_store.delete_collection()
        self.vector_store = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings,
            collection_name="github_agent_memory"
        )
        self.vector_store.persist()

rag_service = RAGService()
