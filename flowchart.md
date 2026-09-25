# Architecture Flowchart

Below is the solution design flowchart demonstrating how the evaluation framework operates. Customer Engineers can reference this to understand the data lifecycle from local repository to Google Cloud.

```mermaid
flowchart TD
    CE((Customer Engineer)) -->|git clone| Git[GitHub Repository\n- config.yaml\n- /data/ \n- /src/]
    Git -->|run setup.sh| GCS[(GCS Bucket\nTest Data & Audio)]
    Git -->|gcloud run deploy| CR[Cloud Run Job\nEvaluation Engine]
    
    Config[\config.yaml\] -.-> |Project Vars| CR
    
    CR -->|Send Inputs| Cymbal(CymbalTV Endpoint)
    Cymbal -->|Voice/Text Output| CR
    
    CR <-->|Execute EvalTask| VAI{Vertex AI Evaluation}
    VAI -->|Scores| CR
    
    CR -->|Write Artifacts/Results| GCS
    CR -->|Output summary| CE
    
    style Git fill:#f5f5f5,stroke:#424242
    style GCS fill:#bbdefb,stroke:#1565c0
    style CR fill:#ffe0b2,stroke:#ef6c00
    style VAI fill:#e8f5e9,stroke:#388e3c
```
