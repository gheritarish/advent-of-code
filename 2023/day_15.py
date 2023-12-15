import structlog

logger = structlog.get_logger()


class Signal:
    def __init__(self, full_signal):
        self.full_signal = full_signal

    def label(self):
        label = ""
        for char in self.full_signal:
            if 97 <= ord(char) <= 122:
                label += char
        return label

    def get_score(self):
        score = 0
        for character in self.full_signal:
            score += ord(character)
            score *= 17
            score = score % 256
        logger.info("signal.score", signal=self.full_signal, score=score)
        return score

    def get_label_score(self):
        score = 0
        label = self.label()
        for character in label:
            score += ord(character)
            score *= 17
            score = score % 256
        logger.info("label.score", label=label, score=score)
        return score

    def get_operation(self):
        if "-" in self.full_signal:
            return "-"
        if "=" in self.full_signal:
            return "+"

    def get_power(self):
        if "=" in self.full_signal:
            power = int(self.full_signal.split("=")[1])
            return power
        return 0


class Lens:
    def __init__(self, label, power):
        self.label = label
        self.power = power


class Box:
    def __init__(self, id):
        self.id = id
        self.lenses = []

    def add_lens(self, lens: Lens):
        for existing_lens in self.lenses:
            if existing_lens.label == lens.label:
                existing_lens.power = lens.power
                return
        self.lenses.append(lens)

    def remove_lens(self, label):
        for k in range(len(self.lenses)):
            if self.lenses[k].label == label:
                self.lenses.pop(k)
                break


def read_file(file_name: str) -> str:
    with open(file_name, "r") as file:
        lines = file.readlines()

    return lines[0].strip()


def get_instructions(line: str) -> list[Signal]:
    signals = []
    for elt in line.split(","):
        signals.append(Signal(full_signal=elt))
    return signals


def get_boxes():
    return {i: Box(id=i) for i in range(256)}


def get_full_boxes(boxes: dict[int, Box], signals: list[Signal]) -> list[Box]:
    for signal in signals:
        match signal.get_operation():
            case "+":
                boxes[signal.get_label_score()].add_lens(
                    Lens(label=signal.label(), power=signal.get_power())
                )
            case "-":
                boxes[signal.get_label_score()].remove_lens(label=signal.label())
    return boxes


def get_second_answer(full_boxes: list[Box]):
    result = 0
    for box in full_boxes.values():
        for k in range(len(box.lenses)):
            result += (box.id + 1) * (k + 1) * box.lenses[k].power
    return result


def main():
    line = read_file("input_15.txt")
    signals = get_instructions(line)
    first_answer = sum([signal.get_score() for signal in signals])
    logger.info("first_question", answer=first_answer)

    boxes = get_boxes()
    full_boxes = get_full_boxes(boxes, signals)
    second_answer = get_second_answer(full_boxes)
    logger.info("second_question", answer=second_answer)


if __name__ == "__main__":
    main()
