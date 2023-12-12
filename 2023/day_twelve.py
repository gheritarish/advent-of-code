import structlog
import functools

from utils import read_file

logger = structlog.get_logger()


class SpringLine:
    def __init__(self, map: str, counts: tuple[int]):
        self.map = map
        self.counts = counts


def get_spring_lines(lines: list[str]) -> list[SpringLine]:
    spring_lines = []
    for line in lines:
        map = line.split(" ")[0]
        str_counts = line.split(" ")[1].strip()
        counts = tuple([int(count) for count in str_counts.split(",")])
        spring_lines.append(SpringLine(map=map, counts=counts))
    return spring_lines


@functools.lru_cache()
def get_line_combination(map: str, counts: tuple[int]) -> int:
    """
    Get the number of combinations possible for a map string, by:

    1. Counting the number of combinations in map[1:] if the first character is a .
    2. If the first character is a ?, replace it by both a . and a # and add the counts
    3. If the first character is a #, if we have no counts left, there is no combinations here. If the map length is
       less than the first count, there is no combination here. If there is a . in the first "count" character, there is
       no combination here. Finally, if the number of counts is higher than 1, ensure the count + 1 character are not #
       (otherwise, there is a rule conflict), or send the next characters and next count to the function.
    4. Finally, send the characters after the count first, and the remaining counts to the function. If it's "" (,),
       return 1.
    """
    if len(map) == 0:
        return 1 if len(counts) == 0 else 0

    if map[0] == ".":
        return get_line_combination(map[1:], counts)

    if map[0] == "?":
        return get_line_combination(
            map.replace("?", ".", 1), counts
        ) + get_line_combination(map.replace("?", "#", 1), counts)

    if map[0] == "#":
        if len(counts) == 0:
            return 0
        if len(map) < counts[0]:
            return 0
        if "." in map[0 : counts[0]]:
            return 0

        if len(counts) > 1:
            if len(map) < counts[0] + 1 or map[counts[0]] == "#":
                return 0
            return get_line_combination(map[counts[0] + 1 :], counts[1:])
        else:
            return get_line_combination(map[counts[0] :], counts[1:])


def get_combination_count(spring_lines: list[SpringLine], copies: int = 1) -> int:
    combinations = 0
    for spring_line in spring_lines:
        if copies > 1:
            map = "?".join(spring_line.map for _ in range(copies))
            counts = spring_line.counts * copies
        else:
            map = spring_line.map
            counts = spring_line.counts
        combinations += get_line_combination(map, counts)
    return combinations


def main():
    lines = read_file("sample_twelve.txt")
    spring_lines = get_spring_lines(lines)
    first_answer = get_combination_count(spring_lines)
    logger.info("first_question", answer=first_answer)
    second_answer = get_combination_count(spring_lines, copies=5)
    logger.info("second_question", answer=second_answer)


if __name__ == "__main__":
    main()
