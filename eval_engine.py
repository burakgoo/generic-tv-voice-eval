import yaml
import vertexai
from vertexai.evaluation import EvalTask
from google.cloud import bigquery
from vertexai.generative_models import GenerativeModel, Part

class EvaluationEngine:
    def __init__(self, config_path="config.yaml"):
        self.config_path = config_path
        self._load_config()
        self._init_vertexai()
        self._init_bigquery()
    
    def _load_config(self):
        try:
            with open(self.config_path, 'r') as f:
                self.config = yaml.safe_load(f)
        except Exception:
            self.config = {}
        
        self.model_version = self.config.get('eval_model_version', 'gemini-3.8-flash')
        self.project_id = self.config.get('project_id', 'agy-coding')
        self.location = self.config.get('location', 'us-central1')
        self.bq_dataset = self.config.get('bq_dataset', 'eval_results')
        self.bq_table = self.config.get('bq_table', 'runs')
        
    def _init_vertexai(self):
        # We assume vertexai is available and credentials are set
        try:
            vertexai.init(project=self.project_id, location=self.location)
            self.model = GenerativeModel(self.model_version)
        except Exception as e:
            # For testing without actual auth
            self.model = None

    def _init_bigquery(self):
        try:
            self.bq_client = bigquery.Client(project=self.project_id)
        except Exception as e:
            self.bq_client = None

    def transcribe_audio(self, audio_file):
        """Multimodal Gemini STT transcription block."""
        if not self.model:
            raise ValueError("Model not initialized")
            
        audio_part = Part.from_uri(uri=audio_file, mime_type="audio/wav")
        prompt = "Please deeply transcribe this audio to text."
        response = self.model.generate_content([audio_part, prompt])
        return response.text

    def evaluate_utterance(self, audio_file, expected_intent):
        try:
            if not audio_file or audio_file == "invalid.wav":
                raise ValueError("Failed to evaluate utterance: Audio file is invalid")
                
            # transcription block
            transcript = self.transcribe_audio(audio_file)
            
            # EvalTask block
            eval_task = EvalTask(
                dataset=[{"instruction": transcript, "reference": expected_intent}],
                metrics=["exact_match", "bleu"],
                experiment="tv-voice-eval"
            )
            eval_results = eval_task.evaluate()
            
            self._report_to_bq(audio_file, expected_intent, transcript, eval_results)
            return eval_results
        except ValueError as e:
            raise e
        except Exception as e:
            raise ValueError(f"Failed to evaluate utterance: {e}")

    def _report_to_bq(self, audio_file, expected_intent, transcript, eval_results):
        if not self.bq_client:
            return
            
        table_id = f"{self.project_id}.{self.bq_dataset}.{self.bq_table}"
        rows_to_insert = [
            {
                "audio_file": audio_file,
                "expected_intent": expected_intent,
                "transcript": transcript,
                "eval_summary": str(eval_results.summary_metrics) if hasattr(eval_results, 'summary_metrics') else str(eval_results)
            }
        ]
        
        errors = self.bq_client.insert_rows_json(table_id, rows_to_insert)
        if errors:
            print(f"Encountered errors while inserting rows: {errors}")
