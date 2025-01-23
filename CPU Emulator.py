#Joshua Younger
#CPU Project

class CPU:
    def __init__(self):
        self.registers = {
            1: 0,
            2: 0,
            3: 0,
            4: 0
        }
        self.memory = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.memory_index = 0
        self.register_key = 1
        self.display = ""
        self.temp_index = 0
        

    ################################# Memory / Registers #####################################
    def load(self, address):
        return self.memory[address]

    def store(self, value):
        if self.memory_index >= 31:
            self.memory_index = 0
            self.memory[self.memory_index] = value
            self.temp_index = self.memory_index
        else:
            self.memory[self.memory_index] = value
            self.memory_index += 1
            self.temp_index = self.memory_index

    def store_to_register(self, value):
        if self.register_key >= 4:
            self.register_key = 1
            self.registers[self.register_key] = int(value, 2)
        else:
            self.registers[self.register_key] = int(value, 2)
            self.register_key += 1

    def load_from_register(self, address):
        index = int(address, 2)
        value = int(self.registers.get(index))
        return value

    def get_last_value(self):
        self.temp_index -= 1
        self.update_display(self.memory[self.temp_index])

    def update_display(self, updated):
        self.display = updated
        print(self.display)

    ################################# Mathmatics ##################################
    def add(self, source_one, source_two):
        num1 = self.load_from_register(source_one)
        num2 = self.load_from_register(source_two)
        calc_value = num1 + num2
        return calc_value

    def subtract(self, source_one, source_two):
        num1 = self.load_from_register(source_one)
        num2 = self.load_from_register(source_two)
        calc_value = num1 - num2
        return calc_value

    def multiply(self, source_one, source_two):
        num1 = self.load_from_register(source_one)
        num2 = self.load_from_register(source_two)
        calc_value = num1 * num2
        return calc_value

    def divide(self, source_one, source_two):
        num1 = self.load_from_register(source_one)
        num2 = self.load_from_register(source_two)
        calc_value = 0
        if num2 != 0:
            calc_value = num1 / num2
        else:
            print('Cannot divide by 0')
        return calc_value

    def binary_to_decimal(self, num):
        decimal = 0
        i = 0
        while(num != 0):
            dec = num % 10
            decimal = decimal + dec * pow(2, i)
            num = num // 10
            i += 1
        return(decimal)

    ################################ Binary Reader ################################
    def binary_reader(self, instruction):
        if len(instruction) != 32:
            self.update_display("Error: Instruction must be 32 bits long.")
            return
        opcode = instruction[0:6]
        source_one = instruction[6:11]
        source_two = instruction[11:16]
        store = instruction[16:26]
        function_code = instruction[26:]
        result = 0

        if opcode == '000001':
            self.store_to_register(store)
            return 
        elif opcode == '100001':
            self.get_last_value()
            return 
        elif opcode != "000000":
            self.update_display('Invalid Opcode')
            return

        if function_code == '100000':
            result = self.add(source_one, source_two)
        elif function_code == '100010':
            result = self.subtract(source_one, source_two)
        elif function_code == '011000':
            result = self.multiply(source_one, source_two)
        elif function_code == '011010':
            result = self.divide(source_one, source_two)
        else:
            self.update_display('Invalid Function')
            return
        self.store(result)
        self.update_display(result)


#################################### Test ########################################

My_CPU = CPU()
# Adds 5 and 10 to registers
My_CPU.binary_reader("00000100000000000000000101000000")
My_CPU.binary_reader("00000100000000000000001010000000")

# Arithmatic

#ADD
My_CPU.binary_reader("00000000001000100000000000100000")
#Subtract
My_CPU.binary_reader("00000000001000100000000000100010")
#Multiply
My_CPU.binary_reader("00000000001000100000000000011000")
#Divide
My_CPU.binary_reader("00000000001000100000000000011010")

# Get last three calculations
My_CPU.binary_reader("10000100000000000000000000000000")
My_CPU.binary_reader("10000100000000000000000000000000")
My_CPU.binary_reader("10000100000000000000000000000000")


#################################### Debug #######################################

#print(My_CPU.registers.items())
#print(My_CPU.memory)
#print(My_CPU.registers.get(type(1)))
#print(My_CPU.register_key)
#print(My_CPU.display)

#num_1 = My_CPU.registers.get(1)
#num_2 = My_CPU.registers.get(2)
#result = num_1 - num_2
#print(result)