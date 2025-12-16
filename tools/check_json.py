#!/usr/bin/env python3
# Python скрипт для проверки JSON check_json.py
import sys
import json
import base64

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 check_json.py <base64_string> <name>")
        sys.exit(1)
    
    encoded = sys.argv[1]
    name = sys.argv[2]
    
    if not encoded or encoded == "NOT_FOUND":
        print(f"❌ {name}: Нет данных")
        return
    
    try:
        decoded = base64.b64decode(encoded).decode('utf-8')
        data = json.loads(decoded)
        score = data.get("tests", [{}])[0].get("score", "N/A")
        max_score = data.get("max_score", "N/A")
        print(f'✅ {name}: Valid JSON, score: {score}/{max_score}')
        print(f'   Structure: {list(data.keys())}')
    except Exception as e:
        print(f'❌ {name}: Invalid JSON: {e}')

if __name__ == "__main__":
    main()
