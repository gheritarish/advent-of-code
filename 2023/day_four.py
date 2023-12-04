import structlog

from utils import read_file

logger = structlog.get_logger()


def get_list_intersection(first_list: list[int], second_list: list[int]) -> list[int]:
    return [elt for elt in first_list if elt in second_list]


class Game:
    def __init__(self, game_id: int, winning_numbers: list[int], numbers: list[int]):
        self.game_id = game_id
        self.winning_numbers = winning_numbers
        self.numbers = numbers

    @property
    def count_winning_numbers(self):
        return len(get_list_intersection(self.winning_numbers, self.numbers))


def get_games_from_lines(lines: list[str]) -> list[Game]:
    games = []
    for line in lines:
        card = line.split(": ")[0]
        raw_winning_numbers = line.split(": ")[1].split(" | ")[0]
        raw_numbers = line.split(": ")[1].split(" | ")[1]
        game_id = int(card.split("Card ")[1])
        winning_numbers = [
            int(number) for number in raw_winning_numbers.split(" ") if number != ""
        ]
        numbers = [int(number) for number in raw_numbers.split(" ") if number != ""]

        game = Game(game_id=game_id, winning_numbers=winning_numbers, numbers=numbers)
        games.append(game)
    return games


def get_card_count(games: list[Game]) -> list[Game]:
    count_winning_numbers = [game.count_winning_numbers for game in games]
    card_count = [1 for _ in range(len(games))]

    for i in range(len(games)):
        for k in range(i + 1, i + count_winning_numbers[i] + 1):
            card_count[k] += card_count[i]

    return card_count


def main():
    lines = read_file("input_four.txt")
    games = get_games_from_lines(lines)
    count_winning_numbers = [game.count_winning_numbers for game in games]
    first_answer = sum(
        [2 ** (count - 1) for count in count_winning_numbers if count > 0]
    )
    logger.info("first_question", answer=first_answer)

    card_count = get_card_count(games)
    second_answer = sum(card_count)
    logger.info("second_question", answer=second_answer)


if __name__ == "__main__":
    main()
