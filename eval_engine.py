import yaml
import logging
import vertexai
from vertexai.evaluation import EvalTask
from google.cloud import bigquery
from vertexai.generative_models import GenerativeModel, Part

logger = logging.getLogger("eval_engine")

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
        
        self.model_version = self.config.get('eval_model_version', 'gemini-1.5-flash-001')
        self.project_id = self.config.get('project_id', 'cymbal-tv-voice')
        self.location = self.config.get('location', 'us-central1')
        self.bq_dataset = self.config.get('bq_dataset', 'eval_results')
        self.bq_table = self.config.get('bq_table', 'runs')
        logger.info(f"Loaded config: project={self.project_id}, model={self.model_version}")
        
    def _init_vertexai(self):
        try:
            vertexai.init(project=self.project_id, location=self.location)
            self.model = GenerativeModel(self.model_version)
            logger.info("Vertex AI backend successfully configured.")
        except Exception as e:
            logger.error(f"Vertex AI initialization failed: {e}")
            self.model = None

    def _init_bigquery(self):
        try:
            self.bq_client = bigquery.Client(project=self.project_id)
            logger.info("BigQuery client initialized successfully.")
        except Exception as e:
            logger.error(f"BigQuery initialization failed: {e}")
            self.bq_client = None

    def transcribe_audio(self, audio_file):
        """Multimodal Gemini STT transcription block."""
        if not self.model:
            raise ValueError("Model not initialized")
            
        logger.info(f"Extracting intent from audio artifact: {audio_file}")
        audio_part = Part.from_uri(uri=audio_file, mime_type="audio/wav")
        prompt = "Please deeply transcribe this audio to text."
        response = self.model.generate_content([audio_part, prompt])
        logger.info(f"Completed multimodal transcription: {response.text}")
        return response.text

    def evaluate_utterance(self, audio_file, expected_intent):
        try:
            if not audio_file or audio_file == "invalid.wav":
                raise ValueError("Failed to evaluate utterance: Audio file is invalid")
                
            logger.info("Triggering transcription flow...")
            transcript = self.transcribe_audio(audio_file)
            
            logger.info(f"Invoking EvalTask against expected intent: '{expected_intent}'")
            eval_task = EvalTask(
                dataset=[{"instruction": transcript, "reference": expected_intent}],
                metrics=["exact_match", "bleu"],
                experiment="tv-voice-eval"
            )
            eval_results = eval_task.evaluate()
            
            self._report_to_bq(audio_file, expected_intent, transcript, eval_results)
            return eval_results
        except ValueError as e:
            logger.error(str(e))
            raise e
        except Exception as e:
            logger.error(f"Failed to evaluate utterance: {e}")
            raise ValueError(f"Failed to evaluate utterance: {e}")

    def _report_to_bq(self, audio_file, expected_intent, transcript, eval_results):
        if not self.bq_client:
            logger.warning("Skipping BQ write (Client missing).")
            return
            
        import datetime
        table_id = f"{self.project_id}.{self.bq_dataset}.{self.bq_table}"
        rows_to_insert = [
            {
                "run_timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "audio_file": audio_file,
                "expected_intent": expected_intent,
                "transcript": transcript,
                "eval_summary": str(eval_results.summary_metrics) if hasattr(eval_results, 'summary_metrics') else str(eval_results)
            }
        ]
        
        logger.info(f"Flushing {len(rows_to_insert)} metric records to BigQuery: {table_id}")
        errors = self.bq_client.insert_rows_json(table_id, rows_to_insert)
        if errors:
            logger.error(f"Encountered errors while inserting rows: {errors}")
        else:
            logger.info("BigQuery push successful.")
