import unittest
from eval_engine import EvaluationEngine

class TestEvalEngine(unittest.TestCase):
    def test_evaluation_engine_throws_error_on_failure(self):
        engine = EvaluationEngine(config_path="test_config.yaml")    
        with self.assertRaisesRegex(ValueError, "Failed to evaluate utterance"):
            engine.evaluate_utterance(audio_file="invalid.wav", expected_intent="TV__SEARCH")

if __name__ == '__main__':
    unittest.main()
