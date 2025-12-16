#!/usr/bin/env python3
import subprocess
import os
import sys

def analyze_task_file(filename):
    """Анализирует файл задачи"""
    if not os.path.exists(filename):
        return None
    
    results = {
        'file': filename,
        'exists': True,
        'pylint_score': 0,
        'flake8_errors': 0,
        'ruff_errors': 0,
        'syntax_ok': False
    }
    
    # Проверка синтаксиса
    try:
        subprocess.run(['python3', '-m', 'py_compile', filename], 
                      capture_output=True, check=True)
        results['syntax_ok'] = True
    except subprocess.CalledProcessError:
        results['syntax_ok'] = False
    
    # PyLint
    try:
        pylint_result = subprocess.run(
            ['pylint', filename, '--exit-zero', '--score=yes'],
            capture_output=True, text=True, timeout=10
        )
        for line in pylint_result.stdout.split('\n'):
            if 'rated at' in line:
                score = line.split('rated at ')[1].split('/')[0]
                results['pylint_score'] = float(score)
                break
    except:
        pass
    
    # Flake8
    try:
        flake8_result = subprocess.run(
            ['flake8', filename],
            capture_output=True, text=True
        )
        results['flake8_output'] = flake8_result.stdout
        results['flake8_errors'] = len(flake8_result.stdout.strip().split('\n')) if flake8_result.stdout.strip() else 0
    except:
        pass
    
    # Ruff - используем --exit-zero чтобы не падать на ошибках
    try:
        ruff_result = subprocess.run(
            ['ruff', 'check', filename, '--exit-zero'],
            capture_output=True, text=True
        )
        results['ruff_output'] = ruff_result.stdout
        
        # Считаем строки с ошибками
        lines = [l for l in ruff_result.stdout.split('\n') if l.strip() and ':' in l and filename in l]
        results['ruff_errors'] = len(lines)
        results['ruff_details'] = lines[:10]
        
    except:
        pass
    
    return results

def analysis():
    task_files = ['task_01.py', 'task_02.py', 'task_03.py']
    
    print("## 🔍 ДЕТАЛЬНЫЙ АНАЛИЗ КАЧЕСТВА КОДА")
    print("### Используются линтеры: PyLint, Flake8, Ruff")
    print("")
    
    # Сводная таблица
    print("### 📊 Сводная таблица по задачам")
    print("")
    print("| Задача | Файл | Синтаксис | PyLint | Flake8 | Ruff | Статус |")
    print("|--------|------|-----------|--------|--------|------|--------|")
    
    for i, task_file in enumerate(task_files, 1):
        result = analyze_task_file(task_file)
        
        if result is None:
            print(f"| Задача {i} | `{task_file}` | ❌ | - | - | - | ❌ Не сдано |")
            continue
        
        # Определяем статус
        if not result['syntax_ok']:
            status = "❌ Синтаксис"
        elif result['pylint_score'] >= 9.0 and result['flake8_errors'] == 0 and result['ruff_errors'] == 0:
            status = "✅ Отлично"
        elif result['pylint_score'] >= 7.0:
            status = "⚠️ Средне"
        else:
            status = "❌ Ошибки"
        
        print(f"| Задача {i} | `{task_file}` | "
              f"{'✅' if result['syntax_ok'] else '❌'} | "
              f"{result['pylint_score']:.1f}/10 | "
              f"{result['flake8_errors']} | "
              f"{result['ruff_errors']} | {status} |")
    
    print("")
    print("---")
    print("")
    
    # Детальный анализ
    for i, task_file in enumerate(task_files, 1):
        result = analyze_task_file(task_file)
        if result is None:
            print(f"### ⚠️ Задача {i}: Файл `{task_file}` не найден")
            print("Студент еще не сдал эту задачу.")
            print("")
            print("---")
            print("")
            continue
        
        print(f"### 📄 Задача {i}: Анализ файла **{task_file}**")
        print("")
        
        if not result['syntax_ok']:
            print("**❌ Синтаксис:** Ошибка в коде")
            print("")
        
        print(f"**🐍 PyLint:** {result['pylint_score']:.1f}/10")
        print("")
        
        if result['flake8_errors'] > 0:
            print(f"**❌ Flake8 ошибки ({result['flake8_errors']}):**")
            print("```")
            print(result['flake8_output'])
            print("```")
        else:
            print("**✅ Flake8:** Нет ошибок")
        print("")
        
        if result['ruff_errors'] > 0:
            print(f"**❌ Ruff ошибки ({result['ruff_errors']}):**")
            print("```")
            for error in result['ruff_details']:
                print(error)
            print("```")
        else:
            print("**✅ Ruff:** Нет ошибок")
            if result['ruff_output'] and "All checks passed" in result['ruff_output']:
                print("```")
                print("All checks passed!")
                print("```")
        print("")
        
        print("---")
        print("")

if __name__ == "__main__":
    analysis()
