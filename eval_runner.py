import argparse
import logging
import csv
import os
from eval_engine import EvaluationEngine

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("eval_runner")

def main():
    logger.info("Initializing Evaluation Engine using config config.yaml...")
    engine = EvaluationEngine(config_path="config.yaml")
    
    dataset_path = "data/golden_dataset.csv"
    asset_bucket = os.environ.get("ASSET_BUCKET", "cymbal-tv-voice-test-harness")
    
    if not os.path.exists(dataset_path):
        logger.error(f"Cannot find {dataset_path} inside container.")
        return
        
    with open(dataset_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            file_rel = row.get("audio_file", "") # e.g. data/sample_0.wav
            if not file_rel:
                continue
                
            file_uri = f"gs://{asset_bucket}/{file_rel}"
            expected = row.get("expected_intent", "")
            
            logger.info(f"Evaluating utterance from {file_uri} (Expected: {expected})...")
            try:
                results = engine.evaluate_utterance(file_uri, expected)
                logger.info(f"Results for {file_rel}: {results}")
            except Exception as e:
                logger.error(f"Error during evaluation of {file_uri}: {e}")

    logger.info("Batch Evaluation loop complete.")

if __name__ == '__main__':
    main()
