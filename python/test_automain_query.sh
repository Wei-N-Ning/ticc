#!/usr/bin/env bash

setUp() {
    set -e
}

expectTinyTestsFound() {
    echo $( python ./automain.py ./testdata/test_nomain.c )

}

expectTinyTestsNotFound() {
    echo $( python ./automain.py ./testdata/test_tinyCUnit.c )
}

setUp
expectTinyTestsFound
expectTinyTestsNotFound

