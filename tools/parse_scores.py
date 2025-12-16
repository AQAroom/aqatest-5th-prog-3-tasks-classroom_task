#!/usr/bin/env python3
import sys
import os

def parsing():
    if len(sys.argv) < 2:
        print("TASK=1")
        print("TASK_SCORE=0")
        return
    
    task = sys.argv[1]
    print(f"TASK={task}")
    
    if task == "1":
        # Проверяем фактическое выполнение
        if os.path.exists("task_01.py"):
            # Здесь должна быть логика парсинга реальных результатов
            # Пока даем минимальный балл за наличие файла
            score = 10
        else:
            score = 0
    elif task == "2":
        if os.path.exists("task_02.py"):
            score = 10
        else:
            score = 0
    elif task == "3":
        if os.path.exists("task_03.py"):
            score = 10
        else:
            score = 0
    else:
        score = 0
    
    print(f"TASK_SCORE={score}")

if __name__ == "__main__":
    parsing()
