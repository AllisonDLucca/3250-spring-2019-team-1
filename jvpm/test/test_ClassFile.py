import unittest
from unittest.mock import mock_open, patch
from jvpm.ClassFile import ClassFile
from jvpm.ClassFile import OpCodes

class TestClassFile(unittest.TestCase):
    def setUp(self):
        m = mock_open(read_data=b'\xCA\xFE\xBA\xBE\x00\x01\x02\x03\x03\x04')
        #_with patch(__name__ + '.open', m):
        with patch('builtins.open', m):
            self.cf = ClassFile()

    def test_magic(self):
        self.assertEqual(self.cf.get_magic(), 'CAFEBABE')

    def test_minor(self):
        self.assertEqual(self.cf.get_minor(), 1)

    def test_major(self):
        self.assertEqual(self.cf.get_major(), 5)

    def test_constant_pool_count(self):
        self.assertEqual(self.cf.get_constant_pool_count(), 7)

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
        m.op_stack.append(23)       #Testing for positive logical shift right
        m.op_stack.append(1)
        m.interpret(0x7c)
        self.assertEqual(m.op_stack.pop(), 11)
        m.op_stack.append(-5)       #Testing for negative logical shift right
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


