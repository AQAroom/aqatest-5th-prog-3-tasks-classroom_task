# tools/code_analysis.py
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
    
    # Flake8 ошибки - включаем все правила
    try:
        flake8_result = subprocess.run(
            ['flake8', filename, '--max-line-length=79', '--extend-ignore=E501'],
            capture_output=True,
            text=True
        )
        results['flake8_output'] = flake8_result.stdout
        if flake8_result.stdout.strip():
            lines = [l.strip() for l in flake8_result.stdout.split('\n') if l.strip()]
            results['flake8_errors'] = len(lines)
            results['flake8_details'] = lines[:15]  # Первые 15 ошибок
        else:
            results['flake8_errors'] = 0
    except Exception as e:
        results['flake8_error'] = str(e)
    
    # Ruff ошибки - используем полный набор правил
    try:
        # Запускаем Ruff с максимальной строгостью
        ruff_result = subprocess.run(
            ['ruff', 'check', filename, '--select=ALL', '--ignore=D203,D211,D212,D213,E501'],
            capture_output=True,
            text=True
        )
        results['ruff_output'] = ruff_result.stdout + ruff_result.stderr
        
        # Парсим ошибки более аккуратно
        error_lines = []
        for line in results['ruff_output'].split('\n'):
            line = line.strip()
            if line and not line.startswith('warning:') and filename in line:
                # Убираем путь к файлу для чистоты вывода
                clean_line = line.split(filename + ':', 1)[-1].strip()
                if clean_line:
                    error_lines.append(f"{filename}:{clean_line}")
        
        results['ruff_errors'] = len(error_lines)
        results['ruff_details'] = error_lines[:15]  # Первые 15 ошибок
        
        # Если Ruff ничего не нашел, но Flake8 нашел, запускаем Ruff с более строгими настройками
        if results['ruff_errors'] == 0 and results['flake8_errors'] > 0:
            ruff_result2 = subprocess.run(
                ['ruff', 'check', filename, '--select=E,W,F,C,B,A,COM,C4,ERA,ICN,INP,ISC,TID,Q,S,TCH,INT,I,N,PLE,PLW,TRY,RUF'],
                capture_output=True,
                text=True
            )
            if ruff_result2.stdout.strip():
                lines = [l.strip() for l in ruff_result2.stdout.split('\n') if l.strip()]
                results['ruff_errors'] = len(lines)
                results['ruff_details'] = lines[:15]
                results['ruff_output'] = ruff_result2.stdout
                
    except Exception as e:
        results['ruff_error'] = str(e)
        print(f"Ruff error for {filename}: {e}", file=sys.stderr)
    
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
    
    for i, task_file in enumerate(task_files, 1):
        result = analyze_task_file(task_file)
        
        if result is None:
            print(f"| Задача {i} | `{task_file}` | ❌ | - | - | - | ❌ Не сдано |")
            continue
        
        # Определяем статус
        if not result['syntax_ok']:
            status = "❌ Ошибка синтаксиса"
        elif result['pylint_score'] >= 9.0 and result['flake8_errors'] == 0 and result['ruff_errors'] == 0:
            status = "✅ Отлично"
        elif result['pylint_score'] >= 7.0 and result['flake8_errors'] <= 5 and result['ruff_errors'] <= 5:
            status = "⚠️ Средне"
        else:
            status = "❌ Много ошибок"
        
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
            if result['ruff_output'] and "All checks passed" not in result['ruff_output']:
                print("```")
                print(result['ruff_output'][:200])
                print("```")
        print("")
        
        # Быстрые советы
        print("**💡 Быстрые советы:**")
        if result['flake8_errors'] > 0:
            print(f"- Исправьте {result['flake8_errors']} ошибок Flake8 (см. выше)")
        if result['ruff_errors'] > 0:
            print(f"- Исправьте {result['ruff_errors']} ошибок Ruff (см. выше)")
        if result['pylint_score'] < 8.0:
            print(f"- Улучшите качество кода (PyLint оценка {result['pylint_score']:.1f}/10)")
        
        print("")
        print("---")
        print("")

if __name__ == "__main__":
    main()
