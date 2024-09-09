class REGVM:
    def __init__(self):
        self.pc = 0
        self.registers = {
            'A': 0,
            'B': 0,
            'C': 0,
            'D': 0
        }
        self.flags = {
            'Z': 0, # zero
            'N': 0  # negative
        }
        self.memory = []

    def load_program(self, program):
        self.memory = program

    def fetch(self):
        if self.pc < len(self.memory):
            instruction = self.memory[self.pc]
            self.pc += 1
            return instruction
        else:
            return None

    def decode_and_execute(self, instruction):
        if not instruction:
            return False

        parts = instruction.split()
        opcode = parts[0]
        args = parts[1:]

        #print("op", opcode, ", args", args)

        if opcode == 'MOV':
            fst = args[0]
            snd = args[1]
            self.registers[fst] = int(snd)

        elif opcode == 'ADD':
            fst = args[0]
            snd = args[1]
            if snd.isalpha():
                self.registers[fst] += self.registers[snd]
            else:
                self.registers[fst] += int(snd)
            self.update_flags(self.registers[fst])

        elif opcode == 'SUB':
            fst = args[0]
            snd = args[1]
            if snd.isalpha():
                self.registers[fst] -= self.registers[snd]
            else:
                self.registers[fst] -= int(snd)
            self.update_flags(self.registers[fst])

        elif opcode == 'MUL':
            fst = args[0]
            snd = args[1]
            if snd.isalpha():
                self.registers[fst] *= self.registers[snd]
            else:
                self.registers[fst] *= int(snd)
            self.update_flags(self.registers[fst])

        elif opcode == 'CMP':
            fst = args[0]
            snd = args[1]
            if self.registers[fst] == int(snd):
                self.flags['Z'] = 1
            else:
                self.flags['Z'] = 0

        elif opcode == 'JMP':
            fst = args[0]
            self.pc = int(fst)

        elif opcode == 'JZ':
            fst = args[0]
            if self.flags['Z']:
                self.pc = int(fst)

        elif opcode == 'PRINT':
            fst = args[0]
            print(f"Register {fst}: {self.registers[fst]}")

        else:
            raise ValueError(f"Unknown opcode: {opcode}")
        
        return True
    
    def update_flags(self, value):
        self.flags['Z'] = 1 if value == 0 else 0
        self.flags['N'] = 1 if value < 0 else 0
    
    def run(self):
        while True:
            instruction = self.fetch()
            if not instruction or not self.decode_and_execute(instruction):
                break

# factorial
factorial = [
    # start:
    "MOV A 1",   # init A with 1
    "MOV B 5",   # init B with 5
    
    # loop:
    "CMP B 0",   # compare B with 0
    "JZ 7",      # if B is 0, jump to end
    
    "MUL A B",   # multiply A by B and store in A
    "SUB B 1",   # subtract 1 from B
    "JMP 2",     # jump to loop
    
    # end:
    "PRINT A",   # Print the result in register A
]

vm = REGVM()
vm.load_program(factorial)
vm.run()
