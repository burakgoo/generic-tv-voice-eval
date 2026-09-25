# Agent Instructions

- **General Rule**: Before starting to work or executing commands, provide a brief description of the planned actions to the user instead of executing commands and notifying them afterwards. Always obtain approval or alignment before proceeding with intrusive or significant actions.

- **Deployment Directive**: When initializing or deploying a Cloud Run Job from source, always verify that the default compute service account possesses `roles/storage.objectViewer` and `roles/artifactregistry.writer` IAM roles.

- **GCP Initialization Directive**: When scaffolding this project in a new GCP environment, agents must aggressively verify or enable the necessary APIs (`run.googleapis.com`, `cloudbuild.googleapis.com`, `artifactregistry.googleapis.com`, and `aiplatform.googleapis.com`) before triggering test suites to prevent live evaluation failures in Vertex.
- Ensure `roles/aiplatform.user` is added to the Compute Engine default service account to prevent inference termination blocks.
