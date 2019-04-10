class ConstantInfo():
    def __init__(self):
        self.tag = 0
        self.info = []
        self.name_index = 0

class MethodInfo():
    def __init__(self):
        self.access_flags = 0
        self.name_index = 0
        self.descriptor_index = 0

class CodeAttribute():
    def __init__(self):
        self.attribute_name_index = 0
        self.attribute_length = 0
        self.max_stack = 0
        self.max_locals = 0
        self.code_length = 0
        self.code = []

class ClassFile():
    def __init__(self):
        with open('Foo.class', 'rb') as binary_file:
            self.data = binary_file.read()
        self.c_pool_table = []
        self.cpoolsize = 0
        #self.interface_table = []
        self.method_table = []
        self.attribute_table = []

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

    def create_c_pool(self):
        index_offset = 10
        switch = {
            3: 4,
            4: 4,
            5: 8,
            6: 8,
            7: 2,
            8: 2,
            9: 4,
            10: 4,
            11: 4,
            12: 4,
            15: 3,
            16: 2,
            18: 4
        }
        max = int(self.get_constant_pool_count()) - 1
        for i in range (0,max):
            thing = ConstantInfo()
            thing.tag = self.data[index_offset]
            index_offset += 1
            if thing.tag == 1:
                bytesNeeded = self.data[index_offset] + self.data[index_offset + 1]
                index_offset += 2
            else:
                bytesNeeded = switch.get(thing.tag)
            for x in range (0,bytesNeeded):
                thing.info.append(self.data[x + index_offset])
            index_offset += bytesNeeded
            #print("Constant #", i, " tag: ", thing.tag, " value: ", thing.info)
            self.c_pool_table.append(thing)
        self.cpoolsize = index_offset - 10
        return index_offset - 10

    def get_constant_pool_size(self):
        if(len(self.c_pool_table)!=self.get_constant_pool_count()-1):
            self.create_c_pool()
        return self.cpoolsize

    def get_flags(self):
        return self.data[10+self.get_constant_pool_size()] + self.data[self.get_constant_pool_size()+11]

    def get_this_class(self):
        return self.data[self.get_constant_pool_size()+12] + self.data[self.get_constant_pool_size()+13]

    def get_super_class(self):
        return self.data[self.get_constant_pool_size()+14] + self.data[self.get_constant_pool_size()+15]

    def get_interface_count(self):
        return self.data[self.get_constant_pool_size()+16] + self.data[self.get_constant_pool_size()+17]

    #def create_interface(self):
    #    itable = [self.get_interface_count()]
    #    for i in range[0,len(itable)]:
    #        itable[i] = self.data[self.get_constant_pool_size() + 18 + i]
    #    self.interface_table = itable

    def get_field_count(self):
        return self.data[18+self.get_constant_pool_size()+self.get_interface_count()] + self.data[19+self.get_constant_pool_size()+self.get_interface_count()]

    #def create_field_table(self):
    #    '''dont wanna do'''
    #    return
    
    def get_field_size(self):
        return self.get_field_count()*2

    def get_method_count(self):
        return self.data[20+self.get_constant_pool_size() + self.get_interface_count() + self.get_field_size()] + self.data[21+self.get_constant_pool_size() + self.get_interface_count() + self.get_field_size()]

    def create_method_table(self):
        count = 22+self.get_constant_pool_size() + self.get_interface_count() + self.get_field_size()
        for i in range(0, self.get_method_count()):
            mtable = MethodInfo()
            mtable.access_flags = self.data[count] + self.data[1+count]
            mtable.name_index = self.data[2+count] + self.data[3 + count]
            mtable.descriptor_index = self.data[4+count] + self.data[5 + count]
            self.method_table.append(mtable)
        return self.method_table

    def get_attribute_count(self):
        count = 28 + self.get_constant_pool_size() + self.get_interface_count() + self.get_field_size()
        return self.data[count] + self.data[1 + count]

    def create_attribute_table(self):
        count = 30 + self.get_constant_pool_size() + self.get_interface_count() + self.get_field_size()
        for i in range(0, self.get_attribute_count()):
            codeAtt = CodeAttribute()
            codeAtt.attribute_name_index = self.data[count] + self.data[1 + count]
            codeAtt.attribute_length = self.data[2 + count] + self.data[3 + count] + self.data[4 + count] + self.data[5 + count]
            codeAtt.max_stack = self.data[6 + count] + self.data[7 + count]
            codeAtt.max_locals = self.data[8 + count] + self.data[9 + count]
            codeAtt.code_length = self.data[10 + count] + self.data[11 + count] + self.data[12 + count] + self.data[13 + count]
            count = count + 13
            for i in range(0, codeAtt.code_length):
                codeAtt.code.append(self.data[count + 1])
                count += 1
            self.attribute_table.append(codeAtt)
        return self.attribute_table

    def run_opcodes(self):
        ops = OpCodes()
        i = 0
        j = 0
        while i < len(self.attribute_table):
            while j < len(self.attribute_table[i].code):
                value = self.attribute_table[i].code[j]
                if value == 54 or value == 21:
                    j += 1
                    ops.interpret(value, [self.attribute_table[i].code[j]])
                elif value == 0xb6 or value == 0xb2:
                    j += 2
                    ops.interpret(value, [self.attribute_table[i].code[j-1], self.attribute_table[i].code[j]], self.c_pool_table)
                else:
                    ops.interpret(value)
                #print("stack: ", ops.op_stack)
                #print("array: ", ops.lva)
                j += 1
            i += 1
        return ops

