from jvpm.ClassFile import ClassFile

def main():
    java = ClassFile()  # pragma: no cover
    print('magic: ', java.get_magic())  # pragma: no cover
    print('minor_version: ', java.get_minor())  # pragma: no cover
    print('major_version: ', java.get_major())  # pragma: no cover
    print('constant_pool_count: ', java.get_constant_pool_count())  # pragma: no cover
    print('parsing constant pool...')  # pragma: no cover
    java.create_c_pool()  # pragma: no cover
    for i in range(0, java.c_pool_table.__len__()):  # pragma: no cover
        constant = java.c_pool_table[i]  # pragma: no cover
        print("Constant #", i, " tag: ", constant.tag, " value: ", constant.info)  # pragma: no cover
    print('interface count: ', java.get_interface_count())  # pragma: no cover
    print('field count: ', java.get_field_count())  # pragma: no cover
    print('method count: ', java.get_method_count())  # pragma: no cover
    java.create_method_table()  # pragma: no cover
    print('attribute count: ', java.get_attribute_count())  # pragma: no cover
    java.create_attribute_table()  # pragma: no cover
    java.run_opcodes()  # pragma: no cover


if '__main__' == __name__: #pragma: no cover
    main()