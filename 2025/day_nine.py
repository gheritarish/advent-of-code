import structlog

from utils import read_file

logger = structlog.get_logger()


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Rectangle:
    def __init__(self, point: Point, opposite_point: Point):
        self.min_x = min(point.x, opposite_point.x)
        self.max_x = max(point.x, opposite_point.x)
        self.min_y = min(point.y, opposite_point.y)
        self.max_y = max(point.y, opposite_point.y)

    def area(self):
        return (self.max_x - self.min_x + 1) * (self.max_y - self.min_y + 1)


def parse_points(lines: list[str]) -> list[Point]:
    points = []
    for line in lines:
        line = line.strip()
        points.append(Point(int(line.split(",")[0]), int(line.split(",")[1])))
    return points


def create_rectangles(points: list[Point]) -> list[Rectangle]:
    rectangles = []
    for i in range(len(points) - 1):
        for j in range(i + 1, len(points)):
            rectangles.append(Rectangle(points[i], points[j]))
    return rectangles


def solve_one(rectangles: list[Rectangle]) -> int:
    return max([rectangle.area() for rectangle in rectangles])


def main():
    lines = read_file("input_9.txt")
    points = parse_points(lines)
    rectangles = create_rectangles(points)

    part_one = solve_one(rectangles)
    logger.info("Part one", result=part_one)


if __name__ == "__main__":
    main()
