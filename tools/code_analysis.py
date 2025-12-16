# tools/code_analysis.py
import subprocess
import os

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
        'syntax_ok': False
    }
    
    # Проверка синтаксиса
    try:
        subprocess.run(['python3', '-m', 'py_compile', filename], 
                      capture_output=True, check=True)
        results['syntax_ok'] = True
    except:
        results['syntax_ok'] = False
    
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
    except:
        pass
    
    # Flake8 ошибки
    try:
        flake8_result = subprocess.run(
            ['flake8', filename, '--count'],
            capture_output=True,
            text=True
        )
        if flake8_result.stdout.strip().isdigit():
            results['flake8_errors'] = int(flake8_result.stdout.strip())
    except:
        pass
    
    # Ruff ошибки
    try:
        ruff_result = subprocess.run(
            ['ruff', 'check', filename],
            capture_output=True,
            text=True
        )
        # Считаем строки с ошибками
        error_lines = [line for line in ruff_result.stdout.split('\n') 
                      if filename in line and ':' in line]
        results['ruff_errors'] = len(error_lines)
    except:
        pass
    
    return results

def code_check():
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
        print("")
        
        print("#### 🐍 PyLint (оценка качества):")
        print("```")
        try:
            pylint_result = subprocess.run(
                ['pylint', task_file, '--exit-zero', '--score=yes'],
                capture_output=True,
                text=True
            )
            lines = pylint_result.stdout.strip().split('\n')
            for line in lines[-5:]:
                print(line)
        except:
            print("Не удалось выполнить PyLint")
        print("```")
        print("")
        
        print("#### ⚡ Ruff (быстрые проверки):")
        print("```")
        try:
            ruff_result = subprocess.run(
                ['ruff', 'check', task_file],
                capture_output=True,
                text=True
            )
            if ruff_result.stdout.strip():
                print(ruff_result.stdout[:300])
                if len(ruff_result.stdout) > 300:
                    print("... (вывод обрезан)")
            else:
                print("✅ Нет ошибок")
        except:
            print("Не удалось выполнить Ruff")
        print("```")
        print("")
        
        print("---")
        print("")

if __name__ == "__main__":
    code_check()
