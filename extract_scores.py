import sys
import json
import base64

def extract_score(encoded_result):
    """Извлекает баллы из base64 закодированного результата"""
    if not encoded_result or encoded_result == 'null':
        print(f"Empty or null result: {encoded_result}")
        return 0
    
    try:
        decoded = base64.b64decode(encoded_result).decode('utf-8')
        print(f"Decoded result: {decoded}")
        data = json.loads(decoded)
        
        # Проверяем разные форматы результатов
        if 'tests' in data and len(data['tests']) > 0:
            score = int(data['tests'][0].get('score', 0))
            print(f"Score from tests[0]: {score}")
            return score
        elif 'score' in data:
            score = int(data['score'])
            print(f"Score from score field: {score}")
            return score
        elif 'result' in data and 'score' in data['result']:
            score = int(data['result']['score'])
            print(f"Score from result.score: {score}")
            return score
        else:
            print(f"Unknown data format: {data}")
            return 0
    except Exception as e:
        print(f"Error extracting score: {e}", file=sys.stderr)
        return 0

if __name__ == "__main__":
    task = sys.argv[1]
    print(f"Processing task: {task}")
    
    # Получаем результаты из переменных окружения
    if task == "1":
        add_result = sys.argv[2]
        sub_result = sys.argv[3]
        div_zero_result = sys.argv[4]
        
        print(f"Addition result: {add_result[:50]}..." if add_result and len(add_result) > 50 else f"Addition result: {add_result}")
        print(f"Subtraction result: {sub_result[:50]}..." if sub_result and len(sub_result) > 50 else f"Subtraction result: {sub_result}")
        print(f"Division by zero result: {div_zero_result[:50]}..." if div_zero_result and len(div_zero_result) > 50 else f"Division by zero result: {div_zero_result}")
        
        add_score = extract_score(add_result)
        sub_score = extract_score(sub_result)
        div_zero_score = extract_score(div_zero_result)
        
        print(f"Scores: addition={add_score}, subtraction={sub_score}, division_by_zero={div_zero_score}")
        
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
