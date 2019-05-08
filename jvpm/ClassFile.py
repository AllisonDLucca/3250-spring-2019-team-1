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
    def __init__(self, path):
        with open(path, 'rb') as binary_file:
            self.data = binary_file.read()
        self.c_pool_table = []
        self.cpoolsize = 0
        self.method_table = []
        self.attribute_table = []
        self._parse_class_file()

    def _parse_class_file(self):
        if self._get_magic() != 'CAFEBABE':
            raise Exception()
        self._create_c_pool()
        self._create_method_table()
        self._create_attribute_table()

    def _get_magic(self):
        magic = ""
        for i in range(4):
            magic += format(self.data[i], '02X')
        return magic

    def _get_minor(self):
        return self.data[4] + self.data[5]

    def _get_major(self):
        return self.data[6] + self.data[7]

    def _get_constant_pool_count(self):
        return self.data[8] + self.data[9]

    def _create_c_pool(self):
        if self.c_pool_table.__len__() > 0:
            return self.c_pool_table

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
        max = int(self._get_constant_pool_count()) - 1
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
            self.c_pool_table.append(thing)
        self.cpoolsize = index_offset - 10
        return index_offset - 10

    def _get_constant_pool_size(self):
        if(len(self.c_pool_table)!=self._get_constant_pool_count()-1):
            self._create_c_pool()
        return self.cpoolsize

    def _get_flags(self):
        return self.data[10+self._get_constant_pool_size()] + self.data[self._get_constant_pool_size()+11]

    def _get_this_class(self):
        return self.data[self._get_constant_pool_size()+12] + self.data[self._get_constant_pool_size()+13]

    def _get_super_class(self):
        return self.data[self._get_constant_pool_size()+14] + self.data[self._get_constant_pool_size()+15]

    def _get_interface_count(self):
        return self.data[self._get_constant_pool_size()+16] + self.data[self._get_constant_pool_size()+17]

    def _get_field_count(self):
        return self.data[18+self._get_constant_pool_size()+self._get_interface_count()] + self.data[19+self._get_constant_pool_size()+self._get_interface_count()]
    
    def _get_field_size(self):
        return self._get_field_count()*2

    def _get_method_count(self):
        return self.data[20+self._get_constant_pool_size() + self._get_interface_count() + self._get_field_size()] + self.data[21+self._get_constant_pool_size() + self._get_interface_count() + self._get_field_size()]

    def _create_method_table(self):
        if self.method_table.__len__() > 0:
            return self.method_table

        count = 22+self._get_constant_pool_size() + self._get_interface_count() + self._get_field_size()
        for i in range(0, self._get_method_count()):
            mtable = MethodInfo()
            mtable.access_flags = self.data[count] + self.data[1+count]
            mtable.name_index = self.data[2+count] + self.data[3 + count]
            mtable.descriptor_index = self.data[4+count] + self.data[5 + count]
            self.method_table.append(mtable)
        return self.method_table

    def _get_attribute_count(self):
        count = 28 + self._get_constant_pool_size() + self._get_interface_count() + self._get_field_size()
        return self.data[count] + self.data[1 + count]

    def _create_attribute_table(self):
        if self.attribute_table.__len__() > 0:
            return self.attribute_table

        count = 30 + self._get_constant_pool_size() + self._get_interface_count() + self._get_field_size()
        for i in range(0, self._get_attribute_count()):
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
        """
        Runs the opcodes in this file
        """
        ops = OpCodes()
        table_index = 0
        code_index = 0
        while table_index < len(self.attribute_table):
            while code_index < len(self.attribute_table[table_index].code):
                value = self.attribute_table[table_index].code[code_index]
                if value == 54 or value == 21 or value == 0x17:
                    code_index += 1
                    ops.interpret(value, [self.attribute_table[table_index].code[code_index]])
                elif value == 0x12:
                    code_index += 1
                    ops.interpret(value, [self.attribute_table[table_index].code[code_index]], self.c_pool_table)
                elif value == 0xb6 or value == 0xb2:
                    code_index += 2
                    ops.interpret(value, [self.attribute_table[table_index].code[code_index-1], self.attribute_table[table_index].code[code_index]], self.c_pool_table)
                else:
                    ops.interpret(value)
                code_index += 1
            table_index += 1
        return ops


