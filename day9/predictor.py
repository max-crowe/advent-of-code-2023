from collections.abc import Generator
from functools import reduce


def reduce_sequence(seq: list[int]) -> Generator[tuple[int, int]]:
    next_seq: list[int] = []
    for i in range(1, len(seq)):
        next_seq.append(seq[i] - seq[i - 1])
    yield seq[0], seq[-1]
    if any(next_seq):
        yield from reduce_sequence(next_seq)


def extrapolate(seq: list[int], left: bool = False) -> int:
    if left:
        return reduce(
            lambda x, y: y - x,
            reversed([pair[0] for pair in reduce_sequence(seq)]),
            0
        )
    return reduce(lambda x, y: x + y, (pair[1] for pair in reduce_sequence(seq)))
