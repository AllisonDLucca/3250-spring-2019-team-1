import unittest
import jvpm.HelloWorld
from unittest.mock import patch, call

class TestHelloWorld(unittest.TestCase):
    @patch('builtins.print')
    def test_HelloWorld(self, mock_print):
        jvpm.HelloWorld.HelloWorld()
        self.assertEqual(mock_print.mock_calls, [
            call.write('Hello world'),
            call.write('Emily Berger'),
            call.write('Allison Lucca'),
            call.write('Justin Figueredo'),
            call.write('Eric Dao'),
            call.write('Michael DeVries'),
	        call.write('Saad Baig'),
            call.write('James Bierschwale'),
	        call.write('Josh Brown')
        ])
