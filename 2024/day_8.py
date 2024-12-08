import structlog

from utils import read_file

logger = structlog.get_logger()


class Antenna:
    def __init__(self, frequency, line, column):
        self.frequency = frequency
        self.line = line
        self.column = column

    def distance_line(self, other_antenna):
        return abs(self.line - other_antenna.line)

    def distance_column(self, other_antenna):
        return abs(self.column - other_antenna.column)

    def create_antinode(self, other_antenna, antinodes):
        antinodes_lines = [
            self.line - self.distance_line(other_antenna),
            other_antenna.line + self.distance_line(other_antenna),
        ]
        if self.column < other_antenna.column:
            antinodes_columns = [
                self.column - self.distance_column(other_antenna),
                other_antenna.column + self.distance_column(other_antenna),
            ]
        else:
            antinodes_columns = [
                self.column + self.distance_column(other_antenna),
                other_antenna.column - self.distance_column(other_antenna),
            ]

        for line, column in zip(antinodes_lines, antinodes_columns):
            if line == line % len(antinodes) and column == column % len(antinodes[0]):
                antinodes[line % len(antinodes)][column % len(antinodes[0])] = "$"
        return antinodes

    def create_harmonic_antinodes(self, other_antenna, antinodes):
        distances = (
            self.distance_line(other_antenna),
            self.distance_column(other_antenna),
        )
        antinodes[self.line][self.column] = "$"
        antinodes[other_antenna.line][other_antenna.column] = "$"
        if self.column < other_antenna.column:
            line = self.line - distances[0]
            column = self.column - distances[1]
            while line >= 0 and column >= 0:
                antinodes[line][column] = "$"
                line -= distances[0]
                column -= distances[1]
            line = other_antenna.line + distances[0]
            column = other_antenna.column + distances[1]
            while line < len(antinodes) and column < len(antinodes[0]):
                antinodes[line][column] = "$"
                line += distances[0]
                column += distances[1]
        elif self.column > other_antenna.column:
            line = self.line - distances[0]
            column = self.column + distances[1]
            while line >= 0 and column < len(antinodes[0]):
                antinodes[line][column] = "$"
                line -= distances[0]
                column += distances[1]
            line = other_antenna.line + distances[0]
            column = other_antenna.column - distances[1]
            while line < len(antinodes) and column >= 0:
                antinodes[line][column] = "$"
                line += distances[0]
                column -= distances[1]
        return antinodes


def parse_antennae(lines):
    antennae = {}
    full_lines = []
    for line_number, line in enumerate(lines):
        new_line = []
        for column_number, char in enumerate(line.strip()):
            if char != ".":
                if char in antennae.keys():
                    antennae[char].append(Antenna(char, line_number, column_number))
                else:
                    antennae[char] = [Antenna(char, line_number, column_number)]
            new_line.append(char)
        full_lines.append(new_line)
    return antennae, full_lines


def solve_first(antennae, lines):
    antinodes = [["." for _ in range(len(lines[0].strip()))] for _ in range(len(lines))]
    for key in antennae.keys():
        for i in range(len(antennae[key])):
            for j in range(i + 1, len(antennae[key])):
                antinodes = antennae[key][i].create_antinode(
                    antennae[key][j], antinodes
                )

    result = 0
    for line in antinodes:
        for elt in line:
            if elt == "$":
                result += 1
    return result


def solve_second(antennae, lines):
    antinodes = [["." for _ in range(len(lines[0].strip()))] for _ in range(len(lines))]
    for key in antennae.keys():
        for i in range(len(antennae[key])):
            for j in range(i + 1, len(antennae[key])):
                antinodes = antennae[key][i].create_harmonic_antinodes(
                    antennae[key][j], antinodes
                )

    result = 0
    for line in antinodes:
        for elt in line:
            if elt == "$":
                result += 1
    return result


def main():
    lines = read_file("input_8.txt")
    antennae, full_lines = parse_antennae(lines)

    first = solve_first(antennae, lines)
    logger.info("First part", first=first)

    second = solve_second(antennae, lines)
    logger.info("Second part", second=second)


if __name__ == "__main__":
    main()
