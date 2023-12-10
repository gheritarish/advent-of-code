import structlog

from utils import read_file
from day_three import Position

logger = structlog.get_logger()


POSSIBLE_PIPES = {
    "|": {
        (0, -1): (0, -1),
        (0, 1): (0, +1),
    },
    "-": {
        (-1, 0): (-1, 0),
        (1, 0): (1, 0),
    },
    "L": {
        (0, 1): (1, 0),
        (-1, 0): (0, -1),
    },
    "J": {
        (0, 1): (-1, 0),
        (1, 0): (0, -1),
    },
    "7": {
        (0, -1): (-1, 0),
        (1, 0): (0, 1),
    },
    "F": {
        (0, -1): (1, 0),
        (-1, 0): (0, 1),
    },
}


class Pipe:
    def __init__(self, character: str, position: Position):
        self.character = character
        self.position = position

    def get_next_pipe(self, previous, lines: list[str]):
        # x, y = self.position.x, self.position.y
        last_move = (
            (self.position.x - previous.position.x),
            (self.position.y - previous.position.y),
        )
        move_x, move_y = POSSIBLE_PIPES[self.character][last_move]
        next_x, next_y = self.position.x + move_x, self.position.y + move_y
        next = lines[next_y][next_x]
        return Pipe(character=next, position=Position(x=next_x, y=next_y))

    def get_from_start(self, lines: list[str]):
        x, y = self.position.x, self.position.y

        for i in [-1, 0, 1]:
            if x + i < 0:
                continue
            else:
                for j in [-1, 0, 1]:
                    if y + j < 0:
                        continue
                    else:
                        char = lines[y + j][x + i]
                        try:
                            possible_moves = POSSIBLE_PIPES[char]
                        except KeyError:
                            continue
                        for move_x, move_y in possible_moves.values():
                            if x == x + i + move_x and y == y + j + move_y:
                                return Pipe(
                                    character=char,
                                    position=Position(x=x + i, y=y + j),
                                )
                            else:
                                continue


def get_start(lines: list[str], pipe_loop: list[Position]) -> list[Pipe]:
    for i in range(len(lines)):
        if "S" not in lines[i]:
            continue
        else:
            for j in range(len(lines[i])):
                if lines[i][j] == "S":
                    pipe_loop.append(Pipe(character="S", position=Position(x=j, y=i)))
                    return pipe_loop
    return pipe_loop


def get_full_loop(lines: list[str], pipe_loop: list[Pipe]) -> list[Pipe]:
    pipe_loop.append(pipe_loop[0].get_from_start(lines=lines))
    while pipe_loop[-1].character != "S":
        pipe_loop.append(pipe_loop[-1].get_next_pipe(pipe_loop[-2], lines))
    return pipe_loop


def get_cleaned_loop(lines: list[str], pipe_loop: list[Pipe]) -> list[list[str]]:
    result = []
    positions = [(pipe.position.x, pipe.position.y) for pipe in pipe_loop]
    for i in range(len(lines)):
        cleaned_line = ""
        for j in range(len(lines[i])):
            if (j, i) not in positions:
                cleaned_line += " "
            else:
                cleaned_line += lines[i][j]
        result.append(cleaned_line)
    return result


def get_inside_points(lines: list[str], pipe_loop: list[Pipe]) -> list[Position]:
    inside_points = []
    positions = [(pipe.position.x, pipe.position.y) for pipe in pipe_loop]
    for i in range(len(lines)):
        crossings = 0
        for j in range(len(lines[i])):
            if (j, i) in positions:
                match lines[i][j]:
                    case "|":
                        crossings += 1
                    case "L":
                        crossings += 1
                    case "J":
                        crossings += 1
            else:
                if crossings % 2 == 1 and lines[i][j] != "\n":
                    inside_points.append(Position(x=j, y=i))
    return inside_points


def main():
    lines = read_file("input_ten.txt")
    pipe_loop = []
    pipe_loop = get_start(lines, pipe_loop)
    pipe_loop = get_full_loop(lines, pipe_loop)
    first_answer = len(pipe_loop) // 2
    logger.info("first_question", answer=first_answer)

    inside_points = get_inside_points(lines, pipe_loop)
    logger.info("second_question", answer=len(inside_points))


if __name__ == "__main__":
    main()
