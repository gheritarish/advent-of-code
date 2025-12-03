import structlog

logger = structlog.get_logger()


class Range:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def find_invalid_ids(self):
        min_invalid_seq_len = len(self.start) // 2
        min_invalid_seq = self.start[:min_invalid_seq_len] if min_invalid_seq_len > 0 else self.start[0]

        max_invalid_seq_len = (len(self.end) // 2) + 1
        max_invalid_seq = self.end[:max_invalid_seq_len]

        if int(min_invalid_seq * 2) > int(self.end):
            return 0

        if int(max_invalid_seq * 2) < int(self.start):
            return 0

        return self.compute_result(min_invalid_seq, max_invalid_seq)

    def compute_result(self, min_invalid_seq, max_invalid_seq):
        result = 0

        while int(min_invalid_seq * 2) < int(self.start):
            min_invalid_seq = str(int(min_invalid_seq) + 1)

        while int(max_invalid_seq * 2) > int(self.end):
            max_invalid_seq = str(int(max_invalid_seq) - 1)

        while int(min_invalid_seq) <= int(max_invalid_seq):
            result += int(min_invalid_seq * 2)
            min_invalid_seq = str(int(min_invalid_seq) + 1)

        return result

    def find_all_invalid_ids(self):
        min_invalid_seq = 1

        max_invalid_seq_len = (len(self.end) // 2) + 1
        max_invalid_seq = self.end[:max_invalid_seq_len]

        found = []
        for value in range(int(min_invalid_seq), int(max_invalid_seq) + 1):
            for i in range(2, len(self.end) + 1):
                candidate = int(str(value) * i)

                if int(self.start) <= candidate <= int(self.end):
                    found.append(candidate)

        return sum(list(set(found)))
            

def get_ranges(name: str) -> list[Range]:
    with open(name, "r") as file:
        lines = file.readlines()
    elements = lines[0].split(",")

    ranges = []
    for element in elements:
        ranges.append(Range(start=element.split("-")[0], end=element.split("-")[1]))
    return ranges


def solve_one(ranges: list[Range]) -> int:
    result = 0
    for range in ranges:
        result += range.find_invalid_ids()
    return result


def solve_two(ranges: list[Range]) -> int:
    result = 0
    for range in ranges:
        result += range.find_all_invalid_ids()
    return result


def main():
    ranges = get_ranges("input_2.txt")
    result = solve_one(ranges)
    logger.info("First part", result=result)

    part_two = solve_two(ranges)
    logger.info("Second part", result=part_two)


if __name__ == "__main__":
    main()
