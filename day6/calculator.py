from math import ceil


def get_winning_products_count(time: int, distance: int) -> int:
    winning_charge_times: list[int] = []
    midpoint = time / 2
    for i in range(1, ceil(midpoint)):
        charge_time = time - i
        distance_with_time = i * charge_time
        if distance_with_time > distance:
            winning_charge_times.append(charge_time)
        elif winning_charge_times:
            break
    count = len(winning_charge_times) * 2
    if midpoint % 1 == 0 and (time - midpoint) * midpoint > distance:
        count += 1
    return count
