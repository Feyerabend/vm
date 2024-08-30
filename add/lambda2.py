
class VirtualMachine:
    def __init__(self):
        self.stack = []
        self.env = {}

    def run(self, instructions):
        pc = 0
        while pc < len(instructions):
            instr = instructions[pc]

            print(f"Executing instruction: {instr}")
            print(f"Stack before execution: {self.stack}")

            if isinstance(instr, tuple) and instr[0] == 'CLOSURE':
                # closure with (body, env)
                self.stack.append(instr)
            else:
                parts = instr.split()
                opcode = parts[0]

                if opcode == 'PUSH':
                    value = parts[1]
                    if value.isdigit():
                        value = int(value)
                        if value == 0:
                            # Church numeral 0
                            self.stack.append(lambda f: lambda x: x)
                        elif value == 1:
                            # Church numeral 1
                            self.stack.append(lambda f: lambda x: f(x))
                        elif value == 2:
                            # Church numeral 2
                            self.stack.append(lambda f: lambda x: f(f(x)))
                        else:
                            # General Church numeral
                            def church_numeral(n):
                                return lambda f: lambda x: f(church_numeral(n - 1)(f)(x)) if n > 0 else x
                            self.stack.append(church_numeral(value))
                    else:
                        self.stack.append(value)

                elif opcode == 'LOAD':
                    var = parts[1]
                    if var in self.env:
                        self.stack.append(self.env[var])
                    else:
                        raise ValueError(f"Variable '{var}' not found in environment")

                elif opcode == 'APPLY':
                    arg = self.stack.pop()
                    func = self.stack.pop()
                    if isinstance(func, tuple) and func[0] == 'CLOSURE':
                        func_body, closure_env = func[1], func[2]
                        new_vm = VirtualMachine()
                        new_vm.env = closure_env.copy()
                        new_vm.env.update({'x': arg})
                        result = new_vm.run(func_body)
                        self.stack.append(result)
                        return result  # stop/return after APPLY since it's the final result
                    elif callable(func):
                        result = func(arg)
                        self.stack.append(result)
                    else:
                        raise ValueError("Expected a function or closure during APPLY")

                elif opcode == 'RET':
                    if not self.stack:
                        raise IndexError("Stack is empty during RET execution")
                    return self.stack.pop()

                elif opcode == 'ADD':
                    if len(self.stack) < 2:
                        raise IndexError("Not enough values on the stack to perform ADD")
                    b = self.stack.pop()
                    a = self.stack.pop()
                    if callable(a) and callable(b):
                        # Church numeral addition
                        def add_church(m, n):
                            return lambda f: lambda x: m(f)(n(f)(x))
                        self.stack.append(add_church(a, b))
                    else:
                        raise TypeError("ADD operation expects Church numerals")
                else:
                    raise ValueError(f"Unknown opcode: {opcode}")

            print(f"Stack after execution: {self.stack}\n")

            pc += 1

        if len(self.stack) == 1:
            return self.stack.pop()
        raise RuntimeError("Program terminated without returning a value")


# helper: define a function to convert Church numerals to integers
def church_to_int(church_numeral):
    return church_numeral(lambda x: x + 1)(0)


def compile_expr(expr):
    if isinstance(expr, str):  # variable
        return [f'LOAD {expr}']
    elif isinstance(expr, int):  # Integer literal
        return [f'PUSH {expr}']
    elif isinstance(expr, tuple):
        if expr[0] == 'lambda':  # Abstraction
            _, var, body = expr
            body_code = compile_expr(body) + ['RET']  # RET to indicate return -- not necessary
            return [('CLOSURE', body_code, {})]  # store closure
        elif expr[0] == 'apply':  # application
            _, func, arg = expr
            return compile_expr(func) + compile_expr(arg) + ['APPLY']
        elif expr[0] == 'add':  # addition
            _, num1, num2 = expr
            return compile_expr(num1) + compile_expr(num2) + ['ADD']
        else:
            raise ValueError("Unknown tuple expression: " + str(expr))
    else:
        raise ValueError("Invalid expression: " + str(expr))


# addition expression: (add 1 19)
expr = ('add', 1, 19)

# compile addition expression to assembly
assembly = compile_expr(expr)
print("Compiled Assembly:")
print(assembly)

# set up the virtual machine and run the compiled assembly
vm = VirtualMachine()
result = vm.run(assembly)

# convert the result Church numeral to integer
print("Final result:", church_to_int(result))  # output: 3
