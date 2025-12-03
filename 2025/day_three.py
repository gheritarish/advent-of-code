import structlog

from utils import read_file

logger = structlog.get_logger()


def get_largest_joltage(line: str, joltage_len: int = 2) -> int:
    max_joltage = int(line[:joltage_len])
    for i in range(len(line) - joltage_len + 1):
        if int(line[i]) > max_joltage // (10 ** (joltage_len - 1)):
            max_joltage = int(line[i : i + joltage_len])

        for j in range(1, joltage_len):
            if int(line[i + j]) > int(str(max_joltage)[j]):
                max_joltage = (max_joltage // 10**(joltage_len - j)) * 10**(joltage_len - j) + int(
                    line[i + j : i + joltage_len]
                )

        if max_joltage == int("9" * joltage_len):
            return max_joltage
    return max_joltage


def solve_one(lines: list[str]) -> int:
    result = 0
    for line in lines:
        print(get_largest_joltage(line.strip()))
        result += get_largest_joltage(line.strip())
    return result


def solve_two(lines: list[str]) -> int:
    result = 0
    for line in lines:
        print(get_largest_joltage(line.strip(), joltage_len=12))
        result += get_largest_joltage(line.strip(), joltage_len=12)
    return result


def main():
    lines = read_file("input_3.txt")
    part_one = solve_one(lines)
    logger.info("Part one", result=part_one)

    part_two = solve_two(lines)
    logger.info("Part two", result=part_two)


if __name__ == "__main__":
    main()
