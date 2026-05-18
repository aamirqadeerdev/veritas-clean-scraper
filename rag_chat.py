import os
import json
import logging
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(message)s')

class LocalRAGSystem:
    def __init__(self):
        """Initializes a local database memory bank on your computer's drive."""
        logging.info("RAG System: Initializing free, local open-source AI embeddings...")
        # A lightweight open-source mathematical brain that helps compare sentence meanings
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.db_dir = "data/vector_db"
        self.vector_store = None

    def build_knowledge_base(self, json_file_path: str):
        """Reads our scraped text chunks and saves them into the vector memory database."""
        if not os.path.exists(json_file_path):
            logging.error(f"RAG Error: Scraped data file not found at {json_file_path}")
            return

        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        text_content = data.get("extracted_text", "")
        site_id = data.get("site_id", "web_node")

        logging.info(f"RAG System: Loading data from {site_id}. Splitting and indexing text blocks...")
        
        # Use a quick separator to break our clean data into a list of reading cards
        chunks = [text_content[i:i+500] for i in range(0, len(text_content), 450)]

        logging.info(f"RAG System: Writing {len(chunks)} text cards into the local Chroma Vector DB...")
        
        # Create and save our local mathematical memory folder
        self.vector_store = Chroma.from_texts(
            texts=chunks,
            embedding=self.embeddings,
            persist_directory=self.db_dir
        )
        logging.info(f"RAG Knowledge base built successfully! Saved locally at: {self.db_dir}")

    def ask_scraped_data(self, user_question: str):
        """Searches the database and retrieves the exact paragraph answers."""
        if not self.vector_store:
            # If the database already exists on disk, load it up instantly
            self.vector_store = Chroma(persist_directory=self.db_dir, embedding_function=self.embeddings)

        # Look up the 2 most relevant matches in our memory cards using vector math
        results = self.vector_store.similarity_search(user_question, k=2)
        
        print("\n=======================================================")
        print(f"🔎 USER QUESTION: {user_question}")
        print("=======================================================")
        print("🤖 RAG RETRIEVED ANSWER BLOCKS FROM YOUR SCRAPED DATA:")
        print("-------------------------------------------------------")
        for idx, doc in enumerate(results, 1):
            print(f"[Match {idx}]: {doc.page_content.strip()}\n")
        print("=======================================================\n")

if __name__ == "__main__":
    rag = LocalRAGSystem()
    
    # 1. Feed our scraped Python Docs dataset into the RAG memory bank
    target_json = "data/certified_training_data.json"
    rag.build_knowledge_base(target_json)
    
    # 2. Open an interactive console question-and-answer loop
    print("\n👋 Welcome to the Veritas RAG Interface!")
    print("You can now search and query your scraped website text data locally.")
    print("Type 'exit' or 'quit' to close the chat dashboard.\n")
    
    while True:
        query = input("Ask a question about the scraped website: ")
        if query.lower() in ['exit', 'quit']:
            print("Shutting down RAG chat interface. Goodbye!")
            break
        if query.strip():
            rag.ask_scraped_data(query)

