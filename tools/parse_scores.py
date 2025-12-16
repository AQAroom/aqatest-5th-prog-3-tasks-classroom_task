#!/usr/bin/env python3
import sys
import json
import base64

def main():
    """Парсит реальные результаты из autograding-io-grader"""
    if len(sys.argv) < 2:
        print("TASK_SCORE=0")
        return
    
    task_num = sys.argv[1]
    total_score = 0
    
    print(f"DEBUG: Парсим задачу {task_num}", file=sys.stderr)
    
    # Парсим все переданные результаты тестов
    for i in range(2, len(sys.argv)):
        encoded = sys.argv[i]
        if not encoded or encoded == 'null':
            print(f"DEBUG: Пустой/несуществующий тест {i-1} для задачи {task_num}", file=sys.stderr)
            continue
            
        try:
            # Декодируем base64
            decoded = base64.b64decode(encoded).decode('utf-8')
            data = json.loads(decoded)
            
            # Для задачи 2 выводим детальную информацию
            if task_num == "2":
                print(f"DEBUG: Тест {i-1} для задачи 2: {json.dumps(data, indent=2)}", file=sys.stderr)
            
            # Суммируем баллы
            if 'tests' in data:
                for test in data['tests']:
                    score = test.get('score', 0)
                    total_score += score
                    print(f"DEBUG: Тест '{test.get('name')}' = {score} баллов (итого: {total_score})", file=sys.stderr)
            elif 'score' in data:
                total_score += data['score']
                print(f"DEBUG: Прямой балл = {data['score']} (итого: {total_score})", file=sys.stderr)
                
        except Exception as e:
            print(f"ERROR: Ошибка парсинга теста {i-1}: {e}", file=sys.stderr)
            print(f"ERROR: Закодированные данные: {encoded[:100]}...", file=sys.stderr)
    
    print(f"DEBUG: Итого для задачи {task_num}: {total_score} баллов", file=sys.stderr)
    print(f"TASK_SCORE={total_score}")

if __name__ == "__main__":
    main()
