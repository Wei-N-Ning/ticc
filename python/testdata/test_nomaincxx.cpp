//
// Created by wein on 3/21/18.
//

#include <cassert>
#include <cstddef>
#include <algorithm>
#include <map>
#include <utility>
#include <vector>

void RunTinyTests();

namespace {

int factory(int n) {
    return n * 10;
}

int factory(double n) {
    return static_cast<int>(n * 10);
}

}

void test_iddqd() {
    assert(100 == factory(10));
    assert(10 == factory(1));
    assert(314 == factory(31.4));
}

void test_idkfa() {
    std::vector<int> v{1, 2, 3};
    int sum = 0;
    for (const auto &n : v) {
        sum += n;
    }
    assert(6 == sum);
}

void test_iddt() {
    using mystack_t = std::vector<double>;
    mystack_t _s;
    auto push = [&](double num) {
        _s.emplace_back(num);
    };
    auto pop = [&]()-> double {
        if (_s.empty()) {
            return 0.0;
        }
        auto last = _s.back();
        _s.pop_back();
        return last;
    };
    auto size = [&]() -> size_t {
        return _s.size();
    };
    push(12);
    push(13);
    push(33);
    assert(3 == size());
    assert(33.0 == pop());
    assert(13.0 == pop());
    assert(1 == size());
}

void test_idnoclip() {
    using std::map;
    using std::for_each;
    map<int, int> sizeById{{1, 3}, {2, 1}, {3, 6}, {4, 5}};
    int sum{0};
    auto f = [&](const std::pair<int, int> &elem) {
        sum += elem.second;
    };
    for_each(sizeById.cbegin(), sizeById.cend(), f);
    assert(15 == sum);
}

int main(int argc, char **argv) {
    RunTinyTests();
    return 0;
}
