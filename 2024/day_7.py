import structlog

from utils import read_file

logger = structlog.get_logger()


def concatenation(x, y):
    return int(str(x) + str(y))


class Operation:
    def __init__(self, total, operations):
        self.total = total
        self.operations = operations

    def is_possible(self):
        values = [self.operations[0]]
        remaining = self.operations[1:]
        while len(remaining) > 0:
            value = remaining[0]
            remaining = remaining[1:]
            old_values = values
            values = [old_value + value for old_value in old_values]
            values.extend([old_value * value for old_value in old_values])

        if self.total in values:
            return True

        return False

    def is_really_possible(self):
        values = [self.operations[0]]
        remaining = self.operations[1:]
        while len(remaining) > 0:
            value = remaining[0]
            remaining = remaining[1:]
            old_values = values

            values = [old_value + value for old_value in old_values]
            values.extend([old_value * value for old_value in old_values])
            values.extend([concatenation(old_value, value) for old_value in old_values])

            values = list(set([value for value in values if value <= self.total]))

        if self.total in values:
            return True

        return False


def parse_inputs(lines) -> list[Operation]:
    instructions = []
    for line in lines:
        total = int(line.split(":")[0])
        raw_operations = line.split(":")[1]
        operations = [int(value) for value in raw_operations.strip().split(" ")]
        instructions.append(Operation(total=total, operations=operations))
    return instructions


def solve_first(instructions: list[Operation]) -> int:
    return sum(operation.total for operation in instructions if operation.is_possible())


def solve_second(instructions: list[Operation]) -> int:
    return sum([operation.total for operation in instructions if operation.is_really_possible()])


def main():
    lines = read_file("input_7.txt")
    instructions = parse_inputs(lines)

    first = solve_first(instructions)
    logger.info("First part", first=first)

    originally_impossible_operations = [
        instruction for instruction in instructions if not instruction.is_possible()
    ]
    partial_second = solve_second(originally_impossible_operations)
    second = first + partial_second
    # 162042343638683
    logger.info("Second part", second=second)


if __name__ == "__main__":
    main()
