import os
import sys

def get_text_files():
    target_files = []
    for root, _, files in os.walk('.'):
        if 'venv' in root or '.git' in root or '__pycache__' in root:
            continue
        for file in files:
            if file.endswith(('.md', '.py', '.json', '.yaml', '.sh', '.txt')):
                target_files.append(os.path.join(root, file))
    return target_files

def test_no_leaked_ip_or_brands():
    banned_terms = ["magenta", "deutsche telekom", "telekom", "api.telekom.de", "schalte auf", "umschalten auf", "öffne ", "schließe ", "starte ", "suche nach"]
    leaked = []
    for filepath in get_text_files():
        if os.path.basename(filepath) in ["test_data_validation.py", "eval_engine.py", "test_eval_engine.py", "README.md", "project_brief.md", "analysis_report.md", "mismatch_report.md", "flowchart.md"]:
            continue
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read().lower()
            for term in banned_terms:
                if term in content:
                    leaked.append(f"{filepath} contains '{term}'")

    if leaked:
        print("Found leaked brand tokens or German phrases:\n" + "\n".join(leaked))
        sys.exit(1)
    else:
        print("All validations passed.")
        sys.exit(0)

if __name__ == "__main__":
    test_no_leaked_ip_or_brands()
