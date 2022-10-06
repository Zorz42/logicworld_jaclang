class VirtualMachine:
    def __init__(self, memory_size: int):
        self.memory = [0] * memory_size
        self.registers = [0] * 8
        self.stack_pointer = 0
        self.program_counter = 0
        self.cycle_count = 0
        self.max_stack = 0

    def getMemorySize(self):
        return len(self.memory)

    def pushToStack(self, value: int):
        self.memory[self.stack_pointer] = value & 0xFF
        self.memory[self.stack_pointer + 1] = (value >> 8) & 0xFF
        self.stack_pointer += 2
        self.max_stack = max(self.stack_pointer, self.max_stack)

    def popFromStack(self) -> int:
        self.stack_pointer -= 2
        return self.memory[self.stack_pointer] + (self.memory[self.stack_pointer + 1] << 8)

    def getReturnCode(self) -> int:
        return self.registers[0]

    def getCycleCount(self) -> int:
        return self.cycle_count

    def run(self, instructions: list[int]):
        for i in range(len(instructions)):
            self.memory[i] = instructions[i]
        self.stack_pointer = len(instructions)

        self.cycle_count = 0
        self.max_stack = 0
        while True:
            curr_opcode = self.memory[self.program_counter]
            if curr_opcode == 0b00000:  # nop
                break
            elif curr_opcode == 0b00001:  # add
                reg_a = self.memory[self.program_counter + 1]
                reg_b = self.memory[self.program_counter + 2]
                reg_save = self.memory[self.program_counter + 3]
                self.registers[reg_save] = self.registers[reg_a] + self.registers[reg_b]
                self.program_counter += 4
            elif curr_opcode == 0b00010:  # sub
                reg_a = self.memory[self.program_counter + 1]
                reg_b = self.memory[self.program_counter + 2]
                reg_save = self.memory[self.program_counter + 3]
                self.registers[reg_save] = self.registers[reg_b] - self.registers[reg_a]
                self.program_counter += 4
            elif curr_opcode == 0b00011:  # bsl
                reg_a = self.memory[self.program_counter + 1]
                reg_b = self.memory[self.program_counter + 2]
                reg_save = self.memory[self.program_counter + 3]
                self.registers[reg_save] = self.registers[reg_a] << self.registers[reg_b]
                self.program_counter += 4
            elif curr_opcode == 0b00100:  # bsr
                reg_a = self.memory[self.program_counter + 1]
                reg_b = self.memory[self.program_counter + 2]
                reg_save = self.memory[self.program_counter + 3]
                self.registers[reg_save] = self.registers[reg_a] >> self.registers[reg_b]
                self.program_counter += 4
            elif curr_opcode == 0b00101:  # or
                reg_a = self.memory[self.program_counter + 1]
                reg_b = self.memory[self.program_counter + 2]
                reg_save = self.memory[self.program_counter + 3]
                self.registers[reg_save] = self.registers[reg_a] | self.registers[reg_b]
                self.program_counter += 4
            elif curr_opcode == 0b00110:  # xor
                reg_a = self.memory[self.program_counter + 1]
                reg_b = self.memory[self.program_counter + 2]
                reg_save = self.memory[self.program_counter + 3]
                self.registers[reg_save] = self.registers[reg_a] ^ self.registers[reg_b]
                self.program_counter += 4
            elif curr_opcode == 0b00111:  # and
                reg_a = self.memory[self.program_counter + 1]
                reg_b = self.memory[self.program_counter + 2]
                reg_save = self.memory[self.program_counter + 3]
                self.registers[reg_save] = self.registers[reg_a] & self.registers[reg_b]
                self.program_counter += 4
            elif curr_opcode == 0b01000:  # not
                reg_a = self.memory[self.program_counter + 1]
                reg_save = self.memory[self.program_counter + 3]
                self.registers[reg_save] = ~self.registers[reg_a]
                self.program_counter += 4
            elif curr_opcode == 0b01001:  # xnor
                reg_a = self.memory[self.program_counter + 1]
                reg_b = self.memory[self.program_counter + 2]
                reg_save = self.memory[self.program_counter + 3]
                self.registers[reg_save] = ~(self.registers[reg_a] ^ self.registers[reg_b])
                self.program_counter += 4
            elif curr_opcode == 0b01010:  # nand
                reg_a = self.memory[self.program_counter + 1]
                reg_b = self.memory[self.program_counter + 2]
                reg_save = self.memory[self.program_counter + 3]
                self.registers[reg_save] = ~(self.registers[reg_a] & self.registers[reg_b])
                self.program_counter += 4
            elif curr_opcode == 0b01011:  # memw
                reg_addr = self.memory[self.program_counter + 1]
                reg_value = self.memory[self.program_counter + 2]
                offset = self.memory[self.program_counter + 3]
                address = self.registers[reg_addr] + offset
                if (offset >> 7) & 1 == 1:
                    address -= 1 << 8
                value = self.registers[reg_value]
                self.memory[address] = value & 0xFF
                self.memory[address + 1] = (value >> 8) & 0xFF
                self.program_counter += 4
            elif curr_opcode == 0b01100:  # memr
                reg_addr = self.memory[self.program_counter + 1]
                offset = self.memory[self.program_counter + 2]
                reg_save = self.memory[self.program_counter + 3]
                address = self.registers[reg_addr] + offset
                if (offset >> 7) & 1 == 1:
                    address -= 1 << 8
                value = self.memory[address] + (self.memory[address + 1] << 8)
                self.registers[reg_save] = value
                self.program_counter += 4
            elif curr_opcode == 0b01101:  # imm
                reg = self.memory[self.program_counter + 1]
                value = self.memory[self.program_counter + 2] + (self.memory[self.program_counter + 3] << 8)
                self.registers[reg] = value
                self.program_counter += 4
            elif curr_opcode == 0b01110:  # mov
                reg = self.memory[self.program_counter + 1]
                reg_save = self.memory[self.program_counter + 3]
                self.registers[reg_save] = self.registers[reg]
                self.program_counter += 4
            elif curr_opcode == 0b01111:  # cmp
                reg1 = self.memory[self.program_counter + 1]
                reg2 = self.memory[self.program_counter + 2]
                flags = self.memory[self.program_counter + 3]
                val1 = self.registers[reg1]
                val2 = self.registers[reg2]
                greater = (flags >> 0) % 2 == 1
                lesser = (flags >> 1) % 2 == 1
                equal = (flags >> 2) % 2 == 1
                result = (val1 > val2 and greater) or (val1 < val2 and lesser) or (val1 == val2 and equal)
                self.registers[0] = 1 if result else 0
                self.program_counter += 4
            elif curr_opcode == 0b10000:  # jmp
                reg = self.memory[self.program_counter + 1]
                cond = self.memory[self.program_counter + 2]
                if cond == 1 or self.registers[0] == 1:
                    self.program_counter = self.registers[reg]
                else:
                    self.program_counter += 4
            # elif curr_opcode == 0b10001:  # gpudraw
            #     self.program_counter += 2
            # elif curr_opcode == 0b10010:  # gpudisplay
            #     self.program_counter += 2
            elif curr_opcode == 0b10011:  # push
                reg = self.memory[self.program_counter + 2]
                self.pushToStack(self.registers[reg])
                self.program_counter += 4
            elif curr_opcode == 0b10100:  # pop
                reg = self.memory[self.program_counter + 3]
                self.registers[reg] = self.popFromStack()
                self.program_counter += 4
            elif curr_opcode == 0b10101:  # setsp
                reg = self.memory[self.program_counter + 1]
                self.stack_pointer = self.registers[reg]
                self.program_counter += 2
            elif curr_opcode == 0b10110:  # getsp
                reg = self.memory[self.program_counter + 3]
                self.registers[reg] = self.stack_pointer
                self.program_counter += 4
            else:
                print(f"Unknown opcode: {curr_opcode} {curr_opcode:b}")
                return

            self.cycle_count += 1
