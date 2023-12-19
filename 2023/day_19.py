from __future__ import annotations

import structlog

logger = structlog.get_logger()


def read_file(name) -> tuple[list[str], list[str]]:
    with open(name, "r") as file:
        lines = file.readlines()
    rules = []
    parts = []
    parse_parts = False
    for line in lines:
        if line == "\n":
            parse_parts = True
            continue
        if parse_parts:
            parts.append(line.strip())
        else:
            rules.append(line.strip())
    return rules, parts


class Condition:
    def __init__(self, category: str, operation: str, value: int, destination: str):
        self.category = category
        self.operation = operation
        self.value = value
        self.destination = destination


class Rule:
    def __init__(self, name, conditions: list[Condition], final_destination: str):
        self.name = name
        self.conditions = conditions
        self.final_destination = final_destination


class Part:
    def __init__(self, x: int, m: int, a: int, s: int):
        self.x = x
        self.m = m
        self.a = a
        self.s = s

    def get_rating(self):
        return self.x + self.m + self.a + self.s

    def is_valid(self, rules: dict[str, Rule]) -> bool:
        destination = "in"
        while destination not in ["A", "R"]:
            destination = get_next_destination(rules[destination], self)
        if destination == "A":
            return True
        return False


class PartRange:
    def __init__(self, origin, end):
        self.origin = origin
        self.end = end

    def length(self):
        return self.end - self.origin + 1


class PartRanges:
    def __init__(self, x: PartRange, m: PartRange, a: PartRange, s: PartRange):
        self.x = x
        self.m = m
        self.a = a
        self.s = s

    def possibilities(self):
        return self.x.length() * self.m.length() * self.a.length() * self.s.length()


def get_next_destination(rule: Rule, part: Part) -> str:
    for condition in rule.conditions:
        match condition.operation:
            case ">":
                match condition.category:
                    case "x":
                        if part.x > condition.value:
                            return condition.destination
                    case "m":
                        if part.m > condition.value:
                            return condition.destination
                    case "a":
                        if part.a > condition.value:
                            return condition.destination
                    case "s":
                        if part.s > condition.value:
                            return condition.destination
            case "<":
                match condition.category:
                    case "x":
                        if part.x < condition.value:
                            return condition.destination
                    case "m":
                        if part.m < condition.value:
                            return condition.destination
                    case "a":
                        if part.a < condition.value:
                            return condition.destination
                    case "s":
                        if part.s < condition.value:
                            return condition.destination
    return rule.final_destination


def get_new_ranges(rule: Rule, part: PartRanges) -> list[tuple[PartRanges, str]]:
    for condition in rule.conditions:
        match condition.operation:
            case ">":
                match condition.category:
                    case "x":
                        if part.x.origin > condition.value:
                            return [(condition.destination, part)]
                        if part.x.origin <= condition.value and part.x.end > condition.value:
                            return [
                                (
                                    rule.name,
                                    PartRanges(
                                        x=PartRange(origin=part.x.origin, end=condition.value),
                                        m=part.m,
                                        a=part.a,
                                        s=part.s,
                                    ),
                                ),
                                (
                                    condition.destination,
                                    PartRanges(
                                        x=PartRange(origin=condition.value + 1, end=part.x.end),
                                        m=part.m,
                                        a=part.a,
                                        s=part.s,
                                    ),
                                ),
                            ]
                    case "m":
                        if part.m.origin > condition.value:
                            return [(condition.destination, part)]
                        if part.m.origin <= condition.value and part.m.end > condition.value:
                            return [
                                (
                                    rule.name,
                                    PartRanges(
                                        x=part.x,
                                        m=PartRange(origin=part.m.origin, end=condition.value),
                                        a=part.a,
                                        s=part.s,
                                    ),
                                ),
                                (
                                    condition.destination,
                                    PartRanges(
                                        x=part.x,
                                        m=PartRange(origin=condition.value + 1, end=part.m.end),
                                        a=part.a,
                                        s=part.s,
                                    ),
                                ),
                            ]
                    case "a":
                        if part.a.origin > condition.value:
                            return [(condition.destination, part)]
                        if part.a.origin <= condition.value and part.a.end > condition.value:
                            return [
                                (
                                    rule.name,
                                    PartRanges(
                                        x=part.x,
                                        m=part.m,
                                        a=PartRange(origin=part.a.origin, end=condition.value),
                                        s=part.s,
                                    ),
                                ),
                                (
                                    condition.destination,
                                    PartRanges(
                                        x=part.x,
                                        m=part.m,
                                        a=PartRange(origin=condition.value + 1, end=part.a.end),
                                        s=part.s,
                                    ),
                                ),
                            ]
                    case "s":
                        if part.s.origin > condition.value:
                            return [(condition.destination, part)]
                        if part.s.origin <= condition.value and part.s.end > condition.value:
                            return [
                                (
                                    rule.name,
                                    PartRanges(
                                        x=part.x,
                                        m=part.m,
                                        a=part.a,
                                        s=PartRange(origin=part.s.origin, end=condition.value),
                                    ),
                                ),
                                (
                                    condition.destination,
                                    PartRanges(
                                        x=part.x,
                                        m=part.m,
                                        a=part.a,
                                        s=PartRange(origin=condition.value + 1, end=part.s.end),
                                    ),
                                ),
                            ]
            case "<":
                match condition.category:
                    case "x":
                        if part.x.end < condition.value:
                            return [(condition.destination, part)]
                        if part.x.origin < condition.value and part.x.end >= condition.value:
                            return [
                                (
                                    condition.destination,
                                    PartRanges(
                                        x=PartRange(origin=part.x.origin, end=condition.value - 1),
                                        m=part.m,
                                        a=part.a,
                                        s=part.s,
                                    ),
                                ),
                                (
                                    rule.name,
                                    PartRanges(
                                        x=PartRange(origin=condition.value, end=part.x.end),
                                        m=part.m,
                                        a=part.a,
                                        s=part.s,
                                    ),
                                ),
                            ]
                    case "m":
                        if part.m.end < condition.value:
                            return [(condition.destination, part)]
                        if part.m.origin < condition.value and part.m.end >= condition.value:
                            return [
                                (
                                    condition.destination,
                                    PartRanges(
                                        x=part.x,
                                        m=PartRange(origin=part.m.origin, end=condition.value - 1),
                                        a=part.a,
                                        s=part.s,
                                    ),
                                ),
                                (
                                    rule.name,
                                    PartRanges(
                                        x=part.x,
                                        m=PartRange(origin=condition.value, end=part.m.end),
                                        a=part.a,
                                        s=part.s,
                                    ),
                                ),
                            ]
                    case "a":
                        if part.a.end < condition.value:
                            return [(condition.destination, part)]
                        if part.a.origin < condition.value and part.a.end >= condition.value:
                            return [
                                (
                                    condition.destination,
                                    PartRanges(
                                        x=part.x,
                                        m=part.m,
                                        a=PartRange(origin=part.a.origin, end=condition.value - 1),
                                        s=part.s,
                                    ),
                                ),
                                (
                                    rule.name,
                                    PartRanges(
                                        x=part.x,
                                        m=part.m,
                                        a=PartRange(origin=condition.value, end=part.a.end),
                                        s=part.s,
                                    ),
                                ),
                            ]
                    case "s":
                        if part.s.end < condition.value:
                            return [(condition.destination, part)]
                        if part.s.origin < condition.value and part.s.end >= condition.value:
                            return [
                                (
                                    condition.destination,
                                    PartRanges(
                                        x=part.x,
                                        m=part.m,
                                        a=part.a,
                                        s=PartRange(origin=part.s.origin, end=condition.value - 1),
                                    ),
                                ),
                                (
                                    rule.name,
                                    PartRanges(
                                        x=part.x,
                                        m=part.m,
                                        a=part.a,
                                        s=PartRange(origin=condition.value, end=part.s.end),
                                    ),
                                ),
                            ]
    return [(rule.final_destination, part)]


