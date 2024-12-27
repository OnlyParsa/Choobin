import re

# دیکشنری برای ذخیره متغیرها
variables = {}
global_variables = {}

# تابع برای اجرای دستور say (چاپ)
def execute_say(expression):
    print(expression)

# تابع برای تعریف توابع با دستور make
def make_function(name, params, body, local_vars):
    def func(*args):
        local_vars.update(dict(zip(params, args)))
        return interpret(body, local_vars)
    variables[name] = func

# تابع برای تجزیه و اجرای دستورات
def interpret(code, local_vars={}):
    code = code.strip()

    # تجزیه دستور say (چاپ)
    if code.startswith("say"):
        expression = code[4:].strip()  # جدا کردن محتویات پرانتز
        if expression.startswith('"') and expression.endswith('"'):
            expression = expression[1:-1]  # حذف نقل قول‌ها
        execute_say(expression)

    # تجزیه دستور تعریف متغیر
    elif "=" in code:
        var_name, value = code.split("=")
        var_name = var_name.strip()
        value = evaluate(value.strip(), local_vars)
        if var_name.startswith("const"):
            if var_name[5:] in global_variables:
                print(f"Error: {var_name[5:]} is already defined!")
                return
            global_variables[var_name[5:]] = value
        else:
            local_vars[var_name] = value
        print(f"{var_name} = {value}")

    # تجزیه دستور تعریف تابع
    elif code.startswith("make"):
        match = re.match(r"make\s+(\w+)\s*\(([\w, ]+)\)\s*{\s*(.*?)\s*}", code, re.DOTALL)
        if match:
            func_name, params_str, body = match.groups()
            params = [param.strip() for param in params_str.split(",")]
            make_function(func_name, params, body, local_vars)

    # دستور شرطی if
    elif code.startswith("if"):
        match = re.match(r"if\s+\((.*)\)\s*{\s*(.*)\s*}", code)
        if match:
            condition, body = match.groups()
            condition = evaluate(condition, local_vars)
            if condition:
                interpret(body, local_vars)

    # دستور for
    elif code.startswith("for"):
        match = re.match(r"for\s+\((\w+)\s+in\s+(\w+)\)\s*{\s*(.*)\s*}", code)
        if match:
            var_name, iterable, body = match.groups()
            iterable = evaluate(iterable, local_vars)
            for item in iterable:
                local_vars[var_name] = item
                interpret(body, local_vars)

    # تکرار دستور repeat
    elif code.startswith("repeat"):
        match = re.match(r"repeat\s+(\d+)\s*{\s*(.*)\s*}", code)
        if match:
            times, body = match.groups()
            for _ in range(int(times)):
                interpret(body, local_vars)

    # پشتیبانی از واردات فایل
    elif code.startswith("import"):
        match = re.match(r"import\s+(\w+)", code)
        if match:
            filename = match.group(1)
            try:
                with open(f"{filename}.txt", "r") as file:
                    code_from_file = file.read()
                    interpret(code_from_file, local_vars)
            except FileNotFoundError:
                print(f"Error: File '{filename}.txt' not found.")

# تابع برای ارزیابی عبارت‌های ریاضی
def evaluate(expression, local_vars):
    expression = expression.strip()
    try:
        result = eval(expression, {}, {**global_variables, **local_vars})
        return result
    except Exception as e:
        return f"Error: {e}"

# ورودی از کاربر
def run():
    print("Choobin Interpreter - وارد کردن کد:")
    while True:
        code = input(">>> ")
        if code.lower() == "exit":
            break
        interpret(code)

# شروع اجرای مفسر
if __name__ == "__main__":
    run()
