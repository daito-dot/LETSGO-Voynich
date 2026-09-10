from __future__ import annotations

import math


class Fenwick:
    def __init__(self, values):
        self.n = len(values)
        self.bit = [0] * (self.n + 1)
        for i, value in enumerate(values):
            self.add(i, value)

    def add(self, i, delta):
        i += 1
        while i <= self.n:
            self.bit[i] += delta
            i += i & -i

    def prefix(self, i):
        if i < 0:
            return 0
        total = 0
        i += 1
        while i:
            total += self.bit[i]
            i -= i & -i
        return total

    def kth(self, k):
        total = self.prefix(self.n - 1)
        if k < 0 or k >= total:
            raise ValueError("k out of range")
        idx = 0
        bitmask = 1 << (self.n.bit_length() - 1)
        while bitmask:
            nxt = idx + bitmask
            if nxt <= self.n and self.bit[nxt] <= k:
                idx = nxt
                k -= self.bit[nxt]
            bitmask >>= 1
        return idx


def type_class_size(counts):
    total = 0
    size = 1
    for count in counts:
        if count < 0:
            raise ValueError("negative count")
        if count:
            size *= math.comb(total + count, count)
            total += count
    return size


def unrank_multiset(counts, rank):
    counts = list(map(int, counts))
    remaining = sum(counts)
    size = type_class_size(counts)
    if rank < 0 or rank >= size:
        raise ValueError("rank out of range")
    tree = Fenwick(counts)
    out = []
    r = int(rank)
    while remaining:
        occurrence = (r * remaining) // size
        symbol = tree.kth(occurrence)
        before = tree.prefix(symbol - 1)
        count = counts[symbol]
        r -= (size * before) // remaining
        size = (size * count) // remaining
        counts[symbol] -= 1
        tree.add(symbol, -1)
        remaining -= 1
        out.append(symbol)
    if r != 0 or size != 1:
        raise AssertionError((r, size))
    return out


def rank_multiset(counts, sequence):
    counts = list(map(int, counts))
    remaining = sum(counts)
    size = type_class_size(counts)
    rank = 0
    tree = Fenwick(counts)
    if len(sequence) != remaining:
        raise ValueError("sequence length mismatch")
    for symbol in sequence:
        if symbol < 0 or symbol >= len(counts) or counts[symbol] <= 0:
            raise ValueError("sequence violates composition")
        before = tree.prefix(symbol - 1)
        count = counts[symbol]
        rank += (size * before) // remaining
        size = (size * count) // remaining
        counts[symbol] -= 1
        tree.add(symbol, -1)
        remaining -= 1
    if size != 1:
        raise AssertionError(size)
    return rank


def payload_bits(counts):
    size = type_class_size(counts)
    bits = size.bit_length() - 1
    return size, bits, 1 << bits


def spread_rank(value, size, bits):
    used = 1 << bits
    if value < 0 or value >= used:
        raise ValueError("payload integer out of range")
    return ((2 * value + 1) * size) // (2 * used)


def inverse_spread_rank(rank, size, bits):
    used = 1 << bits
    if rank < 0 or rank >= size:
        raise ValueError("rank out of range")
    value = ((2 * rank + 1) * used) // (2 * size)
    if value < 0 or value >= used or spread_rank(value, size, bits) != rank:
        raise ValueError("rank is not in the CCDM code image")
    return value


def encode_integer(counts, value):
    size, bits, _ = payload_bits(counts)
    return unrank_multiset(counts, spread_rank(value, size, bits))


def decode_integer(counts, sequence):
    size, bits, _ = payload_bits(counts)
    rank = rank_multiset(counts, sequence)
    return inverse_spread_rank(rank, size, bits)


def self_test():
    cases = ([1], [1, 1], [2, 1], [2, 2], [3, 2, 1], [2, 2, 2], [4, 1, 1], [3, 3, 2])
    for counts in cases:
        size, bits, used = payload_bits(counts)
        seen = set()
        for value in range(used):
            rank = spread_rank(value, size, bits)
            assert rank not in seen
            seen.add(rank)
            sequence = encode_integer(counts, value)
            assert rank_multiset(counts, sequence) == rank
            assert decode_integer(counts, sequence) == value
        for rank in range(size):
            sequence = unrank_multiset(counts, rank)
            assert rank_multiset(counts, sequence) == rank
    return True


if __name__ == "__main__":
    assert self_test()
    print("CCDM_SELF_TEST_OK")
