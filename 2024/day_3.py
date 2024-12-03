import functools
import re

import structlog

from utils import read_file

logger = structlog.get_logger()


def get_operations(lines):
    operations = []
    for line in lines:
        operations.append(re.findall(r"(mul\(\d{1,3},\d{1,3}\)|do\(\)|don't\(\))", line))
    return operations


@functools.lru_cache
def get_multiplication_numbers(multiplication: str) -> tuple[int, int]:
    first_number = int(multiplication.split("mul(")[1].split(",")[0])
    second_number = int(multiplication.split(",")[1].split(")")[0])
    return first_number, second_number


def solve_first(operations: list[list[str]]) -> int:
    answer = 0
    for operation_line in operations:
        for operation in operation_line:
            if operation[0] != "d":
                first_number, second_number = get_multiplication_numbers(operation)
                answer += first_number * second_number
    return answer


def solve_second(operations: list[list[str]]) -> int:
    enabled = True
    answer = 0
    for operation_line in operations:
        for operation in operation_line:
            if operation == "don't()":
                enabled = False
            elif operation == "do()":
                enabled = True
            else:
                if enabled:
                    first_number, second_number = get_multiplication_numbers(operation)
                    answer += first_number * second_number
    return answer



def main():
    lines = read_file("input_3.txt")
    operations = get_operations(lines)
    first = solve_first(operations)
    logger.info("First part", first=first)

    second = solve_second(operations)
    logger.info("Second part", second=second)


if __name__ == "__main__":
    main()
