
import os
import unittest

from tcc import compile_c_cxx


class TestCallPosixCompiler(unittest.TestCase):

    def test_detectLanguageC(self):
        l = compile_c_cxx.CallPosixCompiler.source_language(
            ['a.c', 'b.d', 'aa']
        )
        self.assertEqual('C', l)

    def test_detectLanguageCxx(self):
        l = compile_c_cxx.CallPosixCompiler.source_language(
            ['a.c', 'b.cpp', 'aa']
        )
        self.assertEqual('CXX', l)

    def test_detectLanguageFailed(self):
        self.assertRaises(
            RuntimeError,
            compile_c_cxx.CallPosixCompiler.source_language,
            ['a.ca', 'b.ci', 'aa']
        )

    def test_findKL(self):
        cc, cxx = compile_c_cxx.CallPosixCompiler.find_compiler('clang')
        self.assertTrue(cc)
        self.assertTrue(cxx)

    def test_findCC(self):
        cc, cxx = compile_c_cxx.CallPosixCompiler.find_compiler('cc')
        self.assertTrue(cc)
        self.assertTrue(cxx)


if __name__ == '__main__':
    unittest.main()
