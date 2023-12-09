from collections.abc import Generator
from io import TextIOBase


def iter_sequences_from_input(input_data: TextIOBase) -> Generator[list[int]]:
    for line in input_data:
        yield [int(item) for item in line.strip().split(" ")]
