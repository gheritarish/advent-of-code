import structlog

from utils import read_file

logger = structlog.get_logger()


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Number:
    def __init__(self, value: int, position: Position):
        self.value = value
        self.position = position

    def is_in_engine(self, grid):
        x_coord = self.position.x
        y_coord = self.position.y
        if y_coord > 0:
            for x in range(x_coord - 1, x_coord + len(str(self.value)) + 1):
                if x < 0:
                    continue
                try:
                    elt = grid[y_coord - 1][x]
                except IndexError:
                    continue
                else:
                    if elt not in "1234567890.\n":
                        return True
        if y_coord < len(grid) - 1:
            for x in range(x_coord - 1, x_coord + len(str(self.value)) + 1):
                if x < 0:
                    continue
                try:
                    elt = grid[y_coord + 1][x]
                except IndexError:
                    continue
                else:
                    if elt not in "1234567890.\n":
                        return True

        if x_coord > 0:
            if grid[y_coord][x_coord - 1] not in "1234567890.\n":
                return True
        if x_coord + len(str(self.value)) < len(grid[y_coord]) - 1:
            if grid[y_coord][x_coord + len(str(self.value))] not in "1234567890.\n":
                return True

        return False


class Gear:
    def __init__(self, position: Position):
        self.position = position


    def get_adjacent_numbers(self, numbers: list[Number]) -> list[Number]:
        adjacent_numbers = []
        for number in numbers:
            if number.position.y < self.position.y - 1 or number.position.y > self.position.y + 1:
                continue

            for i in range(number.position.x, number.position.x + len(str(number.value))):
                if self.position.x == i or self.position.x - 1 == i or self.position.x + 1 == i:
                    adjacent_numbers.append(number)
                    break

        return adjacent_numbers




def get_numbers(lines: list[str]) -> list[Number]:
    numbers = []
    for i in range(len(lines)):
        j = 0
        while j < len(lines[i]):
            try:
                value = int(lines[i][j])
            except ValueError:
                j += 1
            else:
                k = 1
                while j+k < len(lines[i]):
                    try:
                        value = int(lines[i][j:j+k])
                    except ValueError:
                        break
                    else:
                        k += 1
                number = Number(value=int(value), position=Position(x=j, y=i))
                numbers.append(number)
                j += k
    return numbers


def get_gears(lines: list[str]) -> list[Gear]:
    gears = []
    for i in range(len(lines)):
        for j in range(len(lines[i])):
            if lines[i][j] == "*":
                gear = Gear(position=Position(x=j, y=i))
                gears.append(gear)
    return gears


def main():
    lines = read_file("input_three.txt")
    numbers = get_numbers(lines)
    first_answer = sum([number.value for number in numbers if number.is_in_engine(lines)])
    logger.info("first_question", answer=first_answer)

    gears = get_gears(lines)
    gear_adjacent_numbers = [gear.get_adjacent_numbers(numbers) for gear in gears]
    second_answer = 0
    for gear_adjacency in gear_adjacent_numbers:
        if len(gear_adjacency) == 2:
            second_answer += gear_adjacency[0].value * gear_adjacency[1].value
    logger.info("second_question", answer=second_answer)


if __name__ == "__main__":
    main()
