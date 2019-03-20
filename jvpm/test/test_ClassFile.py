import unittest
from unittest.mock import mock_open, patch
from jvpm.ClassFile import ClassFile
from jvpm.ClassFile import OpCodes
from jvpm.ClassFile import MethodInfo
from jvpm.ClassFile import CodeAttribute
from jvpm.ClassFile import ConstantInfo

class TestClassFile(unittest.TestCase):
    def setUp(self):
        m = mock_open(read_data=b'\xca\xfe\xba\xbe\x00\x03\x00\x2d\x00\x0a\x01\x00\x10\x6a\x61\x76\x61\x2f\x6c\x61\x6e\x67\x2f\x4f\x62\x6a\x65\x63\x74\x01\x00\x0a\x53\x6f\x75\x72\x63\x65\x46\x69\x6c\x65\x01\x00\x04\x6d\x61\x69\x6e\x01\x00\x04\x43\x6f\x64\x65\x01\x00\x16\x28\x5b\x4c\x6a\x61\x76\x61\x2f\x6c\x61\x6e\x67\x2f\x53\x74\x72\x69\x6e\x67\x3b\x29\x56\x07\x00\x09\x01\x00\x07\x74\x65\x73\x74\x32\x2e\x6a\x07\x00\x01\x01\x00\x03\x41\x64\x64\x00\x21\x00\x06\x00\x08\x00\x00\x00\x00\x00\x01\x00\x09\x00\x03\x00\x05\x00\x01\x00\x04\x00\x00\x00\x2f\x00\x01\x00\x01\x00\x00\x00\x07\x04\x05\x60\x36\x00\x15\x00')  # xb6\x50\x21')   x06\x07\x7e\x08\x02\x6c\x05\x06\x68\x07\x74\x08\x03\x80\x04\x05\x70\x06\x07\x78\x08\x04\x7a\x05\x06\x64\x07\x08\x7c\x04\x05\x82\x00\x00\x00\x00\x00\x01\x00\x02\x00\x00\x00\x02\x00\x07')

        #_with patch(__name__ + '.open', m):
        with patch('builtins.open', m):
            self.cf = ClassFile()

    def test_magic(self):
        self.assertEqual(self.cf.get_magic(), 'CAFEBABE')

    def test_minor(self):
        self.assertEqual(self.cf.get_minor(), 3)

    def test_major(self):
        self.assertEqual(self.cf.get_major(), 45)

    def test_constant_pool_count(self):
        self.assertEqual(self.cf.get_constant_pool_count(), 10)

    def test_create_c_pool(self):
        self.cf.create_c_pool()
        self.assertEqual(self.cf.c_pool_table.__len__(), 9)
        self.assertEqual(type(self.cf.c_pool_table[0]), type(ConstantInfo()))

    def test_get_constant_pool_size(self):
        self.assertEqual(self.cf.get_constant_pool_size(), 93)

    def test_get_flags(self):
        self.assertEqual(self.cf.get_flags(), 33)

    def test_get_this_class(self):
        self.assertEqual(self.cf.get_this_class(), 6)

    def test_get_super_class(self):
        self.assertEqual(self.cf.get_super_class(), 8)

    def test_get_interface_count(self):
        self.assertEqual(self.cf.get_interface_count(), 0)

    def test_get_field_count(self):
        self.assertEqual(self.cf.get_field_count(), 0)

    def test_get_field_size(self):
        self.assertEqual(self.cf.get_field_size(), 0)

    def test_get_method_count(self):
        self.assertEqual(self.cf.get_method_count(), 1)

    def test_get_field_size(self):
        self.assertEqual(self.cf.get_field_size(), 0)

    def test_create_method_table(self):
        methods = self.cf.create_method_table()
        self.assertEqual(methods.__len__(), 1)
        self.assertEqual(type(methods[0]), type(MethodInfo()))

    def test_get_attribute_count(self):
        self.assertEqual(self.cf.get_attribute_count(), 1)

    def test_create_attribute_table(self):
        attributes = self.cf.create_attribute_table()
        self.assertEqual(attributes.__len__(), 1)
        self.assertEqual(type(attributes[0]), type(CodeAttribute()))

    def test_run_opcodes(self):
        self.cf.create_attribute_table()
        ops = self.cf.run_opcodes()
        self.assertEqual(ops.op_stack, [3])

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



