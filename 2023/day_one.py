from utils import read_file

import structlog
import re

log = structlog.get_logger()


transform_string = {
    "one": 1,
    "1": 1,
    "two": 2,
    "2": 2,
    "three": 3,
    "3": 3,
    "four": 4,
    "4": 4,
    "five": 5,
    "5": 5,
    "six": 6,
    "6": 6,
    "seven": 7,
    "7": 7,
    "eight": 8,
    "8": 8,
    "nine": 9,
    "9": 9,
}


def get_number(line: str, order_regex, revert_regex) -> int:
    first_number = re.search(order_regex, line).group()
    last_number = re.search(revert_regex, line[::-1]).group()
    number = int(transform_string[first_number]) * 10 + int(transform_string[last_number[::-1]])
    return number


def get_file_numbers(lines: list[str], order_regex, revert_regex) -> list[int]:
    return [get_number(line, order_regex, revert_regex) for line in lines]


def main():
    lines = read_file("input_one.txt")
    FIRST_REGEX = r"[0-9]"
    first_question = sum(get_file_numbers(lines, FIRST_REGEX, FIRST_REGEX))
    log.info("first_question", first_answer=first_question)
    SECOND_REGEX = r"([0-9]|one|two|three|four|five|six|seven|eight|nine)"
    SECOND_REGEX_REVERSE = "([0-9]|eno|owt|eerht|ruof|evif|xis|neves|thgie|enin)"
    second_answer = sum(get_file_numbers(lines, SECOND_REGEX, SECOND_REGEX_REVERSE))
    log.info("second_question", second_answer=second_answer)


if __name__ == "__main__":
    main()
