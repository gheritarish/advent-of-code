import structlog

from day_three import Position
from utils import read_file

logger = structlog.get_logger()


DIRECTIONS = {
    "D": (-1, 0),
    "U": (1, 0),
    "L": (0, -1),
    "R": (0, 1),
}


DIRECTION_CONVERTER = {
    "0": "R",
    "1": "D",
    "2": "L",
    "3": "U",
}


class Vertex:
    def __init__(self, position: Position, color: str | None = None):
        self.position = position
        self.color = color


def get_vertices(lines) -> tuple[list[Vertex], int]:
    vertices = []
    vertices.append(Vertex(position=Position(x=0, y=0), color=None))
    full_length = 0
    for line in lines:
        line = line.strip()
        direction, length, color = line.split(" ")
        point_x = vertices[-1].position.x + DIRECTIONS[direction][0] * int(length)
        point_y = vertices[-1].position.y + DIRECTIONS[direction][1] * int(length)
        vertices.append(Vertex(position=Position(x=point_x, y=point_y), color=color))
        full_length += int(length)

    return vertices, full_length


def get_vertices_hexa(lines) -> tuple[list[Vertex], int]:
    vertices = []
    vertices.append(Vertex(position=Position(x=0, y=0)))
    full_length = 0
    for line in lines:
        line = line.strip()
        hexa = line.split(" ")[2]
        int_direction = hexa[-2]
        hexa_length = hexa[2:-2]
        length = int(hexa_length, 16)
        direction = DIRECTIONS[DIRECTION_CONVERTER[int_direction]]

        point_x = vertices[-1].position.x + direction[0] * int(length)
        point_y = vertices[-1].position.y + direction[1] * int(length)
        vertices.append(Vertex(position=Position(x=point_x, y=point_y)))
        full_length += int(length)
    return vertices, full_length



def get_area(vertices: list[Vertex], length: int) -> int:
    area = abs(
        sum(
            (vertex_1.position.y + vertex_2.position.y) * (vertex_1.position.x - vertex_2.position.x) / 2
            for vertex_1, vertex_2 in zip(vertices, vertices[1:])
        ),
    )
    return int(area + length / 2 + 1)


def main():
    lines = read_file("input_18.txt")
    vertices, length = get_vertices(lines)
    first_answer = get_area(vertices, length)
    logger.info("first_question", answer=first_answer)

    new_vertices, new_length = get_vertices_hexa(lines)
    second_answer = get_area(new_vertices, new_length)
    logger.info("second_question", answer=second_answer)


if __name__ == "__main__":
    main()
