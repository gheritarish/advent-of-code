import structlog

from utils import read_file

log = structlog.get_logger()


class Sensor:
    def __init__(self, x, y, beacon_x, beacon_y):
        self.sensor = (x, y)
        self.beacon = (beacon_x, beacon_y)

    def manhattan_distance(self):
        dist_x = abs(self.sensor[0] - self.beacon[0])
        dist_y = abs(self.sensor[1] - self.beacon[1])
        return dist_x + dist_y


def parse_input(lines):
    sensors = []
    for line in lines:
        sensor_coord = line.split(":")[0]
        beacon_coord = line.split(":")[1]
        sensor_x = sensor_coord.split(",")[0].split("x=")[1]
        sensor_y = sensor_coord.split(",")[1].split("y=")[1]
        beacon_x = beacon_coord.split(",")[0].split("x=")[1]
        beacon_y = beacon_coord.split(",")[1].split("y=")[1]
        sensors.append(
            Sensor(int(sensor_x), int(sensor_y), int(beacon_x), int(beacon_y)),
        )
    return sensors


def solve_one(sensors: list[Sensor], *, row: int) -> int:
    discovered_points = set()
    for sensor in sensors:
        remaining_distance = sensor.manhattan_distance() - abs(row - sensor.sensor[1])
        if remaining_distance < 0:
            continue
        if (sensor.sensor[0], row) != (sensor.beacon[0], sensor.beacon[1]):
            discovered_points.add(sensor.sensor[0])
        for i in range(1, remaining_distance + 1):
            if (sensor.sensor[0] - i, row) != (sensor.beacon[0], sensor.beacon[1]):
                discovered_points.add(sensor.sensor[0] - i)

            if (sensor.sensor[0] + i, row) != (sensor.beacon[0], sensor.beacon[1]):
                discovered_points.add(sensor.sensor[0] + i)
    return len(discovered_points)


def merge_ranges(ranges):
    ranges.sort(key=lambda x: x[0])
    merged = []
    for i in range(len(ranges) - 1):
        if (
            ranges[i + 1][0] <= ranges[i][1] <= ranges[i + 1][1]
            or ranges[i + 1][0] == ranges[i][1] + 1
        ):
            ranges[i + 1] = [ranges[i][0], ranges[i + 1][1]]
            continue
        elif ranges[i][0] <= ranges[i + 1][0] and ranges[i][1] >= ranges[i + 1][1]:
            ranges[i + 1] = ranges[i]
            continue
        else:
            merged.append(ranges[i])
    merged.append(ranges[-1])
    return merged


def solve_two(sensors: list[Sensor]) -> int:
    for row in range(4000001):
        no_found = []
        for sensor in sensors:
            remaining_distance = sensor.manhattan_distance() - abs(
                row - sensor.sensor[1],
            )
            if remaining_distance < 0:
                continue
            else:
                no_found.append(
                    [
                        sensor.sensor[0] - remaining_distance,
                        sensor.sensor[0] + remaining_distance,
                    ],
                )
        range_found = merge_ranges(no_found)
        if len(range_found) > 1:
            return 4000000 * (range_found[0][1] + 1) + row


def main():
    lines = read_file("input_15.txt")
    sensors = parse_input(lines)
    result = solve_one(sensors, row=2000000)
    log.info("part_one", result=result)
    result = solve_two(sensors)
    log.info("part_two", result=result)


if __name__ == "__main__":
    main()
