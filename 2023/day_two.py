import structlog
from utils import read_file

logger = structlog.get_logger()

RED_CUBES = 12
BLUE_CUBES = 14
GREEN_CUBES = 13


class Set:
    def __init__(self, blue = 0, red = 0, green = 0):
        self.blue = int(blue)
        self.red = int(red)
        self.green = int(green)


class Game:
    def __init__(self, id: int, sets: list[Set]):
        self.id = id
        self.sets = sets

    def is_possible(self, max_red, max_blue, max_green) -> bool:
        for set_instance in self.sets:
            if set_instance.green > max_green:
                return False
            elif set_instance.red > max_red:
                return False
            elif set_instance.blue > max_blue:
                return False
        return True

    def get_power(self):
        min_blue = max([set_instance.blue for set_instance in self.sets])
        min_green = max([set_instance.green for set_instance in self.sets])
        min_red = max([set_instance.red for set_instance in self.sets])
        return min_blue * min_red * min_green


def parse_file(lines: list[str]) -> list[Game]:
    games = []
    for line in lines:
        line = line.split("\n")[0]
        game = line.split(": ")[0]
        sets = line.split(": ")[1]
        game_id = int(game.split(" ")[1])
        set_instances = []
        for game_set in sets.split("; "):
            set_values = {}
            for color in game_set.split(", "):
                set_values[color.split(" ")[1]] = color.split(" ")[0]
            set_instance = Set(**set_values)
            set_instances.append(set_instance)
        games.append(Game(game_id, set_instances))

    return games



def main():
    lines =  read_file("input_two.txt")
    games = parse_file(lines)
    answer = sum([game.id for game in games if game.is_possible(max_red=RED_CUBES, max_blue=BLUE_CUBES, max_green=GREEN_CUBES)])
    logger.info("first_question", answer=answer)
    answer = sum([game.get_power() for game in games])
    logger.info("second_question", answer=answer)


if __name__ == "__main__":
    main()
