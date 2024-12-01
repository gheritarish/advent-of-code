import structlog

from utils import read_file

logger = structlog.get_logger()


def parse_lines(lines: list[str]) -> tuple[list[int], list[int]]:
    first_list = []
    second_list = []
    for line in lines:
        first_list.append(int(line.split(" ")[0]))
        second_list.append(int(line.split(" ")[-1]))
    return first_list, second_list


def solve_one(first_list: list[int], second_list: list[int]) -> int:
    first_list.sort()
    second_list.sort()
    return sum([abs(x - y) for (x, y) in zip(first_list, second_list)])


def solve_two(first_list: list[int], second_list: list[int]) -> int:
    second_list_as_dict = {}
    for elt in second_list:
        second_list_as_dict[elt] = second_list.count(elt)

    second_answer = 0
    for elt in first_list:
        try:
            second_answer += elt * second_list_as_dict[elt]
        except KeyError:
            continue
    return second_answer


def main():
    lines = read_file("input_1.txt")
    first_list, second_list = parse_lines(lines)
    first = solve_one(first_list, second_list)
    logger.info("First part", answer=first)

    second = solve_two(first_list, second_list)
    logger.info("Second part", answer=second)


if __name__ == "__main__":
    main()
