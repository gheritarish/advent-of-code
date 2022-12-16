import functools

import structlog

from utils import read_file

log = structlog.get_logger()


class Valve:
    def __init__(self, flow, destinations):
        self.flow = flow
        self.destinations = destinations


def parse_input(lines):
    valves = dict()
    for line in lines:
        line = line.strip("\n")
        valve_name = line[6:8]  # Valve name has two letters
        flow = line.split(";")[0].split("rate=")[1]
        destination_names = line.split("to valve")[1]
        destinations = []
        for destination in destination_names.split(" ")[1:]:
            destinations.append(destination.split(",")[0])

        valves[valve_name] = Valve(int(flow), destinations)
    return valves


@functools.lru_cache(maxsize=None)
def best_flows(current, opened, minutes_left):
    if minutes_left <= 0:
        return 0
    best_flow = 0
    if current not in opened:
        flow_current = (minutes_left - 1) * valves[current].flow
        now_opened = tuple(sorted(opened + (current,)))
        for destination in valves[current].destinations:
            if flow_current != 0:
                best_flow = max(
                    best_flow,
                    flow_current
                    + best_flows(destination, now_opened, minutes_left - 2),
                )
            best_flow = max(
                best_flow,
                best_flows(destination, opened, minutes_left - 1),
            )

    return best_flow


def solve_one(valves):
    return best_flows("AA", (), 30)


lines = read_file("input_16.txt")
valves = parse_input(lines)
result = solve_one(valves)
log.info("part_one", result=result)
