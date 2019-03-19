class ClassFile():
    def __init__(self):
        with open('test.class', 'rb') as binary_file:
            self.data = binary_file.read()

    def get_magic(self):
        magic = ""
        for i in range(4):
            magic += format(self.data[i], '02X')
        return magic

    def get_minor(self):
        return self.data[4] + self.data[5]

    def get_major(self):
        return self.data[6] + self.data[7]

    def get_constant_pool_count(self):
        return self.data[8] + self.data[9]

class OpCodes():
    def __init__(self):
        self.op_stack = []  # operand stack for the opcodes
        self.lva = []       # local variable array initialized
        self.table = {0x00: self.not_implemented, 0x02: self.iconst_m1, 0x03: self.iconst_0, 0x04: self.iconst_1, 0x05: self.iconst_2, 0x06: self.iconst_3, 
        0x07: self.iconst_4, 0x08: self.iconst_5, 0x60: self.iadd, 0x7e: self.iand, 0x6c: self.idiv, 0x68: self.imul, 0x74: self.ineg, 0x80: self.ior,
        0x70: self.irem, 0x78: self.ishl, 0x7a: self.ishr, 0x64: self.isub, 0x7c: self.iushr, 0x82: self.ixor, 0x1a: self.iload_0, 0x1b: self.iload_1,
        0x1c: self.iload_2, 0x1d: self.iload_3, 0x3b: self.istore_0, 0x3c: self.istore_1, 0x3d: self.istore_2, 0x3e: self.istore_3, 0x91: self.i2b, 0x92: self.i2c, 0x87: self.i2d, 0x86: self.i2f,
        0x85: self.i2l, 0x93: self.i2s}

    def not_implemented(self):
        return 'not implemented'

    def interpret(self, value):
        return self.table[value]()

    def iconst_m1(self):
        self.op_stack.append(-1)

    def iconst_0(self):
        self.op_stack.append(0)

    def iconst_1(self):
        self.op_stack.append(1)

    def iconst_2(self):
        self.op_stack.append(2)

    def iconst_3(self):
        self.op_stack.append(3)

    def iconst_4(self):
        self.op_stack.append(4)

    def iconst_5(self):
        self.op_stack.append(5)

    def iadd(self):
        value2 = self.op_stack.pop()
        value1 = self.op_stack.pop()
        self.op_stack.append(value1 + value2)

    def iand(self):
        value2 = self.op_stack.pop()
        value1 = self.op_stack.pop()
        self.op_stack.append(value1 & value2)

    def idiv(self):
        value2 = self.op_stack.pop()
        value1 = self.op_stack.pop()
        self.op_stack.append(value1//value2)

    def imul(self):
        value2 = self.op_stack.pop()
        value1 = self.op_stack.pop()
        self.op_stack.append(value1 * value2)

    def ineg(self):
        self.op_stack.append(self.op_stack.pop() * -1)

    def ior(self):
        value2 = self.op_stack.pop()
        value1 = self.op_stack.pop()
        self.op_stack.append(value1 | value2)

    def irem(self):
        value2 = self.op_stack.pop()
        value1 = self.op_stack.pop()
        self.op_stack.append(value1 % value2)
    
    def ishl(self):
        value2 = self.op_stack.pop()
        value1 = self.op_stack.pop()
        self.op_stack.append(value1 << value2)

    def ishr(self):
        value2 = self.op_stack.pop()
        value1 = self.op_stack.pop()
        self.op_stack.append(value1 >> value2)

    def isub(self):
        value2 = self.op_stack.pop()
        value1 = self.op_stack.pop()
        self.op_stack.append(value1 - value2)
    
    def iushr(self):
        value2 = self.op_stack.pop()
        value1 = self.op_stack.pop()
        s = value2 & 0x1f
        if value1 >= 0:
            self.op_stack.append(value1 >> s)
        else:
            self.op_stack.append((value1+0x100000000) >> s)

    def ixor(self):
        value2 = self.op_stack.pop()
        value1 = self.op_stack.pop()
        self.op_stack.append(value1 ^ value2)

    def iload_0(self):
        self.op_stack.append(self.lva[0])

    def iload_1(self):
        self.op_stack.append(self.lva[1])

    def iload_2(self):
        self.op_stack.append(self.lva[2])

    def iload_3(self):
        self.op_stack.append(self.lva[3])

    def istore_0(self):
        if len(self.lva) == 0:
            self.lva.append(self.op_stack.pop())
        else:
            self.lva[0] = self.op_stack.pop()

    def istore_1(self):
        if len(self.lva) == 1:
            self.lva.append(self.op_stack.pop())
        else:
            self.lva[1] = self.op_stack.pop()

    def istore_2(self):
        if len(self.lva) == 2:
            self.lva.append(self.op_stack.pop())
        else:
            self.lva[2] = self.op_stack.pop()

    def istore_3(self):
        if len(self.lva) == 3:
            self.lva.append(self.op_stack.pop())
        else:
            self.lva[3] = self.op_stack.pop()

    def i2b(self):                          #Josh
        value1 = self.op_stack.pop()
        self.op_stack.append(bytes(value1))

    def i2c(self):
        value1 = self.op_stack.pop()
        self.op_stack.append(chr(value1))

    def i2d(self):
        value1 = self.op_stack.pop()
        self.op_stack.append(isinstance(value1, int))

    def i2f(self):
        value1 = self.op_stack.pop()
        self.op_stack.append(float(value1))

    def i2l(self):
        value1 = self.op_stack.pop()
        self.op_stack.append(isinstance(value1, int))

    def i2s(self):
        value1 = self.op_stack.pop()
        self.op_stack.append(isinstance(value1, int))
    

if '__main__' == __name__:
    java = ClassFile() #pragma: no cover
    print('magic: ', java.get_magic()) #pragma: no cover
    print('minor_version: ', java.get_minor()) #pragma: no cover
    print('major_version: ', java.get_major()) #pragma: no cover
    print('constant_pool_count: ', java.get_constant_pool_count()) #pragma: no cover