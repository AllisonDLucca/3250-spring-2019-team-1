import struct
import re
import numpy as np


class OpCodes:
    def __init__(self):
        self._op_stack = []  # operand stack for the opcodes
        self._lva = []  # local variable array initialized
        self._table = {
            0x00: self._not_implemented,
            0x02: self._iconst_m1,
            0x03: self._iconst_0,
            0x04: self._iconst_1,
            0x05: self._iconst_2,
            0x06: self._iconst_3,
            0x07: self._iconst_4,
            0x08: self._iconst_5,
            0x60: self._iadd,
            0x7E: self._iand,
            0x6C: self._idiv,
            0x68: self._imul,
            0x74: self._ineg,
            0x80: self._ior,
            0x70: self._irem,
            0x78: self._ishl,
            0x7A: self._ishr,
            0x64: self._isub,
            0x7C: self._iushr,
            0x82: self._ixor,
            0x15: self._iload,
            0x1A: self._iload_0,
            0x1B: self._iload_1,
            0x1C: self._iload_2,
            0x1D: self._iload_3,
            0x36: self._istore,
            0x3B: self._istore_0,
            0x3C: self._istore_1,
            0x3D: self._istore_2,
            0x3E: self._istore_3,
            0x91: self._i2b,
            0x92: self._i2c,
            0x87: self._i2d,
            0x86: self._i2f,
            0x85: self._i2l,
            0x93: self._i2s,
            0xB6: self._invokevirtual,
            0xB2: self._getstatic,
            0x12: self._ldc,
            0x8B: self._f2i,
            0x8C: self._f2l,
            0x8D: self._f2d,
            0xB1: self._ret,
            0xB: self._fconst_0,
            0xC: self._fconst_1,
            0xD: self._fconst_2,
            0x17: self._fload,
            0x22: self._fload_0,
            0x23: self._fload_1,
            0x24: self._fload_2,
            0x25: self._fload_3,
            0x1E: self._lload_0,
            0x1F: self._lload_1,
            0x20: self._lload_2,
            0x21: self._lload_3,
            0x16: self._lload,
            0x9: self._lconst_0,
            0xA: self._lconst_1,
            0x3F: self._lstore_0,
            0x40: self._lstore_1,
            0x41: self._lstore_2,
            0x42: self._lstore_3,
            0x37: self._lstore,
            0x61: self._ladd,
            0x65: self._lsub,
            0x69: self._lmul,
            0x6D: self._ldiv,
            0x71: self._lrem,
            0x75: self._lneg,
            0x7D: self._lushr,
            0x7F: self._land,
            0x81: self._lor,
            0x83: self._lxor,
            0x88: self._l2i,
            0x89: self._l2f,
            0x8A: self._l2d,
        }

    def _not_implemented(self):
        return "not implemented"

    def interpret(self, value, operands=None, constants=None):
        """
        Takes an input of a hex value that represents a
        byte long Opcode label for the Java Virtual machine and then
        executes the corresponding method in this file using the other input fields.

        The operands variable takes an optional array
        of operands to be used with the executed Opcode.

        The constants variable takes an optional array
        of constants to be used with the executed Opcode.
        """
        if operands is not None and constants is not None:
            return self._table[value](operands, constants)
        elif operands is not None and constants is None:
            return self._table[value](operands)
        else:
            return self._table[value]()

    def _iconst_m1(self):
        self._op_stack.append(-1)

    def _iconst_0(self):
        self._op_stack.append(0)

    def _iconst_1(self):
        self._op_stack.append(1)

    def _iconst_2(self):
        self._op_stack.append(2)

    def _iconst_3(self):
        self._op_stack.append(3)

    def _iconst_4(self):
        self._op_stack.append(4)

    def _iconst_5(self):
        self._op_stack.append(5)

    def _iadd(self):
        value2 = self._op_stack.pop()
        value1 = self._op_stack.pop()
        self._op_stack.append(value1 + value2)

    def _iand(self):
        value2 = self._op_stack.pop()
        value1 = self._op_stack.pop()
        self._op_stack.append(value1 & value2)

    def _idiv(self):
        value2 = self._op_stack.pop()
        value1 = self._op_stack.pop()
        try:
            self._op_stack.append(value1 // value2)
        except ZeroDivisionError:
            return "Error: Divides by Zero"

    def _imul(self):
        value2 = self._op_stack.pop()
        value1 = self._op_stack.pop()
        self._op_stack.append(value1 * value2)

    def _ineg(self):
        self._op_stack.append(self._op_stack.pop() * -1)

    def _ior(self):
        value2 = self._op_stack.pop()
        value1 = self._op_stack.pop()
        self._op_stack.append(value1 | value2)

    def _irem(self):
        value2 = self._op_stack.pop()
        value1 = self._op_stack.pop()
        try:
            self._op_stack.append(value1 % value2)
        except ZeroDivisionError:
            return "Error: Divides by Zero"

    def _ishl(self):
        value2 = self._op_stack.pop()
        value1 = self._op_stack.pop()
        self._op_stack.append(value1 << value2)

    def _ishr(self):
        value2 = self._op_stack.pop()
        value1 = self._op_stack.pop()
        self._op_stack.append(value1 >> value2)

    def _isub(self):
        value2 = self._op_stack.pop()
        value1 = self._op_stack.pop()
        self._op_stack.append(value1 - value2)

    def _iushr(self):
        value2 = self._op_stack.pop()
        value1 = self._op_stack.pop()
        s = value2 & 0x1F
        if value1 >= 0:
            self._op_stack.append(value1 >> s)
        else:
            self._op_stack.append((value1 + 0x100000000) >> s)

    def _ixor(self):
        value2 = self._op_stack.pop()
        value1 = self._op_stack.pop()
        self._op_stack.append(value1 ^ value2)

    def _iload(self, operands):
        index = operands.pop()
        self._op_stack.append(self._lva[index])

    def _iload_0(self):
        self._op_stack.append(self._lva[0])

    def _iload_1(self):
        self._op_stack.append(self._lva[1])

    def _iload_2(self):
        self._op_stack.append(self._lva[2])

    def _iload_3(self):
        self._op_stack.append(self._lva[3])

    def _istore(self, operands):
        index = operands.pop()
        if len(self._lva) <= index:
            self._lva.append(self._op_stack.pop())
        else:
            self._lva[index] = self._op_stack.pop()

    def _istore_0(self):
        if self._lva == 0:
            self._lva.append(self._op_stack.pop())
        else:
            self._lva[0] = self._op_stack.pop()

    def _istore_1(self):
        if len(self._lva) == 1:
            self._lva.append(self._op_stack.pop())
        else:
            self._lva[1] = self._op_stack.pop()

    def _istore_2(self):
        if len(self._lva) == 2:
            self._lva.append(self._op_stack.pop())
        else:
            self._lva[2] = self._op_stack.pop()

    def _istore_3(self):
        if len(self._lva) == 3:
            self._lva.append(self._op_stack.pop())
        else:
            self._lva[3] = self._op_stack.pop()

    def _i2b(self):  # Josh
        value1 = self._op_stack.pop()
        self._op_stack.append(int(value1))

    def _i2c(self):
        value1 = self._op_stack.pop()
        self._op_stack.append(chr(value1))

    def _i2d(self):
        value1 = self._op_stack.pop()
        self._op_stack.append(float(value1))

    def _i2f(self):
        value1 = self._op_stack.pop()
        self._op_stack.append(float(value1))

    def _i2l(self):
        value1 = self._op_stack.pop()
        self._op_stack.append(int(value1))

    def _i2s(self):
        value1 = self._op_stack.pop()
        self._op_stack.append(int(value1))

    def _lload_0(self):
        frag1 = self._lva[0]
        frag2 = self._lva[1]
        self._op_stack.append(frag1)
        self._op_stack.append(frag2)

    def _lload_1(self):
        frag1 = self._lva[1]
        frag2 = self._lva[2]
        self._op_stack.append(frag1)
        self._op_stack.append(frag2)

    def _lload_2(self):
        frag1 = self._lva[2]
        frag2 = self._lva[3]
        self._op_stack.append(frag1)
        self._op_stack.append(frag2)

    def _lload_3(self):
        frag1 = self._lva[3]
        frag2 = self._lva[4]
        self._op_stack.append(frag1)
        self._op_stack.append(frag2)

    def _lload(self, operands):
        index = operands.pop()
        frag1 = self._lva[index]
        frag2 = self._lva[index + 1]
        self._op_stack.append(frag1)
        self._op_stack.append(frag2)

    def _lconst_0(self):
        self._op_stack.append(0)
        self._op_stack.append(0)

    def _lconst_1(self):
        self._op_stack.append(0)
        self._op_stack.append(1)

    def _lstore_0(self):
        frag2 = self._op_stack.pop()
        frag1 = self._op_stack.pop()
        if self._lva == 0:
            self._lva.append(frag1)
            self._lva.append(frag2)
        else:
            self._lva[0] = frag1
            if len(self._lva) == 1:
                self._lva.append(frag2)
            else:
                self._lva[1] = frag2

    def _lstore_1(self):
        frag2 = self._op_stack.pop()
        frag1 = self._op_stack.pop()
        if len(self._lva) == 1:
            self._lva.append(frag1)
            self._lva.append(frag2)
        else:
            self._lva[1] = frag1
            if len(self._lva) == 2:
                self._lva.append(frag2)
            else:
                self._lva[2] = frag2

    def _lstore_2(self):
        frag2 = self._op_stack.pop()
        frag1 = self._op_stack.pop()
        if len(self._lva) == 2:
            self._lva.append(frag1)
            self._lva.append(frag2)
        else:
            self._lva[2] = frag1
            if len(self._lva) == 3:
                self._lva.append(frag2)
            else:
                self._lva[3] = frag2

    def _lstore_3(self):
        frag2 = self._op_stack.pop()
        frag1 = self._op_stack.pop()
        if len(self._lva) == 3:
            self._lva.append(frag1)
            self._lva.append(frag2)
        else:
            self._lva[3] = frag1
            if len(self._lva) == 4:
                self._lva.append(frag2)
            else:
                self._lva[4] = frag2

    def _lstore(self, operands):
        index = operands.pop()
        frag2 = self._op_stack.pop()
        frag1 = self._op_stack.pop()
        if len(self._lva) == index:
            self._lva.append(frag1)
            self._lva.append(frag2)
        else:
            self._lva[index] = frag1
            if len(self._lva) == index + 1:
                self._lva.append(frag2)
            else:
                self._lva[index + 1] = frag2

    def _ladd(self):
        second_op2 = self._op_stack.pop()
        second_op1 = self._op_stack.pop()
        first_op2 = self._op_stack.pop()
        first_op1 = self._op_stack.pop()
        first_op = self._longcomb(first_op1, first_op2)
        second_op = self._longcomb(second_op1, second_op2)
        answer = first_op + second_op
        answer1, answer2 = self._longsplit(answer)
        self._op_stack.append(answer1)
        self._op_stack.append(answer2)

    def _lsub(self):
        second_op2 = self._op_stack.pop()
        second_op1 = self._op_stack.pop()
        first_op2 = self._op_stack.pop()
        first_op1 = self._op_stack.pop()
        first_op = self._longcomb(first_op1, first_op2)
        second_op = self._longcomb(second_op1, second_op2)
        answer = first_op - second_op
        answer1, answer2 = self._longsplit(answer)
        self._op_stack.append(answer1)
        self._op_stack.append(answer2)

    def _lmul(self):
        second_op2 = self._op_stack.pop()
        second_op1 = self._op_stack.pop()
        first_op2 = self._op_stack.pop()
        first_op1 = self._op_stack.pop()
        first_op = self._longcomb(first_op1, first_op2)
        second_op = self._longcomb(second_op1, second_op2)
        answer = first_op * second_op
        answer1, answer2 = self._longsplit(answer)
        self._op_stack.append(answer1)
        self._op_stack.append(answer2)

    def _ldiv(self):
        second_op2 = self._op_stack.pop()
        second_op1 = self._op_stack.pop()
        first_op2 = self._op_stack.pop()
        first_op1 = self._op_stack.pop()
        first_op = self._longcomb(first_op1, first_op2)
        second_op = self._longcomb(second_op1, second_op2)
        answer = first_op / second_op
        answer1, answer2 = self._longsplit(answer)
        self._op_stack.append(answer1)
        self._op_stack.append(answer2)

    def _lrem(self):
        second_op2 = self._op_stack.pop()
        second_op1 = self._op_stack.pop()
        first_op2 = self._op_stack.pop()
        first_op1 = self._op_stack.pop()
        first_op = self._longcomb(first_op1, first_op2)
        second_op = self._longcomb(second_op1, second_op2)
        answer = first_op % second_op
        answer1, answer2 = self._longsplit(answer)
        self._op_stack.append(answer1)
        self._op_stack.append(answer2)

    def _lneg(self):
        val2 = self._op_stack.pop()
        val1 = self._op_stack.pop()
        val = self._longcomb(val1, val2)
        answer = val * -1
        answer1, answer2 = self._longsplit(answer)
        self._op_stack.append(answer1)
        self._op_stack.append(answer2)

    def _lushr(self):
        value2 = self._op_stack.pop()
        value1 = self._op_stack.pop()
        s = value2 & 0x3F
        if value1 >= 0:
            self._op_stack.append(value1 >> s)
        else:
            self._op_stack.append((value1 + 0x10000000000000000) >> s)

    def _land(self):
        second_op2 = self._op_stack.pop()
        second_op1 = self._op_stack.pop()
        first_op2 = self._op_stack.pop()
        first_op1 = self._op_stack.pop()
        first_op = self._longcomb(first_op1, first_op2)
        second_op = self._longcomb(second_op1, second_op2)
        answer = first_op & second_op
        answer1, answer2 = self._longsplit(answer)
        self._op_stack.append(answer1)
        self._op_stack.append(answer2)

    def _lor(self):
        second_op2 = self._op_stack.pop()
        second_op1 = self._op_stack.pop()
        first_op2 = self._op_stack.pop()
        first_op1 = self._op_stack.pop()
        first_op = self._longcomb(first_op1, first_op2)
        second_op = self._longcomb(second_op1, second_op2)
        answer = first_op | second_op
        answer1, answer2 = self._longsplit(answer)
        self._op_stack.append(answer1)
        self._op_stack.append(answer2)

    def _lxor(self):
        second_op2 = self._op_stack.pop()
        second_op1 = self._op_stack.pop()
        first_op2 = self._op_stack.pop()
        first_op1 = self._op_stack.pop()
        first_op = self._longcomb(first_op1, first_op2)
        second_op = self._longcomb(second_op1, second_op2)
        answer = first_op ^ second_op
        answer1, answer2 = self._longsplit(answer)
        self._op_stack.append(answer1)
        self._op_stack.append(answer2)

    def _l2i(self):
        value2 = self._op_stack.pop()
        value1 = self._op_stack.pop()
        valuea = self._longcomb(value1, value2)
        self._op_stack.append(int(valuea))

    def _l2f(self):
        value2 = self._op_stack.pop()
        value1 = self._op_stack.pop()
        valuea = self._longcomb(value1, value2)
        self._op_stack.append(float(valuea))

    def _l2d(self):
        value2 = self._op_stack.pop()
        value1 = self._op_stack.pop()
        valuea = self._longcomb(value1, value2)
        self._op_stack.append(float(valuea))

    def _get_str_from_cpool(self, index, c_pool):

        const_ref = c_pool[index]

        if const_ref.tag != 1:
            class_index = const_ref.info[0] + const_ref.info[1] - 1
            val = self._get_str_from_cpool(class_index, c_pool)

            if const_ref.tag == 10:
                val += "."
            elif const_ref.tag == 12:
                val += ":"

            if const_ref.info.__len__() > 2:
                name_type_index = const_ref.info[2] + const_ref.info[3] - 1
                val += self._get_str_from_cpool(name_type_index, c_pool)

            return val

        else:
            return bytes(const_ref.info).decode("utf-8")

    def _invokevirtual(self, operands, c_pool):
        num1 = operands.pop()
        num2 = operands.pop()
        method = self._get_str_from_cpool(num1 + num2 - 1, c_pool)
        if method == "java/io/PrintStream.println:(I)V":
            print(self._op_stack.pop())
        elif method == "java/io/PrintStream.println:(Ljava/lang/String;)V":
            print(self._op_stack.pop())
        elif method == "java/util/Scanner.nextInt:()I":
            data = input("Enter a number: ")
            while re.match(r"[-+]?\d+$", data) is None:
                print("Invalid input")
                data = input("Enter a number: ")
            int1 = int(data)
            self._op_stack.append(int1)

    def _getstatic(self, operands, c_pool):
        value1 = operands.pop()
        value2 = operands.pop()
        return self._get_str_from_cpool(value1 + value2 - 1, c_pool)

    def _ldc(self, operands, c_pool):
        value = operands.pop()
        self._op_stack.append(self._get_str_from_cpool(value - 1, c_pool))

    # Splits long in half and returns first and second frag as int32
    def _longsplit(self, val):
        val = np.int64(val)
        frag2 = np.int32(val & 0x00000000FFFFFFFF)
        frag1 = np.int32((val >> 32) & 0x00000000FFFFFFFF)
        return frag1, frag2

    # Takes two fragments and combines them, returning a 64 bit int
    def _longcomb(self, frag1, frag2):
        frag1 = np.int64((0x00000000FFFFFFFF & frag1) << 32)
        frag2 = np.int64(0x00000000FFFFFFFF & frag2)
        return frag1 + frag2

    def _fconst_0(self):
        self._op_stack.append(np.float32(0.0))

    def _fconst_1(self):
        self._op_stack.append(np.float32(1.0))

    def _fconst_2(self):
        self._op_stack.append(np.float32(2.0))

    def _fload(self, operands):
        index = operands.pop()
        self._op_stack.append(self._lva[index])

    def _fload_0(self):
        self._op_stack.append(self._lva[0])

    def _fload_1(self):
        self._op_stack.append(self._lva[1])

    def _fload_2(self):
        self._op_stack.append(self._lva[2])

    def _fload_3(self):
        self._op_stack.append(self._lva[3])

    def _f2i(self):
        value1 = struct.unpack("!f", bytes.fromhex(self._op_stack.pop()))[0]
        self._op_stack.append(np.int32(value1))

    def _f2l(self):
        value1 = np.int64(struct.unpack("!f", bytes.fromhex(self._op_stack.pop()))[0])
        value2 = np.right_shift(value1, 32)
        value3 = np.bitwise_and(value1, 0x00000000FFFFFFFF)
        self._op_stack.append(np.int32(value2))
        self._op_stack.append(np.int32(value3))

    def _f2d(self):
        value1 = np.float64(struct.unpack("!f", bytes.fromhex(self._op_stack.pop()))[0])
        hexval = hex(struct.unpack("<Q", struct.pack("<d", value1))[0])
        value2 = hexval[2:10]
        value3 = hexval[10:18]
        self._op_stack.append(int(value2, 16))
        self._op_stack.append(int(value3, 16))

    def _ret(self):
        return ""
