import argparse
import pandas as pd
import json
import os
import time
import concurrent.futures
from google import genai
from google.genai import types

def dict_to_entities_str(e_raw):
    if not e_raw:
        return 'nan'
    try:
        out = []
        for e in e_raw:
            out.append(f"{e.get('name')}: '{e.get('canonical')}'")
        return ", ".join(sorted(out))
    except:
        return 'nan'

def evaluate_single(row, prompt, client, model_id, process_request_tool):
    transcript = row.get("transcript")
    orig = row.get("orig_utterance")
    if pd.isna(transcript) or not str(transcript).strip():
        transcript = orig
    transcript = str(transcript)
    expected_intent = str(row.get("expected_intent"))

    out_intent = "N/A"
    out_entities = []

    config = types.GenerateContentConfig(
        system_instruction=prompt,
        tools=[process_request_tool],
        temperature=0.0
    )

    start_time = time.time()
    try:
        response = client.models.generate_content(
            model=model_id,
            contents=transcript,
            config=config
        )
        if response.function_calls:
            for fc in response.function_calls:
                if fc.name == "process_request":
                    args = fc.args
                    out_intent = args.get("intent", "N/A")
                    out_entities = args.get("entities", [])
                    break
    except Exception as e:
        print(f"Error on '{transcript}': {e}")
        
    latency = time.time() - start_time
    out_ent_str = dict_to_entities_str(out_entities)
    
    # We consider it a match if our intent is literally inside the acceptable comma-separated expected intent string
    is_match = (out_intent in expected_intent) and out_intent != "N/A" and out_intent != ""
    # special case if expected is n/a
    if out_intent == "N/A" and (expected_intent == "N/A" or pd.isna(expected_intent) or expected_intent == "nan"):
        is_match = True

    return {
        "utterance": transcript, 
        "expected_intent": expected_intent,
        "actual_intent": out_intent,
        "actual_entities": out_ent_str,
        "intent_match": is_match,
        "latency_sec": round(latency, 3)
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt_file")
    parser.add_argument("--output", default="results.json")
    parser.add_argument("--sample", type=float, default=1.0)
    args = parser.parse_args()

    os.environ["GOOGLE_CLOUD_PROJECT"] = "agy-coding"
    os.environ["GOOGLE_CLOUD_LOCATION"] = "global"
    os.environ["GOOGLE_GENAI_USE_ENTERPRISE"] = "true"
    if "GOOGLE_APPLICATION_CREDENTIALS" in os.environ:
        del os.environ["GOOGLE_APPLICATION_CREDENTIALS"]

    client = genai.Client()
    model_id = "gemini-3.5-flash-lite"

    with open(args.prompt_file, 'r', encoding='utf-8') as f:
        prompt = f.read()

    golden_intents = [
        "TV__EXIT", "TV__NAVIGATE", "TV__NAVIGATION_KEY", "TV__NEXT_CHANNEL", "TV__OK",
        "TV__OPEN_MENU", "TV__OPEN_PARTNER_APP", "TV__PAUSE", "TV__PLAY", "TV__POWER",
        "TV__PROGRAM", "TV__RESTART", "TV__RETURN", "TV__SEARCH", "TV__SWITCH_CHANNEL",
        "TV__VOLUME", "TV__PROGRAM_WHEN_WHERE", "N/A"
    ]

    process_request_tool = types.Tool(
        function_declarations=[
            types.FunctionDeclaration(
                name="process_request",
                description="Process a TV voice assistant request and return intent and entities.",
                parameters={
                    "type": "OBJECT",
                    "properties": {
                        "utterance": {"type": "STRING"},
                        "intent": {
                            "type": "STRING",
                            "enum": golden_intents
                        },
                        "entities": {
                            "type": "ARRAY",
                            "items": {
                                "type": "OBJECT",
                                "properties": {
                                    "name": {"type": "STRING"},
                                    "literal": {"type": "STRING"},
                                    "canonical": {"type": "STRING"}
                                }
                            }
                        }
                    },
                    "required": ["utterance", "intent"]
                }
            )
        ]
    )

    df = pd.read_excel('results_compared_20260729_110300_prompt_without_channels_apps.xlsx', engine='openpyxl')
    
    if args.sample < 1.0:
        sample_size = int(len(df) * args.sample)
        # Use a reproducible random sample so it grabs a good distribution
        df = df.sample(n=sample_size, random_state=42).reset_index()
    
    results = []
    correct_intents = 0
    total = len(df)
    
    print(f"Starting {model_id} eval for {total} utterances with {args.prompt_file} ...")

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(evaluate_single, row, prompt, client, model_id, process_request_tool): idx for idx, row in df.iterrows()}
        for future in concurrent.futures.as_completed(futures):
            res = future.result()
            res["id"] = futures[future] + 1
            results.append(res)
            if res["intent_match"]:
                correct_intents += 1
            marker = "✅" if res['intent_match'] else "❌"
            print(f"[{res['id']}/{total}] {marker} {res['latency_sec']}s | {res['utterance']} -> {res['actual_intent']} (Expected: {res['expected_intent']})")

    results.sort(key=lambda x: x["id"])
    acc = (correct_intents / total * 100) if total else 0
    avg_latency = sum(r["latency_sec"] for r in results) / total if total else 0
    
    print(f"\nEvaluation Complete! Intent Accuracy: {acc:.2f}% ({correct_intents}/{total}) | Avg Latency: {avg_latency:.3f}s")
    
    with open(args.output, "w") as f:
        json.dump({"accuracy": acc, "total": total, "correct": correct_intents, "avg_latency": avg_latency, "details": results}, f, indent=2)

if __name__ == "__main__":
    main()
