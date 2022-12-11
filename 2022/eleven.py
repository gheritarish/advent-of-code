import uuid
from math import lcm

import structlog

from utils import read_file

log = structlog.get_logger()


class Object:
    def __init__(self, priority):
        self.id = uuid.uuid4()
        self.priority = priority

    def update_priority(self, new_priority):
        self.priority = new_priority


class Monkey:
    def __init__(
        self,
        id,
        operation_sign,
        operation_number,
        test,
        test_true,
        test_false,
        objects,
    ):
        self.id = id
        self.operation_sign = operation_sign
        self.operation_number = operation_number
        self.test = test
        self.test_true = test_true
        self.test_false = test_false
        self.objects = dict()
        self.examined = 0
        for obj in objects:
            self.objects[obj.id] = obj

    def add_item(self, item):
        self.objects[item.id] = item

    def remove_item(self, item):
        self.objects.pop(item.id)


def turn(monkey, monkeys, base=3) -> dict[int, Monkey]:
    for item in monkey.objects.values():
        if monkey.operation_sign == "+":
            if monkey.operation_number == "old":
                item.update_priority(item.priority + item.priority)
            else:
                item.update_priority(item.priority + int(monkey.operation_number))
        else:
            if monkey.operation_number == "old":
                item.update_priority(item.priority * item.priority)
            else:
                item.update_priority(item.priority * int(monkey.operation_number))
        monkey.examined += 1

        if base == 3:
            item.update_priority(item.priority // base)
        else:
            item.update_priority(item.priority % base)

    for item in monkey.objects.values():
        if item.priority % monkey.test == 0:
            monkeys[monkey.test_true].add_item(item)
        else:
            monkeys[monkey.test_false].add_item(item)

    monkey.objects = dict()

    return monkeys


def make_round(monkeys, base=3):
    for monkey_id in monkeys.keys():
        monkeys = turn(monkeys[monkey_id], monkeys, base)
    return monkeys


def solve_one(monkeys, base=3):
    for i in range(20):
        make_round(monkeys, base)
    examined = [monkey.examined for monkey in monkeys.values()]
    examined.sort(reverse=True)
    return examined[0] * examined[1]


def solve_two(monkeys, base):
    for i in range(10000):
        monkeys = make_round(monkeys, base)
    examined = [monkey.examined for monkey in monkeys.values()]
    examined.sort(reverse=True)
    return examined[0] * examined[1]


def parse(file_name: str) -> dict[int, Monkey]:
    with open(file_name, "r") as file:
        monkeys_to_parse = file.read().split("\n\n")

    monkeys = dict()
    for monkey_to_parse in monkeys_to_parse:
        the_monkey = monkey_to_parse.split("\n")[0].split(":")[0]
        the_id = int(the_monkey.split(" ")[1])
        the_items = monkey_to_parse.split("\n")[1].split("items: ")[1]
        objects = []
        for the_item in the_items.split(", "):
            objects.append(Object(int(the_item)))

        the_operation = monkey_to_parse.split("\n")[2].split("old ")[1]
        the_operation_sign = the_operation.split(" ")[0]
        the_operation_number = the_operation.split(" ")[1]
        the_test = int(monkey_to_parse.split("\n")[3].split(" by ")[1])
        test_true = int(monkey_to_parse.split("\n")[4].split(" monkey ")[1])
        test_false = int(monkey_to_parse.split("\n")[5].split(" monkey ")[1])
        monkey = Monkey(
            the_id,
            the_operation_sign,
            the_operation_number,
            the_test,
            test_true,
            test_false,
            objects,
        )
        monkeys[monkey.id] = monkey

    return monkeys


def main():
    monkeys = parse("input_11.txt")
    result = solve_one(monkeys)
    log.info("part_one", result=result)

    monkeys = parse("input_11.txt")
    base = lcm(*(monkey.test for monkey in monkeys.values()))
    result = solve_two(monkeys, base)
    log.info("part_two", result=result)


if __name__ == "__main__":
    main()
