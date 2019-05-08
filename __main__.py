from jvpm.ClassFile import ClassFile
import sys

def main(path):
    java = ClassFile(path)
    java.run_opcodes()

if '__main__' == __name__: #pragma: no cover
    try:
        main(sys.argv[1])
    except:
        print("A path to a java .class file is required. Try the format: python __main__.py <path>")