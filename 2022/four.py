import structlog

from utils import read_file

log = structlog.get_logger()


def contains(first, second):
    if (
        int(first.split("-")[0]) <= int(second.split("-")[0])
        and int(first.split("-")[1]) >= int(second.split("-")[1])
    ) or (
        int(first.split("-")[0]) >= int(second.split("-")[0])
        and int(first.split("-")[1]) <= int(second.split("-")[1])
    ):
        return True


def overlaps(first, second):
    if (
        int(first.split("-")[0])
        <= int(second.split("-")[0])
        <= int(first.split("-")[1])
    ) or (
        int(second.split("-")[0])
        <= int(first.split("-")[0])
        <= int(second.split("-")[1])
    ):
        return True


def part_one(pairs):
    score = 0
    for pair in pairs:
        pair.strip()
        contain = contains(pair.split(",")[0], pair.split(",")[1])
        if contain:
            score += 1

    log.info("fully_contains", value=score)


def part_two(pairs):
    score = 0
    for pair in pairs:
        pair.strip()
        overlap = overlaps(pair.split(",")[0], pair.split(",")[1])
        if overlap:
            score += 1

    log.info("overlaps", value=score)


def main():
    pairs = read_file("input_04.txt")
    part_one(pairs)
    part_two(pairs)


if __name__ == "__main__":
    main()
