
import os
import unittest
import subprocess
import shlex
import sys

import automain
from automain import Parser, Stream, Formatter, main
import testdata

StringIO = automain.StringIO

_sourceFileSUT = \
"""
//
// Created by wein on 3/10/18.
//

static int *SUT = 0;

void RunTinyTests();

void test_1() {
    int i = 0;
    i += 10;
}

void SetUpGlobal {
    SUT = malloc(sizeof(int) * 16);
}

void TearDownGlobal {
    free(SUT);
}

void test_2() {
    int i = 1;
    i -= 10;
}

int main(int argc, char **argv) {
    RunTinyTests();
}
"""


class TestStream(unittest.TestCase):

    def test_(self):
        stream = Stream(StringIO.StringIO(_sourceFileSUT))
        for _ in range(2):
            stream.next_line()
        self.assertEqual('// Created by wein on 3/10/18.\n', stream.current_line())


class TestFuncDeclaration(unittest.TestCase):

    def test_to_string(self):
        cases = [
            ('foobar', dict(signature=''), dict(), 'void foobar();'),

            ('foo', dict(signature='int *{}(size_t sz, int *arr)'), dict(externDecl=True),
             'extern int *foo(size_t sz, int *arr);'),

            ('SETUP', dict(), dict(externDecl=True), 'extern void SETUP();'),  # create a global set-up function decl

            ('TearDown', dict(), dict(), 'void TearDown();'),  # create a per-case tear-down function decl
        ]
        for name, kwargs, options, expect in cases:
            actual = automain.FuncDeclaration(name, **kwargs).to_string(options=options)
            self.assertEqual(expect, actual)

    def test_create_from_source(self):
        cases = [
            ('void test_something() {\n', 'test_something', 'void {}()'),
            ('int test_retvalue(struct arg *p) {\n', 'test_retvalue', 'int {}(struct arg *p)')
        ]

        def to_stream(l):
            ss = StringIO.StringIO(l)
            return Stream(ss)

        for line, name, sig in cases:
            so = automain.TestFunctionDeclaration.create(to_stream(line))
            self.assertTrue(so)
            self.assertEqual(name, so.func_name)
            self.assertEqual(sig, so.signature)


class TestIncludeStatement(unittest.TestCase):

    def test_to_string(self):
        cases = [
            ('math.h', dict(is_std_library=True), dict(CXX=True), '#include <cmath>'),
            ('math.h', dict(is_std_library=True), dict(), '#include <math.h>'),
            ('doom.hpp', dict(), dict(), '#include <doom.hpp>')
        ]
        for name, kwargs, options, expect in cases:
            actual = automain.IncludeStatement(name, **kwargs).to_string(options=options)
            self.assertEqual(expect, actual)


class TestFuncScopeBegin(unittest.TestCase):

    def test_(self):
        cases = [
            ('Launch', dict(), dict(), 'void Launch() {'),
            ('Gen', dict(ret='struct dude *', args=['size_t sz', 'int precise_mode']), dict(),
             'struct dude * Gen(size_t sz, int precise_mode) {'),
        ]
        for func, kwargs, options, expected in cases:
            actual = automain.FuncScopeBegin(func, **kwargs).to_string(options=options)
            self.assertEqual(expected, actual)


class TestTimer(unittest.TestCase):

    def test_expectCompiledExecuted(self):
        ss = StringIO.StringIO()
        ss.write(automain.IncludeStatement('time.h').to_string() + '\n')
        ss.write(automain.IncludeStatement('stdio.h').to_string() + '\n')
        ss.write(automain.FuncScopeBegin(
            'main',
            ret='int',
            args=['int argc', 'char **argv']).to_string() + '\n')
        ss.write(automain.CTimerBegin().to_string() + '\n')
        ss.write('for (int i=0; i<1000; ++i)    ;\n')
        ss.write(automain.CTimerEnd().to_string() + '\n')
        ss.write(automain.ScopeEnd().to_string() + '\n')
        with open('/tmp/test_timer.c', 'w') as fp:
            fp.write(ss.getvalue())
        self.assertEqual(
            0, subprocess.call(shlex.split('gcc /tmp/test_timer.c -o /tmp/test_timer'), stdout=subprocess.PIPE))
        self.assertEqual(
            0, subprocess.call(shlex.split('/tmp/test_timer'), stdout=subprocess.PIPE)
        )


