import heapq

import structlog

from utils import read_file

logger = structlog.get_logger()


def parse_heat_losses(lines: list[str]) -> list[str]:
    heat_losses = []
    for line in lines:
        heat_losses.append([int(value) for value in line.strip()])
    return heat_losses


def bfs(grid, part: int = 1):
    to_search = [(0, 0, 0, -1, -1)]
    done = {}

    while len(to_search) > 0:
        # logger.info("lengths", searches=len(to_search), done=len(done))
        heat_cost, x, y, last_direction, direction_count = heapq.heappop(to_search)
        # to_search = to_search[1:]
        if (x, y, last_direction, direction_count) in done:
            # assert heat_cost >= done[(x, y, last_direction, direction_count)]
            continue

        done[(x, y, last_direction, direction_count)] = heat_cost
        for direction, (dx, dy) in enumerate([(-1, 0), (0, 1), (1, 0), (0, -1)]):
            Nx = x + dx
            Ny = y + dy

            new_direction = direction
            new_direction_count = 1 if new_direction != last_direction else direction_count + 1

            not_reverse = (new_direction + 2) % 4 != last_direction
            if part == 1:
                is_valid = new_direction_count <= 3
            if part == 2:
                is_valid = (
                    new_direction_count <= 10
                    and (new_direction == last_direction or direction_count >= 4 or direction_count == -1)
                    and not (Ny == len(grid) - 1 and Nx == len(grid[0]) - 1 and new_direction_count < 4)
                )

            if is_valid and 0 <= Nx < len(grid[0]) and 0 <= Ny < len(grid) and not_reverse:
                destination_heat_loss = grid[Ny][Nx]
                heapq.heappush(
                    to_search,
                    (heat_cost + destination_heat_loss, Nx, Ny, new_direction, new_direction_count),
                )

    return done


def get_first_answer(done, grid):
    values = []
    max_y = len(grid) - 1
    max_x = len(grid[0]) - 1
    for (x, y, _, _), value in done.items():
        if x == max_x and y == max_y:
            values.append(value)
    return min(values)


def main():
    lines = read_file("input_17.txt")
    heat_losses = parse_heat_losses(lines)
    done = bfs(heat_losses)
    first_answer = get_first_answer(done, heat_losses)
    logger.info("first_question", answer=first_answer)

    done = bfs(heat_losses, part=2)
    first_answer = get_first_answer(done, heat_losses)
    logger.info("first_question", answer=first_answer)


if __name__ == "__main__":
    main()
