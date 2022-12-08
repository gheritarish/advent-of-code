import structlog

from utils import read_file

log = structlog.get_logger()


class Tree:
    def __init__(self, height):
        self.height = height
        self.viewed = 0

    def scenic_score(self, forest, x, y, max_x, max_y):
        if x > 0:
            value_x_inf = 0
            for i in range(x - 1, -1, -1):
                if forest[i][y].height >= self.height:
                    value_x_inf += 1
                    break
                else:
                    value_x_inf += 1
        else:
            value_x_inf = 1

        if x < max_x - 1:
            value_x_sup = 0
            for i in range(x + 1, max_x):
                if forest[i][y].height >= self.height:
                    value_x_sup += 1
                    break
                else:
                    value_x_sup += 1
        else:
            value_x_sup = 1

        if y > 0:
            value_y_inf = 0
            for i in range(y - 1, -1, -1):
                if forest[x][i].height >= self.height:
                    value_y_inf += 1
                    break
                else:
                    value_y_inf += 1
        else:
            value_y_inf = 1

        if y < max_y - 1:
            value_y_sup = 0
            for i in range(y + 1, max_y):
                if forest[x][i].height >= self.height:
                    value_y_sup += 1
                    break
                else:
                    value_y_sup += 1
        else:
            value_y_sup = 1

        return value_x_inf * value_x_sup * value_y_inf * value_y_sup


def parse_trees(lines):
    trees = []
    for line in lines:
        rank = [Tree(int(char)) for char in line.strip()]
        trees.append(rank)
    return trees


def solve_one(forest):
    for i in range(len(forest)):
        heighest = -1
        for j in range(len(forest[i])):
            if forest[i][j].height > heighest:
                heighest = forest[i][j].height
                forest[i][j].viewed = 1

        heighest = -1
        for k in range(len(forest[i]) - 1, -1, -1):
            if forest[i][k].height > heighest:
                heighest = forest[i][k].height
                forest[i][k].viewed = 1

    for i in range(len(forest[0])):
        heighest = -1
        for j in range(len(forest)):
            if forest[j][i].height > heighest:
                heighest = forest[j][i].height
                forest[j][i].viewed = 1

        heighest = -1
        for k in range(len(forest) - 1, -1, -1):
            if forest[k][i].height > heighest:
                heighest = forest[k][i].height
                forest[k][i].viewed = 1

    return sum(
        sum(forest[i][k].viewed for k in range(len(forest[0])))
        for i in range(len(forest))
    )


def solve_two(forest):
    max_scenic_score = 0
    for i in range(len(forest)):
        for j in range(len(forest[i])):
            if forest[i][j].viewed == 1:
                scenic = forest[i][j].scenic_score(
                    forest,
                    i,
                    j,
                    len(forest[i]),
                    len(forest),
                )
                if scenic >= max_scenic_score:
                    max_scenic_score = scenic
    return max_scenic_score


def main():
    lines = read_file("input_08.txt")
    forest = parse_trees(lines)
    result = solve_one(forest)
    log.info("part_one", result=result)
    result = solve_two(forest)
    log.info("part_two", result=result)


if __name__ == "__main__":
    main()
