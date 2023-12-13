import structlog
import uuid

from utils import read_file

logger = structlog.get_logger()


def get_perfect_reflection(lines: list[str]):
    for k in range(len(lines) - 1):
        next = False
        top, bottom = k, k + 1
        top_lines, bottom_lines = [], []
        while top >= 0 and bottom < len(lines):
            top_lines.append(lines[top])
            bottom_lines.append(lines[bottom])
            top -= 1
            bottom += 1

        for top_line, bottom_line in zip(top_lines, bottom_lines):
            if top_line != bottom_line:
                next = True
                break
        if not next:
            return k
    return None


def get_perfect_reflection_with_smudge(lines: list[str]):
    actual = None
    for k in range(len(lines) - 1):
        diff = 0
        next = False
        top, bottom = k, k + 1
        top_lines, bottom_lines = [], []
        while top >= 0 and bottom < len(lines):
            top_lines.append(lines[top])
            bottom_lines.append(lines[bottom])
            top -= 1
            bottom += 1

        for top_line, bottom_line in zip(top_lines, bottom_lines):
            for i in range(len(top_line)):
                if top_line[i] != bottom_line[i]:
                    diff += 1
            if diff > 1:
                next = True
                break
        if not next:
            if diff == 1:
                return k
    return actual


class Field:
    def __init__(self, map: list[str]):
        self.id = uuid.uuid4()
        self.map = map

    def mirror(self) -> list[str]:
        mirrored_map = []
        for k in range(len(self.map[0])):
            line = ""
            for map_line in self.map:
                line += map_line[k]
            mirrored_map.append(line)
        return mirrored_map

    def get_pattern_summary(self):
        line_mirror = get_perfect_reflection(self.map)
        if line_mirror is not None:
            return {"horizontal": line_mirror + 1}

        if line_mirror is None:
            column_mirror = get_perfect_reflection(self.mirror())
            return {"vertical": column_mirror + 1}

    def get_pattern_summary_with_smudge(self):
        line_mirror = get_perfect_reflection_with_smudge(self.map)
        if line_mirror is not None:
            return {"horizontal": line_mirror + 1}

        if line_mirror is None:
            column_mirror = get_perfect_reflection_with_smudge(self.mirror())
            return {"vertical": column_mirror + 1}


def parse_fields(lines: list[str]) -> list[Field]:
    fields = []
    field_lines = []
    for line in lines:
        if line != "\n":
            field_lines.append(line.strip())
        else:
            fields.append(Field(map=field_lines))
            field_lines = []
    fields.append(Field(map=field_lines))
    return fields


def get_first_answer(fields: list[Field]) -> int:
    result = {"vertical": 0, "horizontal": 0}
    for field in fields:
        pattern_summary = field.get_pattern_summary()
        for key, value in pattern_summary.items():
            result[key] += value
    return 100 * result["horizontal"] + result["vertical"]


def get_second_answer(fields: list[Field]) -> int:
    result = {"vertical": 0, "horizontal": 0}
    for field in fields:
        pattern_summary = field.get_pattern_summary_with_smudge()
        for key, value in pattern_summary.items():
            result[key] += value
    return 100 * result["horizontal"] + result["vertical"]


def main():
    lines = read_file("input_13.txt")
    fields = parse_fields(lines)
    first_answer = get_first_answer(fields)
    logger.info("first_question", answer=first_answer)

    second_answer = get_second_answer(fields)
    logger.info("second_question", answer=second_answer)


if __name__ == "__main__":
    main()
