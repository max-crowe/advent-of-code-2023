from io import TextIOBase


def get_race_stats_from_input(input_data: TextIOBase, strip_spaces: bool = False) -> list[tuple[int, int]]:
    times: list[int] = []
    distances: list[int] = []
    for line in input_data:
        label, _, raw_numbers = line.strip().partition(":")
        if strip_spaces:
            raw_numbers = raw_numbers.replace(" ", "")
        numbers = [int(number) for number in raw_numbers.split(" ") if number]
        if label == "Time":
            times.extend(numbers)
        else:
            distances.extend(numbers)
    if strip_spaces:
        assert len(times) == len(distances) == 1
    else:
        assert len(times) == len(distances)
    return [(times[i], distances[i]) for i in range(len(times))]
