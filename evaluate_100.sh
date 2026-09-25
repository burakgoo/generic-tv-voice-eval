#!/bin/bash
source venv/bin/activate
export GOOGLE_CLOUD_PROJECT="agy-coding"
export GOOGLE_CLOUD_LOCATION="global"
export GOOGLE_GENAI_USE_ENTERPRISE="true"
unset GOOGLE_APPLICATION_CREDENTIALS
python3 evaluate_cymbal.py prompts/v2_optimized.md --output results_100.json --sample 1.0
