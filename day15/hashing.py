def get_hash(data: str) -> int:
    value = 0
    for char in data:
        value += ord(char)
        value = (value * 17) % 256
    return value
