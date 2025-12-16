import subprocess
import sys
import os

def run_linter(command, file_path):
    """Запускает линтер и возвращает результат"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return "Таймаут выполнения"
    except Exception as e:
        return f"Ошибка: {str(e)}"

def check_code():
    task_files = ["task_01.py", "task_02.py", "task_03.py"]
    
    for task_file in task_files:
        if not os.path.exists(task_file):
            print(f"⚠️ Файл {task_file} не найден")
            print()
            continue
            
        print(f"### 📄 Анализ файла: **{task_file}**")
        print()
        
        # Ruff
        print("#### ⚡ Ruff:")
        print("```")
        ruff_result = run_linter(f"ruff check {task_file} --exit-zero", task_file)
        print(ruff_result[:500])  # Ограничиваем вывод
        if len(ruff_result) > 500:
            print("... (вывод обрезан)")
        print("```")
        print()
        
        # Pylint
        print("#### 🐍 Pylint:")
        print("```")
        pylint_result = run_linter(f"pylint {task_file} --exit-zero --score=yes", task_file)
        # Берем только последние 5 строк с оценкой
        lines = pylint_result.strip().split('\n')
        for line in lines[-5:]:
            print(line)
        print("```")
        print()
        
        print("---")

if __name__ == "__main__":
    check_code()
