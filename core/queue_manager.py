import os
import json
import logging
from queue import Queue

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(message)s')

class TargetQueueManager:
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.execution_queue = Queue()
        
    def load_targets(self) -> bool:
        if not os.path.exists(self.config_path):
            logging.error(f"Critical Configuration Failure: Target file not found at {self.config_path}")
            return False
        try:
            with open(self.config_path, 'r', encoding='utf-8') as file:
                config_data = json.load(file)
            targets_list = config_data.get("targets", [])
            if not targets_list:
                logging.warning("Target validation warning: Configuration file contains an empty target pool.")
                return False
            for target in targets_list:
                self.execution_queue.put(target)
                logging.info(f"Target successfully queued into Veritas pipeline ➔ Node ID: {target.get('site_id')}")
            logging.info(f"Pipeline Initialization Success: Total targets enqueued: {self.execution_queue.qsize()}")
            return True
        except Exception as e:
            logging.error(f"System Level Initialization Exception: {e}")
            return False

    def fetch_next_target(self) -> dict:
        if not self.execution_queue.empty():
            return self.execution_queue.get()
        return None