class TestCallFunction(unittest.TestCase):

    def test_(self):
        cases = [
            ('foo', dict(), dict(), 'foo();'),
            ('foo', dict(ret_var='a'), dict(), 'a = foo();'),
            ('foo', dict(args=['sz, precise_mode, &o_buf']), dict(),
             'foo(sz, precise_mode, &o_buf);'),
            ('foo', dict(ret_var='struct dude *d'), dict(), 'struct dude *d = foo();')
        ]
        for fn, kwargs, options, expected in cases:
            actual = automain.CallFunction(fn, **kwargs).to_string(options=options)
            self.assertEqual(expected, actual)


class AcceptanceTestCSource(unittest.TestCase):

    def setUp(self):
        self.o_path = '/tmp/test_nomain_automain.c'
        self.bin_path = self.o_path + '.bin'
        self.i_path = testdata.file_path('test_nomain.c')
        sys.argv = ['', self.i_path, self.o_path]

    def test_expectOutFileGenerated(self):
        main()
        self.assertTrue(os.path.exists(self.o_path))

    def test_expectOutFileContents(self):
        main()
        with open(self.o_path, 'r') as fp:
            s = fp.read()
        # include
        self.assertIn('#include <stdio.h>', s)
        # decl
        self.assertIn('extern void test_given_when_then();', s)
        self.assertIn('extern void test_arrange_action_assert', s)
        # test entry point
        self.assertIn('test_given_when_then();', s)

    def test_expectCompiledExecuted(self):
        main()
        ret = subprocess.call(shlex.split('gcc {} {} -o {}'.format(self.i_path, self.o_path, self.bin_path)),
                              stdout=subprocess.PIPE)
        self.assertEqual(0, ret)
        ret = subprocess.call(shlex.split(self.bin_path), stdout=subprocess.PIPE)
        self.assertEqual(0, ret)


class AcceptanceTestSetupTearDown(unittest.TestCase):

    def setUp(self):
        self.o_path = '/tmp/test_nomain_setupteardown_automain.c'
        self.bin_path = self.o_path + '.bin'
        self.i_path = testdata.file_path('test_nomain_setupteardown.c')
        sys.argv = ['', self.i_path, self.o_path]

    def test_expectCompiledExecuted(self):
        main()
        ret = subprocess.call(shlex.split('gcc {} {} -o {}'.format(self.i_path, self.o_path, self.bin_path)),
                              stdout=subprocess.PIPE)
        self.assertEqual(0, ret)
        ret = subprocess.call(shlex.split(self.bin_path), stdout=subprocess.PIPE)
        self.assertEqual(0, ret)


class AcceptanceTestCXXSource(unittest.TestCase):

    def setUp(self):
        self.o_path = '/tmp/test_nomaincxx_automain.cpp'
        self.bin_path = self.o_path + '.bin'
        self.i_path = testdata.file_path('test_nomaincxx.cpp')
        sys.argv = ['', self.i_path, self.o_path]

    def test_expectCompiledExecuted(self):
        main()
        ret = subprocess.call(shlex.split('g++ -std=c++11 {} {} -o {}'.format(self.i_path, self.o_path, self.bin_path)),
                              stdout=subprocess.PIPE)
        self.assertEqual(0, ret)
        ret = subprocess.call(shlex.split(self.bin_path), stdout=subprocess.PIPE)
        self.assertEqual(0, ret)


if __name__ == '__main__':
    unittest.main()
