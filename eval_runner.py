import argparse
from eval_engine import EvaluationEngine

def main():
    parser = argparse.ArgumentParser(description="Evaluate a TV Voice audio file.")
    parser.add_argument("audio_file", help="Path to the audio file")
    parser.add_argument("expected_intent", help="The expected canonical intent")
    parser.add_argument("--config", default="config.yaml", help="Path to config file")
    args = parser.parse_args()

    print(f"Initializing Evaluation Engine using config {args.config}...")
    engine = EvaluationEngine(config_path=args.config)
    
    print(f"Evaluating utterance from {args.audio_file} (Expected: {args.expected_intent})...")
    try:
        results = engine.evaluate_utterance(args.audio_file, args.expected_intent)
        print("Evaluation complete.")
        print(f"Results: {results}")
    except Exception as e:
        print(f"Error during evaluation: {e}")

if __name__ == '__main__':
    main()
