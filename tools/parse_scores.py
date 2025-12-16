#!/usr/bin/env python3
import sys
import json
import base64
import os

def parse_score(encoded_result):
    """Парсит баллы из закодированного результата autograding"""
    if not encoded_result or encoded_result == 'null':
        return 0
    try:
        decoded = base64.b64decode(encoded_result).decode('utf-8')
        data = json.loads(decoded)
        print(f"DEBUG: Parsed data: {json.dumps(data, indent=2)}", file=sys.stderr)
        
        # Формат который мы видим в логах
        if 'tests' in data and len(data['tests']) > 0:
            total_score = sum(test.get('score', 0) for test in data['tests'])
            print(f"DEBUG: Total score from tests: {total_score}", file=sys.stderr)
            return total_score
        elif 'score' in data:
            print(f"DEBUG: Score from root: {data['score']}", file=sys.stderr)
            return data['score']
        else:
            print(f"DEBUG: Unknown format", file=sys.stderr)
            return 0
    except Exception as e:
        print(f"ERROR parsing score: {e}", file=sys.stderr)
        return 0

def main():
    """Основная функция"""
    if len(sys.argv) < 2:
        print("Usage: python3 parse_scores.py <task_number> [results...]")
        sys.exit(1)
    
    task = sys.argv[1]
    
    if task == "1":
        if len(sys.argv) != 5:
            print("Usage for task 1: python3 parse_scores.py 1 <add_result> <sub_result> <div_result>")
            sys.exit(1)
        
        add_score = parse_score(sys.argv[2])
        sub_score = parse_score(sys.argv[3])
        div_score = parse_score(sys.argv[4])
        
        total = add_score + sub_score + div_score
        print(f"TASK_SCORE={total}")
        print(f"DEBUG: Task 1 final score: {total}", file=sys.stderr)
        
    elif task == "2":
        # Для задачи 2 пока просто проверяем файл
        if os.path.exists("task_02.py"):
            print("TASK_SCORE=10")
        else:
            print("TASK_SCORE=0")
            
    elif task == "3":
        # Для задачи 3 пока просто проверяем файл
        if os.path.exists("task_03.py"):
            print("TASK_SCORE=10")
        else:
            print("TASK_SCORE=0")
    else:
        print("TASK_SCORE=0")

if __name__ == "__main__":
    main()
