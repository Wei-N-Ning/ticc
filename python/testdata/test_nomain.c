//
// Created by wein on 3/10/18.
//

#include <stdlib.h>

static int *SUT = 0;

void RunTinyTests();

void test_given_when_then() {
    int i = 0;
    i += 10;
}

void SetUpGlobal() {
    SUT = malloc(sizeof(int) * 16);
}

void TearDownGlobal() {
    free(SUT);
}

void test_arrange_action_assert() {
    int i = 1;
    i -= 10;
}

int main(int argc, char **argv) {
    RunTinyTests();
}
