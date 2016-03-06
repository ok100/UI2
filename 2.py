#!/usr/bin/env python

import heapq
import itertools
import time


# Heuristika: pocet policok ktore nie su na svojom mieste
# state - stav pre ktory sa ma vypocitat heuristika
# x - pocet stlpcov
# y - pocet riadkov
def h_misplaced_tiles(state, x, y):
    return sum(1 for t in zip(state.arr, state.final) if t[0] != t[1])


# Heuristika: sucet vzdialenosti policok od cielovej pozicie
# state - stav pre ktory sa ma vypocitat heuristika
# x - pocet stlpcov
# y - pocet riadkov
def h_manhattan_distance(state, x, y):
    h = 0
    for i in state.arr:
        i1 = state.arr.index(i)
        i2 = state.final.index(i)
        h += abs(i1 % x - i2 % x) + abs(i1 // y - i2 // y)
    return h


# Heuristika: ziadna (prehladavanie do sirky)
# state - stav pre ktory sa ma vypocitat heuristika
# x - pocet stlpcov
# y - pocet riadkov
def h_none(state, x, y):
    return 0


class State:
    # final - cielovy stav
    # arr - sucasny stav
    # parent - odkaz na rodica
    # op - operator ktorym sme sa dostali do stavu
    # x - pocet stlpcov
    # y - pocet riadkov
    def __init__(self, final, arr, parent=None, op=None, x=3, y=3):
        self.final = final
        self.arr = arr
        self.parent = parent
        self.is_final = self.arr == self.final
        self.op = op
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.arr == other.arr

    def __hash__(self):
        return hash(tuple(self.arr))

    def expand(self):
        children = []

        empty = self.arr.index(0)
        x = empty % self.x
        y = empty // self.x

        # HORE
        if y < self.y - 1:
            arr = list(self.arr)
            arr[empty] = arr[empty + self.x]
            arr[empty + self.x] = 0
            children.append(State(self.final, arr, self, 'HORE', self.x, self.y))

        # DOLE
        if y > 0:
            arr = list(self.arr)
            arr[empty] = arr[empty - self.x]
            arr[empty - self.x] = 0
            children.append(State(self.final, arr, self, 'DOLE', self.x, self.y))

        # VLAVO
        if x < self.x - 1:
            arr = list(self.arr)
            arr[empty] = arr[empty + 1]
            arr[empty + 1] = 0
            children.append(State(self.final, arr, self, 'VLAVO', self.x, self.y))

        # VPRAVO
        if x > 0:
            arr = list(self.arr)
            arr[empty] = arr[empty - 1]
            arr[empty - 1] = 0
            children.append(State(self.final, arr, self, 'VPRAVO', self.x, self.y))

        return children


class PriorityQueue:
    def __init__(self):
        self.queue = []
        self.entries = {}
        self.counter = itertools.count()

    def __str__(self):
        return str(self.queue)

    def __bool__(self):
        return bool(self.entries)

    def __contains__(self, item):
        return item in self.entries

    def __len__(self):
        return len(self.queue)

    def add(self, item, priority):
        if item in self.entries:
            self.remove(item)
        count = next(self.counter)
        entry = [priority, count, item]
        self.entries[item] = entry
        heapq.heappush(self.queue, entry)

    def remove(self, item):
        entry = self.entries.pop(item)
        entry[-1] = None

    def pop(self):
        while self.queue:
            priority, count, item = heapq.heappop(self.queue)
            if item is not None:
                del self.entries[item]
                return item
        raise KeyError


# s - pociatocny stav
# e - koncovy stav
# x - pocet stlpcov
# y - pocet riadkov
# h - heuristika
def solve(arr_start, arr_end, x, y, h):
    print('-' * 80)
    print('Heuristika: ' + h.__name__)
    print('-' * 80)

    start = State(arr_end, arr_start, x=x, y=y)

    queue = PriorityQueue()
    closed = set()

    queue.add(start, h(start, x, y))

    t1 = float(time.time())

    while queue:
        s = queue.pop()

        if s.is_final:
            path = []
            while s.op:
                path.insert(0, s.op)
                s = s.parent
            print('Postupnost krokov: ' + ', '.join(path))
            print('Dlzka cesty: %d' % len(path))
            break

        for n in s.expand():
            if n not in queue and n not in closed:
                queue.add(n, h(n, x, y))

        closed.add(s)
    else:
        print('Riesenie neexistuje!')

    t2 = float(time.time())

    print('Pocet nespracovanych stavov: %d' % len(queue))
    print('Pocet spracovanych stavov: %d' % len(closed))
    print('Celkovy pocet vygenerovanych stavov: %d' % (len(queue) + len(closed)))
    print('Cas: %.2f s' % (t2 - t1))


# s - pociatocny stav
# e - koncovy stav
# x - pocet stlpcov
# y - pocet riadkov
def run_test(s, e, x, y):
    run_test.n += 1
    print('=' * 80)
    print('Testovaci pripad %d:' % run_test.n)
    print('Velkost: %dx%d' % (x, y))
    print('Pociatocny stav:')
    print(s)
    print('Koncovy stav:')
    print(e)
    print('=' * 80)
    solve(s, e, x, y, h_misplaced_tiles)
    solve(s, e, x, y, h_manhattan_distance)
    solve(s, e, x, y, h_none)


run_test.n = 0


if __name__ == '__main__':
    # x - pocet riadkov
    # y - pocet stlpcov

    x, y = (3, 2)
    s = [1, 5, 2, 4, 0, 3]
    e = [1, 2, 3, 4, 5, 0]
    run_test(s, e, x, y)

    x, y = (3, 3)
    s = [2, 4, 3, 1, 5, 0, 7, 8, 6]
    e = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    run_test(s, e, x, y)

    x, y = (3, 4)
    s = [4, 1, 2, 5, 8, 3, 10, 0, 6, 11, 7, 9]
    e = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 0]
    run_test(s, e, x, y)

    x, y = (3, 3)
    s = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    e = [8, 0, 6, 5, 4, 7, 2, 3, 1]
    run_test(s, e, x, y)
