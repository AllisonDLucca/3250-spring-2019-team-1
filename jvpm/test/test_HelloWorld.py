import unittest
import sys
import jvpm.HelloWorld
from unittest.mock import Mock, call

class TestHelloWorld(unittest.TestCase):
    def test_HelloWorld(self):
        sys.stdout = unittest.mock.Mock()
        jvpm.HelloWorld.HelloWorld()
        sys.stdout.assert_has_calls(
            [call.write('Hello world'), call.write('\n'),
            call.write('Emily Berger'), call.write('\n'),
            call.write('Allison Lucca'), call.write('\n'),
            call.write('Justin Figueredo'), call.write('\n'),
            call.write('Eric Dao'), call.write('\n'),
            call.write('Michael DeVries'), call.write('\n')
			call.write('Saad Baig'), call.write('\n')]
        )
