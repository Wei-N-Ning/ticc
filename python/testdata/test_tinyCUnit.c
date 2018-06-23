//
// Include this header in your test executable
//

#include "tinyCUnit.h"

int sut() {
    return 10;
}

int factory(int size) {
    return size * 10;
}

int main(int argc, char **argv) {

    InitializeTinyTests();

    NewTinyTest("ExpectValueIs10") ((void) {
        AssertEqual(10, sut());
    });

    NewTinyTest("GivenSizeExpectProduct") ((void) {
        AssertEqual(30, factory(3));
    });

    RunTinyTests();

    return 0;
}
