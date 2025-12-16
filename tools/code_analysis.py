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
        'flake8_output': '',
        'ruff_details': []
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
            ['flake8', filename, '--statistics'],
            capture_output=True,
            text=True
        )
        results['flake8_output'] = flake8_result.stdout
        if flake8_result.stdout.strip():
            lines = [l for l in flake8_result.stdout.split('\n') if filename in l]
            results['flake8_errors'] = len(lines)
            results['flake8_details'] = lines[:10]  # Первые 10 ошибок
        else:
            results['flake8_errors'] = 0
    except Exception as e:
        results['flake8_error'] = str(e)
    
    # Ruff ошибки - более детальный анализ
    try:
        # Запускаем Ruff с детальным выводом
        ruff_result = subprocess.run(
            ['ruff', 'check', filename, '--output-format', 'concise'],
            capture_output=True,
            text=True
        )
        results['ruff_output'] = ruff_result.stdout + ruff_result.stderr
        
        # Парсим ошибки
        error_lines = []
        for line in results['ruff_output'].split('\n'):
            if filename in line and ':' in line:
                error_lines.append(line.strip())
        
        results['ruff_errors'] = len(error_lines)
        results['ruff_details'] = error_lines[:10]  # Первые 10 ошибок
        
        # Если Ruff говорит "All checks passed", но мы считаем ошибки
        if "All checks passed" in results['ruff_output'] and results['ruff_errors'] == 0:
            # Перезапускаем с другим форматом
            ruff_result2 = subprocess.run(
                ['ruff', 'check', filename, '--statistics'],
                capture_output=True,
                text=True
            )
            if "found" in ruff_result2.stdout:
                # Парсим число найденных ошибок
                import re
                match = re.search(r'found (\d+)', ruff_result2.stdout)
                if match:
                    results['ruff_errors'] = int(match.group(1))
                    
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
            print(f"```\n{result['syntax_error'][:200]}\n```")
        print("")
        
        print(f"**PyLint оценка:** {result['pylint_score']}/10")
        print("")
        
        if result['flake8_errors'] > 0 and 'flake8_details' in result:
            print(f"**Flake8 ошибки ({result['flake8_errors']}):**")
            print("```")
            for error in result['flake8_details']:
                print(error)
            if result['flake8_errors'] > 10:
                print(f"... и еще {result['flake8_errors'] - 10} ошибок")
            print("```")
        elif result['flake8_errors'] > 0:
            print(f"**Flake8:** ❌ {result['flake8_errors']} ошибок")
            print("```")
            print(result['flake8_output'][:500])
            print("```")
        else:
            print("**Flake8:** ✅ Нет ошибок")
        print("")
        
        if result['ruff_errors'] > 0 and result['ruff_details']:
            print(f"**Ruff ошибки ({result['ruff_errors']}):**")
            print("```")
            for error in result['ruff_details']:
                print(error)
            if result['ruff_errors'] > 10:
                print(f"... и еще {result['ruff_errors'] - 10} ошибок")
            print("```")
        elif result['ruff_errors'] > 0:
            print(f"**Ruff:** ❌ {result['ruff_errors']} ошибок")
            print("```")
            print(result['ruff_output'][:500])
            print("```")
        elif "All checks passed" in result['ruff_output']:
            print("**Ruff:** ✅ Все проверки пройдены")
        else:
            print(f"**Ruff:** ❓ {result['ruff_output'][:100]}")
        print("")
        
        print("---")
        print("")

if __name__ == "__main__":
    main()
