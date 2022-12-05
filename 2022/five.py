import structlog

log = structlog.get_logger()


class Stack:
    def __init__(self, elt):
        self.items = [elt]

    def add(self, elt):
        self.items.append(elt)

    def remove(self, number):
        if number > len(self.items):
            new_length = 0
        else:
            new_length = len(self.items) - number
        removed = self.items[new_length:]
        self.items = self.items[:new_length]
        return removed


def get_parts(file_name):
    with open(file_name, "r") as file:
        parts = file.read().split("\n\n")


def swap(stacks, movement, reverse=False):
    if movement == "":
        return stacks
    number = int(movement.split("-")[0])
    origin = int(movement.split("-")[1]) - 1
    destination = int(movement.split("-")[2]) - 1

    removed_items = stacks[origin].remove(number)
    if reverse:
        removed_items.reverse()
    for item in removed_items:
        stacks[destination].add(item)

    return stacks


def create_stacks(description):
    stacks = []
    stack_def = description[-2]
    # Each stack has a rank in the list (from 0 to max, corresponding to its name minus 1)
    # Each stack contains a list of items
    for i in range(1, len(description[-1]), 4):
        stacks.append(Stack(stack_def[i]))

    description.reverse()
    for line in description[2:]:
        for i in range(1, len(line), 4):
            if line[i] != " ":
                stacks[i // 4].add(line[i])

    return stacks


def part_one(parts):
    stacks = create_stacks(parts[0].split("\n"))
    for move in parts[1].split("\n"):
        stacks = swap(stacks, move, reverse=True)
    values = ""
    for stack in stacks:
        if stack.items:
            values += stack.items[-1]
    log.info("top_items", list=values)


def part_two(parts):
    stacks = create_stacks(parts[0].split("\n"))
    for move in parts[1].split("\n"):
        stacks = swap(stacks, move, reverse=False)
    values = ""
    for stack in stacks:
        if stack.items:
            values += stack.items[-1]
    log.info("top_items", list=values)



def main():
    parts = open("bla.txt", "r").read().split("\n\n")
    part_one(parts)
    part_two(parts)


if __name__ == "__main__":
    main()
