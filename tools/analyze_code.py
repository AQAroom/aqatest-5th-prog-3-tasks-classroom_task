# tools/analyze_code.py
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
    """Анализ кода всех задач"""
    task_files = ["task_01.py", "task_02.py", "task_03.py"]
    
    print("## 🔍 ДЕТАЛЬНЫЙ АНАЛИЗ КАЧЕСТВА КОДА ДЛЯ КАЖДОЙ ЗАДАЧИ")
    print("")
    
    # Сводная таблица
    print("### 📊 Сводная таблица по задачам")
    print("")
    print("| Задача | Файл | Найден | Оценка |")
    print("|--------|------|--------|--------|")
    
    found_count = 0
    for task_file in task_files:
        if os.path.exists(task_file):
            # Получаем оценку Pylint для файла
            try:
                result = subprocess.run(
                    f"pylint {task_file} --exit-zero --score=yes",
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                # Ищем строку с оценкой
                score_line = [line for line in result.stdout.split('\n') if 'rated at' in line]
                if score_line:
                    score = score_line[0].split('rated at ')[1].split('/')[0]
                else:
                    score = "N/A"
            except:
                score = "N/A"
            
            print(f"| Задача {task_file[5]} | `{task_file}` | ✅ | {score}/10 |")
            found_count += 1
        else:
            print(f"| Задача {task_file[5]} | `{task_file}` | ❌ | - |")
    
    print("")
    print(f"**Найдено файлов: {found_count}/3**")
    print("")
    print("---")
    print("")
    
    # Детальный анализ каждого файла
    for task_file in task_files:
        if not os.path.exists(task_file):
            print(f"### ⚠️ Файл `{task_file}` не найден")
            print("")
            print("Студент еще не сдал эту задачу или файл имеет другое название.")
            print("")
            print("---")
            print("")
            continue
            
        print(f"### 📄 Анализ файла: **{task_file}**")
        print("")
        
        # Ruff
        print("#### ⚡ Ruff (быстрая проверка):")
        print("```")
        ruff_result = run_linter(f"ruff check {task_file} --exit-zero", task_file)
        if ruff_result.strip():
            print(ruff_result[:800])  # Ограничиваем вывод
            if len(ruff_result) > 800:
                print("... (вывод обрезан)")
        else:
            print("✅ Все проверки пройдены успешно!")
        print("```")
        print("")
        
        # Pylint
        print("#### 🐍 Pylint (комплексная оценка):")
        print("```")
        pylint_result = run_linter(f"pylint {task_file} --exit-zero --score=yes", task_file)
        # Берем только последние 10 строк с оценкой
        lines = pylint_result.strip().split('\n')
        if len(lines) > 10:
            print("\n".join(lines[-10:]))
        else:
            print(pylint_result)
        print("```")
        print("")
        
        # Flake8
        print("#### ✨ Flake8 (стиль кода):")
        print("```")
        flake8_result = run_linter(f"flake8 {task_file} --count --statistics --exit-zero", task_file)
        if flake8_result.strip():
            print(flake8_result[:500])
            if len(flake8_result) > 500:
                print("... (вывод обрезан)")
        else:
            print("✅ Нет нарушений стиля!")
        print("```")
        print("")
        
        # Быстрые советы
        print("#### 💡 Быстрые советы для этой задачи:")
        print("")
        
        # Проверяем наличие типичных ошибок
        with open(task_file, 'r') as f:
            content = f.read()
        
        if "input()" in content and not any(x in content for x in ["try:", "except", "int(", "float("]):
            print("- ⚠️ Проверьте обработку ввода пользователя - используйте `try-except` для преобразования типов")
        
        if len(content.split('\n')) > 50:
            print("- ⚠️ Код слишком длинный - попробуйте разбить на функции")
        
        if "print(" in content and "input(" in content:
            print("- ✅ Хорошо: используются стандартные функции ввода/вывода")
        
        print("")