class OpCodes():
    def __init__(self):
        self.op_stack = []  # operand stack for the opcodes
        self.lva = []       # local variable array initialized
        self.table = {0x00: self.not_implemented, 0x02: self.iconst_m1, 0x03: self.iconst_0, 0x04: self.iconst_1, 0x05: self.iconst_2, 0x06: self.iconst_3, 
        0x07: self.iconst_4, 0x08: self.iconst_5, 0x60: self.iadd, 0x7e: self.iand, 0x6c: self.idiv, 0x68: self.imul, 0x74: self.ineg, 0x80: self.ior,
        0x70: self.irem, 0x78: self.ishl, 0x7a: self.ishr, 0x64: self.isub, 0x7c: self.iushr, 0x82: self.ixor, 0x15: self.iload, 0x1a: self.iload_0, 0x1b: self.iload_1,
        0x1c: self.iload_2, 0x1d: self.iload_3, 0x36: self.istore, 0x3b: self.istore_0, 0x3c: self.istore_1, 0x3d: self.istore_2, 0x3e: self.istore_3, 0x91: self.i2b, 0x92: self.i2c, 0x87: self.i2d, 0x86: self.i2f,
        0x85: self.i2l, 0x93: self.i2s, 0xb6: self.invokevirtual, 0xb2: self.getstatic}


    def not_implemented(self):
        return 'not implemented'

    def interpret(self, value, operands = None, constants = None):
        if operands is not None and constants is not None:
            return self.table[value](operands, constants)
        elif operands is not None and constants is None:
            return self.table[value](operands)
        else:
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

    def iload(self, operands):
        index = operands.pop()
        self.op_stack.append(self.lva[index])

    def iload_0(self):
        self.op_stack.append(self.lva[0])

    def iload_1(self):
        self.op_stack.append(self.lva[1])

    def iload_2(self):
        self.op_stack.append(self.lva[2])

    def iload_3(self):
        self.op_stack.append(self.lva[3])

    def istore(self, operands):
        index = operands.pop()
        if len(self.lva) <= index:
            self.lva.append(self.op_stack.pop())
        else:
            self.lva[index] = self.op_stack.pop()

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
        self.op_stack.append(int(value1))

    def i2c(self):
        value1 = self.op_stack.pop()
        self.op_stack.append(chr(value1))

    def i2d(self):
        value1 = self.op_stack.pop()
        self.op_stack.append(float(value1))

    def i2f(self):
        value1 = self.op_stack.pop()
        self.op_stack.append(float(value1))

    def i2l(self):
        value1 = self.op_stack.pop()
        self.op_stack.append(int(value1))

    def i2s(self):
        value1 = self.op_stack.pop()
        self.op_stack.append(int(value1))

    def get_str_from_cpool(self, index, c_pool):

        const_ref = c_pool[index]

        if const_ref.tag != 1:
            class_index = const_ref.info[0] + const_ref.info[1] - 1
            val = self.get_str_from_cpool(class_index, c_pool)

            if const_ref.tag == 10:
                val += '.'
            elif const_ref.tag == 12:
                val += ':'

            if const_ref.info.__len__() > 2:
                name_type_index = const_ref.info[2] + const_ref.info[3] - 1
                val += self.get_str_from_cpool(name_type_index, c_pool)

            return val

        else:
            return bytes(const_ref.info).decode("utf-8")

    def invokevirtual(self, operands, c_pool):
        num1 = operands.pop()
        num2 = operands.pop()
        method = self.get_str_from_cpool(num1 + num2 - 1, c_pool)
        if method == 'java/io/PrintStream.println:(I)V':
            print(self.op_stack.pop())
        elif method == 'java/io/PrintStream.println:(Ljava/lang/String;)V':
            print(self.op_stack.pop())
            
    def getstatic(self, operands, c_pool):
        value1 = operands.pop()
        value2 = operands.pop()
        return self.get_str_from_cpool(value1 + value2, c_pool)


if '__main__' == __name__: #pragma: no cover
    java = ClassFile() #pragma: no cover
    print('magic: ', java.get_magic()) #pragma: no cover
    print('minor_version: ', java.get_minor()) #pragma: no cover
    print('major_version: ', java.get_major()) #pragma: no cover
    print('constant_pool_count: ', java.get_constant_pool_count()) #pragma: no cover
    print('parsing constant pool...') #pragma: no cover
    java.create_c_pool() #pragma: no cover
    for i in range(0, java.c_pool_table.__len__()): #pragma: no cover
        constant = java.c_pool_table[i] #pragma: no cover
        print("Constant #", i, " tag: ", constant.tag, " value: ", constant.info) #pragma: no cover
    print('interface count: ', java.get_interface_count()) #pragma: no cover
    print('field count: ', java.get_field_count()) #pragma: no cover
    print('method count: ', java.get_method_count()) #pragma: no cover
    java.create_method_table() #pragma: no cover
    print('attribute count: ', java.get_attribute_count()) #pragma: no cover
    java.create_attribute_table() #pragma: no cover
    java.run_opcodes() #pragma: no cover
