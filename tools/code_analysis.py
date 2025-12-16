# tools/code_analysis.py
import subprocess
import os
import sys

def analyze_task_file(filename):
    """Анализирует файл задачи и возвращает результаты"""
    if not os.path.exists(filename):
        return None
    
    results = {
        'file': filename,
        'exists': True,
        'pylint_score': 0,
        'flake8_errors': 0,
        'ruff_errors': 0,
        'syntax_ok': False,
        'ruff_output': '',
        'flake8_output': ''
    }
    
    # Проверка синтаксиса
    try:
        subprocess.run(['python3', '-m', 'py_compile', filename], 
                      capture_output=True, check=True)
        results['syntax_ok'] = True
    except subprocess.CalledProcessError as e:
        results['syntax_ok'] = False
        results['syntax_error'] = e.stderr.decode()
    
    # PyLint оценка
    try:
        pylint_result = subprocess.run(
            ['pylint', filename, '--exit-zero', '--score=yes'],
            capture_output=True,
            text=True,
            timeout=10
        )
        for line in pylint_result.stdout.split('\n'):
            if 'rated at' in line:
                score = line.split('rated at ')[1].split('/')[0]
                results['pylint_score'] = float(score)
                break
    except Exception as e:
        results['pylint_error'] = str(e)
    
    # Flake8 ошибки
    try:
        flake8_result = subprocess.run(
            ['flake8', filename],
            capture_output=True,
            text=True
        )
        results['flake8_output'] = flake8_result.stdout
        results['flake8_errors'] = len(flake8_result.stdout.strip().split('\n')) if flake8_result.stdout.strip() else 0
    except Exception as e:
        results['flake8_error'] = str(e)
    
    # Ruff ошибки
    try:
        ruff_result = subprocess.run(
            ['ruff', 'check', filename],
            capture_output=True,
            text=True
        )
        results['ruff_output'] = ruff_result.stdout
        results['ruff_errors'] = len(ruff_result.stdout.strip().split('\n')) if ruff_result.stdout.strip() else 0
    except Exception as e:
        results['ruff_error'] = str(e)
    
    return results

def main():
    """Основная функция анализа"""
    task_files = ['task_01.py', 'task_02.py', 'task_03.py']
    
    print("## 🔍 ДЕТАЛЬНЫЙ АНАЛИЗ КАЧЕСТВА КОДА")
    print("")
    
    # Сводная таблица
    print("### 📊 Сводная таблица по задачам")
    print("")
    print("| Задача | Файл | Синтаксис | PyLint | Flake8 | Ruff | Статус |")
    print("|--------|------|-----------|--------|--------|------|--------|")
    
    for task_file in task_files:
        result = analyze_task_file(task_file)
        
        if result is None:
            print(f"| Задача {task_file[5]} | `{task_file}` | ❌ | - | - | - | ❌ |")
            continue
        
        # Определяем статус
        if (result['syntax_ok'] and 
            result['pylint_score'] >= 8.0 and 
            result['flake8_errors'] == 0 and 
            result['ruff_errors'] == 0):
            status = "✅ Отлично"
        elif result['syntax_ok']:
            status = "⚠️ Средне"
        else:
            status = "❌ Ошибка"
        
        print(f"| Задача {task_file[5]} | `{task_file}` | "
              f"{'✅' if result['syntax_ok'] else '❌'} | "
              f"{result['pylint_score']}/10 | "
              f"{result['flake8_errors']} | "
              f"{result['ruff_errors']} | {status} |")
    
    print("")
    print("---")
    print("")
    
    # Детальный анализ каждого файла
    for task_file in task_files:
        result = analyze_task_file(task_file)
        if result is None:
            print(f"### ⚠️ Файл `{task_file}` не найден")
            print("")
            print("Студент еще не сдал эту задачу.")
            print("")
            print("---")
            print("")
            continue
        
        print(f"### 📄 Анализ файла: **{task_file}**")
        print("")
        
        print(f"**Синтаксис:** {'✅ Корректен' if result['syntax_ok'] else '❌ Ошибка'}")
        if not result['syntax_ok'] and 'syntax_error' in result:
            print(f"```\n{result['syntax_error']}\n```")
        print("")
        
        print(f"**PyLint оценка:** {result['pylint_score']}/10")
        print("")
        
        if result['flake8_errors'] > 0:
            print(f"**Flake8 ошибки ({result['flake8_errors']}):**")
            print("```")
            print(result['flake8_output'])
            print("```")
        else:
            print("**Flake8:** ✅ Нет ошибок")
        print("")
        
        if result['ruff_errors'] > 0:
            print(f"**Ruff ошибки ({result['ruff_errors']}):**")
            print("```")
            print(result['ruff_output'])
            print("```")
        else:
            print("**Ruff:** ✅ Нет ошибок")
        print("")
        
        print("---")
        print("")

if __name__ == "__main__":
    main()
