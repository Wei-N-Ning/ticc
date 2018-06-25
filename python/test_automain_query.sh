#!/usr/bin/env bash

setUp() {
    set -e
}

expectTinyTestsFound() {
    echo $( ./automain.py ./testdata/test_nomain.c )

}

expectTinyTestsNotFound() {
    echo $( ./automain.py ./testdata/test_tinyCUnit.c )
}

setUp
expectTinyTestsFound
expectTinyTestsNotFound

