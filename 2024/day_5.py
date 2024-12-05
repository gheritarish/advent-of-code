from __future__ import annotations

import structlog

from utils import read_file

logger = structlog.get_logger()


class Instruction:
    def __init__(self, first_page, second_page):
        self.first_page = first_page
        self.second_page = second_page

    def accepts(self, manual: Manual, key: str | None = "pages"):
        pages = []
        manual_pages = getattr(manual, key)
        for page in manual_pages:
            if pages == [] and page == self.second_page:
                pages.append(page)
            elif pages == [] and page == self.first_page:
                pages.append(page)
            elif len(pages) == 1 and page == self.second_page:
                return True
            elif len(pages) == 1 and page == self.first_page:
                return False
        return True


class Manual:
    def __init__(self, pages):
        self.pages = pages

    def is_valid(self, instructions: list[Instruction], key: str | None = "pages") -> bool:
        for instruction in instructions:
            if not instruction.accepts(self, key):
                return False
        return True

    def get_middle_page(self):
        page_index = len(self.pages) // 2
        return self.pages[page_index]

    def reorder(self, instructions: list[Instruction]) -> Manual:
        if len(getattr(self, "reordered_pages", [])) > 0:
            original_pages = self.reordered_pages
        else:
            original_pages = self.pages
        self.reordered_pages = []
        first_page =  original_pages[0]
        for i in range(1, len(original_pages)):
            pages = [first_page, original_pages[i]]
            reordered = len(self.reordered_pages)
            for instruction in instructions:
                if not instruction.accepts(Manual(pages)):
                    self.reordered_pages.append(original_pages[i])
                    break
            if len(self.reordered_pages) == reordered:
                self.reordered_pages.append(first_page)
                first_page = original_pages[i]

        self.reordered_pages.append(first_page)

        if self.is_valid(instructions, "reordered_pages"):
            return self
        else:
            self.reorder(instructions)
            return self

    def get_reordered_middle_page(self):
        page_index = len(self.reordered_pages) // 2
        return self.reordered_pages[page_index]


def parse_instruction(line: str) -> Instruction:
    return Instruction(int(line.split("|")[0]), int(line.split("|")[1]))

def parse_manual(line: str) -> Manual:
    str_pages = line.split(",")
    return Manual([int(page) for page in str_pages])


def parse_input(lines) -> tuple[list[Instruction], list[Manual]]:
    instructions = []
    manuals = []

    for line in lines:
        if line == "" or line == "\\n" or line == "\n":
            continue
        else:
            if len(line.split("|")) == 2:
                instructions.append(parse_instruction(line))
            else:
                manuals.append(parse_manual(line))
    return instructions, manuals


def solve_first(instructions: list[Instruction], manuals: list[Manual]) -> int:
    valid_manuals = []
    for manual in manuals:
        if manual.is_valid(instructions):
            valid_manuals.append(manual)

    return sum([manual.get_middle_page() for manual in valid_manuals])


def solve_second(instructions: list[Instruction], manuals: list[Manual]) -> int:
    invalid_manuals = []
    for manual in manuals:
        if not manual.is_valid(instructions):
            invalid_manuals.append(manual)

    reordered_manuals = []
    for manual in invalid_manuals:
        reordered_manuals.append(manual.reorder(instructions))

    return sum([manual.get_reordered_middle_page() for manual in reordered_manuals])



def main():
    lines = read_file("input_5.txt")
    instructions, manuals = parse_input(lines)
    first = solve_first(instructions, manuals)
    logger.info("First part", first=first)

    second = solve_second(instructions, manuals)
    logger.info("Second part", second=second)


if __name__ == "__main__":
    main()
