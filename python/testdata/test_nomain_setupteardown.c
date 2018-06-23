//
// Created by wein on 3/10/18.
//

#include <stdlib.h>
#include <memory.h>
#include <assert.h>

void RunTinyTests();

struct TestSuite {
    int *arr;
};

static struct TestSuite *testSuite = 0;

void SetUpGlobal() {
    testSuite = malloc(sizeof(struct TestSuite));
    testSuite->arr = malloc(sizeof(int) * 8);
    memset(testSuite->arr, 0, sizeof(testSuite->arr));
}

void setUp() {
    assert(testSuite);
}

void TearDownGlobal() {
    if (testSuite) {
        if (testSuite->arr) {
            free(testSuite->arr);
        }
        free(testSuite);
        testSuite = 0;
    }
}

void tearDown() {
    assert(testSuite);
}

int factory(int n) {
    return n * 10;
}

void test_given_when_then() {
    int r = 0;
    assert(0 == testSuite->arr[0]);
    r = factory(testSuite->arr[0] + 1);
    assert(10 == r);
}

void test_arrange_action_assert() {
    int i = 1;
    i -= 10;
}

int main(int argc, char **argv) {
    RunTinyTests();
    return 0;
}
