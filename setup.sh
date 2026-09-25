#!/bin/bash
set -e

PROJECT_ID=$(grep 'project_id:' config.yaml | awk -F '"' '{print $2}')
BUCKET=$(grep 'gcs_asset_bucket:' config.yaml | awk -F '"' '{print $2}')
REGION=$(grep 'region:' config.yaml | awk -F '"' '{print $2}')

if [ -z "$BUCKET" ]; then
    BUCKET="cymbal-tv-voice-assets-$RANDOM"
    echo "Creating GCS bucket $BUCKET in $PROJECT_ID..."
    # Create bucket
    gcloud storage buckets create gs://$BUCKET --project=$PROJECT_ID --location=$REGION || true
    # Update local config
    sed -i "s/gcs_asset_bucket: \"\"/gcs_asset_bucket: \"$BUCKET\"/g" config.yaml
else
    echo "Using configured bucket gs://$BUCKET"
fi

echo "Provisioning BigQuery pipeline dashboards..."
bq mk -d --location=$REGION cymbal-tv-voice:eval_results || true
cat << 'EOF' > bq_schema.json
[
  {"name": "run_timestamp", "type": "TIMESTAMP"},
  {"name": "audio_file", "type": "STRING"},
  {"name": "expected_intent", "type": "STRING"},
  {"name": "transcript", "type": "STRING"},
  {"name": "determined_intent", "type": "STRING"},
  {"name": "exact_match_score", "type": "FLOAT"},
  {"name": "bleu_score", "type": "FLOAT"}
]
EOF
bq mk --table cymbal-tv-voice:eval_results.runs bq_schema.json || echo "table already exists"
rm bq_schema.json

echo "Uploading local datasets to GCS..."
mkdir -p data # ensure it exists
echo "Uploading golden evaluation dataset audio clips (*.wav) and mapping tables if they exist locally..."
gcloud storage cp -r data/ gs://$BUCKET/data/ || echo "Upload finished or skipped"

echo "Bootstrapping GCP APIs and IAM roles..."
gcloud services enable run.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com aiplatform.googleapis.com || true

PROJECT_NUM=$(gcloud projects describe $PROJECT_ID --format="value(projectNumber)")
COMPUTE_SA="${PROJECT_NUM}-compute@developer.gserviceaccount.com"

gcloud projects add-iam-policy-binding $PROJECT_ID --member="serviceAccount:$COMPUTE_SA" --role="roles/storage.objectViewer" || true
gcloud projects add-iam-policy-binding $PROJECT_ID --member="serviceAccount:$COMPUTE_SA" --role="roles/artifactregistry.writer" || true
gcloud projects add-iam-policy-binding $PROJECT_ID --member="serviceAccount:$COMPUTE_SA" --role="roles/aiplatform.user" || true
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$PROJECT_NUMBER-compute@developer.gserviceaccount.com" \
  --role="roles/bigquery.dataEditor"

echo "Deploying to Cloud Run Jobs..."
if [ ! -f Dockerfile ]; then
    echo "FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD [\"python\", \"eval_runner.py\"]" > Dockerfile
fi

if [ ! -f requirements.txt ]; then
    echo "google-cloud-aiplatform[evaluation]
pyyaml" > requirements.txt
fi

gcloud run jobs deploy tv-voice-eval-job \
  --source . \
  --region $REGION \
  --project $PROJECT_ID \
  --set-env-vars="ASSET_BUCKET=$BUCKET" \
  --execute-now

echo "Setup Complete!"
