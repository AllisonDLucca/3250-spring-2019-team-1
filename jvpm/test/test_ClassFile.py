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
        OpCodes().interpret(0x02)
        self.assertEqual(OpCodes().op_stack.pop(), -1)

    def test_iconst_0(self):
        OpCodes().interpret(0x03)
        self.assertEqual(OpCodes().op_stack.pop(), 0)

    def test_iconst_1(self):
        OpCodes().interpret(0x04)
        self.assertEqual(OpCodes().op_stack.pop(), 1)

    def test_iconst_2(self):
        OpCodes().interpret(0x05)
        self.assertEqual(OpCodes().op_stack.pop(), 2)

    def test_iconst_3(self):
        OpCodes().interpret(0x06)
        self.assertEqual(OpCodes().op_stack.pop(), 3)

    def test_iconst_4(self):
        OpCodes().interpret(0x07)
        self.assertEqual(OpCodes().op_stack.pop(), 4)

    def test_iconst_5(self):
        OpCodes().interpret(0x08)
        self.assertEqual(OpCodes().op_stack.pop(), 5)
