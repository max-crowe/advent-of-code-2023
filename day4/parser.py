from collections.abc import Generator
from io import TextIOBase

from .card import Card


def get_numbers_from_flat_list(number_list: str) -> set[int]:
    return set(int(number) for number in number_list.split(" ") if len(number))


def get_cards_from_input(input_data: TextIOBase) -> Generator[Card]:
    for line in input_data:
        card_name, _, all_numbers = line.strip().partition(":")
        _, _, card_id = card_name.partition(" ")
        winning_numbers, _, numbers = all_numbers.strip().partition("|")
        yield Card(
            id=int(card_id),
            winning_numbers=get_numbers_from_flat_list(winning_numbers),
            numbers=get_numbers_from_flat_list(numbers)
        )
