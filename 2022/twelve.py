from collections import defaultdict

import structlog

from utils import read_file

log = structlog.get_logger()

DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]


def parse_heights(lines):
    heights = []
    for line in lines:
        height_line = [char for char in line.strip()]
        heights.append(height_line)
    return heights


def bfs(grid, root_point, reverse=False, destination=None):
    paths = defaultdict(lambda: 10e15)
    paths[(root_point[1], root_point[0])] = 0
    to_search = [(root_point[0], root_point[1], 0)]
    while len(to_search) > 0:
        x, y, steps = to_search[0]
        to_search = to_search[1:]
        origin_height = ord(grid[y][x])

        for (dx, dy) in DIRECTIONS:
            Nx = x + dx
            Ny = y + dy
            if Nx < 0 or Nx >= len(grid[0]) or Ny < 0 or Ny >= len(grid):
                continue

            destination_height = ord(grid[Ny][Nx])

            if not reverse and not origin_height - destination_height >= -1:
                continue

            if reverse and not destination_height - origin_height >= -1:
                continue

            if paths[(Ny, Nx)] > steps + 1:
                paths[(Ny, Nx)] = steps + 1
                to_search.append((Nx, Ny, steps + 1))
                if destination and (Nx, Ny) == destination:
                    return paths
                if not destination and grid[Ny][Nx] == "a":
                    return paths

    return paths


def solve_one(heights, Sx, Sy, Ex, Ey):
    paths = bfs(heights, (Sx, Sy), reverse=False, destination=(Ex, Ey))
    return paths[(Ey, Ex)]


def solve_two(heights, Ex, Ey):
    paths = bfs(heights, (Ex, Ey), reverse=True)
    return min([dist for ((y, x), dist) in paths.items() if heights[y][x] == "a"])


def main():
    lines = read_file("input_12.txt")
    heights = parse_heights(lines)

    for y, row in enumerate(heights):
        for x, char in enumerate(row):
            if char == "S":
                Sx, Sy = x, y
            if char == "E":
                Ex, Ey = x, y

    heights[Sy][Sx] = "a"
    heights[Ey][Ex] = "z"
    result = solve_one(heights, Sx, Sy, Ex, Ey)
    log.info("part_one", result=result)
    result = solve_two(heights, Ex, Ey)
    log.info("part_two", result=result)


if __name__ == "__main__":
    main()
