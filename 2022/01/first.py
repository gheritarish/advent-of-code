import structlog

logger = structlog.get_logger()


def get_list() -> list:
    with open("bla.txt", "r") as file:
        lines = file.readlines()
        values = []
        for line in lines:
            line.strip("\n")
            values.append(int(line))
    return values


def sums_and_sort() -> list:
    values = get_list()

    sums = []
    current_sum = 0
    for value in values:
        if value == 0:
            sums.append(current_sum)
            current_sum = 0
        else:
            current_sum += value

    sums.sort(reverse=True)
    return sums


def main():
    sums = sums_and_sort()
    logger.info("max_calories", values=sums[0])
    sum_three = sums[0] + sums[1] + sums[2]
    logger.info("three_max_calories", values=sum_three)


if __name__ == "__main__":
    main()
