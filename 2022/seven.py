from __future__ import annotations

import structlog

from utils import read_file

log = structlog.get_logger()

TOTAL_SIZE = 70000000


class Directory:
    def __init__(self, name, *, file_size: int = 0, parent: Directory = None):
        self.name = name
        self.file_size = file_size
        self.children = set()
        if parent:
            self.parent = parent
        else:
            self.parent = None

    def size(self):
        if len(self.children) == 0:
            return self.file_size
        else:
            return self.file_size + sum([child.size() for child in self.children])

    def find(self, new_dir: str):
        for directory in self.children:
            if directory.name == new_dir:
                return directory
            else:
                continue


def is_command(line: str):
    if line[0] == "$":
        return True
    return False


def command(line: str):
    if "cd " in line[2:]:
        return "cd"
    else:
        return "ls"


def full_extend(directories, directory: Directory):
    if len(directory.children) == 0:
        directories.add(directory)
        return directories
    else:
        directories.add(directory)
        for child in directory.children:
            directories = full_extend(directories, child)
        return directories


def root(directory: Directory):
    while directory.parent is not None:
        return root(directory.parent)
    return directory


def parse(lines: list[str]) -> Directory:
    assert lines[0].strip().split("$ ")[1] == "cd /"
    current_dir = Directory("/", file_size=0, parent=None)

    for line in lines[1:]:
        if is_command(line):
            match command(line):
                case "cd":
                    new_dir = line.strip().split("cd ")[1]
                    if new_dir == "..":
                        current_dir = current_dir.parent
                    else:
                        current_dir = current_dir.find(new_dir)
                case "ls":
                    continue
        else:
            first = line.strip().split(" ")[0]
            second = line.strip().split(" ")[1]
            if first == "dir":
                current_dir.children.add(
                    Directory(second, file_size=0, parent=current_dir)
                )
            else:
                current_dir.file_size += int(first)

    return root(current_dir)


def solve_one(sizes):
    result = 0
    for elt in sizes:
        if elt <= 100000:
            result += elt
        else:
            continue
    return result


def solve_two(sizes):
    sizes.sort()

    available_size = TOTAL_SIZE - sizes[-1]  # root takes all the other sizes
    for elt in sizes:
        if elt + available_size < 30000000:
            continue
        return elt


def main():
    lines = read_file("input_07.txt")
    root_dir = parse(lines)
    directories = full_extend(set(), root_dir)
    sizes = [directory.size() for directory in directories]
    assert max(sizes) == root_dir.size()
    result = solve_one(sizes)
    log.info("part_one", size=result)

    result = solve_two(sizes)
    log.info("part_two", size=result)


if __name__ == "__main__":
    main()
