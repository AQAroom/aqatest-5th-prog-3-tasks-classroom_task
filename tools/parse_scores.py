#!/usr/bin/env python3
import sys
import json
import base64
import os

def main():
    """Парсит реальные результаты из autograding-io-grader"""
    print(f"DEBUG: Парсим задачу {sys.argv[1] if len(sys.argv) > 1 else 'unknown'}", file=sys.stderr)
    print(f"DEBUG: Аргументов: {len(sys.argv)}", file=sys.stderr)
    
    total_score = 0
    
    # Парсим все переданные результаты тестов
    for i in range(2, len(sys.argv)):
        encoded = sys.argv[i]
        if not encoded or encoded == 'null':
            print(f"DEBUG: Пустой аргумент {i}", file=sys.stderr)
            continue
            
        try:
            # Декодируем base64
            decoded = base64.b64decode(encoded).decode('utf-8')
            data = json.loads(decoded)
            
            print(f"DEBUG: Данные теста {i-1}: {json.dumps(data, indent=2)}", file=sys.stderr)
            
            # Суммируем баллы
            if 'tests' in data:
                for test in data['tests']:
                    score = test.get('score', 0)
                    total_score += score
                    print(f"DEBUG: Тест '{test.get('name')}' = {score} баллов", file=sys.stderr)
            elif 'score' in data:
                total_score += data['score']
                print(f"DEBUG: Прямой балл = {data['score']}", file=sys.stderr)
                
        except Exception as e:
            print(f"ERROR: Ошибка парсинга: {e}", file=sys.stderr)
    
    print(f"DEBUG: Итого баллов: {total_score}", file=sys.stderr)
    print(f"TASK_SCORE={total_score}")

if __name__ == "__main__":
    main()
