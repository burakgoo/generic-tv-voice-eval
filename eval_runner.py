import argparse
import logging
from eval_engine import EvaluationEngine

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("eval_runner")

def main():
    parser = argparse.ArgumentParser(description="Evaluate a TV Voice audio file.")
    parser.add_argument("--audio_file", default="gs://cymbal-tv-voice-test-harness/dummy.wav", help="Path to the audio file")
    parser.add_argument("--expected_intent", default="Switch to Channel 1", help="The expected canonical intent")
    parser.add_argument("--config", default="config.yaml", help="Path to config file")
    args = parser.parse_args()

    logger.info(f"Initializing Evaluation Engine using config {args.config}...")
    engine = EvaluationEngine(config_path=args.config)
    
    logger.info(f"Evaluating utterance from {args.audio_file} (Expected: {args.expected_intent})...")
    try:
        results = engine.evaluate_utterance(args.audio_file, args.expected_intent)
        logger.info("Evaluation complete.")
        logger.info(f"Results: {results}")
    except Exception as e:
        logger.error(f"Error during evaluation: {e}")

if __name__ == '__main__':
    main()
