import structlog
import functools

from utils import read_file

logger = structlog.get_logger()


NUMBER_CYCLES = 1000000000


def mirror(map: list[str]) -> list[str]:
    mirrored_map = []
    for j in range(len(map[0])):
        line = ""
        for map_line in map:
            line += map_line[j]
        mirrored_map.append(line)
    return mirrored_map


class Block:
    def __init__(self, start: int, block: str):
        self.start = start
        self.block = block

    def count_sliding_rocks(self):
        return self.block.count("O")

    def get_block_load(self, column_size: int) -> int:
        block_load = 0
        for i in range(self.count_sliding_rocks()):
            block_load += column_size - self.start - i
        return block_load

    def move(self):
        moved_block = ""
        for _ in range(self.count_sliding_rocks()):
            moved_block += "O"
        for _ in range(self.count_sliding_rocks(), len(self.block)):
            moved_block += "."
        return moved_block


def get_column_blocks(column: str) -> list[Block]:
    k = 0
    blocks = []
    while k < len(column):
        i = 0
        block = ""
        while k + i < len(column) and column[k + i] != "#":
            block += column[k + i]
            i += 1
        blocks.append(Block(start=k, block=block))
        k += i + 1
    return blocks


def get_power_at_position(column: str) -> int:
    power = 0
    for k in range(len(column)):
        if column[k] == "O":
            power += len(column) - k
    return power


@functools.lru_cache()
def get_moved_column(column: str) -> str:
    moved_column = ""
    k = 0
    while k < len(column):
        if column[k] == "#":
            moved_column += "#"
            k += 1
        else:
            i = 0
            block = ""
            while k + i < len(column) and column[k + i] != "#":
                block += column[k + i]
                i += 1
            block_instance = Block(start=k, block=block)
            moved_block = block_instance.move()
            moved_column += moved_block
            k += i
    return moved_column


def get_column_load(column: str) -> int:
    column_size = len(column)
    blocks = get_column_blocks(column)
    return sum([block.get_block_load(column_size) for block in blocks])


def cycle(lines: list[str]) -> int:
    new_columns = lines
    for i in range(4):
        columns = mirror(new_columns)
        if i == 0 or i == 1:
            new_columns = [get_moved_column(column) for column in columns]
        elif i == 2 or i == 3:
            new_columns = [get_moved_column(column[::-1]) for column in columns]
            new_columns = [column[::-1] for column in new_columns]
    return new_columns


def get_part_two(lines) -> int:
    new_lines = lines
    grid_power = {}
    seen_at = {}
    for i in range(1, NUMBER_CYCLES):
        lines = cycle(new_lines)
        new_lines = lines
        if str(new_lines) in seen_at:
            cycle_length = i - seen_at[str(new_lines)]
            cycle_start = seen_at[str(new_lines)]
            break
        grid_power[i] = sum([get_power_at_position(column) for column in mirror(lines)])
        seen_at[str(new_lines)] = i

    line_value = ((NUMBER_CYCLES - cycle_start) % cycle_length) + cycle_start
    return grid_power[line_value]


def main():
    lines = read_file("input_14.txt")
    lines = [line.strip() for line in lines]
    columns = mirror(lines)
    first_answer = sum([get_column_load(column) for column in columns])
    logger.info("first_question", answer=first_answer)

    second_answer = get_part_two(lines)
    logger.info("second_question", answer=second_answer)


if __name__ == "__main__":
    main()
