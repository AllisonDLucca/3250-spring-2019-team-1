from jvpm.OpCodes import OpCodes

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
        with open('TestyTesticles.class', 'rb') as binary_file:
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
                elif value == 0x12:
                    j += 1
                    ops.interpret(value, [self.attribute_table[i].code[j]], self.c_pool_table)
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
