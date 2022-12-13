from collections.abc import Iterable

import structlog

log = structlog.get_logger()


class Signal:
    def __init__(self, first, second):
        if any(char not in "\n0123456789,[]" for char in first):
            raise AssertionError()
        self.first = eval(first, {"__builtins__": {}}, {})
        if any(char not in "\n0123456789,[]" for char in second):
            raise AssertionError()
        self.second = eval(second, {"__builtins__": {}}, {})


def compare(first, second):
    if not isinstance(first, Iterable) and not isinstance(
        second,
        Iterable,
    ):
        return 0 if first == second else -1 if first < second else 1
    try:
        first = iter(first)
    except TypeError:
        first = iter((first,))
    try:
        second = iter(second)
    except TypeError:
        second = iter((second,))
    while True:
        try:
            left = next(first)
        except StopIteration:
            try:
                next(second)
                return -1
            except StopIteration:
                return 0
        try:
            right = next(second)
        except StopIteration:
            return 1
        comparison = compare(left, right)
        if comparison:
            return comparison


def parse(file_name: str):
    with open(file_name, "r") as file:
        pairs = file.read().split("\n\n")

    signals = []
    for pair in pairs:
        signals.append(Signal(pair.split("\n")[0], pair.split("\n")[1]))
    return signals


def solve_one(signals):
    total = 0
    for idx, signal in enumerate(signals):
        if compare(signal.first, signal.second) <= 0:
            total += idx + 1
    return total


def solve_two(signals):
    divider1, divider2 = [[2], [6]]
    count1, count2 = 1, 1
    for signal in signals:
        if compare(signal.first, divider1) < 0:
            count1 += 1
        elif compare(signal.first, divider2) < 0:
            count2 += 1

        if compare(signal.second, divider1) < 0:
            count1 += 1
        elif compare(signal.second, divider2) < 0:
            count2 += 1
    return count1 * (count1 + count2)


def main():
    signals = parse("input_13.txt")
    result = solve_one(signals)
    log.info("part_one", result=result)
    result = solve_two(signals)
    log.info("part_two", result=result)


if __name__ == "__main__":
    main()
