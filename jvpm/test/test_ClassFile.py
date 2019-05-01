import unittest
from unittest.mock import mock_open, patch
from jvpm.ClassFile import ClassFile
from jvpm.ClassFile import MethodInfo
from jvpm.ClassFile import CodeAttribute
from jvpm.ClassFile import ConstantInfo
from unittest.mock import patch, call

class TestClassFile(unittest.TestCase):
    def setUp(self):
        m = mock_open(read_data=b'\xca\xfe\xba\xbe\x00\x03\x00\x2d\x00\x0a\x01\x00\x10\x6a\x61\x76\x61\x2f\x6c\x61\x6e\x67\x2f\x4f\x62\x6a\x65\x63\x74\x01\x00\x0a\x53\x6f\x75\x72\x63\x65\x46\x69\x6c\x65\x01\x00\x04\x6d\x61\x69\x6e\x01\x00\x04\x43\x6f\x64\x65\x01\x00\x16\x28\x5b\x4c\x6a\x61\x76\x61\x2f\x6c\x61\x6e\x67\x2f\x53\x74\x72\x69\x6e\x67\x3b\x29\x56\x07\x00\x09\x01\x00\x07\x74\x65\x73\x74\x32\x2e\x6a\x07\x00\x01\x01\x00\x03\x41\x64\x64\x00\x21\x00\x06\x00\x08\x00\x00\x00\x00\x00\x01\x00\x09\x00\x03\x00\x05\x00\x01\x00\x04\x00\x00\x00\x2f\x00\x01\x00\x01\x00\x00\x00\x0c\x04\x05\x60\x36\x00\x15\x00\xb6\x00\x01\x12\x01')  # x06\x07\x7e\x08\x02\x6c\x05\x06\x68\x07\x74\x08\x03\x80\x04\x05\x70\x06\x07\x78\x08\x04\x7a\x05\x06\x64\x07\x08\x7c\x04\x05\x82\x00\x00\x00\x00\x00\x01\x00\x02\x00\x00\x00\x02\x00\x07')

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
        self.assertEqual(ops._op_stack, [3, 'java/lang/Object'])
