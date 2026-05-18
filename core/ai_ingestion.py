
import os
import json
import logging
from langchain_text_splitters import RecursiveCharacterTextSplitter

class AIIngestionStorage:
    def __init__(self, output_dir: str = "data"):
        """Initializes the data storage directory framework."""
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def save_to_json(self, data: dict, filename: str = "certified_training_data.json") -> str:
        """Saves the verified structured document block into our local file database."""
        target_path = os.path.join(self.output_dir, filename)
        
        try:
            # Save our clean data with spaces and indents so it is easy to read
            with open(target_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            logging.info(f"Storage System: Verified data block written safely to disk at {target_path}")
            return target_path
        except Exception as e:
            logging.error(f"Storage Failure: Could not export dataset structure: {e}")
            return ""

    def simulate_rag_chunking(self, validated_data: dict):
        """Uses LangChain tools to slice large text blocks down into optimized AI chunks."""
        text_content = validated_data.get("extracted_text", "")
        
        logging.info("AI Ingestion: Preparing LangChain splitters for data compilation...")
        
        # Configure a smart text cutter that slices paragraphs at natural punctuation marks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,       # Each AI reading card will be around 500 characters long
            chunk_overlap=50      # Keeps 50 characters of context from the previous card so thoughts don't get cut off
        )
        
        # Run the text slicer
        ai_chunks = text_splitter.split_text(text_content)
        
        logging.info(f"AI Ingestion: Successfully indexed and generated {len(ai_chunks)} clean text context chunks!")
        
        # Display a preview of the processed text fragments
        if ai_chunks:
            logging.info(f"AI Chunk 1 Preview: {ai_chunks[0][:120]}...")

