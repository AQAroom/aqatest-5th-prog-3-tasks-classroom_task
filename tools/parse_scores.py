#!/usr/bin/env python3
import sys
import json
import base64
import os

def decode_autograding_result(encoded_result):
    """Декодирует результат autograding-io-grader"""
    if not encoded_result or encoded_result == 'null':
        return 0
    
    try:
        decoded = base64.b64decode(encoded_result).decode('utf-8')
        data = json.loads(decoded)
        
        # Логируем для отладки
        print(f"Декодированные данные: {json.dumps(data, indent=2)}", file=sys.stderr)
        
        # Извлекаем баллы разными способами
        if 'tests' in data and data['tests']:
            total = 0
            for test in data['tests']:
                total += test.get('score', 0)
                print(f"Тест: {test.get('name')}, баллы: {test.get('score', 0)}", file=sys.stderr)
            return total
        elif 'score' in data:
            print(f"Прямой score: {data['score']}", file=sys.stderr)
            return data['score']
        elif 'points' in data:
            print(f"Прямой points: {data['points']}", file=sys.stderr)
            return data['points']
        else:
            print("Не удалось найти баллы в данных", file=sys.stderr)
            return 0
            
    except Exception as e:
        print(f"Ошибка декодирования: {e}", file=sys.stderr)
        return 0

def parsing():
    """Парсит результаты тестов из аргументов"""
    if len(sys.argv) < 2:
        print("TASK_SCORE=0")
        return
    
    task = sys.argv[1]
    total_score = 0
    
    print(f"Парсинг для задачи {task}", file=sys.stderr)
    print(f"Всего аргументов: {len(sys.argv)}", file=sys.stderr)
    
    # Для отладки выводим все аргументы
    for i, arg in enumerate(sys.argv):
        print(f"Аргумент {i}: {arg[:50]}{'...' if len(arg) > 50 else ''}", file=sys.stderr)
    
    if task == "1":
        # Для задачи 1: парсим все тесты из шагов
        # Сложение, вычитание, деление на ноль
        if len(sys.argv) >= 5:
            for encoded_result in sys.argv[2:5]:
                score = decode_autograding_result(encoded_result)
                total_score += score
                print(f"Добавлено {score} баллов, итого: {total_score}", file=sys.stderr)
    elif task == "2":
        # Для задачи 2: простая/сложная проверка палиндрома, пустая строка
        if len(sys.argv) >= 5:
            for encoded_result in sys.argv[2:5]:
                score = decode_autograding_result(encoded_result)
                total_score += score
                print(f"Добавлено {score} баллов, итого: {total_score}", file=sys.stderr)
    elif task == "3":
        # Для задачи 3: Фибоначчи 0, 1, 10
        if len(sys.argv) >= 5:
            for encoded_result in sys.argv[2:5]:
                score = decode_autograding_result(encoded_result)
                total_score += score
                print(f"Добавлено {score} баллов, итого: {total_score}", file=sys.stderr)
    
    # Дополнительная проверка: если файл существует, но тесты не прошли
    # МОЖЕТ давать минимальные баллы за попытку (но это уже бизнес-логика)
    file_exists = False
    if task == "1" and os.path.exists("task_01.py"):
        file_exists = True
    elif task == "2" and os.path.exists("task_02.py"):
        file_exists = True
    elif task == "3" and os.path.exists("task_03.py"):
        file_exists = True
    
    print(f"Файл существует: {file_exists}", file=sys.stderr)
    print(f"Итоговые баллы: {total_score}", file=sys.stderr)
    
    # Если хотим давать баллы за наличие файла (не обязательно)
    # if file_exists and total_score == 0:
    #     total_score = 5  # минимальный балл за попытку
    
    print(f"TASK_SCORE={total_score}")

if __name__ == "__main__":
    parsing()
