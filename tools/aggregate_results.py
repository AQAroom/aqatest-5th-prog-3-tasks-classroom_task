#!/usr/bin/env python3
"""
Агрегирует результаты тестов в один JSON для GitHub Classroom Reporter
"""

import sys
import json
import base64

def decode_autograding_result(encoded_result):
    """Декодирует результат autograding-io-grader"""
    if not encoded_result or encoded_result in ('null', 'undefined', ''):
        return {'score': 0, 'max_score': 0, 'tests': []}
    
    try:
        decoded = base64.b64decode(encoded_result).decode('utf-8')
        return json.loads(decoded)
    except Exception as e:
        print(f"ERROR decoding result: {e}", file=sys.stderr)
        return {'score': 0, 'max_score': 0, 'tests': []}

def aggregate_task(task_name, max_score, *encoded_results):
    """
    Агрегирует несколько тестов в один результат
    Возвращает base64-encoded JSON для GitHub Classroom
    """
    total_score = 0
    all_tests = []
    test_count = 0
    
    print(f"Aggregating {task_name}...", file=sys.stderr)
    
    for i, encoded in enumerate(encoded_results):
        if not encoded:
            continue
            
        data = decode_autograding_result(encoded)
        
        if 'tests' in data:
            for test in data['tests']:
                score = test.get('score', 0)
                total_score += score
                test_count += 1
                print(f"  Test {test_count}: {test.get('name')} = {score} points", file=sys.stderr)
                all_tests.append(test)
    
    print(f"Total for {task_name}: {total_score}/{max_score}", file=sys.stderr)
    
    # Создаем агрегированный результат
    result = {
        "version": 1,
        "status": "pass" if total_score >= max_score * 0.8 else "fail",
        "max_score": max_score,
        "tests": [
            {
                "name": task_name,
                "status": "pass" if total_score >= max_score * 0.8 else "fail",
                "score": total_score,
                "output": f"Всего тестов: {test_count}, Набрано баллов: {total_score}/{max_score}"
            }
        ]
    }
    
    # Кодируем в base64
    encoded_result = base64.b64encode(
        json.dumps(result).encode('utf-8')
    ).decode('utf-8')
    
    return encoded_result

def main():
    if len(sys.argv) < 4:
        print("Usage: python3 aggregate_results.py <task_name> <max_score> <encoded_result1> [<encoded_result2> ...]")
        sys.exit(1)
    
    task_name = sys.argv[1]
    max_score = int(sys.argv[2])
    encoded_results = sys.argv[3:]
    
    # Агрегируем результаты
    aggregated = aggregate_task(task_name, max_score, *encoded_results)
    
    # Выводим в формате для GitHub Actions
    print(f"AGGREGATED_RESULT={aggregated}")

if __name__ == "__main__":
    main()
