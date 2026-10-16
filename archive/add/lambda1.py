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
                # A closure with (body, env)
                self.stack.append(instr)
            else:
                parts = instr.split()
                opcode = parts[0]

                if opcode == 'PUSH':
                    value = parts[1]
                    if value.isdigit():
                        self.stack.append(int(value))
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
                        new_vm.env.update({'x': arg})  # single argument for now
                        result = new_vm.run(func_body)
                        self.stack.append(result)
                        return result  # stop/return after APPLY since it's the final result
                    else:
                        raise ValueError("Expected a function or closure during APPLY")

                elif opcode == 'RET':
                    if not self.stack:
                        raise IndexError("Stack is empty during RET execution")
                    return self.stack.pop()

            print(f"Stack after execution: {self.stack}\n")

            pc += 1

        if len(self.stack) == 1:
            return self.stack.pop()
        raise RuntimeError("Program terminated without returning a value")


def compile_expr(expr):
    if isinstance(expr, str):  # variable
        return [f'LOAD {expr}']
    elif isinstance(expr, int):  # integer literal
        return [f'PUSH {expr}']
    elif isinstance(expr, tuple):
        if expr[0] == 'lambda':  # abstraction
            _, var, body = expr
            body_code = compile_expr(body) + ['RET']  # RET to indicate return -- not really needed
            return [('CLOSURE', body_code, {})]  # store as a 'closure'
        elif expr[0] == 'apply':  # application
            _, func, arg = expr
            return compile_expr(func) + compile_expr(arg) + ['APPLY']
        else:
            raise ValueError("Unknown tuple expression: " + str(expr))
    else:
        raise ValueError("Invalid expression: " + str(expr))


# lambda expression: (lambda x. x) 2
expr = ('apply', ('lambda', 'x', 'x'), 2)

# compile lambda expression to assembly
assembly = compile_expr(expr)
print("compiled assembly:")
print(assembly)

# run compiled assembly
vm = VirtualMachine()
result = vm.run(assembly)

print("Final result:", result)  # output: 2
