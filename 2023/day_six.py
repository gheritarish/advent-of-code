from utils import read_file

import structlog

logger = structlog.get_logger()


class Race:
    def __init__(self, time: int = 0, record: int = 0):
        self.time = time
        self.record = record

    def count_winning_possibilities(self):
        middle = self.time // 2
        possibilities = 0
        speed = middle
        while speed * (self.time - speed) > self.record:
            possibilities += 1
            speed -= 1
        if self.time % 2 == 0:
            return possibilities * 2 - 1
        return possibilities * 2


def parse_races(lines: list[str], different: bool = True) -> list[Race]:
    races = []
    race_times = [elt for elt in lines[0].split("Time: ")[1].split(" ") if elt != ""]
    race_records = [
        elt for elt in lines[1].split("Distance: ")[1].split(" ") if elt != ""
    ]
    assert len(race_times) == len(race_records)
    if different:
        for index, time in enumerate(race_times):
            race = Race(time=int(time), record=int(race_records[index]))
            races.append(race)
    else:
        full_time = ""
        full_record = ""
        for time in race_times:
            full_time += time
        for record in race_records:
            full_record += record

        races = [Race(time=int(full_time), record=int(full_record))]
    return races


def product(values: list[int]) -> int:
    result = 1
    for value in values:
        result *= value
    return result


def main():
    lines = read_file("input_six.txt")
    races = parse_races(lines, different=True)
    first_answer = product([race.count_winning_possibilities() for race in races])
    logger.info("first_question", answer=first_answer)

    new_races = parse_races(lines, different=False)
    second_answer = new_races[0].count_winning_possibilities()
    logger.info("second_question", answer=second_answer)


if __name__ == "__main__":
    main()
