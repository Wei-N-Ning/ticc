
import os
import shlex
import subprocess


doc = """
compile
-------

#### Usage:
```
tcc <compiler> out_path i_file1 i_file2 ... i_filen -- flags link_flags
```

<compiler>: to specify the compiler program.

supported choices are: cc, clang

both are expected to be supplied by the underlying operating system,

for example on Ubuntu 16, cc is by default gcc 5.4; clang is by default clang 3.8 if 
installed 
"""


class CallPosixCompiler(object):

    C_LANG = ('.c', )
    CXX_LANG = ('.cxx', '.cc', '.cpp')

    def __init__(self, compl_exe):
        self.compl = compl_exe
        _, __ = self.find_compiler(compl_exe)
        self.cc = _
        self.cxx = __

    def compile(self, i_files, out_path, flags='', link_flags=''):
        lang = self.source_language(i_files)
        compl = self.cc
        if lang == 'CXX':
            compl = self.cxx
        cmd_line = '{COMPL} {FLAGS} -o {OUTPATH} {IFILES} {LINKFLAGS}'.format(
            COMPL=compl,
            FLAGS=flags,
            OUTPATH=out_path,
            IFILES=' '.join(i_files),
            LINKFLAGS=link_flags
        )
        if os.path.exists(out_path):
            os.remove(out_path)
        p = subprocess.Popen(shlex.split(cmd_line), stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        if p.wait() != 0 or not os.path.exists(out_path):
            raise RuntimeError('Compilation error:\n'
                               'stderr:\n{}\n'
                               'stdout:\n{}\n'.format(p.stderr.read(), p.stdout.read()))

    @staticmethod
    def find_compiler(compl_exe):
        if compl_exe == 'clang':
            cc = subprocess.check_output(shlex.split('/bin/which clang'))
            cxx = subprocess.check_output(shlex.split('/bin/which clang++'))
            return cc, cxx
        if compl_exe == 'cc':
            cc = subprocess.check_output(shlex.split('/bin/which cc'))
            cxx = subprocess.check_output(shlex.split('/bin/which c++'))
            return cc, cxx
        raise RuntimeError('Unsupported compiler type: {}'.format(compl_exe))

    @staticmethod
    def source_language(i_files):
        l = dict([(_, 0)
                  for _ in CallPosixCompiler.C_LANG + CallPosixCompiler.CXX_LANG])
        for i_file in i_files:
            _ = os.path.splitext(i_file)[-1]
            if _ in l:
                l[_] = l[_] + 1
        for _ in sorted(l, reverse=True):
            if l[_]:
                if _ in CallPosixCompiler.CXX_LANG:
                    return 'CXX'
                if _ in CallPosixCompiler.C_LANG:
                    return 'C'
        raise RuntimeError('Can not detect source languages:\n'
                           '{}'.format(i_files))


def _compile_posix(compl_exe, out_path, i_files, flags='', link_flags=''):
    CallPosixCompiler(compl_exe).compile(i_files, out_path, flags=flags, link_flags=link_flags)


def compile_posix(*args):
    compl_exe = 'cc'
    out_path = ''
    i_files = list()
    flags = list()
    link_flags = list()

    for idx, arg in enumerate(args):
        if arg == 'clang':
            compl_exe = 'clang'
            continue

        if not out_path:
            out_path = arg
            continue

        if arg != '--':
            i_files.append(arg)
            continue

        if arg == '--':
            flags = arg[idx + 1:]
            break

    print(
        compl_exe,
        out_path,
        i_files,
        flags,
        link_flags
    )
