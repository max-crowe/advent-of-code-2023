ENGLISH_DIGITS = {k: str(i) for i, k in enumerate([
    "zero",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
])}


class NoDigitsInStringError(ValueError):
    pass


def handle(val: str) -> int:
    digits = [char for char in val if char.isdigit()]
    try:
        return int(f"{digits[0]}{digits[-1]}")
    except IndexError:
        raise NoDigitsInStringError


def handle_with_replacement(val: str) -> int:
    forward_digits = [char for char in replace_named_digits(val) if char.isdigit()]
    reverse_digits = [char for char in replace_named_digits(val, True) if char.isdigit()]
    try:
        return int(f"{forward_digits[0]}{reverse_digits[-1]}")
    except IndexError:
        raise NoDigitsInStringError


def do_replacement_if_digit_found(val: str, idx: int) -> tuple[str, bool]:
    for digit_name, digit in ENGLISH_DIGITS.items():
        if val[idx:].startswith(digit_name):
            return val[0:idx] + digit + val[idx+len(digit_name):], True
    return val, False


def replace_named_digits(val: str, reverse: bool = False) -> str:
    if reverse:
        idx = len(val) - 1
        while idx >= 0:
            val, replacement_done = do_replacement_if_digit_found(val, idx)
            if replacement_done:
                break
            idx -= 1
    else:
        idx = 0
        while idx < len(val):
            val, replacement_done = do_replacement_if_digit_found(val, idx)
            if replacement_done:
                break
            idx += 1
    return val
