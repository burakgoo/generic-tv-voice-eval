import unittest
from unittest.mock import patch, MagicMock
from eval_engine import EvaluationEngine

class TestEvalVerification(unittest.TestCase):
    @patch('eval_engine.EvalTask')
    @patch('eval_engine.EvaluationEngine.transcribe_audio')
    @patch('eval_engine.bigquery.Client')
    def test_dummy_utterance_eval(self, mock_bq, mock_transcribe, mock_eval_task):
        mock_transcribe.return_value = "Switch to channel one"
        
        mock_eval_instance = MagicMock()
        base_results = MagicMock()
        base_results.summary_metrics = {"exact_match": 1.0, "bleu": 1.0}
        mock_eval_instance.evaluate.return_value = base_results
        mock_eval_task.return_value = mock_eval_instance

        engine = EvaluationEngine("test_config.yaml")
        # Ensure BQ client is set to the mocked one
        engine.bq_client = mock_bq.return_value
        engine.bq_client.insert_rows_json.return_value = []
        
        results = engine.evaluate_utterance("dummy.wav", "TV__SWITCH_CHANNEL")
        
        mock_transcribe.assert_called_once_with("dummy.wav")
        mock_eval_task.assert_called_once_with(
            dataset=[{"instruction": "Switch to channel one", "reference": "TV__SWITCH_CHANNEL"}],
            metrics=["exact_match", "bleu"],
            experiment="tv-voice-eval"
        )
        engine.bq_client.insert_rows_json.assert_called_once()
        print("Verification dummy test passed. Intent scored correctly.", results.summary_metrics)

if __name__ == '__main__':
    unittest.main()
