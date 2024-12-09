import structlog

from utils import read_file

logger = structlog.get_logger()


class Block:
    def __init__(self, content: str, file_id: int | None = None):
        self.content = content
        self.file_id = file_id

    def __str__(self):
        if self.content == ".":
            return self.content
        return f"{self.file_id}"


def parse_input(lines: list[str]) -> list[Block]:
    line = lines[0].strip()
    blocks = []
    for index in range(0, len(line), 2):
        len_file = int(line[index])
        try:
            len_void = int(line[index + 1])
        except IndexError:
            len_void = 0
        blocks.extend([Block(line[index], file_id=index // 2) for _ in range(len_file)])
        blocks.extend([Block(".") for _ in range(len_void)])

    return blocks


def get_last_non_empty_block(blocks: list[Block]):
    for index, block in enumerate(blocks[::-1]):
        if block.content != ".":
            return index
    return 0

def reorder(blocks: list[Block]) -> list[Block]:
    reordered_blocks = blocks
    for index in range(len(blocks)):
        if reordered_blocks[index].content == ".":
            empty_block = reordered_blocks[index]
            last_non_empty_block_index = get_last_non_empty_block(reordered_blocks)
            if index > len(reordered_blocks) - last_non_empty_block_index - 1:
                break
            reordered_blocks[index] = reordered_blocks[len(reordered_blocks) - last_non_empty_block_index - 1]
            reordered_blocks[len(reordered_blocks) - last_non_empty_block_index - 1] = empty_block
    return reordered_blocks


def get_len_file(reordered_blocks, file_id, index):
    len_file = 0
    index = index
    while reordered_blocks[index].file_id == file_id:
        len_file += 1
        index -= 1
    return len_file


def get_first_fitting_id(reordered_blocks, len_file):
    index = 0
    found = False
    while not found:
        jdx = 0
        while jdx < len_file:
            if index + jdx >= len(reordered_blocks):
                return len(reordered_blocks)
            if reordered_blocks[index + jdx].content != ".":
                index += jdx + 1
                jdx = 0
            else:
                jdx += 1
                if jdx == len_file:
                    return index
    return index + 1


def move(reordered_blocks, index, len_file, first_fitting_id):
    empty_blocks = [reordered_blocks[i] for i in range(first_fitting_id, first_fitting_id + len_file)]
    blocks = [reordered_blocks[i] for i in range(index, index - len_file, -1)]
    for i in range(len_file):
        reordered_blocks[first_fitting_id + i] = blocks[i]
        reordered_blocks[index - i] = empty_blocks[i]
    return reordered_blocks


def intelligent_reorder(blocks: list[Block]) -> list[Block]:
    reordered_blocks = blocks
    index = len(blocks) - 1
    while index > 0:
        if reordered_blocks[index].content == ".":
            index -= 1
        else:
            len_file = get_len_file(reordered_blocks, reordered_blocks[index].file_id, index)
            first_fitting_id = get_first_fitting_id(reordered_blocks, len_file)
            if first_fitting_id > index:
                index -= len_file
            else:
                reordered_blocks = move(reordered_blocks, index, len_file, first_fitting_id)
                index -= len_file
    return reordered_blocks

def checksum(ordered_blocks: list[Block]):
    checksum = 0
    index = 0
    while index < len(ordered_blocks):
        if ordered_blocks[index].content != ".":
            checksum += ordered_blocks[index].file_id * index
            index += 1
        else:
            index += 1
    return checksum


def solve_first(blocks: list[Block]):
    ordered_blocks = reorder(blocks)
    return checksum(ordered_blocks)


def solve_second(blocks: list[Block]):
    ordered_blocks = intelligent_reorder(blocks)
    return checksum(ordered_blocks)


def main():
    lines = read_file("input_9.txt")
    blocks = parse_input(lines)

    # first = solve_first(blocks)
    # logger.info("First part", first=first)

    second = solve_second(blocks)
    logger.info("Second part", second=second)


if __name__ == "__main__":
    main()
