from typing import Self

import structlog

from day_eight import get_lcm
from utils import read_file

logger = structlog.get_logger()

HIGH = "high"
LOW = "low"
ON = 1
OFF = 0


class Communication:
    def __init__(self, name: str, destinations: list[str] | list[Self]):
        self.name = name
        self.destinations = destinations

    def handle_signal(self, origin: Self, pulse: str):
        raise NotImplementedError()


class FlipFlop(Communication):
    def __init__(self, name: str, destinations: list[Communication]):
        super().__init__(name, destinations)
        self.status = OFF

    def handle_signal(self, origin: Communication, pulse: str):
        if pulse == HIGH:
            return

        if self.status == OFF:
            self.status = ON
            return HIGH

        else:
            self.status = OFF
            return LOW


class Conjunction(Communication):
    def __init__(self, name: str, destinations: list[Communication]):
        super().__init__(name, destinations)

    def initialize_inputs(self, communications: dict[str, Communication]):
        self.inputs = {}
        for communication in communications.values():
            for destination in communication.destinations:
                if destination.name == self.name:
                    self.inputs[communication.name] = LOW

    def is_high(self):
        high = True
        for input in self.inputs.values():
            if input == LOW:
                return False
        return high

    def handle_signal(self, origin: Communication, pulse: str):
        if origin.name in self.inputs.keys():
            self.inputs[origin.name] = pulse

        if self.is_high():
            return LOW
        return HIGH


class Broadcast(Communication):
    def __init__(self, name: str, destinations: list[Communication]):
        super().__init__(name, destinations)

    def handle_signal(self, origin: Communication | None = None, pulse: str | None = None):
        return pulse


def parse_communications(lines: list[str]) -> list[Communication]:
    communications = {}
    for line in lines:
        line = line.strip()
        match line[0]:
            case "%":
                name = line.split("%")[1].split(" ")[0]
                destinations = line.split("-> ")[1]
                destinations_string = destinations.split(", ")
                communications[name] = FlipFlop(name=name, destinations=destinations_string)
            case "&":
                name = line.split("&")[1].split(" ")[0]
                destinations = line.split("-> ")[1]
                destinations_string = destinations.split(", ")
                communications[name] = Conjunction(name=name, destinations=destinations_string)
            case _:
                name = line.split(" ->")[0]
                destinations = line.split("-> ")[1]
                destinations_string = destinations.split(", ")
                communications[name] = Broadcast(name=name, destinations=destinations_string)

    for communication in communications.values():
        destinations_elements = []
        for destination in communication.destinations:
            if destination in communications.keys():
                destinations_elements.append(communications[destination])
            else:
                destinations_elements.append(Communication(name=destination, destinations=[]))
        communication.destinations = destinations_elements

    for communication in communications.values():
        if isinstance(communication, Conjunction):
            communication.initialize_inputs(communications)

    return communications


def handle_button_push(communications: dict[str, Communication]):
    counts = {LOW: 0, HIGH: 0}
    pulse = LOW
    counts[pulse] += 1
    destination = "broadcaster"
    signal_iteration = {0: [(None, destination, pulse)]}
    key = 0
    while key in signal_iteration.keys():
        origins = signal_iteration[key]
        if len(origins) >= 1:
            signal_iteration[key + 1] = []
        for (origin, handler_name, pulse) in origins:
            try:
                handler = communications[handler_name]
            except KeyError:
                continue
            next_pulse = handler.handle_signal(origin, pulse)
            if next_pulse:
                next_destinations = handler.destinations
                for destination in next_destinations:
                    signal_iteration[key + 1].append((handler, destination.name, next_pulse))
                    counts[next_pulse] += 1
        key += 1
    return counts


def new_handle_button_push(communications: dict[str, Communication], iteration: int, stops: dict[str, int | None]):
    pulse = LOW
    destination = "broadcaster"
    signal_iteration = {1: [(None, destination, pulse)]}
    key = 1
    while key in signal_iteration.keys():
        origins = signal_iteration[key]
        if len(origins) >= 1:
            signal_iteration[key + 1] = []
        for (origin, handler_name, pulse) in origins:
            try:
                handler = communications[handler_name]
            except KeyError:
                continue
            next_pulse = handler.handle_signal(origin, pulse)
            if next_pulse:
                next_destinations = handler.destinations
                for destination in next_destinations:
                    if destination.name in stops.keys() and next_pulse == LOW:
                        stops[destination.name] = iteration
                    signal_iteration[key + 1].append((handler, destination.name, next_pulse))
        key += 1
    return stops


def get_first_answer(communications):
    counts = {LOW: 0, HIGH: 0}
    for i in range(1000):
        to_add = handle_button_push(communications)
        counts[LOW] += to_add[LOW]
        counts[HIGH] += to_add[HIGH]
    return counts[LOW] * counts[HIGH]


def get_second_answer(communications):
    key = 1
    stops = {
        "rd": None,
        "bt": None,
        "fv": None,
        "pr": None,
    }
    while not all(val is not None for val in stops.values()):
        stops = new_handle_button_push(communications, iteration=key, stops=stops)
        key += 1
    return get_lcm(stops.values())


def main():
    lines = read_file("input_20.txt")
    communications = parse_communications(lines)
    first_answer = get_first_answer(communications)
    logger.info("first_question", answer=first_answer)

    communications = parse_communications(lines)
    second_answer = get_second_answer(communications)
    logger.info("second_question", answer=second_answer)


if __name__ == "__main__":
    main()
