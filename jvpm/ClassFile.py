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
        self.table = {0x00: self.not_implemented, 0x02: self.iconst_m1}

    def not_implemented(self):
        return 'not implemented'

    def interpret(self, value):
        return self.table[value]()

    def iconst_m1(self):
        self.op_stack.append(-1)




if '__main__' == __name__:
    java = ClassFile() #pragma: no cover
    print('magic: ', java.get_magic()) #pragma: no cover
    print('minor_version: ', java.get_minor()) #pragma: no cover
    print('major_version: ', java.get_major()) #pragma: no cover
    print('constant_pool_count: ', java.get_constant_pool_count()) #pragma: no cover