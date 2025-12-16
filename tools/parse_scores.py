#!/usr/bin/env python3
import sys
import json
import base64
import os

def parsing():
    if len(sys.argv) < 2:
        print("TASK_SCORE=0")
        return
    
    task = sys.argv[1]
    
    if task == "1":
        # Для задачи 1 парсим все три результата
        if len(sys.argv) != 5:
            print("TASK_SCORE=0")
            return
            
        total_score = 0
        for encoded_result in sys.argv[2:5]:
            if not encoded_result or encoded_result == 'null':
                continue
            try:
                decoded = base64.b64decode(encoded_result).decode('utf-8')
                data = json.loads(decoded)
                
                # Извлекаем баллы
                if 'tests' in data and data['tests']:
                    for test in data['tests']:
                        total_score += test.get('score', 0)
                elif 'score' in data:
                    total_score += data['score']
                    
            except Exception:
                pass
        
        print(f"TASK_SCORE={total_score}")
        
    elif task == "2":
        # Для задач 2 и 3 пока просто проверяем наличие файлов
        if os.path.exists("task_02.py"):
            print("TASK_SCORE=10")
        else:
            print("TASK_SCORE=0")
            
    elif task == "3":
        if os.path.exists("task_03.py"):
            print("TASK_SCORE=10")
        else:
            print("TASK_SCORE=0")
    else:
        print("TASK_SCORE=0")

if __name__ == "__main__":
    parsing()
