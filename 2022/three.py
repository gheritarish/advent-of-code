import structlog

from utils import read_file

log = structlog.get_logger()


def find_double(sack):
    half = len(sack) // 2
    first_part = sack[:half]
    second_part = sack[half:]
    for item in first_part:
        if item in second_part:
            return item
        else:
            continue
    assert False  # Fail here if no error is found in a rucksack


def find_badge(sacks: list):
    common_01 = ""
    for item in sacks[0]:
        if item in sacks[1]:
            common_01 = common_01 + item
    for item in sacks[2]:
        if item in common_01:
            return item
    assert False  # Fail here if no badge is found in a group of three elves


def get_priority(letter):
    """
    ASCII conversion: A is 65, Z is 90. a is 97, z is 122.
    The idea: convert upper to ascii, if letter was small, substract 64, otherwise substract 38 (65 - x = 27)
    """
    upper_l = letter.upper()
    if upper_l == letter:
        return ord(upper_l) - 38
    return ord(upper_l) - 64


def part_one(rucksacks: list):
    priorities = 0
    for sack in rucksacks:
        sack = sack.strip()
        assert len(sack) % 2 == 0
        double = find_double(sack)
        priorities += get_priority(double)
    log.info("priority", value=priorities)


def part_two(rucksacks: list):
    priorities = 0
    assert len(rucksacks) % 3 == 0
    for i in range(0, len(rucksacks), 3):
        badge = find_badge([rucksacks[i], rucksacks[i+1], rucksacks[i+2]])
        priorities += get_priority(badge)
    log.info("priority", value=priorities)


def main():
    rucksacks = read_file("03_input.txt")
    part_one(rucksacks)
    part_two(rucksacks)


if __name__ == "__main__":
    main()
