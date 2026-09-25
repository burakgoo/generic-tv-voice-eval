# Generic TV Voice Evaluation Framework

This repository provides a reproducible, cloud-native evaluation framework for assessing the performance of TV voice assistants. It is designed to be easily cloneable and deployable by Customer Engineers (CEs).

## Architecture Approach
To ensure high reproducibility and ease of deployment:
- **Local Data ➔ Cloud Data**: All golden test datasets and audio assets are checked into this GitHub repository. A setup script pushes these assets to a Google Cloud Storage (GCS) bucket in your project upon initialization.
- **Execution Engine**: The test suite is packaged and deployed as a **Cloud Run Job**. Cloud Run Jobs are ideal for batch execution of evaluation suites without encountering strict serverless timeouts.
- **Evaluation**: We utilize **Vertex AI Evaluation (`EvalTask`)** as an LLM-as-a-judge to semantically grade the assistant's responses and generate synthetic test variations.

## Quickstart

1. **Clone the repository**
2. **Update Configuration**
   Edit `config.yaml` to include your Google Cloud Project ID and desired GCS bucket name.
3. **Run Setup**
   Execute the setup script (which will push `./data` to your GCS bucket and deploy the Cloud Run Job):
   ```bash
   ./setup.sh
   ```
4. **Execute an Evaluation Suite**
   ```bash
   gcloud run jobs execute tv-voice-eval-job --region=us-central1
   ```

For a visual breakdown of the architecture, please view `flowchart.md`.

## IAM Prerequisites
If you are deploying from source (`--source .`), ensure that your default Compute service account (`[PROJECT_NUMBER]-compute@developer.gserviceaccount.com`) has the following IAM roles:
- `roles/storage.objectViewer` (to read the uploaded zipped source file)
- `roles/artifactregistry.writer` (to push the built Docker container)

This allows Cloud Build to function successfully in your isolated environment!

## API Prerequisites
Before deploying the framework, you must ensure that your Google Cloud Project has the following APIs enabled:
- Cloud Run API (`run.googleapis.com`)
- Cloud Build API (`cloudbuild.googleapis.com`)
- Artifact Registry API (`artifactregistry.googleapis.com`)
- Vertex AI API (`aiplatform.googleapis.com`) - *Crucial for the LLM evaluation logic to avoid runtime crashes!*

You can enable these individually via the GCP Console or by running:
`gcloud services enable run.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com aiplatform.googleapis.com`