def parse_rules(lines: list[str]) -> dict[str, Rule]:
    rules = {}
    for line in lines:
        name = line.split("{")[0].split("}")[0]
        conditions = line.split("{")[1].split("}")[0]
        condition_list = []
        for condition in conditions.split(",")[:-1]:
            category = condition[0]
            operation = condition[1]
            value = int(condition[2:].split(":")[0])
            destination = condition.split(":")[1]
            condition_list.append(
                Condition(category=category, operation=operation, value=value, destination=destination),
            )

            final_destination = conditions.split(",")[-1]
            rules[name] = Rule(name=name, conditions=condition_list, final_destination=final_destination)
    return rules


def parse_parts(lines: list[str]) -> list[Part]:
    parts = []
    for line in lines:
        elements = line.split("{")[1].split("}")[0]
        for k, element in enumerate(elements.split(",")):
            if k == 0:
                x = int(element.split("=")[1])
            if k == 1:
                m = int(element.split("=")[1])
            if k == 2:
                a = int(element.split("=")[1])
            if k == 3:
                s = int(element.split("=")[1])
        parts.append(Part(x=x, m=m, a=a, s=s))
    return parts


def get_first_answer(parts: list[Part], rules: dict[str, Rule]) -> int:
    valid_parts = []
    for part in parts:
        if part.is_valid(rules):
            valid_parts.append(part)

    answer = 0
    for part in valid_parts:
        answer += part.get_rating()

    return answer


def get_second_answer(rules) -> int:
    part_range = PartRanges(
        x=PartRange(origin=1, end=4000),
        a=PartRange(origin=1, end=4000),
        m=PartRange(origin=1, end=4000),
        s=PartRange(origin=1, end=4000),
    )
    new_ranges = [("in", part_range)]

    valid = []
    while len(new_ranges) > 0:
        (destination, part_range) = new_ranges[0]
        new_ranges = new_ranges[1:]
        if destination == "A":
            valid.append(part_range)
            continue
        if destination == "R":
            continue
        new_ranges.extend(get_new_ranges(rules[destination], part_range))

    answer = 0
    for part_range in valid:
        answer += part_range.possibilities()
    return answer


def main():
    rule_lines, part_lines = read_file("input_19.txt")
    rules = parse_rules(rule_lines)
    parts = parse_parts(part_lines)

    first_answer = get_first_answer(parts, rules)
    logger.info("first_question", answer=first_answer)

    second_answer = get_second_answer(rules)
    logger.info("second_question", answer=second_answer)


if __name__ == "__main__":
    main()
