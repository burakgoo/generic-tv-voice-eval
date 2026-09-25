# First Analysis Report: Cymbal TV Gemini Live Evaluation

## 1. Overview of Artifacts Provided
*   **Audio Data** (`audio_AT.zip`): Extracted successfully. It contains 95 synthetic German/Austrian `.wav` audio files representing typical voice commands for a TV assistant.
*   **Test Results Data** (`results_compared_20260729_110300_prompt_without_channels_apps.xlsx`): 95 evaluated rows comparing expected vs. actual model outputs using a "compact prompt" strategy (without full channel/app lists). 
*   **Prompt Instructions** (`classification_instructions_without_channels_and_apps.md`): The system prompt defining entity schemas and strict intent categorizations.

## 2. Quantitative Results & Accuracy
Based on the provided dataset evaluation:
*   **Total Test Cases:** 95
*   **Intent Accuracy:** ~97% (Only 3 intent misclassifications).
*   **Entity Extraction Accuracy:** ~84% (15 entity mismatches).

## 3. Deep-Dive into Failures

### 3.1 Intent Mismatches
The model only missed 3 intents, and all are edge cases of semantic ambiguity:
1.  **"Zeige mir das Programm"** (Show me the program/guide)
    *   *Expected:* `TV__OPEN_MENU`
    *   *Actual:* `TV__PROGRAM`
    *   *Analysis:* "Programm" can mean the TV guide (EPG) or actual content. The model leaned toward asking for programming.
2.  **"Zu Kanal 11"** (To channel 11)
    *   *Expected:* `TV__NAVIGATE`
    *   *Actual:* `TV__SWITCH_CHANNEL`
    *   *Analysis:* The phrase "To channel 11" implies tuning directly to it, making `TV__SWITCH_CHANNEL` a very rational choice compared to just "navigating".
3.  **"Gehe zurück"** (Go back)
    *   *Expected:* `TV__RETURN`
    *   *Actual:* `TV__EXIT`
    *   *Analysis:* Returning to a previous screen vs. exiting a menu is often context-dependent, making this a highly forgivable misclassification.

### 3.2 Entity Mismatches (The "Yellow" Canonical Errors)
Almost all 15 entity mismatches are related to canonical channel/app name mappings. Because the prompt intentionally omitted the long lists of channels/apps, the model successfully extracted the literal targets but failed (or guessed incorrectly) at their strict canonical definitions.
*   **HD/Base Channel Confusion:** "Was läuft auf ZDF" -> the model mapped to `ZDF`, but the incumbent expects `ZDF HD`. Same for `ORF 1` vs `ORF 1 HD`.
*   **Numeric Parsing:** "Umschalten auf Sender sixx" (Switch to channel sixx) -> the model extracted literal '6' rather than `sixx HD`.
*   **App Synonyms:** "Gehe zu ORF app" -> expected `ORF ON`, model gave `ORF-App`.
*   **Missing Synonyms:** "Starte den Videotext" -> model completely missed extracting the app `Teletext`. 

## 4. Disagreement between Instructions and Target Intents
There is a slight schema mismatch between the provided `classification_instructions_without_channels_and_apps.md` and the expected values in the Excel file:
*   The instructions dictate intents like `TV__SWITCH_CHANNEL_NO_APP` and `TV__NAVIGATE_CHANNEL`.
*   The test results evaluate against `TV__SWITCH_CHANNEL` and `TV__NAVIGATE`.
*   It appears the evaluation dataset expects an older/different schema than the included Markdown instructions dictate. This needs to be harmonized.

## 5. Proposed Next Steps & Gemini Optimization Strategy
To outperform the incumbent solution using Gemini Live:

1.  **Adopt the Downstream Entity-Resolution Strategy (as proposed by Cymbal):**
    *   The model should only extract the *literal* string (e.g., "Sixx", "ORF 1").
    *   Move canonical mapping (`ZDF` -> `ZDF HD`) to an external RAG/Dictionary tool call or standard code lookup. This keeps the prompt short, fast, and eliminates LLM hallucinations on channel mappings.
2.  **Harmonize the Prompt and Eval Pipeline:**
    *   Ensure the regression tests (the expected intents in the Excel file) match the new exact schema detailed in the Markdown.
3.  **Implement a Few-Shot Example Store (RAG):**
    *   For ambiguous edge cases like "Zeige mir das Programm" or "Gehe zurück", inject 5-10 pre-defined examples into the prompt dynamically using a vector search or just hardcode the most confusing ones. The model will mimic the behavior instantly without needing complex descriptive rules.
4.  **Targeted Prompt Adjustments:**
    *   Add a rule linking "Videotext" to the `app` entity.
    *   Clarify the rule boundary explicitly between `TV__OPEN_MENU` (for EPG) and `TV__PROGRAM` (for querying content).
