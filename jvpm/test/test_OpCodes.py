import unittest
import numpy as np
from jvpm.OpCodes import OpCodes
from jvpm.ClassFile import ConstantInfo
from unittest.mock import patch, call

class TestOpCodes(unittest.TestCase):

    def test_not_implmented(self):
        self.assertEqual(OpCodes().interpret(0), 'not implemented')

    def test_iconst_m1(self):
        m = OpCodes()
        m.interpret(0x02)
        self.assertEqual(-1, m._op_stack.pop())

    def test_iconst_0(self):
        m = OpCodes()
        m.interpret(0x03)
        self.assertEqual(m._op_stack.pop(), 0)

    def test_iconst_1(self):
        m = OpCodes()
        m.interpret(0x04)
        self.assertEqual(m._op_stack.pop(), 1)

    def test_iconst_2(self):
        m = OpCodes()
        m.interpret(0x05)
        self.assertEqual(m._op_stack.pop(), 2)

    def test_iconst_3(self):
        m = OpCodes()
        m.interpret(0x06)
        self.assertEqual(m._op_stack.pop(), 3)

    def test_iconst_4(self):
        m = OpCodes()
        m.interpret(0x07)
        self.assertEqual(m._op_stack.pop(), 4)

    def test_iconst_5(self):
        m = OpCodes()
        m.interpret(0x08)
        self.assertEqual(m._op_stack.pop(), 5)

    def test_iadd(self):
        m = OpCodes()
        m._op_stack.append(1)
        m._op_stack.append(2)
        m.interpret(0x60)
        self.assertEqual(m._op_stack.pop(), 3)

    def test_iand(self):
        m = OpCodes()
        m._op_stack.append(1)
        m._op_stack.append(3)
        m.interpret(0x7e)
        self.assertEqual(m._op_stack.pop(), 1)

    def test_idiv(self):
        m = OpCodes()
        m._op_stack.append(6)
        m._op_stack.append(3)
        m.interpret(0x6c)
        self.assertEqual(m._op_stack.pop(), 2)
        m._op_stack.append(6)
        m._op_stack.append(0)
        self.assertEqual(m.interpret(0x6c), 'Error: Divides by Zero')

    def test_imul(self):
        m = OpCodes()
        m._op_stack.append(3)
        m._op_stack.append(2)
        m.interpret(0x68)
        self.assertEqual(m._op_stack.pop(), 6)

    def test_ineg(self):
        m = OpCodes()
        m._op_stack.append(1)
        m.interpret(0x74)
        self.assertEqual(m._op_stack.pop(), -1)

    def test_ior(self):
        m = OpCodes()
        m._op_stack.append(1)
        m._op_stack.append(2)
        m.interpret(0x80)
        self.assertEqual(m._op_stack.pop(), 3)

    def test_irem(self):
        m = OpCodes()
        m._op_stack.append(7)
        m._op_stack.append(3)
        m.interpret(0x70)
        self.assertEqual(m._op_stack.pop(), 1)
        m._op_stack.append(7)
        m._op_stack.append(0)
        self.assertEqual(m.interpret(0x70), 'Error: Divides by Zero')

    def test_ishl(self):
        m = OpCodes()
        m._op_stack.append(4)
        m._op_stack.append(3)
        m.interpret(0x78)
        self.assertEqual(m._op_stack.pop(), 32)

    def test_ishr(self):
        m = OpCodes()
        m._op_stack.append(4)
        m._op_stack.append(2)
        m.interpret(0x7a)
        self.assertEqual(m._op_stack.pop(), 1)

    def test_isub(self):
        m = OpCodes()
        m._op_stack.append(2)
        m._op_stack.append(1)
        m.interpret(0x64)
        self.assertEqual(m._op_stack.pop(), 1)

    def test_iushr(self):
        m = OpCodes()
        m._op_stack.append(23)  # Testing for positive logical shift right
        m._op_stack.append(1)
        m.interpret(0x7c)
        self.assertEqual(m._op_stack.pop(), 11)
        m._op_stack.append(-5)  # Testing for negative logical shift right
        m._op_stack.append(3)
        m.interpret(0x7c)
        self.assertEqual(m._op_stack.pop(), 536870911)

    def test_ixor(self):
        m = OpCodes()
        m._op_stack.append(4)
        m._op_stack.append(4)
        m.interpret(0x82)
        self.assertEqual(m._op_stack.pop(), 0)

    def test_iload(self):
        m = OpCodes()
        m._lva.append(0)
        m._lva.append(1)
        m._lva.append(2)
        m._lva.append(3)
        m._lva.append(4)
        m.interpret(0x15, [4])
        self.assertEqual(m._op_stack.pop(), 4)

    def test_iload_0(self):
        m = OpCodes()
        m._lva.append(0)
        m.interpret(0x1a)
        self.assertEqual(m._op_stack.pop(), 0)

    def test_iload_1(self):
        m = OpCodes()
        m._lva.append(0)
        m._lva.append(1)
        m.interpret(0x1b)
        self.assertEqual(m._op_stack.pop(), 1)

    def test_iload_2(self):
        m = OpCodes()
        m._lva.append(0)
        m._lva.append(1)
        m._lva.append(2)
        m.interpret(0x1c)
        self.assertEqual(m._op_stack.pop(), 2)

    def test_iload_3(self):
        m = OpCodes()
        m._lva.append(0)
        m._lva.append(1)
        m._lva.append(2)
        m._lva.append(3)
        m.interpret(0x1d)
        self.assertEqual(m._op_stack.pop(), 3)

    def test_istore(self):
        m = OpCodes()
        m._lva.append(0)
        m._lva.append(1)
        m._lva.append(2)
        m._lva.append(3)
        m._op_stack.append(4)
        m.interpret(0x36, [4])
        self.assertEqual(m._lva[4], 4)
        m._op_stack.append(5)
        m.interpret(0x36, [4])
        self.assertEqual(m._lva[4], 5)

    def test_istore_0(self):
        m = OpCodes()
        m._op_stack.append(0)
        m.interpret(0x3b)
        self.assertEqual(m._lva[0], 0)
        m._op_stack.append(1)
        m.interpret(0x3b)
        self.assertEqual(m._lva[0], 1)

    def test_istore_1(self):
        m = OpCodes()
        m._lva.append(0)
        m._op_stack.append(1)
        m.interpret(0x3c)
        self.assertEqual(m._lva[1], 1)
        m._op_stack.append(2)
        m.interpret(0x3c)
        self.assertEqual(m._lva[1], 2)

    def test_istore_2(self):
        m = OpCodes()
        m._lva.append(0)
        m._lva.append(1)
        m._op_stack.append(2)
        m.interpret(0x3d)
        self.assertEqual(m._lva[2], 2)
        m._op_stack.append(3)
        m.interpret(0x3d)
        self.assertEqual(m._lva[2], 3)

    def test_istore_3(self):
        m = OpCodes()
        m._lva.append(0)
        m._lva.append(1)
        m._lva.append(2)
        m._op_stack.append(3)
        m.interpret(0x3e)
        self.assertEqual(m._lva[3], 3)
        m._op_stack.append(4)
        m.interpret(0x3e)
        self.assertEqual(m._lva[3], 4)

    def test_i2b(self):
        m = OpCodes()
        m._op_stack.append(3)
        m.interpret(0x91)
        assert isinstance(m._op_stack.pop(), int)

    def test_i2c(self):
        m = OpCodes()
        m._op_stack.append(69)
        m.interpret(0x92)
        assert isinstance(m._op_stack.pop(), str)

    def test_i2d(self):
        m = OpCodes()
        m._op_stack.append(2)
        m.interpret(0x87)
        assert isinstance(m._op_stack.pop(), float)

    def test_i2f(self):
        m = OpCodes()
        m._op_stack.append(5)
        m.interpret(0x86)
        assert isinstance(m._op_stack.pop(), float)

    def test_i2l(self):
        m = OpCodes()
        m._op_stack.append(8)
        m.interpret(0x85)
        assert isinstance(m._op_stack.pop(), int)

    def test_i2s(self):
        m = OpCodes()
        m._op_stack.append(4)
        m.interpret(0x93)
        assert isinstance(m._op_stack.pop(), int)

    def test_fstore(self):
        m = OpCodes()
        m._lva.append(0.0)
        m._lva.append(1.0)
        m._lva.append(2.0)
        m._lva.append(3.0)
        m._op_stack.append(4.0)
        m.interpret(0x38, [4])
        self.assertEqual(m._lva[4], 4.0)
        m._op_stack.append(5.0)
        m.interpret(0x38, [4])
        self.assertEqual(m._lva[4], 5.0)

    def test_fstore_0(self):
        m = OpCodes()
        m._op_stack.append(1.0)
        m.interpret(0x43)
        self.assertEqual(m._lva[0], 1.0)
        m._op_stack.append(2.0)
        m.interpret(0x43)
        self.assertEqual(m._lva[0], 2.0)

    def test_fstore_1(self):
        m = OpCodes()
        m._lva.append(0.0)
        m._op_stack.append(1.0)
        m.interpret(0x44)
        self.assertEqual(m._lva[1], 1.0)
        m._op_stack.append(2.0)
        m.interpret(0x44)
        self.assertEqual(m._lva[1], 2.0)

    def test_fstore_2(self):
        m = OpCodes()
        m._lva.append(0.0)
        m._lva.append(1.0)
        m._op_stack.append(2.0)
        m.interpret(0x45)
        self.assertEqual(m._lva[2], 2.0)
        m._op_stack.append(3.0)
        m.interpret(0x45)
        self.assertEqual(m._lva[2], 3.0)

    def test_fstore_3(self):
        m = OpCodes()
        m._lva.append(0.0)
        m._lva.append(1.0)
        m._lva.append(2.0)
        m._op_stack.append(3.0)
        m.interpret(0x46)
        self.assertEqual(m._lva[3], 3.0)
        m._op_stack.append(4.0)
        m.interpret(0x46)
        self.assertEqual(m._lva[3], 4.0)

    def test_fadd(self):
        m = OpCodes()
        m._op_stack.append(np.float32(1.5))
        m._op_stack.append(np.float32(2.4))
        m.interpret(0x62)
        self.assertEqual(m._op_stack.pop(), np.float32(3.9))

    def test_fsub(self):
        m = OpCodes()
        m._op_stack.append(np.float32(3.5))
        m._op_stack.append(np.float32(1.4))
        m.interpret(0x66)
        self.assertEqual(m._op_stack.pop(), np.float32(2.1))

    def test_fmul(self):
        m = OpCodes()
        m._op_stack.append(np.float32(2.5))
        m._op_stack.append(np.float32(1.0))
        m.interpret(0x6a)
        self.assertEqual(m._op_stack.pop(), np.float32(2.5))

    def test_fdiv(self):
        m = OpCodes()
        m._op_stack.append(np.float32(2.0))
        m._op_stack.append(np.float32(2.0))
        m.interpret(0x6e)
        self.assertEqual(m._op_stack.pop(), np.float32(1.0))
        m._op_stack.append(np.float32(2.0))
        m._op_stack.append(np.float32(0.0))
        self.assertEqual(m.interpret(0x6e), 'Error: Divides by Zero')

    def test_frem(self):
        m = OpCodes()
        m._op_stack.append(np.float32(3.0))
        m._op_stack.append(np.float32(2.0))
        m.interpret(0x72)
        self.assertEqual(m._op_stack.pop(), np.float32(1.0))
        m._op_stack.append(np.float32(5.0))
        m._op_stack.append(np.float32(0.0))
        self.assertEqual(m.interpret(0x72), 'Error: Divides by Zero')

    def test_fneg(self):
        m = OpCodes()
        m._op_stack.append(np.float32(3.0))
        m.interpret(0x76)
        self.assertEqual(m._op_stack.pop(), np.float(-3.0))

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
        self.assertEqual(m._get_str_from_cpool(0, c), 'A.B:C')

    def test_lload_0(self):
        m = OpCodes()
        m._lva.append(0)
        m._lva.append(1)
        m.interpret(0x1e)
        self.assertEqual(m._op_stack.pop(), 1)
        self.assertEqual(m._op_stack.pop(), 0)

    def test_lload_1(self):
        m = OpCodes()
        m._lva.append(0)
        m._lva.append(0)
        m._lva.append(1)
        m.interpret(0x1f)
        self.assertEqual(m._op_stack.pop(), 1)
        self.assertEqual(m._op_stack.pop(), 0)

    def test_lload_2(self):
        m = OpCodes()
        m._lva.append(0)
        m._lva.append(0)
        m._lva.append(0)
        m._lva.append(1)
        m.interpret(0x20)
        self.assertEqual(m._op_stack.pop(), 1)
        self.assertEqual(m._op_stack.pop(), 0)

    def test_lload_3(self):
        m = OpCodes()
        m._lva.append(0)
        m._lva.append(0)
        m._lva.append(0)
        m._lva.append(0)
        m._lva.append(1)
        m.interpret(0x21)
        self.assertEqual(m._op_stack.pop(), 1)
        self.assertEqual(m._op_stack.pop(), 0)

    def test_lload(self):
        m = OpCodes()
        m._lva.append(0)
        m._lva.append(1)
        m._lva.append(2)
        m._lva.append(3)
        m._lva.append(0)
        m._lva.append(1)
        m.interpret(0x16, [4])
        self.assertEqual(m._op_stack.pop(), 1)
        self.assertEqual(m._op_stack.pop(), 0)

    def test_lconst_0(self):
        m = OpCodes()
        m.interpret(0x9)
        self.assertEqual(0, m._op_stack.pop())
        self.assertEqual(0, m._op_stack.pop())

    def test_lconst_1(self):
        m = OpCodes()
        m.interpret(0xa)
        self.assertEqual(1, m._op_stack.pop())
        self.assertEqual(0, m._op_stack.pop())

    def test_lstore_0(self):
        m = OpCodes()
        m._op_stack.append(0)
        m._op_stack.append(1)
        m.interpret(0x3f)
        self.assertEqual(m._lva[0], 0)
        self.assertEqual(m._lva[1], 1)
        n = OpCodes()
        n._lva.append(5)
        n._op_stack.append(0)
        n._op_stack.append(1)
        n.interpret(0x3f)
        self.assertEqual(n._lva[0], 0)
        self.assertEqual(n._lva[1], 1)
        o = OpCodes()
        o._lva.append(5)
        o._lva.append(5)
        o._op_stack.append(0)
        o._op_stack.append(1)
        o.interpret(0x3f)
        self.assertEqual(o._lva[0], 0)
        self.assertEqual(o._lva[1], 1)

    def test_lstore_1(self):
        m = OpCodes()
        m._lva.append(0)
        m._op_stack.append(0)
        m._op_stack.append(1)
        m.interpret(0x40)
        self.assertEqual(m._lva[1], 0)
        self.assertEqual(m._lva[2], 1)
        n = OpCodes()
        n._lva.append(5)
        n._lva.append(5)
        n._op_stack.append(0)
        n._op_stack.append(1)
        n.interpret(0x40)
        self.assertEqual(n._lva[1], 0)
        self.assertEqual(n._lva[2], 1)
        o = OpCodes()
        o._lva.append(5)
        o._lva.append(5)
        o._lva.append(5)
        o._op_stack.append(0)
        o._op_stack.append(1)
        o.interpret(0x40)
        self.assertEqual(o._lva[1], 0)
        self.assertEqual(o._lva[2], 1)

    def test_lstore_2(self):
        m = OpCodes()
        m._lva.append(0)
        m._lva.append(0)
        m._op_stack.append(0)
        m._op_stack.append(1)
        m.interpret(0x41)
        self.assertEqual(m._lva[2], 0)
        self.assertEqual(m._lva[3], 1)
        n = OpCodes()
        n._lva.append(5)
        n._lva.append(5)
        n._lva.append(5)
        n._op_stack.append(0)
        n._op_stack.append(1)
        n.interpret(0x41)
        self.assertEqual(n._lva[2], 0)
        self.assertEqual(n._lva[3], 1)
        o = OpCodes()
        o._lva.append(5)
        o._lva.append(5)
        o._lva.append(5)
        o._lva.append(5)
        o._op_stack.append(0)
        o._op_stack.append(1)
        o.interpret(0x41)
        self.assertEqual(o._lva[2], 0)
        self.assertEqual(o._lva[3], 1)

    def test_lstore_3(self):
        m = OpCodes()
        m._lva.append(0)
        m._lva.append(0)
        m._lva.append(0)
        m._op_stack.append(0)
        m._op_stack.append(1)
        m.interpret(0x42)
        self.assertEqual(m._lva[3], 0)
        self.assertEqual(m._lva[4], 1)
        n = OpCodes()
        n._lva.append(5)
        n._lva.append(5)
        n._lva.append(5)
        n._lva.append(5)
        n._op_stack.append(0)
        n._op_stack.append(1)
        n.interpret(0x42)
        self.assertEqual(n._lva[3], 0)
        self.assertEqual(n._lva[4], 1)
        o = OpCodes()
        o._lva.append(5)
        o._lva.append(5)
        o._lva.append(5)
        o._lva.append(5)
        o._lva.append(5)
        o._op_stack.append(0)
        o._op_stack.append(1)
        o.interpret(0x42)
        self.assertEqual(o._lva[3], 0)
        self.assertEqual(o._lva[4], 1)

    def test_lstore(self):
        m = OpCodes()
        m._lva.append(0)
        m._lva.append(0)
        m._lva.append(0)
        m._lva.append(0)
        m._op_stack.append(0)
        m._op_stack.append(1)
        m.interpret(0x37, [4])
        self.assertEqual(m._lva[4], 0)
        self.assertEqual(m._lva[5], 1)
        n = OpCodes()
        n._lva.append(5)
        n._lva.append(5)
        n._lva.append(5)
        n._lva.append(5)
        n._lva.append(5)
        n._op_stack.append(0)
        n._op_stack.append(1)
        n.interpret(0x37, [4])
        self.assertEqual(n._lva[4], 0)
        self.assertEqual(n._lva[5], 1)
        o = OpCodes()
        o._lva.append(5)
        o._lva.append(5)
        o._lva.append(5)
        o._lva.append(5)
        o._lva.append(5)
        o._lva.append(5)
        o._op_stack.append(0)
        o._op_stack.append(1)
        o.interpret(0x37, [4])
        self.assertEqual(o._lva[4], 0)
        self.assertEqual(o._lva[5], 1)

    def test_ladd(self):
        m = OpCodes()
        m._op_stack.append(0)
        m._op_stack.append(1)
        m._op_stack.append(0)
        m._op_stack.append(2)
        m.interpret(0x61)
        self.assertEqual(m._op_stack.pop(), 3)
        self.assertEqual(m._op_stack.pop(), 0)

    def test_lsub(self):
        m = OpCodes()
        m._op_stack.append(0)
        m._op_stack.append(2)
        m._op_stack.append(0)
        m._op_stack.append(1)
        m.interpret(0x65)
        self.assertEqual(m._op_stack.pop(), 1)
        self.assertEqual(m._op_stack.pop(), 0)

    def test_lmul(self):
        m = OpCodes()
        m._op_stack.append(0)
        m._op_stack.append(3)
        m._op_stack.append(0)
        m._op_stack.append(2)
        m.interpret(0x69)
        self.assertEqual(m._op_stack.pop(), 6)
        self.assertEqual(m._op_stack.pop(), 0)

    def test_ldiv(self):
        m = OpCodes()
        m._op_stack.append(0)
        m._op_stack.append(6)
        m._op_stack.append(0)
        m._op_stack.append(3)
        m.interpret(0x6d)
        self.assertEqual(m._op_stack.pop(), 2)
        self.assertEqual(m._op_stack.pop(), 0)

    def test_lrem(self):
        m = OpCodes()
        m._op_stack.append(0)
        m._op_stack.append(7)
        m._op_stack.append(0)
        m._op_stack.append(3)
        m.interpret(0x71)
        self.assertEqual(m._op_stack.pop(), 1)
        self.assertEqual(m._op_stack.pop(), 0)

    def test_lneg(self):
        m = OpCodes()
        m._op_stack.append(0)
        m._op_stack.append(1)
        m.interpret(0x75)
        self.assertEqual(m._op_stack.pop(), -1)
        self.assertEqual(m._op_stack.pop(), -1)

    def test_lushr(self):
        m = OpCodes()
        m._op_stack.append(23)  # Testing for positive logical shift right
        m._op_stack.append(1)
        m.interpret(0x7d)
        self.assertEqual(m._op_stack.pop(), 11)
        m._op_stack.append(-5)  # Testing for negative logical shift right
        m._op_stack.append(3)
        m.interpret(0x7d)
        self.assertEqual(m._op_stack.pop(), 2305843009213693951)

    def test_land(self):
        m = OpCodes()
        m._op_stack.append(0)
        m._op_stack.append(1)
        m._op_stack.append(0)
        m._op_stack.append(1)
        m.interpret(0x7f)
        self.assertEqual(m._op_stack.pop(), 1)
        self.assertEqual(m._op_stack.pop(), 0)

    def test_lor(self):
        m = OpCodes()
        m._op_stack.append(0)
        m._op_stack.append(1)
        m._op_stack.append(0)
        m._op_stack.append(2)
        m.interpret(0x81)
        self.assertEqual(m._op_stack.pop(), 3)
        self.assertEqual(m._op_stack.pop(), 0)

    def test_lxor(self):
        m = OpCodes()
        m._op_stack.append(0)
        m._op_stack.append(1)
        m._op_stack.append(0)
        m._op_stack.append(2)
        m.interpret(0x83)
        self.assertEqual(m._op_stack.pop(), 3)
        self.assertEqual(m._op_stack.pop(), 0)

    def test_l2i(self):
        m = OpCodes()
        m._op_stack.append(0)
        m._op_stack.append(2)
        m.interpret(0x88)
        assert isinstance(m._op_stack.pop(), int)

    def test_l2f(self):
        m = OpCodes()
        m._op_stack.append(0)
        m._op_stack.append(2)
        m.interpret(0x89)
        assert isinstance(m._op_stack.pop(), float)

    def test_l2d(self):
        m = OpCodes()
        m._op_stack.append(0)
        m._op_stack.append(2)
        m.interpret(0x8a)
        assert isinstance(m._op_stack.pop(), float)        
        
    def test_longsplit(self):
        m = OpCodes()
        self.assertEqual((0, -1), m._longsplit(4294967295))
        self.assertEqual((1, 0), m._longsplit(4294967296))

    def test_longcomb(self):
        m = OpCodes()
        self.assertEqual(4294967295, m._longcomb(0, -1))
        self.assertEqual(4294967296, m._longcomb(1, 0))

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
        m._op_stack.append(5)
        m.interpret(0xb6, [0, 1], c)
        str1.info = [106, 97, 118, 97, 47, 105, 111, 47, 80, 114, 105, 110, 116, 83, 116, 114, 101, 97, 109]
        str2.info = [112, 114, 105, 110, 116, 108, 110]
        str3.info = [40, 76, 106, 97, 118, 97, 47, 108, 97, 110, 103, 47, 83, 116, 114, 105, 110, 103, 59, 41, 86]
        c = [methrefobj, classobj, nameandtypeobj, str1, str2, str3]
        m._op_stack.append("Hello World!")
        m.interpret(0xb6, [0, 1], c)
        self.assertEqual(mock_print.mock_calls, [
            call(5),
            call('Hello World!')
        ])
        with patch('builtins.input', return_value='5'):
            str1.info = [110, 101, 120, 116, 73, 110, 116, 58, 40, 41, 73]
            str2.info = [106, 97, 118, 97, 47, 117, 116, 105, 108, 47, 83, 99, 97, 110, 110, 101, 114]
            c = [methrefobj, classobj, str1, str2]
            m.interpret(0xb6, [0, 1], c)
            m._op_stack.append(5)
            self.assertEqual(m._op_stack.pop(), 5)

    def test_getstatic(self):
        m = OpCodes()
        const_info = ConstantInfo()
        const_info.tag = 1
        const_info.info = [70, 111, 111]
        imp_info = m.interpret(0xb2, [0, 0], [const_info])
        assert isinstance(imp_info, str)
        
    def test_ldc(self):
        m = OpCodes()
        str1 = ConstantInfo()
        str1.tag = 1
        str1.info = [72, 101, 108, 108, 111]
        m.interpret(0x12, [0], [str1])
        self.assertEqual(m._op_stack.pop(), "Hello")

    def test_fconst_0(self):
        m = OpCodes()
        m.interpret(0xb)
        self.assertEqual(m._op_stack.pop(), np.float32(0.0))

    def test_fconst_1(self):
        m = OpCodes()
        m.interpret(0xc)
        self.assertEqual(m._op_stack.pop(), np.float32(1.0))

    def test_fconst_2(self):
        m = OpCodes()
        m.interpret(0xd)
        self.assertEqual(m._op_stack.pop(), np.float32(2.0))

    def test_fload(self):
        m = OpCodes()
        m._lva.append(0.0)
        m._lva.append(1.0)
        m._lva.append(2.0)
        m._lva.append(3.0)
        m._lva.append(4.0)
        m.interpret(0x17, [4])
        self.assertEqual(m._op_stack.pop(), 4)

    def test_fload_0(self):
        m = OpCodes()
        m._lva.append(0.0)
        m.interpret(0x22)
        self.assertEqual(m._op_stack.pop(), np.float32(0.0))

    def test_fload_1(self):
        m = OpCodes()
        m._lva.append(0.0)
        m._lva.append(1.0)
        m.interpret(0x23)
        self.assertEqual(m._op_stack.pop(), np.float32(1.0))

    def test_fload_2(self):
        m = OpCodes()
        m._lva.append(0.0)
        m._lva.append(1.0)
        m._lva.append(2.0)
        m.interpret(0x24)
        self.assertEqual(m._op_stack.pop(), np.float32(2.0))

    def test_fload_3(self):
        m = OpCodes()
        m._lva.append(0.0)
        m._lva.append(1.0)
        m._lva.append(2.0)
        m._lva.append(3.0)
        m.interpret(0x25)
        self.assertEqual(m._op_stack.pop(), np.float32(3.0))

    def test_f2i(self):
        m = OpCodes()
        m._op_stack.append('3f800000')
        m.interpret(0x8b)
        self.assertEqual(np.dtype(m._op_stack.pop()), 'int32')

    def test_f2l(self):
        m = OpCodes()
        m._op_stack.append('3f800000')
        m.interpret(0x8c)
        self.assertEqual(m._op_stack.pop(), 1)
        self.assertEqual(m._op_stack.pop(), 0)

    def test_f2d(self):
        m = OpCodes()
        m._op_stack.append('3f800000')
        m.interpret(0x8d)
        self.assertEqual(m._op_stack.pop(), 0)
        self.assertEqual(m._op_stack.pop(), 0x3ff00000)

    def test_ret(self):
        m = OpCodes()
        self.assertEqual(m.interpret(0xb1), '')
