import sys
import json
import base64

def extract_score(encoded_result):
    """Извлекает баллы из base64 закодированного результата"""
    if not encoded_result:
        return 0
    
    try:
        decoded = base64.b64decode(encoded_result).decode('utf-8')
        data = json.loads(decoded)
        
        # Проверяем разные форматы результатов
        if 'tests' in data and len(data['tests']) > 0:
            return int(data['tests'][0].get('score', 0))
        elif 'score' in data:
            return int(data['score'])
        elif 'result' in data and 'score' in data['result']:
            return int(data['result']['score'])
        else:
            return 0
    except Exception as e:
        print(f"Error extracting score: {e}", file=sys.stderr)
        return 0

if __name__ == "__main__":
    task = sys.argv[1]
    
    # Получаем результаты из переменных окружения
    if task == "1":
        add_result = sys.argv[2]
        sub_result = sys.argv[3]
        div_zero_result = sys.argv[4]
        
        add_score = extract_score(add_result)
        sub_score = extract_score(sub_result)
        div_zero_score = extract_score(div_zero_result)
        
        total = add_score + sub_score + div_zero_score
        print(f"TASK1_TOTAL={total}")
        print(f"TASK1_DETAILS=addition:{add_score},subtraction:{sub_score},division_by_zero:{div_zero_score}")
        
    elif task == "2":
        simple_result = sys.argv[2]
        not_result = sys.argv[3]
        empty_result = sys.argv[4]
        
        simple_score = extract_score(simple_result)
        not_score = extract_score(not_result)
        empty_score = extract_score(empty_result)
        
        total = simple_score + not_score + empty_score
        print(f"TASK2_TOTAL={total}")
        print(f"TASK2_DETAILS=simple_palindrome:{simple_score},not_palindrome:{not_score},empty_string:{empty_score}")
        
    elif task == "3":
        fib0_result = sys.argv[2]
        fib1_result = sys.argv[3]
        fib10_result = sys.argv[4]
        
        fib0_score = extract_score(fib0_result)
        fib1_score = extract_score(fib1_result)
        fib10_score = extract_score(fib10_result)
        
        total = fib0_score + fib1_score + fib10_score
        print(f"TASK3_TOTAL={total}")
        print(f"TASK3_DETAILS=fibonacci_0:{fib0_score},fibonacci_1:{fib1_score},fibonacci_10:{fib10_score}")
