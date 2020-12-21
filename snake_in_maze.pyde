# variables
w = 30
snake_start_cell = [0, 0]
snake_dest_cell = [0, 0]
snake = [[-5, 15], [5, 15], [15, 15]]
reached = True
solve_path = []
step = 0
path_step = 0

wall_open = [48, 49, 50, 51, 52, 53, 54]
all_cells_open_path = []

open_set = {}
closed_set = {}


def setup():
    global img, all_cells_open_path
    size(600, 600)
    img = loadImage('maze.jpg')
    frameRate(30)
    for r in range(img.height / w):
        for c in range(img.width / w):
            all_cells_open_path.append(get_open_wall(r, c))

def draw():
    global img, reached, step, path_step, solve_path
    background(255)
    image(img, 0, 0)
    if not reached:
        if solve_path[path_step] == 'r':
            snake.append(
                [snake[len(snake) - 1][0] + 10, snake[len(snake) - 1][1]])
        elif solve_path[path_step] == 'l':
            snake.append(
                [snake[len(snake) - 1][0] - 10, snake[len(snake) - 1][1]])
        elif solve_path[path_step] == 'b':
            snake.append(
                [snake[len(snake) - 1][0], snake[len(snake) - 1][1] + 10])
        elif solve_path[path_step] == 't':
            snake.append(
                [snake[len(snake) - 1][0], snake[len(snake) - 1][1] - 10])
        snake.pop(0)
        step += 1
        if step == 3:
            path_step += 1
            step = 0
        if path_step == len(solve_path):
            reached = True
    draw_snake()

def mousePressed():
    global path_step, step, w, reached, snake_start_cell, snake_dest_cell, solve_path, open_set, closed_set
    if reached and (mouseY // w)!=snake_dest_cell[0] and (mouseX // w) != snake_dest_cell[1]:
        snake_start_cell = [snake_dest_cell[0], snake_dest_cell[1]]
        snake_dest_cell = [mouseY // w, mouseX // w]
        solve_path = []
        open_set = {}
        closed_set = {}
        solve_path = main(snake_start_cell)
        step = 0
        path_step = 0
        reached = False


def draw_snake():
    global snake
    for s in snake:
        rectMode(CENTER)
        rect(s[0], s[1], 10, 10)


class Cell:

    def __init__(self, current, previous, dir):
        self.current = current
        self.previous = previous
        self.dir = dir

    def ravel_index(self):
        return self.current[0] * 20 + self.current[1]

def get_open_wall(r, c):
    global img, w
    center = center_of_cell(r, c)
    diro = []
    if red(img.get(center[0] + w / 2, center[1])) in wall_open:
        diro.append('r')
    if red(img.get(center[0] - w / 2, center[1])) in wall_open:
        diro.append('l')
    if red(img.get(center[0], center[1] - w / 2)) in wall_open:
        diro.append('t')
    if red(img.get(center[0], center[1] + w / 2)) in wall_open:
        diro.append('b')

    return diro


def center_of_cell(r, c):
    global w
    x = c * w + w / 2
    y = r * w + w / 2
    return [x, y]


def main(current):
    global all_cells_open_path, closed_set, open_set
    open_set[str(current)] = Cell(current, current, '')
    while True:
        new_open_set = {}
        for cell in open_set.values():
            closed_set[str(cell.current)] = cell
            for op in all_cells_open_path[cell.ravel_index()]:
                if op == 'r':
                    next = [cell.current[0], cell.current[1] + 1]
                elif op == 'b':
                    next = [cell.current[0] + 1, cell.current[1]]
                elif op == 'l':
                    next = [cell.current[0], cell.current[1] - 1]
                elif op == 't':
                    next = [cell.current[0] - 1, cell.current[1]]

                if str(next) in closed_set.keys() or str(next) in open_set.keys():
                    continue
                new_open_set[str(next)] = Cell(next, cell.current, op)
        del open_set
        open_set = new_open_set.copy()
        if check_goal(open_set):
            return goal_path(open_set, closed_set)

def check_goal(open_set):
    global snake_dest_cell
    if str(snake_dest_cell) in open_set.keys():
        return True
    else:
        return False

def goal_path(open_set, closed_set):
    global snake_dest_cell, snake_start_cell
    path = []
    cell = open_set[str(snake_dest_cell)]

    while cell.current != snake_start_cell:
        path.insert(0, cell.dir)
        cell = closed_set[str(cell.previous)]

    return path
