"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # 256 bytes of memory
        self.ram = [0] * 256

        # 8 registers
        self.reg = [0] * 8

        # PC Counter
        self.pc = 0

        # Flag register
        self.fl = 0b00000000



    def load(self, filename):
        """Load a program into memory."""

        address = 0

        try:
            with open(filename) as f:
                for line in f:
                    # Skip comments
                    comment_split = line.split('#')

                    # Strip out white space
                    num = comment_split[0].strip()

                    # Ignore blank lines
                    if num == '':
                        continue

                    val = int(num, 2)
                    self.ram[address] = val
                    address += 1
                    # print(val)
        
        except FileNotFoundError:
            print('File not found')
            sys.exit(2)
        # For now, we've just hardcoded a program:

        # program = [
        #     # # From print8.ls8
        #     # 0b10000010, # LDI R0,8
        #     # 0b00000000,
        #     # 0b00001000,
        #     # 0b01000111, # PRN R0
        #     # 0b00000000,
        #     # 0b00000001, # HLT
        # ]

        # for instruction in program:
            


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | FLAG: %02X | %02X %02X %02X |" % (
            self.pc,
            self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_read(self, MAR):
        value = self.ram[MAR]
        return value

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR
        return

    def HLT(self):
        return False

    def LDI(self, i):
        oa = self.ram_read(i+1)
        ob = self.ram_read(i+2)
        self.reg[oa] = ob

    def PRN(self, i):
        oa = self.ram_read(i+1)
        print(self.reg[oa])

    def MULT(self, i):
        oa = self.ram_read(i+1)
        ob = self.ram_read(i+2)
        self.reg[oa] = self.reg[oa] * self.reg[ob]

    def COMP(self, i):
        # print('This instruction is handled by the ALU.')
        oa = self.ram_read(i+1)
        ob = self.ram_read(i+2)
        
        if self.reg[oa] == self.reg[ob]:
            self.fl = 1
        elif self.reg[oa] > self.reg[ob]:
            self.fl = 2
        elif self.reg[oa] < self.reg[ob]:
            self.fl = 4
        else:
            fl = 0
            print('Unable to compare.')

    def JMP(self, r):
        self.pc = self.reg[r]
    
    def JEQ(self, i):
        if self.fl == 1:
            self.JMP(self.ram_read(i+1))
        else:
            self.pc += 2

    def JNE(self, i):
        if self.fl != 1:
            self.JMP(self.ram_read(i+1))
        else:
            self.pc += 2


    def run(self):
        """Run the CPU."""
        running = True
        while running:
            IR = self.ram[self.pc]
            # print(IR)
            # operand_a = self.ram_read(self.pc+1)
            # operand_b = self.ram_read(self.pc+2)
            if IR == 0b10000010:
                # self.trace()
                self.LDI(self.pc)
                self.pc += 3
            elif IR == 0b01000111:
                # self.trace()
                self.PRN(self.pc)
                self.pc += 2
            elif IR == 0b10100010:
                # self.trace()
                self.MULT(self.pc)
                self.pc += 3
            elif IR == 0b00000001:
                # self.trace()
                running = self.HLT()
            elif IR == 0b10100111:
                # self.trace()
                self.COMP(self.pc)
                self.pc += 3
            elif IR == 0b01010101:
                # self.trace()
                self.JEQ(self.pc)
            elif IR == 0b01010110:
                # self.trace()
                self.JNE(self.pc)
            elif IR == 0b01010100:
                self.JMP(self.ram_read(self.pc + 1))
            else: 
                print('Unknown Instruction.')
                running = self.HLT()

        

        
