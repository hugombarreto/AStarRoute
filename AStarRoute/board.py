import pygame
import numpy as np
from a_star import Grid, Node


def compute_path(grid, start, finish, show_try_path=False):
    graph_grid = Grid(get_numpy_grid_from_list_grid(grid))
    path_trace = graph_grid.a_star(Node(start), Node(finish))

    if show_try_path:
        for key in path_trace.keys():
            grid[key[0]][key[1]] = 5

    if finish not in path_trace:
        return grid

    current_node = path_trace[finish].parent

    while current_node != start:
        grid[current_node[0]][current_node[1]] = 4
        current_node = path_trace[current_node].parent

    return grid


def set_screen(window_size, grid_size, margin):
    grid_tile_width = ((window_size[0] - margin) / grid_size[0]) - margin
    grid_tile_height = ((window_size[1] - margin) / grid_size[1]) - margin
    screen = pygame.display.set_mode(window_size, pygame.HWSURFACE |
                                     pygame.DOUBLEBUF | pygame.RESIZABLE)

    return screen, grid_tile_width, grid_tile_height


def get_numpy_grid_from_list_grid(list_grid):
    return np.array(map(lambda column: map(lambda i: np.inf if i == 1 else 1,
                                           column), list_grid))


def main():
    # colors
    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)

    # board colors
    background_color = black
    tile_color_filled = black
    tile_color_blank = white
    start_color = red
    finish_color = green
    path_color = blue
    try_color = (200, 200, 200)

    margin = 1
    window_size = (1000, 1000)
    grid_size = (100, 100)

    screen, grid_tile_width, grid_tile_height = set_screen(window_size,
                                                           grid_size, margin)

    grid = [[0] * grid_size[1] for i in xrange(grid_size[0])]
    changes_grid = [[False] * grid_size[1] for i in xrange(grid_size[0])]
    done = False
    mouse_pressed = False
    screen_modf = True
    user_set_start = False
    start_tile = None
    end_tile = None

    pygame.display.set_caption("A* Testing")
    clock = pygame.time.Clock()

    while not done:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                done = True

            elif event.type == pygame.VIDEORESIZE:
                mouse_pressed = False
                window_size = event.dict['size']
                screen, grid_tile_width, grid_tile_height = \
                    set_screen(window_size, grid_size, margin)
                screen_modf = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    if (start_tile and end_tile) is not None:
                        grid = compute_path(grid, start_tile, end_tile, True)
                        screen_modf = True
                if event.key == pygame.K_c:
                    grid = [[0] * grid_size[1] for i in xrange(grid_size[0])]
                    changes_grid = [[False] * grid_size[1] for i in
                                    xrange(grid_size[0])]
                    done = False
                    mouse_pressed = False
                    screen_modf = True
                    user_set_start = False
                    start_tile = None
                    end_tile = None
                if ((event.key == pygame.K_s) and
                   ((start_tile and end_tile) is not None)):
                    grid_object = Grid(get_numpy_grid_from_list_grid(grid))
                    grid_object.save("grid", "../tests/boards/",
                                     start_tile, end_tile)

            if event.type == pygame.MOUSEMOTION and mouse_pressed:
                pos = pygame.mouse.get_pos()
                y = pos[0] // (grid_tile_width + margin)
                x = pos[1] // (grid_tile_height + margin)
                if x >= grid_size[0] or y >= grid_size[1]:
                    continue
                if not changes_grid[x][y]:
                    changes_grid[x][y] = True
                    if (x, y) == start_tile:
                        start_tile = None
                    if (x, y) == end_tile:
                        end_tile = None
                    grid[x][y] = int(not grid[x][y])
                    screen_modf = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[2]:
                    pos = pygame.mouse.get_pos()
                    y = pos[0] // (grid_tile_width + margin)
                    x = pos[1] // (grid_tile_height + margin)
                    if x >= grid_size[0] or y >= grid_size[1]:
                        continue
                    if not changes_grid[x][y]:
                        if user_set_start:
                            if end_tile is not None:
                                grid[end_tile[0]][end_tile[1]] = 0
                            grid[x][y] = 3
                            end_tile = (x, y)
                            if end_tile == start_tile:
                                start_tile = None
                        else:
                            if start_tile is not None:
                                grid[start_tile[0]][start_tile[1]] = 0
                            grid[x][y] = 2
                            start_tile = (x, y)
                            if end_tile == start_tile:
                                end_tile = None
                        user_set_start = not user_set_start
                        screen_modf = True
                else:
                    mouse_pressed = True

            if event.type == pygame.MOUSEBUTTONUP:
                mouse_pressed = False
                changes_grid = [[False] * grid_size[1] for i in
                                xrange(grid_size[0])]

        if screen_modf:
            screen.fill(background_color)
            for x, row in enumerate(grid):
                for y, v in enumerate(row):
                    color = [tile_color_blank, tile_color_filled, start_color,
                             finish_color, path_color, try_color][v]
                    pygame.draw.rect(screen, color,
                                     [(margin + grid_tile_width) * y + margin,
                                      (margin + grid_tile_height) * x + margin,
                                      grid_tile_width, grid_tile_height])

            pygame.display.flip()
            screen_modf = False
        clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    main()
