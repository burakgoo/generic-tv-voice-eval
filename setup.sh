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

echo "Uploading local datasets to GCS..."
mkdir -p data # ensure it exists
gcloud storage cp -r data/ gs://$BUCKET/data/ || echo "Upload finished or skipped"

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
  --execute-now

echo "Setup Complete!"
