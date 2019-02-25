class ConstantInfo():
    def __init__(self):
        self.tag = 0
        self.info = []
        self.name_index = 0

class methodInfo():
    def __init__(self):
        self.value = 0

class ClassFile():
    def __init__(self):
        with open('test.class', 'rb') as binary_file:
            self.data = binary_file.read()
        self.c_pool_table = []
        self.cpoolsize = 0
        self.interface_table = []
        self.method_table= []

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
                index_offset += 1
            print("Constant #", i, " tag: ", thing.tag, " value: ", thing.info)
            self.c_pool_table.append(thing)
<<<<<<< HEAD
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

    def create_interface(self):
        itable = [self.get_interface_count()]
        for i in range[0,len(itable)]:
            itable[i] = self.data[self.get_constant_pool_size() + 18 + i]
        self.interface_table = itable 

    def get_field_count(self):
        return self.data[18+self.get_constant_pool_size()+self.get_interface_count()]

    def create_field_table(self):
        '''dont wanna do'''
        return 
    
    def get_field_size(self):
        return self.get_field_count()*2
=======
        print(index_offset)
        return index_offset

    def get_flags(self):
        offset = self.get_constant_pool_size()
        return self.data[offset] + self.data[offset+1]

    def get_this_class(self):
        offset = self.get_constant_pool_size()
        return self.data[offset+2] + self.data[offset+3]

    def get_super_class(self):
        offset = self.get_constant_pool_size()
        return self.data[offset+4] + self.data[offset+5]

    def get_interface_count(self):
        offset = self.get_constant_pool_size()
        return self.data[offset+6] + self.data[offset+7]
>>>>>>> c51701562bc583dd7b156e9029b45450fffcb387

    def get_method_count(self):
        return self.data[20+self.get_constant_pool_size() + self.get_interface_count() + self.get_field_size()] + self.data[21+self.get_constant_pool_size() + self.get_interface_count() + self.get_field_size()]

    def create_method_table(self):
        mtable = methodInfo()
        for i in range(0, self.get_method_count()):
            print("I have no clue")
    


class OpCodes():
    def __init__(self):
        self.table = {0x00: self.not_implemented}

    def not_implemented(self):
        return 'not implemented'

    def interpret(self, value):
        return self.table[value]()

if '__main__' == __name__:
    java = ClassFile() #pragma: no cover
    print('magic: ', java.get_magic()) #pragma: no cover
    print('minor_version: ', java.get_minor()) #pragma: no cover
    print('major_version: ', java.get_major()) #pragma: no cover
    print('constant_pool_count: ', java.get_constant_pool_count()) #pragma: no cover
    print('interface count: ', java.get_interface_count())
    print('method count: ', java.get_method_count())