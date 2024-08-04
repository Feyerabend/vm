import dvm as dvm

class Test:
    def __init__(self, vm):
        self.vm = vm

    def run_test(self, test_name):
        if hasattr(self, test_name):
            getattr(self, test_name)()
        else:
            print(f"Unknown test: {test_name}")

    def test_arithmetic(self):
        print("Running arithmetic test ..")
        print("1 + 2") 
        code = [dvm.OP.SET.value, 1, dvm.OP.SET.value, 2, dvm.OP.ADD.value, dvm.OP.PRINT.value, dvm.OP.HALT.value]
        self.reset_vm(code, start=0)
        self.vm.run()  # Expected output: 3
        print("Expected output: 3.")

    def test_division_by_zero(self):
        print("Running division by zero test ..")
        code = [dvm.OP.SET.value, 1, dvm.OP.SET.value, 0, dvm.OP.DIV.value, dvm.OP.PRINT.value, dvm.OP.HALT.value]
        self.reset_vm(code, start=0)
        try:
            self.vm.run()  # Should raise an exception
        except Exception as e:
            print(f"Exception caught: {e}")

    def test_subtraction(self):
        print("Running subtraction test ..")
        print("5 - 3") 
        code = [dvm.OP.SET.value, 5, dvm.OP.SET.value, 3, dvm.OP.SUB.value, dvm.OP.PRINT.value, dvm.OP.HALT.value]
        self.reset_vm(code, start=0)
        self.vm.run()  # Expected output: 2
        print("Expected output: 2.")

    def test_multiplication(self):
        print("Running multiplication test ..")
        print("4 * 3") 
        code = [dvm.OP.SET.value, 4, dvm.OP.SET.value, 3, dvm.OP.MUL.value, dvm.OP.PRINT.value, dvm.OP.HALT.value]
        self.reset_vm(code, start=0)
        self.vm.run()  # Expected output: 12
        print("Expected output: 12.")

    def test_load_store(self):
        print("Running load/store test ..")
        print("Storing 7 in variable 0 and loading it") 
        code = [dvm.OP.SET.value, 7, dvm.OP.STORE.value, 0, dvm.OP.LOAD.value, 0, dvm.OP.PRINT.value, dvm.OP.HALT.value]
        self.reset_vm(code, start=0)
        self.vm.run()  # Expected output: 7
        print("Expected output: 7.")

    def test_conditional_jump(self):
        print("Running conditional jump test ..")
        print("Conditional jump based on value (1 != 0, jump to HALT)") 
        code = [
            dvm.OP.SET.value, 1,
            dvm.OP.JPNZ.value, 7,
            dvm.OP.SET.value, 0,        # skip
            dvm.OP.PRINT.value,         # skip
            dvm.OP.HALT.value
        ]
        self.reset_vm(code, start=0)
        self.vm.run()  # Expected output: no output since it jumps directly to HALT
        print("Expected no output due to conditional jump.")

    def test_and(self):
        print("Running AND test ..")
        print("1 AND 1") 
        code = [dvm.OP.SET.value, 1, dvm.OP.SET.value, 1, dvm.OP.AND.value, dvm.OP.PRINT.value, dvm.OP.HALT.value]
        self.reset_vm(code, start=0)
        self.vm.run()  # Expected output: 1
        print("Expected output: 1.")

    def test_eq(self):
        print("Running EQ test ..")
        print("1 == 1") 
        code = [dvm.OP.SET.value, 1, dvm.OP.SET.value, 1, dvm.OP.EQ.value, dvm.OP.PRINT.value, dvm.OP.HALT.value]
        self.reset_vm(code, start=0)
        self.vm.run()  # Expected output: 1 (true)
        print("Expected output: 1.")

    def test_gt(self):
        print("Running GT test ..")
        print("2 > 1") 
        code = [dvm.OP.SET.value, 2, dvm.OP.SET.value, 1, dvm.OP.GT.value, dvm.OP.PRINT.value, dvm.OP.HALT.value]
        self.reset_vm(code, start=0)
        self.vm.run()  # Expected output: 1 (true)
        print("Expected output: 1.")

    def test_gq(self):
        print("Running GQ test ..")
        print("2 >= 1") 
        code = [dvm.OP.SET.value, 2, dvm.OP.SET.value, 1, dvm.OP.GQ.value, dvm.OP.PRINT.value, dvm.OP.HALT.value]
        self.reset_vm(code, start=0)
        self.vm.run()  # Expected output: 1 (true)
        print("Expected output: 1.")

    def test_lt(self):
        print("Running LT test ..")
        print("1 < 2") 
        code = [dvm.OP.SET.value, 1, dvm.OP.SET.value, 2, dvm.OP.LT.value, dvm.OP.PRINT.value, dvm.OP.HALT.value]
        self.reset_vm(code, start=0)
        self.vm.run()  # Expected output: 1 (true)
        print("Expected output: 1.")

    def test_lq(self):
        print("Running LQ test ..")
        print("1 <= 2") 
        code = [dvm.OP.SET.value, 1, dvm.OP.SET.value, 2, dvm.OP.LQ.value, dvm.OP.PRINT.value, dvm.OP.HALT.value]
        self.reset_vm(code, start=0)
        self.vm.run()  # Expected output: 1 (true)
        print("Expected output: 1.")

    def test_mod(self):
        print("Running MOD test ..")
        print("5 % 2") 
        code = [dvm.OP.SET.value, 5, dvm.OP.SET.value, 2, dvm.OP.MOD.value, dvm.OP.PRINT.value, dvm.OP.HALT.value]
        self.reset_vm(code, start=0)
        self.vm.run()  # Expected output: 1
        print("Expected output: 1.")

    def test_neq(self):
        print("Running NEQ test ..")
        print("1 != 2") 
        code = [dvm.OP.SET.value, 1, dvm.OP.SET.value, 2, dvm.OP.NEQ.value, dvm.OP.PRINT.value, dvm.OP.HALT.value]
        self.reset_vm(code, start=0)
        self.vm.run()  # Expected output: 1 (true)
        print("Expected output: 1.")

    def test_or(self):
        print("Running OR test ..")
        print("1 OR 0") 
        code = [dvm.OP.SET.value, 1, dvm.OP.SET.value, 0, dvm.OP.OR.value, dvm.OP.PRINT.value, dvm.OP.HALT.value]
        self.reset_vm(code, start=0)
        self.vm.run()  # Expected output: 1
        print("Expected output: 1.")

    def test_xor(self):
        print("Running XOR test ..")
        print("1 XOR 0") 
        code = [dvm.OP.SET.value, 1, dvm.OP.SET.value, 0, dvm.OP.XOR.value, dvm.OP.PRINT.value, dvm.OP.HALT.value]
        self.reset_vm(code, start=0)
        self.vm.run()  # Expected output: 1
        print("Expected output: 1.")

    def test_rstore_rload(self):
        print("Running RSTORE and RLOAD test ..")
        print("Storing value 42 at index 2 and then loading it back")
        code = [
            dvm.OP.SET.value, 42,
            dvm.OP.SET.value, 2,
            dvm.OP.RSTORE.value,
            dvm.OP.SET.value, 2,
            dvm.OP.RLOAD.value,
            dvm.OP.PRINT.value,
            dvm.OP.HALT.value
        ]
        self.reset_vm(code, start=0)
        self.vm.run()  # Expected output: 42
        print("Expected output: 42.")

    def test_rstore_out_of_bounds(self):
        print("Running RSTORE out of bounds test ..")
        print("Attempting to store value 42 at an out-of-bounds index 10")
        code = [
            dvm.OP.SET.value, 42,
            dvm.OP.SET.value, 10,
            dvm.OP.RSTORE.value,
            dvm.OP.HALT.value
        ]
        self.reset_vm(code, start=0)
        try:
            self.vm.run()  # Expected to raise an exception
        except Exception as e:
            print(f"Expected exception: {e}")

    def test_rload_out_of_bounds(self):
        print("Running RLOAD out of bounds test ..")
        print("Attempting to load value from an out-of-bounds index 10")
        code = [
            dvm.OP.SET.value, 10,
            dvm.OP.RLOAD.value,
            dvm.OP.HALT.value
        ]

    def test_function_call(self):
        print("Running function call test ..")
        print("Calling function with 2 arguments, adding them, and returning the result")
        code = [
            # Main program
            dvm.OP.SET.value, 5,
            dvm.OP.STARG.value, 0,
            dvm.OP.SET.value, 3,
            dvm.OP.STARG.value, 1,
            dvm.OP.CALL.value, 14,
            dvm.OP.LOAD.value, 0,
            dvm.OP.PRINT.value,
            dvm.OP.HALT.value,
            # add two arguments (starting at address 14)
            dvm.OP.LDARG.value, 0,
            dvm.OP.LDARG.value, 1,
            dvm.OP.ADD.value,
            dvm.OP.STORE.value, 0,
            dvm.OP.RET.value
        ]
        self.reset_vm(code, start=0)
        self.vm.run()  # Expected output: 8
        print("Expected output: 8.")

    def reset_vm(self, code, start):
        self.vm.stack = []
        self.vm.sp = -1
        self.vm.fp = 0
        self.vm.pc = start
        self.vm.code = code
        self.vm.arrs = [0] * len(self.vm.arrs)
        self.vm.args = [0] * len(self.vm.args)
        self.vm.vars = [0] * len(self.vm.vars)

def main():
    # Create a VM instance
    vm = dvm.VM([], 0, 2048, 2048, 2048)
    tester = Test(vm)

    # Run tests
    tests = [
        "test_arithmetic",
        "test_division_by_zero",
        "test_subtraction",
        "test_multiplication",
        "test_load_store",
        "test_conditional_jump",
        "test_and",
        "test_eq",
        "test_gt",
        "test_gq",
        "test_lt",
        "test_lq",
        "test_mod",
        "test_neq",
        "test_or",
        "test_xor",
        "test_rstore_rload",
        "test_rstore_out_of_bounds",
        "test_rload_out_of_bounds",
        "test_function_call"
    ]

    for test in tests:
        tester.run_test(test)

if __name__ == "__main__":
    main()
