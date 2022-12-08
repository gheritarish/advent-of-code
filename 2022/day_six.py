import structlog

from utils import read_file

log = structlog.get_logger()


def find_differences(signal, count: int):
    candidate = signal[0 : count - 1]
    i = count - 1
    while i < len(signal):
        if signal[i] not in candidate and len(set(candidate + signal[i])) == count:
            return i + 1
        else:
            candidate = candidate[1:] + signal[i]
            i += 1


def main():
    lines = read_file("input_06.txt")
    signal = lines[0].strip()
    first_result = find_differences(signal, count=4)
    log.info("marker_place", value=first_result)
    second_result = find_differences(signal, count=14)
    log.info("message_place", value=second_result)


if __name__ == "__main__":
    main()
