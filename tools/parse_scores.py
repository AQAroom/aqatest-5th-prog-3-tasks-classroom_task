# tools/code_analysis.py - исправленная версия для Ruff
import subprocess
import os
import sys
import re

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
            ['flake8', filename, '--max-line-length=79'],
            capture_output=True,
            text=True
        )
        results['flake8_output'] = flake8_result.stdout
        if flake8_result.stdout.strip():
            lines = [l.strip() for l in flake8_result.stdout.split('\n') if l.strip()]
            results['flake8_errors'] = len(lines)
            results['flake8_details'] = lines[:15]
        else:
            results['flake8_errors'] = 0
    except Exception as e:
        results['flake8_error'] = str(e)
    
    # Ruff ошибки - правильный парсинг
    try:
        # Запускаем Ruff с подробным выводом
        ruff_result = subprocess.run(
            ['ruff', 'check', filename, '--output-format', 'full'],
            capture_output=True,
            text=True
        )
        results['ruff_output'] = ruff_result.stdout
        
        # Парсим вывод Ruff правильно
        error_lines = []
        for line in results['ruff_output'].split('\n'):
            line = line.strip()
            if line and ':' in line and not line.startswith('Found'):
                # Пример строки: "task_01.py:5:5: E222 Multiple spaces after operator"
                if filename in line:
                    error_lines.append(line)
        
        results['ruff_errors'] = len(error_lines)
        results['ruff_details'] = error_lines[:15]
        
        # Если Ruff не нашел ошибок, но хочет показать что-то
        if not error_lines and results['ruff_output']:
            # Проверяем, есть ли статистика
            stats_match = re.search(r'Found (\d+) error', results['ruff_output'])
            if stats_match:
                results['ruff_errors'] = int(stats_match.group(1))
                
    except Exception as e:
        results['ruff_error'] = str(e)
        print(f"Ruff error for {filename}: {e}", file=sys.stderr)
    
    return results

def main():
    """Основная функция анализа"""
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
        elif result['pylint_score'] >= 7.0 and result['flake8_errors'] <= 3 and result['ruff_errors'] <= 3:
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
    
    # Детальный анализ каждого файла
    for i, task_file in enumerate(task_files, 1):
        result = analyze_task_file(task_file)
        if result is None:
            print(f"### ⚠️ Задача {i}: Файл `{task_file}` не найден")
            print("")
            print("Студент еще не сдал эту задачу.")
            print("")
            print("---")
            print("")
            continue
        
        print(f"### 📄 Задача {i}: Анализ файла **{task_file}**")
        print("")
        
        print(f"**Синтаксис:** {'✅ Корректен' if result['syntax_ok'] else '❌ Ошибка'}")
        if not result['syntax_ok'] and 'syntax_error' in result:
            print("```")
            print(result['syntax_error'][:300])
            print("```")
        print("")
        
        print(f"**PyLint оценка:** {result['pylint_score']:.1f}/10")
        print("")
        
        if result['flake8_errors'] > 0:
            print(f"**❌ Flake8 ошибки ({result['flake8_errors']}):**")
            print("```")
            if 'flake8_details' in result and result['flake8_details']:
                for error in result['flake8_details']:
                    print(error)
                if result['flake8_errors'] > 15:
                    print(f"... и еще {result['flake8_errors'] - 15} ошибок")
            else:
                print(result['flake8_output'][:800])
            print("```")
        else:
            print("**✅ Flake8:** Нет ошибок")
        print("")
        
        if result['ruff_errors'] > 0:
            print(f"**❌ Ruff ошибки ({result['ruff_errors']}):**")
            print("```")
            if result['ruff_details']:
                for error in result['ruff_details']:
                    print(error)
                if result['ruff_errors'] > 15:
                    print(f"... и еще {result['ruff_errors'] - 15} ошибок")
            elif result['ruff_output']:
                print(result['ruff_output'][:800])
            else:
                print("Найдены ошибки, но детали недоступны")
            print("```")
        else:
            print("**✅ Ruff:** Нет ошибок")
            if result['ruff_output']:
                print("```")
                print(result['ruff_output'][:200])
                print("```")
        print("")
        
        print("---")
        print("")

if __name__ == "__main__":
    main()
