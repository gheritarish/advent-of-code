import operator
from functools import reduce

import structlog

from utils import read_file

logger = structlog.get_logger()


class Operation:
    def __init__(self):
        self.elements = []
        self.operator = ""

    def add_element(self, element):
        self.elements.append(element)

    def change_operator(self, operator):
        self.operator = operator

    def solve(self):
        if self.operator == "*":

            return reduce(operator.mul, self.elements, 1)
        elif self.operator == "+":
            return sum(self.elements)

    def __str__(self):
        return f" {self.operator} ".join([f"{element}" for element in self.elements])


def parse_lines(lines: list[str]) -> list[Operation]:
    operations = [Operation() for _ in range(len(lines[0].strip().split()))]

    for line in lines:
        line = line.strip()
        for i, element in enumerate(line.split()):
            if element in ["+", "*"]:
                operations[i].change_operator(element)
            else:
                operations[i].add_element(int(element))
    return operations


def parse_lines_new(lines: list[str]) -> list[Operation]:
    lines = [line[:-1] for line in lines]
    operations = [Operation() for _ in range(len(lines[0].strip().split()))]

    max_spaces = len(lines)

    k = 0
    for i in range(len(lines[0])):
        number_spaces = 0
        element = []
        for j in range(max_spaces):
            if lines[j][i] in ["+", "*"]:
                operations[k].change_operator(lines[j][i])
            elif lines[j][i] != " ":
                element.append(lines[j][i])
            else:
                number_spaces += 1

        if len(element) > 0:
            operations[k].add_element(int("".join(char for char in element)))
        if number_spaces == max_spaces:
            k += 1
    return operations


def compute_all(operations: list[Operation]) -> int:
    result = 0
    for operation in operations:
        result += operation.solve()
    return result


def main():
    lines = read_file("input_6.txt")
    operations = parse_lines(lines)

    part_one = compute_all(operations)
    logger.info("First part", result=part_one)

    new_operations = parse_lines_new(lines)

    part_two = compute_all(new_operations)
    logger.info("Second part", result=part_two)


if __name__ == "__main__":
    main()
