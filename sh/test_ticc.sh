#!/usr/bin/env bash

dir=$( dirname ${0} )

setUp() {
    set -e
    rm -rf /tmp/sut /tmp/_ /tmp/_.* /tmp/__*
    mkdir /tmp/sut
}

# expect the resulting binary to be
# fully functional
# expect the program to be built with
# correct compilation flags
test_buildAndRunCProgram() {
    cat > /tmp/sut/_.c <<EOF
#include <stdio.h>
int main() {
    printf("thereisacow\n");
    return 0;
}
EOF
    ( ${dir}/ticc run /tmp/sut/_.c -- -O3 -frecord-gcc-switches &&
    echo "c program seems working" )
    ( readelf -p .GCC.command.line /tmp/ticc/_ |
    grep -P --color '\-O3|\-frecord' >/dev/null &&
    echo "find compiler flags" )
}

test_buildAndRunCXX11Program() {
    cat > /tmp/sut/_.cc <<EOF
#include <vector>
#include <iostream>
#ifndef MAGIC_NUM
#define MAGIC_NUM 0
#endif
class A {
public:
    static const int a = 100;
};
int main() {
    using namespace std;
    vector<A> va(10);
    int sum = 0;
    for (const auto& elem : va) {
        sum += elem.a;
    }
    if (sum != MAGIC_NUM) {
        return 1;
    }
    cout << "thereisnospoon: " << sum << endl;
    return 0;
}
EOF
    ( ${dir}/ticc run /tmp/sut/_.cc -- -DMAGIC_NUM=1000 -frecord-gcc-switches &&
    echo "c++ program seems working" )
    ( readelf -p .GCC.command.line /tmp/ticc/_ |
    grep -P --color '\-D MAGIC' >/dev/null &&
    echo "find compiler flags" )
}

test_buildAndDisassembleCProgram() {
    cat > /tmp/sut/_.c <<EOF
#include <stdio.h>
void shout() {
    const char buf[] = "iddqdidkfa";
    printf("%s\n", buf);
}
int main() {
    shout();
    return 0;
}
EOF
    ( ${dir}/ticc dasm /tmp/sut/_.c shout |
    grep -P --color '[a-fA-F0-9]+\s+call' >/dev/null &&
    echo "disassemble seems successful (find subroutine)" )
}

test_buildAndDisassembleCXXProgram() {
    cat > /tmp/sut/_.cc <<EOF
#include <thread>
void worker() {
    for (int i = 0; i < 1000; ++i) {
        ;
    }
}
int main() {
    std::thread th(worker);
    th.join();
    return 0;
}
EOF
    ( ${dir}/ticc dasm /tmp/sut/_.cc -- -pthread |
    grep -P 'std::thread th' >/dev/null &&
    echo "disassemble seems successful (find source line)")
}

setUp
test_buildAndRunCProgram
test_buildAndRunCXX11Program
test_buildAndDisassembleCProgram
test_buildAndDisassembleCXXProgram
