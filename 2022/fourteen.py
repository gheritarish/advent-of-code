import structlog

from utils import read_file

log = structlog.get_logger()


def get_walls(lines):
    room_walls = []
    for line in lines:
        wall_traces = line.split(" -> ")
        wall_traces = [wall_trace.split(",") for wall_trace in wall_traces]
        for wall_trace in wall_traces:
            wall_trace[0] = int(wall_trace[0])
            wall_trace[1] = int(wall_trace[1])
        room_walls.append(wall_traces)
    return room_walls


def get_dimensions(walls: list[list[int, int]]) -> (int, int, int):
    """
    We want to avoid using a too large grid if we don't need to.
    The idea is to limit ourselves to a grid from [min_x_found, max_x_found], [0, max_y_found]
    To do so, we get the min_x from the input, the max_x from the input, and the max_y from the input.
    """
    x_coordinates = []
    y_coordinates = []
    for line in walls:
        for point in line:
            x_coordinates.append(point[0])
            y_coordinates.append(point[1])
    return min(x_coordinates), max(x_coordinates), max(y_coordinates)


def draw_room(small_x, big_x, big_y, walls, floor):
    """
    Get the room with the rocks and the beginning of sand.
    . means there is nothing, # means there is rock.
    """

    # Empty room
    room = []
    for y in range(big_y + 1):
        row = ["." for _ in range(big_x - small_x + 1)]
        room.append(row)

    if floor:
        room.append(["#" for _ in range(big_x - small_x + 1)])

    # With rocks
    for wall in walls:
        for i in range(len(wall) - 1):
            rock1 = wall[i]
            rock2 = wall[i + 1]

            if rock1[0] > rock2[0] or rock1[1] > rock2[1]:
                rock1, rock2 = rock2, rock1

            for vx in range(rock1[0], rock2[0] + 1):
                for vy in range(rock1[1], rock2[1] + 1):
                    dx = vx - small_x
                    dy = vy
                    room[dy][dx] = "#"

    sand_x = 500 - small_x
    sand_y = 0
    sand = [sand_x, sand_y]

    return room, sand


def sand_fall(room, sand):
    x_pos, y_pos = sand

    # Make sand fall until out of bonds
    if room[y_pos][x_pos] == "o":
        return False
    while True:
        if x_pos < 0 or x_pos >= len(room[0]) or y_pos >= len(room):
            return False

        # Go down
        if y_pos == len(room) - 1 or room[y_pos + 1][x_pos] == ".":
            y_pos += 1
            continue

        # Go down-left
        if x_pos == 0 or room[y_pos + 1][x_pos - 1] == ".":
            y_pos += 1
            x_pos -= 1
            continue

        # Go down-right
        if x_pos == 0 or room[y_pos + 1][x_pos + 1] == ".":
            y_pos += 1
            x_pos += 1
            continue

        # Cannot move?
        break

    room[y_pos][x_pos] = "o"
    return True


def part_one(room, sand):
    units = 0

    while True:
        sand_fell = sand_fall(room, sand)
        if not sand_fell:
            break
        units += 1
    return units


def part_one(room, sand):
    units = 0

    while True:
        sand_fell = sand_fall(room, sand)
        if not sand_fell:
            break
        units += 1
    return units


def main():
    lines = read_file("input_14.txt")
    room_walls = get_walls(lines)
    small_x, big_x, big_y = get_dimensions(room_walls)
    room, sand = draw_room(small_x, big_x, big_y, room_walls, floor=False)
    result = part_one(room, sand)
    log.info("part_one", result=result)

    new_room, sand = draw_room(
        small_x - big_y,
        big_x + big_y,
        big_y + 1,
        room_walls,
        floor=True,
    )
    result = part_one(new_room, sand)
    log.info("part_two", result=result)


if __name__ == "__main__":
    main()
