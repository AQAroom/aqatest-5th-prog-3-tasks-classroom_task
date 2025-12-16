#!/usr/bin/env python3
import sys
import json
import base64

def decode_and_sum_scores(*encoded_results):
    """Декодирует и суммирует баллы из закодированных результатов"""
    total_score = 0
    
    for encoded in encoded_results:
        if not encoded or encoded == 'null':
            continue
            
        try:
            # Декодируем base64
            decoded_json = base64.b64decode(encoded).decode('utf-8')
            data = json.loads(decoded_json)
            
            print(f"Данные: {json.dumps(data, indent=2)}", file=sys.stderr)
            
            # Извлекаем баллы
            if 'tests' in data:
                for test in data['tests']:
                    score = test.get('score', 0)
                    total_score += score
                    print(f"Найден тест: {test.get('name')}, баллы: {score}", file=sys.stderr)
            elif 'score' in data:
                total_score += data['score']
                print(f"Прямой балл: {data['score']}", file=sys.stderr)
                
        except Exception as e:
            print(f"Ошибка декодирования: {e}", file=sys.stderr)
    
    return total_score

def parsing():
    if len(sys.argv) < 2:
        print("TASK_SCORE=0")
        return
    
    task_num = sys.argv[1]
    
    # Для задачи 1 должно быть 3 теста
    if task_num == "1" and len(sys.argv) >= 5:
        total = decode_and_sum_scores(sys.argv[2], sys.argv[3], sys.argv[4])
        print(f"TASK_SCORE={total}")
    # Для задачи 2 должно быть 3 теста
    elif task_num == "2" and len(sys.argv) >= 5:
        total = decode_and_sum_scores(sys.argv[2], sys.argv[3], sys.argv[4])
        print(f"TASK_SCORE={total}")
    # Для задачи 3 должно быть 3 теста
    elif task_num == "3" and len(sys.argv) >= 5:
        total = decode_and_sum_scores(sys.argv[2], sys.argv[3], sys.argv[4])
        print(f"TASK_SCORE={total}")
    else:
        print("TASK_SCORE=0")

if __name__ == "__main__":
    parsing()
