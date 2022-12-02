import structlog

logger = structlog.get_logger()


"""
Rules:
    A: rock
    B: paper
    C: scissors

A < B < C < A...

My side:
    X: rock
    Y: paper
    Z: scissors
"""


def read_file(name):
    with open(name, "r") as file:
        lines = file.readlines()
    return lines


class Turn:
    def __init__(self, line: str):
        self.opponent = line.split(" ")[0]
        self.myself = line.split(" ")[1].strip()

    def fight(self):
        if self.myself == "Y":
            return 3
        elif self.myself == "Z":
            return 6
        else:
            return 0

    def score(self):
        fight_score = self.fight()
        self_score = 0
        if self.opponent == "A":
            if fight_score == 3:
                self_score = 1
            elif fight_score == 0:
                self_score = 3
            else:
                self_score = 2
        elif self.opponent == "B":
            if fight_score == 3:
                self_score = 2
            elif fight_score == 6:
                self_score = 3
            else:
                self_score = 1
        else:
            if fight_score == 3:
                self_score = 3
            elif fight_score == 6:
                self_score = 1
            else:
                self_score = 2
        return fight_score + self_score


def create_turns():
    lines = read_file("./input.txt")
    turns = []
    for line in lines:
        turns.append(Turn(line))

    return turns


def main():
    turns = create_turns()
    total_score = 0
    for turn in turns:
        total_score += turn.score()
    logger.info("total_score", value=total_score)


if __name__ == "__main__":
    main()
