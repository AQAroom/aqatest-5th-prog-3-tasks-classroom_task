#!/usr/bin/env python3
import sys
import json
import base64

def main():
    """Парсит реальные результаты из autograding-io-grader"""
    print(f"DEBUG: Всего аргументов: {len(sys.argv)}", file=sys.stderr)
    
    total_score = 0
    test_count = 0
    
    # Парсим все переданные результаты тестов
    for i in range(2, len(sys.argv)):
        encoded = sys.argv[i]
        if not encoded or encoded == 'null':
            continue
            
        try:
            # Декодируем base64
            decoded = base64.b64decode(encoded).decode('utf-8')
            data = json.loads(decoded)
            
            print(f"DEBUG [{i}]: {json.dumps(data, indent=2)}", file=sys.stderr)
            
            # Суммируем баллы из всех тестов
            if 'tests' in data:
                for test in data['tests']:
                    score = test.get('score', 0)
                    total_score += score
                    test_count += 1
                    print(f"  Тест: {test.get('name')} = {score} баллов", file=sys.stderr)
            elif 'score' in data:
                total_score += data['score']
                test_count += 1
            
        except Exception as e:
            print(f"ERROR: Ошибка парсинга {encoded[:50]}...: {e}", file=sys.stderr)
    
    print(f"DEBUG: Всего тестов: {test_count}, сумма баллов: {total_score}", file=sys.stderr)
    print(f"TASK_SCORE={total_score}")

if __name__ == "__main__":
    main()
