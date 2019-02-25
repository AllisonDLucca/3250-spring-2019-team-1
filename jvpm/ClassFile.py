class ConstantInfo():
    tag = 0
    info = []
    name_index = 0

class ClassFile():
    def __init__(self):
        with open('test.class', 'rb') as binary_file:
            self.data = binary_file.read()
        self.c_pool_table = []

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

    def get_constant_pool_size(self):
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
            thing.tag = self.data[i + index_offset]
            index_offset += 1
            if thing.tag == 1:
                bytesNeeded = self.data[i + index_offset] + self.data[i + index_offset + 1]
                index_offset += 2
            else:
                bytesNeeded = switch.get(thing.tag)
            for x in range (0,bytesNeeded):
                thing.info.append(self.data[i + index_offset])
                index_offset += 1
            self.c_pool_table.append(thing)
            index_offset -= 1
        print(index_offset)
        return index_offset

    def get_flags(self):
        offset = self.get_constant_pool_count()
        return self.data[offset] + self.data[offset+1]

    def get_this_class(self):
        offset = self.get_constant_pool_count()
        return self.data[offset+2] + self.data[offset+3]

    def get_super_class(self):
        offset = self.get_constant_pool_count()
        return self.data[offset+4] + self.data[offset+5]

    def get_interface_count(self):
        offset = self.get_constant_pool_count()
        return self.data[offset+6] + self.data[offset+7]


    


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
    #print('interface count: ' + java.get_interface_count())
    print('interface count: ', java.get_interface_count())