import numpy as np

class OpCodes():
    def __init__(self):
        self.op_stack = []  # operand stack for the opcodes
        self.lva = []  # local variable array initialized
        self.table = {0x00: self.not_implemented, 0x02: self.iconst_m1, 0x03: self.iconst_0, 0x04: self.iconst_1,
                      0x05: self.iconst_2, 0x06: self.iconst_3,
                      0x07: self.iconst_4, 0x08: self.iconst_5, 0x60: self.iadd, 0x7e: self.iand, 0x6c: self.idiv,
                      0x68: self.imul, 0x74: self.ineg, 0x80: self.ior,
                      0x70: self.irem, 0x78: self.ishl, 0x7a: self.ishr, 0x64: self.isub, 0x7c: self.iushr,
                      0x82: self.ixor, 0x15: self.iload, 0x1a: self.iload_0, 0x1b: self.iload_1,
                      0x1c: self.iload_2, 0x1d: self.iload_3, 0x36: self.istore, 0x3b: self.istore_0,
                      0x3c: self.istore_1, 0x3d: self.istore_2, 0x3e: self.istore_3, 0x91: self.i2b, 0x92: self.i2c,
                      0x87: self.i2d, 0x86: self.i2f,
                      0x85: self.i2l, 0x93: self.i2s, 0xb6: self.invokevirtual, 0xb2: self.getstatic,
                      0x1e: self.lload_0, 0x1f: self.lload_1, 0x20:self.lload_2, 0x21:self.lload_3, 0x16:self.lload,
                      0x9: self.lconst_0, 0xa: self.lconst_1, 0x3f: self.lstore_0, 0x40: self.lstore_1,
                      0x41: self.lstore_2, 0x42: self.lstore_3, 0x37: self.lstore, 0x61: self.ladd, 0x65: self.lsub,
                      0x69: self.lmul, 0x6d: self.ldiv, 0x71: self.lrem, 0x75: self.lneg, 0x7d: self.lushr,
                      0x7f: self.land, 0x81: self.lor, 0x83: self.lxor, 0x88: self.l2i, 0x89: self.l2f, 0x8a: self.l2d}

    def not_implemented(self):
        return 'not implemented'

    def interpret(self, value, operands=None, constants=None):
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
        try:
            self.op_stack.append(value1//value2)
        except ZeroDivisionError:
            return 'Error: Divides by Zero'

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
        try:
            self.op_stack.append(value1 % value2)
        except ZeroDivisionError:
            return 'Error: Divides by Zero'

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
            self.op_stack.append((value1 + 0x100000000) >> s)

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

    def i2b(self):  # Josh
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

    def lload_0(self):
        frag1 = self.lva[0]
        frag2 = self.lva[1]
        self.op_stack.append(frag1)
        self.op_stack.append(frag2)

    def lload_1(self):
        frag1 = self.lva[1]
        frag2 = self.lva[2]
        self.op_stack.append(frag1)
        self.op_stack.append(frag2)

    def lload_2(self):
        frag1 = self.lva[2]
        frag2 = self.lva[3]
        self.op_stack.append(frag1)
        self.op_stack.append(frag2)

    def lload_3(self):
        frag1 = self.lva[3]
        frag2 = self.lva[4]
        self.op_stack.append(frag1)
        self.op_stack.append(frag2)

    def lload(self, operands):
        index = operands.pop()
        frag1 = self.lva[index]
        frag2 = self.lva[index+1]
        self.op_stack.append(frag1)
        self.op_stack.append(frag2)

    def lconst_0(self):
        self.op_stack.append(0)
        self.op_stack.append(0)

    def lconst_1(self):
        self.op_stack.append(0)
        self.op_stack.append(1)

    def lstore_0(self):
        frag2 = self.op_stack.pop()
        frag1 = self.op_stack.pop()
        if len(self.lva) == 0:
            self.lva.append(frag1)
            self.lva.append(frag2)
        else:
            self.lva[0] = frag1
            if len(self.lva) == 1:
                self.lva.append(frag2)
            else:
                self.lva[1] = frag2

    def lstore_1(self):
        frag2 = self.op_stack.pop()
        frag1 = self.op_stack.pop()
        if len(self.lva) == 1:
            self.lva.append(frag1)
            self.lva.append(frag2)
        else:
            self.lva[1] = frag1
            if len(self.lva) == 2:
                self.lva.append(frag2)
            else:
                self.lva[2] = frag2

    def lstore_2(self):
        frag2 = self.op_stack.pop()
        frag1 = self.op_stack.pop()
        if len(self.lva) == 2:
            self.lva.append(frag1)
            self.lva.append(frag2)
        else:
            self.lva[2] = frag1
            if len(self.lva) == 3:
                self.lva.append(frag2)
            else:
                self.lva[3] = frag2

    def lstore_3(self):
        frag2 = self.op_stack.pop()
        frag1 = self.op_stack.pop()
        if len(self.lva) == 3:
            self.lva.append(frag1)
            self.lva.append(frag2)
        else:
            self.lva[3] = frag1
            if len(self.lva) == 4:
                self.lva.append(frag2)
            else:
                self.lva[4] = frag2

    def lstore(self, operands):
        index = operands.pop()
        frag2 = self.op_stack.pop()
        frag1 = self.op_stack.pop()
        if len(self.lva) == index:
            self.lva.append(frag1)
            self.lva.append(frag2)
        else:
            self.lva[index] = frag1
            if len(self.lva) == index + 1:
                self.lva.append(frag2)
            else:
                self.lva[index + 1] = frag2

    def ladd(self):
        second_op2 = self.op_stack.pop()
        second_op1 = self.op_stack.pop()
        first_op2 = self.op_stack.pop()
        first_op1 = self.op_stack.pop()
        first_op = self.longcomb(first_op1, first_op2)
        second_op = self.longcomb(second_op1, second_op2)
        answer = first_op + second_op
        answer1, answer2 = self.longsplit(answer)
        self.op_stack.append(answer1)
        self.op_stack.append(answer2)

    def lsub(self):
        second_op2 = self.op_stack.pop()
        second_op1 = self.op_stack.pop()
        first_op2 = self.op_stack.pop()
        first_op1 = self.op_stack.pop()
        first_op = self.longcomb(first_op1, first_op2)
        second_op = self.longcomb(second_op1, second_op2)
        answer = first_op - second_op
        answer1, answer2 = self.longsplit(answer)
        self.op_stack.append(answer1)
        self.op_stack.append(answer2)

    def lmul(self):
        second_op2 = self.op_stack.pop()
        second_op1 = self.op_stack.pop()
        first_op2 = self.op_stack.pop()
        first_op1 = self.op_stack.pop()
        first_op = self.longcomb(first_op1, first_op2)
        second_op = self.longcomb(second_op1, second_op2)
        answer = first_op * second_op
        answer1, answer2 = self.longsplit(answer)
        self.op_stack.append(answer1)
        self.op_stack.append(answer2)

    def ldiv(self):
        second_op2 = self.op_stack.pop()
        second_op1 = self.op_stack.pop()
        first_op2 = self.op_stack.pop()
        first_op1 = self.op_stack.pop()
        first_op = self.longcomb(first_op1, first_op2)
        second_op = self.longcomb(second_op1, second_op2)
        try:
            answer = first_op / second_op
            answer1, answer2 = self.longsplit(answer)
            self.op_stack.append(answer1)
            self.op_stack.append(answer2)
        except ZeroDivisionError:
            return 'Error: Divides by Zero'

    def lrem(self):
        second_op2 = self.op_stack.pop()
        second_op1 = self.op_stack.pop()
        first_op2 = self.op_stack.pop()
        first_op1 = self.op_stack.pop()
        first_op = self.longcomb(first_op1, first_op2)
        second_op = self.longcomb(second_op1, second_op2)
        answer = first_op % second_op
        answer1, answer2 = self.longsplit(answer)
        self.op_stack.append(answer1)
        self.op_stack.append(answer2)

    def lneg(self):
        val2 = self.op_stack.pop()
        val1 = self.op_stack.pop()
        val = self.longcomb(val1, val2)
        answer = val * -1
        answer1, answer2 = self.longsplit(answer)
        self.op_stack.append(answer1)
        self.op_stack.append(answer2)

    def lushr(self):
        value2 = self.op_stack.pop()
        value1 = self.op_stack.pop()
        s = value2 & 0x3f
        if value1 >= 0:
            self.op_stack.append(value1 >> s)
        else:
            self.op_stack.append((value1 + 0x10000000000000000) >> s)

    def land(self):
        second_op2 = self.op_stack.pop()
        second_op1 = self.op_stack.pop()
        first_op2 = self.op_stack.pop()
        first_op1 = self.op_stack.pop()
        first_op = self.longcomb(first_op1, first_op2)
        second_op = self.longcomb(second_op1, second_op2)
        answer = first_op & second_op
        answer1, answer2 = self.longsplit(answer)
        self.op_stack.append(answer1)
        self.op_stack.append(answer2)

    def lor(self):
        second_op2 = self.op_stack.pop()
        second_op1 = self.op_stack.pop()
        first_op2 = self.op_stack.pop()
        first_op1 = self.op_stack.pop()
        first_op = self.longcomb(first_op1, first_op2)
        second_op = self.longcomb(second_op1, second_op2)
        answer = first_op | second_op
        answer1, answer2 = self.longsplit(answer)
        self.op_stack.append(answer1)
        self.op_stack.append(answer2)

    def lxor(self):
        second_op2 = self.op_stack.pop()
        second_op1 = self.op_stack.pop()
        first_op2 = self.op_stack.pop()
        first_op1 = self.op_stack.pop()
        first_op = self.longcomb(first_op1, first_op2)
        second_op = self.longcomb(second_op1, second_op2)
        answer = first_op ^ second_op
        answer1, answer2 = self.longsplit(answer)
        self.op_stack.append(answer1)
        self.op_stack.append(answer2)

    def l2i(self):
        value2 = self.op_stack.pop()
        value1 = self.op_stack.pop()
        valuea = self.longcomb(value1, value2)
        self.op_stack.append(int(valuea))

    def l2f(self):
        value2 = self.op_stack.pop()
        value1 = self.op_stack.pop()
        valuea = self.longcomb(value1, value2)
        self.op_stack.append(float(valuea))

    def l2d(self):
        value2 = self.op_stack.pop()
        value1 = self.op_stack.pop()
        valuea = self.longcomb(value1, value2)
        self.op_stack.append(float(valuea))



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

    def longsplit(self, val):    # Splits long in half and returns first and second frag as int32
        val = np.int64(val)
        frag2 = np.int32(val & 0x00000000ffffffff)
        frag1 = np.int32((val >> 32) & 0x00000000ffffffff)
        return frag1, frag2

    def longcomb(self, frag1, frag2):   # Takes two fragments and combines them, returning a 64 bit int
        frag1 = np.int64((0x00000000ffffffff & frag1) << 32)
        frag2 = np.int64(0x00000000ffffffff & frag2)
        return frag1 + frag2

