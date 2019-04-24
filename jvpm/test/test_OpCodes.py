import unittest
import numpy as np
from jvpm.OpCodes import OpCodes
from jvpm.ClassFile import ConstantInfo
from unittest.mock import patch, call

class TestOpCodes(unittest.TestCase):

    def test_not_implmented(self):
        self.assertEqual(OpCodes().interpret(0), 'not implemented')
        with self.assertRaises(KeyError):
            OpCodes().interpret(1)

    def test_iconst_m1(self):
        m = OpCodes()
        m.interpret(0x02)
        self.assertEqual(-1, m.op_stack.pop())

    def test_iconst_0(self):
        m = OpCodes()
        m.interpret(0x03)
        self.assertEqual(m.op_stack.pop(), 0)

    def test_iconst_1(self):
        m = OpCodes()
        m.interpret(0x04)
        self.assertEqual(m.op_stack.pop(), 1)

    def test_iconst_2(self):
        m = OpCodes()
        m.interpret(0x05)
        self.assertEqual(m.op_stack.pop(), 2)

    def test_iconst_3(self):
        m = OpCodes()
        m.interpret(0x06)
        self.assertEqual(m.op_stack.pop(), 3)

    def test_iconst_4(self):
        m = OpCodes()
        m.interpret(0x07)
        self.assertEqual(m.op_stack.pop(), 4)

    def test_iconst_5(self):
        m = OpCodes()
        m.interpret(0x08)
        self.assertEqual(m.op_stack.pop(), 5)

    def test_iadd(self):
        m = OpCodes()
        m.op_stack.append(1)
        m.op_stack.append(2)
        m.interpret(0x60)
        self.assertEqual(m.op_stack.pop(), 3)

    def test_iand(self):
        m = OpCodes()
        m.op_stack.append(1)
        m.op_stack.append(3)
        m.interpret(0x7e)
        self.assertEqual(m.op_stack.pop(), 1)

    def test_idiv(self):
        m = OpCodes()
        m.op_stack.append(6)
        m.op_stack.append(3)
        m.interpret(0x6c)
        self.assertEqual(m.op_stack.pop(), 2)
        m.op_stack.append(6)
        m.op_stack.append(0)
        self.assertEqual(m.interpret(0x6c), 'Error: Divides by Zero')

    def test_imul(self):
        m = OpCodes()
        m.op_stack.append(3)
        m.op_stack.append(2)
        m.interpret(0x68)
        self.assertEqual(m.op_stack.pop(), 6)

    def test_ineg(self):
        m = OpCodes()
        m.op_stack.append(1)
        m.interpret(0x74)
        self.assertEqual(m.op_stack.pop(), -1)

    def test_ior(self):
        m = OpCodes()
        m.op_stack.append(1)
        m.op_stack.append(2)
        m.interpret(0x80)
        self.assertEqual(m.op_stack.pop(), 3)

    def test_irem(self):
        m = OpCodes()
        m.op_stack.append(7)
        m.op_stack.append(3)
        m.interpret(0x70)
        self.assertEqual(m.op_stack.pop(), 1)
        m.op_stack.append(7)
        m.op_stack.append(0)
        self.assertEqual(m.interpret(0x70), 'Error: Divides by Zero')

    def test_ishl(self):
        m = OpCodes()
        m.op_stack.append(4)
        m.op_stack.append(3)
        m.interpret(0x78)
        self.assertEqual(m.op_stack.pop(), 32)

    def test_ishr(self):
        m = OpCodes()
        m.op_stack.append(4)
        m.op_stack.append(2)
        m.interpret(0x7a)
        self.assertEqual(m.op_stack.pop(), 1)

    def test_isub(self):
        m = OpCodes()
        m.op_stack.append(2)
        m.op_stack.append(1)
        m.interpret(0x64)
        self.assertEqual(m.op_stack.pop(), 1)

    def test_iushr(self):
        m = OpCodes()
        m.op_stack.append(23)  # Testing for positive logical shift right
        m.op_stack.append(1)
        m.interpret(0x7c)
        self.assertEqual(m.op_stack.pop(), 11)
        m.op_stack.append(-5)  # Testing for negative logical shift right
        m.op_stack.append(3)
        m.interpret(0x7c)
        self.assertEqual(m.op_stack.pop(), 536870911)

    def test_ixor(self):
        m = OpCodes()
        m.op_stack.append(4)
        m.op_stack.append(4)
        m.interpret(0x82)
        self.assertEqual(m.op_stack.pop(), 0)

    def test_iload(self):
        m = OpCodes()
        m.lva.append(0)
        m.lva.append(1)
        m.lva.append(2)
        m.lva.append(3)
        m.lva.append(4)
        m.interpret(0x15, [4])
        self.assertEqual(m.op_stack.pop(), 4)

    def test_iload_0(self):
        m = OpCodes()
        m.lva.append(0)
        m.interpret(0x1a)
        self.assertEqual(m.op_stack.pop(), 0)

    def test_iload_1(self):
        m = OpCodes()
        m.lva.append(0)
        m.lva.append(1)
        m.interpret(0x1b)
        self.assertEqual(m.op_stack.pop(), 1)

    def test_iload_2(self):
        m = OpCodes()
        m.lva.append(0)
        m.lva.append(1)
        m.lva.append(2)
        m.interpret(0x1c)
        self.assertEqual(m.op_stack.pop(), 2)

    def test_iload_3(self):
        m = OpCodes()
        m.lva.append(0)
        m.lva.append(1)
        m.lva.append(2)
        m.lva.append(3)
        m.interpret(0x1d)
        self.assertEqual(m.op_stack.pop(), 3)

    def test_istore(self):
        m = OpCodes()
        m.lva.append(0)
        m.lva.append(1)
        m.lva.append(2)
        m.lva.append(3)
        m.op_stack.append(4)
        m.interpret(0x36, [4])
        self.assertEqual(m.lva[4], 4)
        m.op_stack.append(5)
        m.interpret(0x36, [4])
        self.assertEqual(m.lva[4], 5)

    def test_istore_0(self):
        m = OpCodes()
        m.op_stack.append(0)
        m.interpret(0x3b)
        self.assertEqual(m.lva[0], 0)
        m.op_stack.append(1)
        m.interpret(0x3b)
        self.assertEqual(m.lva[0], 1)

    def test_istore_1(self):
        m = OpCodes()
        m.lva.append(0)
        m.op_stack.append(1)
        m.interpret(0x3c)
        self.assertEqual(m.lva[1], 1)
        m.op_stack.append(2)
        m.interpret(0x3c)
        self.assertEqual(m.lva[1], 2)

    def test_istore_2(self):
        m = OpCodes()
        m.lva.append(0)
        m.lva.append(1)
        m.op_stack.append(2)
        m.interpret(0x3d)
        self.assertEqual(m.lva[2], 2)
        m.op_stack.append(3)
        m.interpret(0x3d)
        self.assertEqual(m.lva[2], 3)

    def test_istore_3(self):
        m = OpCodes()
        m.lva.append(0)
        m.lva.append(1)
        m.lva.append(2)
        m.op_stack.append(3)
        m.interpret(0x3e)
        self.assertEqual(m.lva[3], 3)
        m.op_stack.append(4)
        m.interpret(0x3e)
        self.assertEqual(m.lva[3], 4)

    def test_i2b(self):
        m = OpCodes()
        m.op_stack.append(3)
        m.i2b()
        assert isinstance(m.op_stack.pop(), int)

    def test_i2c(self):
        m = OpCodes()
        m.op_stack.append(69)
        m.i2c()
        assert isinstance(m.op_stack.pop(), str)

    def test_i2d(self):
        m = OpCodes()
        m.op_stack.append(2)
        m.i2d()
        assert isinstance(m.op_stack.pop(), float)

    def test_i2f(self):
        m = OpCodes()
        m.op_stack.append(5)
        m.i2f()
        assert isinstance(m.op_stack.pop(), float)

    def test_i2l(self):
        m = OpCodes()
        m.op_stack.append(8)
        m.i2l()
        assert isinstance(m.op_stack.pop(), int)

    def test_i2s(self):
        m = OpCodes()
        m.op_stack.append(4)
        m.i2s()
        assert isinstance(m.op_stack.pop(), int)

    def test_fstore(self):
        m = OpCodes()
        m.lva.append(0)
        m.lva.append(1)
        m.lva.append(2)
        m.lva.append(3)
        m.op_stack.append(4)
        m.interpret(0x38, [4])
        self.assertEqual(m.lva[4], 4)
        m.op_stack.append(5)
        m.interpret(0x38, [4])
        self.assertEqual(m.lva[4], 5)

    def test_get_str_from_cpool(self):
        methrefobj = ConstantInfo()
        methrefobj.tag = 10
        methrefobj.info = [0, 2, 0, 3]
        classobj = ConstantInfo()
        classobj.tag = 7
        classobj.info = [0, 4]
        nameandtypeobj = ConstantInfo()
        nameandtypeobj.tag = 12
        nameandtypeobj.info = [0, 5, 0, 6]
        str1 = ConstantInfo()
        str1.tag = 1
        str1.info = [0x41]
        str2 = ConstantInfo()
        str2.tag = 1
        str2.info = [0x42]
        str3 = ConstantInfo()
        str3.tag = 1
        str3.info = [0x43]
        c = [methrefobj, classobj, nameandtypeobj, str1, str2, str3]
        m = OpCodes()
        self.assertEqual(m.get_str_from_cpool(0, c), 'A.B:C')

    @patch('builtins.print')
    def test_invokevirtual(self, mock_print):
        methrefobj = ConstantInfo()
        methrefobj.tag = 10
        methrefobj.info = [0, 2, 0, 3]
        classobj = ConstantInfo()
        classobj.tag = 7
        classobj.info = [0, 4]
        nameandtypeobj = ConstantInfo()
        nameandtypeobj.tag = 12
        nameandtypeobj.info = [0, 5, 0, 6]
        str1 = ConstantInfo()
        str1.tag = 1
        str1.info = [106, 97, 118, 97, 47, 105, 111, 47, 80, 114, 105, 110, 116, 83, 116, 114, 101, 97, 109]
        str2 = ConstantInfo()
        str2.tag = 1
        str2.info = [112, 114, 105, 110, 116, 108, 110]
        str3 = ConstantInfo()
        str3.tag = 1
        str3.info = [40, 73, 41, 86]
        c = [methrefobj, classobj, nameandtypeobj, str1, str2, str3]
        m = OpCodes()
        m.op_stack.append(5)
        m.invokevirtual([0, 1], c)
        str1.info = [106, 97, 118, 97, 47, 105, 111, 47, 80, 114, 105, 110, 116, 83, 116, 114, 101, 97, 109]
        str2.info = [112, 114, 105, 110, 116, 108, 110]
        str3.info = [40, 76, 106, 97, 118, 97, 47, 108, 97, 110, 103, 47, 83, 116, 114, 105, 110, 103, 59, 41, 86]
        c = [methrefobj, classobj, nameandtypeobj, str1, str2, str3]
        m.op_stack.append("Hello World!")
        m.invokevirtual([0, 1], c)
        self.assertEqual(mock_print.mock_calls, [
            call(5),
            call('Hello World!')
        ])
        with patch('builtins.input', return_value='5'):
            str1.info = [110, 101, 120, 116, 73, 110, 116, 58, 40, 41, 73]
            str2.info = [106, 97, 118, 97, 47, 117, 116, 105, 108, 47, 83, 99, 97, 110, 110, 101, 114]
            c = [methrefobj, classobj, str1, str2]
            m.invokevirtual([0, 1], c)
            m.op_stack.append(5)
            self.assertEqual(m.op_stack.pop(), 5)

    def test_getstatic(self):
        m = OpCodes()
        const_info = ConstantInfo()
        const_info.tag = 1
        const_info.info = [70, 111, 111]
        imp_info = m.getstatic([0, 0], [const_info])
        assert isinstance(imp_info, str)

    def test_ldc(self):
        m = OpCodes()
        str1 = ConstantInfo()
        str1.tag = 1
        str1.info = [72, 101, 108, 108, 111]
        m.ldc([0], [str1])
        self.assertEqual(m.op_stack.pop(), "Hello")

    def test_f2i(self):
        m = OpCodes()
        m.op_stack.append('3f800000')
        m.f2i()
        self.assertEqual(np.dtype(m.op_stack.pop()), 'int32')

    def test_f2l(self):
        m = OpCodes()
        m.op_stack.append('3f800000')
        m.f2l()
        self.assertEqual(m.op_stack.pop(), 1)
        self.assertEqual(m.op_stack.pop(), 0)

    def test_f2d(self):
        m = OpCodes()
        m.op_stack.append('3f800000')
        m.f2d()
        self.assertEqual(m.op_stack.pop(), 0)
        self.assertEqual(m.op_stack.pop(), 0x3ff00000)

    def test_ret(self):
        m = OpCodes()
        self.assertEqual(m.ret(), '')
