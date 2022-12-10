import structlog

from utils import read_file

log = structlog.get_logger()


def get_command(line):
    line = line.strip()
    first = line.split(" ")[0]
    if first == "noop":
        second = 0
    else:
        second = int(line.split(" ")[1])
    return first, second


def solve_one(lines):
    register = [1]
    for line in lines:
        first, second = get_command(line)
        if first == "noop":
            register.append(register[-1])
        else:
            register.append(register[-1])
            register.append(register[-1] + second)
    return sum(register[19 + 40 * x] * (20 + 40 * x) for x in range(6))


def solve_two(lines):
    pixels = [["." for _ in range(40)] for _ in range(6)]
    sprite = 1
    passing = 0
    index = 0
    to_add = 0
    for x in range(6):
        for i in range(40):
            if abs(i - sprite) < 2:
                pixels[x][i] = "#"
            else:
                pixels[x][i] = "."

            if passing == 0:
                first, second = get_command(lines[index])
                index += 1
                if first == "addx":
                    passing = 1
                    to_add = second
            else:
                passing -= 1
                if passing == 0:
                    sprite += to_add
    return pixels


def main():
    lines = read_file("input_10.txt")
    result = solve_one(lines)
    log.info("part_one", result=result)
    pixels = solve_two(lines)
    for pixel_line in pixels:
        print(pixel_line)


if __name__ == "__main__":
    main()
