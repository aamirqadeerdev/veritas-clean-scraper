
import os
import asyncio
from core.queue_manager import TargetQueueManager
from core.compliance import EthicalComplianceGate, logging
from core.extraction_engine import AsynchronousExtractor
from core.validation_gateway import DataValidationGateway
from core.ai_ingestion import AIIngestionStorage

async def main():
    logging.info("=============================================")
    logging.info("      LAUNCHING VERITAS CLEAN SCRAPER        ")
    logging.info("=============================================")
    
    config_file_path = os.path.join("config", "targets.json")
    pipeline_queue = TargetQueueManager(config_path=config_file_path)
    
    compliance_gate = EthicalComplianceGate()
    extractor = AsynchronousExtractor()
    validator = DataValidationGateway()
    # Initialize our new storage and LangChain ingestion layer
    ai_storage = AIIngestionStorage()
    
    if pipeline_queue.load_targets():
        logging.info("All Verification Checkpoints: READY.")
        
        next_job = pipeline_queue.fetch_next_target()
        target_url = next_job['url']
        
        logging.info(f"Processing Node: {next_job['site_id']} ➔ Initiating Verification.")
        
        # 1. Run the ethical compliance gate
        if compliance_gate.is_scraping_allowed(target_url):
            compliance_gate.enforce_politeness_delay()
            logging.info(f"Active Job Worker hand-off confirmed for node: {next_job['site_id']}")
            
            # 2. Run the extraction engine to get the text
            clean_text = await extractor.fetch_page_content(target_url)
            
            if clean_text:
                payload = {
                    "source_url": target_url,
                    "site_id": next_job['site_id'],
                    "extracted_text": clean_text
                }
                
                # 3. Run the validation and privacy gateway
                validated_data = validator.process_and_verify(payload)
                
                if validated_data:
                    # 4. RUN THE STORAGE EXPORTER
                    ai_storage.save_to_json(validated_data)
                    
                    # 5. RUN THE LANGCHAIN CHUNKER HANDSHAKE
                    ai_storage.simulate_rag_chunking(validated_data)
                    
                    logging.info("=============================================")
                    logging.info("   VERITAS PIPELINE RUN COMPLETE: SUCCESS!   ")
                    logging.info("=============================================")
                else:
                    logging.error("Document rejected by validation gateway.")
            else:
                logging.error("Extraction failed or empty payload generated.")
        else:
            logging.error(f"Skipping job node [{next_job['site_id']}] due to compliance failure.")
            
    else:
        logging.error("Pipeline initialization sequence failed.")

if __name__ == "__main__":
    asyncio.run(main())

