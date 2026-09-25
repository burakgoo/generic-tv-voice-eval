# Project Brief: Cymbal TV Voice Assistant Evaluation (Gemini Live vs. Incumbent)

## 1. Executive Summary
Cymbal TV (Cymbal) evaluated the Gemini Live model for processing TV voice commands (specifically intent classification and entity extraction). While the Gemini Live approach is strategically interesting, the current evaluated setup does not yet outperform their current production baseline (which uses TTS followed by regex and GPT-based LLM processing). Consequently, the immediate focus has shifted to evaluating Gemini text models while Google reviews optimization options for the Live approach.

## 2. Background and Context
*   **Customer:** Cymbal TV (Cymbal)
*   **Current Architecture:** Pipelined approach: TTS -> Regex -> GPT-based LLM processing.
*   **Evaluated Solution:** Gemini Live model processing audio to output classifications.
*   **Current Status:** Gemini Live results were good but fell short of the incumbent approach. 
*   **Latency:** The active Live setup was observed at ~1.5 seconds, with an additional resolution call adding ~0.5 seconds in the evaluated design.

## 3. Evaluation Scope and Methodology
*   **Evaluated Capabilities:** Intent classification and entity extraction for representative TV voice-assistant commands.
*   **Test Input:** High-quality synthetic audio covering core use cases, including Austrian and Hungarian scenarios.
*   **Out of Scope (for current evaluation):** Background noise, far-field conditions, multiple speakers, TV/movie domain knowledge, and recommendation quality.
*   **Test Dataset:** Synthesized audio samples, system prompts, test results.

## 4. Technical Findings & Challenges
*   **Prompt Size / Context:** Including all channel names, app names, and synonyms reduced classification reliability.
*   **Optimal Architecture (Evaluated):** Keep the prompt small; handle canonical channel/app mapping in a downstream entity-resolution component.
*   **Structured Output Issues:** The Live model struggled with native structured output; it required tool calling as a workaround for retrieving transcript, intent, and entities. 
*   **Model Quirks:** Gemini 2.5 Live was not pursued further because function calls and structured responses were frequently incomplete or malformed.

## 5. Google Feedback & Proposals
Google aims to analyze the current setup and provide concrete recommendations to improve Gemini Live performance:
*   **Prompt Optimization:** Specifically target recurring semantic distinctions (power state, volume direction, channel navigation). Adapt prompts specifically for Gemini instead of reusing the incumbent's prompts.
*   **Retrieval/Few-Shot:** Evaluate an Example Store / few-shot retrieval approach to add similar reference cases to the prompt.
*   **Architecture Review:** Continue using tool-calling and external entity-resolution. Review the current technical setup and surrounding architecture to make recommendations more concrete.
*   **Model Comparison:** Use a larger Gemini model to support prompt improvement and compare text-model behavior with the Live model.
*   **Tooling:** Automate the regression pipeline to facilitate easier testing of model, prompt, and code variations.
*   **Collaboration:** Request detailed remaining failure cases from Cymbal to identify patterns, and request architecture, results, prompts, and golden test data where permitted.

## 6. Action Plan & Next Steps
| Owner | Action | Expected Output | Timing / Dependency |
| :--- | :--- | :--- | :--- |
| **Cymbal** | Complete Gemini text-model evaluation. | Comparison with baseline and Live results. | Current evaluation track. |
| **Cymbal** | Prepare shareable evidence package. | Architecture, results, selected examples, prompts/data. | Subject to privacy/compliance review. |
| **Cymbal** | Continue TV/movie knowledge/recommendation tests. | Separate view of domain capability. | Planned within PI. |
| **Google** | Review detailed failures internally. | Concrete optimization ideas/hypotheses. | Target: 19 August. |
| **Google** | Assess prompt and Example Store options. | Recommendations for improved Live setup. | Depends on share package. |
| **Joint** | Fast clarification and refinement. | Technical follow-up via existing channels. | Ongoing. |
| **Joint** | Decide on Live re-evaluation prioritization. | Sprint 3 scope/priority decision. | Sprint 3 planning (Aug 25). |

## 7. Timeline
*   **By 19 August:** Google to provide initial feedback, findings, and optimization proposals.
*   **Before Sprint 3 Planning:** Cymbal reviews Google's feedback and evaluates whether additional Gemini Live activities should be prioritized.
*   **25 August (Sprint 3 Start):** Potential re-evaluation and follow-up work begins if feedback indicates worthwhile improvement opportunities.

## 8. Test Data Metrics & Documentation
Notes on the customer's test results document structure:
*   `transcript`: Input transcription provided by the model.
*   `resolved_utterance`: Utterance resolution explicitly requested by the prompt.
*   `intent`, `entities`: Results extracted from the tool call.
*   `entities_filtered`: Filtered and slightly modified entity values for easier comparison.
*   `comparison_intent`, `comparison_entities`: Observed differences between expected and actual results, using the following color coding:
    *   **Yellow:** Canonical channel/app values resolvable in an additional refinement component (non-critical).
    *   **Orange:** Acceptable or less severe differences.
    *   **Red:** Misclassifications.
