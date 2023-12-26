from io import TextIOBase


def get_values_from_input_data(input_data: TextIOBase) -> list[str]:
    return input_data.read().strip().split(",")
