import re

# حافظه برای ذخیره متغیرها و توابع
variables = {}
functions = {}

# ارزیابی عبارات
def evaluate(expression, local_vars={}):
    try:
        # بررسی رشته
        if expression.startswith('"') and expression.endswith('"'):
            return expression[1:-1]
        # ارزیابی متغیرها یا عبارات ریاضی
        return eval(expression, {}, {**variables, **local_vars})
    except Exception as e:
        raise ValueError(f"Error evaluating expression: {expression} ({e})")

# اجرای دستور 'say'
def execute_say(command, local_vars):
    match = re.match(r'say\s+(.+)', command)
    if match:
        value = evaluate(match.group(1), local_vars)
        print(value)
    else:
        raise SyntaxError(f"Invalid syntax in 'say': {command}")

# اجرای دستور 'set'
def execute_set(command, local_vars):
    match = re.match(r'set\s+(\w+)\s*=\s*(.+)', command)
    if match:
        var_name = match.group(1)
        value = evaluate(match.group(2), local_vars)
        variables[var_name] = value
    else:
        raise SyntaxError(f"Invalid syntax in 'set': {command}")

# اجرای حلقه 'repeat'
def execute_repeat(command, local_vars):
    match = re.match(r'repeat\s+(\d+)\s*\{\s*(.+)\s*\}', command)
    if match:
        count = int(match.group(1))
        body = match.group(2)
        for _ in range(count):
            interpret(body, local_vars)
    else:
        raise SyntaxError(f"Invalid syntax in 'repeat': {command}")

# اجرای کد
def interpret(line, local_vars={}):
    line = line.strip()
    if line.startswith("say"):
        execute_say(line, local_vars)
    elif line.startswith("set"):
        execute_set(line, local_vars)
    elif line.startswith("repeat"):
        execute_repeat(line, local_vars)
    else:
        raise SyntaxError(f"Unknown command: {line}")

# رابط کاربری
def run():
    print("Choobin Interpreter - وارد کردن کد:")
    while True:
        try:
            code = input(">>> ")
            if code.lower() == "exit":
                break
            interpret(code)
        except Exception as e:
            print(e)

if __name__ == "__main__":
    run()
