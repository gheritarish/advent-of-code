from utils import read_file

import structlog

logger = structlog.get_logger()


class Value:
    def __init__(self, history: list[int]):
        self.history = history

    def get_next_value(self) -> int:
        differences = []
        differences.append(
            [self.history[i] - self.history[i - 1] for i in range(1, len(self.history))]
        )
        while set(differences[-1]) != {0}:
            differences.append(
                [
                    differences[-1][i] - differences[-1][i - 1]
                    for i in range(1, len(differences[-1]))
                ]
            )

        k = len(differences) - 2
        while k >= 0:
            differences[k].append(differences[k][-1] + differences[k+1][-1])
            k -= 1
        return self.history[-1] + differences[0][-1]

    def get_prev_value(self) -> int:
        differences = []
        last = [0]
        last.extend(
            [self.history[i] - self.history[i - 1] for i in range(1, len(self.history))]
        )
        differences.append(last)
        while set(differences[-1]) != {0}:
            new = [0]
            new.extend(
                [
                    differences[-1][i] - differences[-1][i - 1]
                    for i in range(2, len(differences[-1]))
                ]
            )
            differences.append(new)

        k = len(differences) - 2
        while k >= 0:
            differences[k][0] = differences[k][1] - differences[k+1][0]
            k -= 1
        return self.history[0] - differences[0][0]



def parse_values(lines: list[str]) -> list[Value]:
    values = []
    for line in lines:
        line = line.strip()
        history = [int(value) for value in line.split(" ")]
        values.append(Value(history))

    return values


def main():
    lines = read_file("input_nine.txt")
    values = parse_values(lines)
    first_answer = sum([value.get_next_value() for value in values])
    logger.info("first_question", answer=first_answer)
    second_answer = sum([value.get_prev_value() for value in values])
    logger.info("second_question", answer=second_answer)


if __name__ == "__main__":
    main()
