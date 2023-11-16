
def find_path(start, goal, level, turns_allowed):
    open_list = []
    closed_list = []

    def heuristic(node):
        return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

    open_list.append((start, 0))
    came_from = {}

    g_score = {(x, y): float('inf') for y, row in enumerate(level) for x, cell in enumerate(row)}
    g_score[start] = 0

    while open_list:
        current, current_g = min(open_list, key=lambda item: item[1] + heuristic(item[0]))
        open_list.remove((current, current_g))

        if current == goal:
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            path.reverse()
            return path

        closed_list.append(current)

        for neighbor in get_neighbors(current, level, turns_allowed):
            if neighbor in closed_list:
                continue
            tentative_g = current_g + 1  # Assuming a constant cost for moving from one node to another
            if neighbor not in open_list or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score = tentative_g + heuristic(neighbor)
                if neighbor not in [item[0] for item in open_list]:
                    open_list.append((neighbor, f_score))

    return None


def get_neighbors(node, level, turns_allowed):
    x, y = node
    neighbors = []
    if turns_allowed[0] and x < len(level[y]) - 1 and level[y][x + 1] < 3:
        neighbors.append((x + 1, y))
    if turns_allowed[1] and x > 0 and level[y][x - 1] < 3:
        neighbors.append((x - 1, y))
    if turns_allowed[2] and y < len(level) - 1 and level[y + 1][x] < 3:
        neighbors.append((x, y + 1))
    if turns_allowed[3] and y > 0 and level[y - 1][x] < 3:
        neighbors.append((x, y - 1))
    return neighbors


def get_direction(current, next_node):
    x1, y1 = current
    x2, y2 = next_node
    if x1 < x2:
        return 0  # RIGHT
    elif x1 > x2:
        return 1  # LEFT
    elif y1 < y2:
        return 3  # DOWN
    elif y1 > y2:
        return 2  # UP


def get_targets(blink_x, blink_y, ink_x, ink_y, pink_x, pink_y, clyd_x, clyd_y, player_x, player_y):
    if player_x < 450:
        runaway_x = 900
    else:
        runaway_x = 0
    if player_y < 450:
        runaway_y = 900
    else:
        runaway_y = 0
    return_target = (380, 400)

    if not blinky.dead:
        if 340 < blink_x < 560 and 340 < blink_y < 500:
            blink_target = (400, 100)
        else:
            blink_target = (player_x, player_y)
    else:
        blink_target = return_target

    if not inky.dead:
        # Calculate Inky's target position based on Clyde's position and Pac-Man's position
        inky_target_x = 2 * player_x - blink_x
        inky_target_y = 2 * player_y - blink_y

        if 340 < ink_x < 560 and 340 < ink_y < 500:
            ink_target = (400, 100)
        else:
            ink_target = (inky_target_x, inky_target_y)
    else:
        ink_target = return_target

    if not pinky.dead:
        if 340 < pink_x < 560 and 340 < pink_y < 500:
            pink_target = (400, 100)
        else:
            if direction == 0:
                pink_target = (player_x+100, player_y)
            elif direction == 1:
                pink_target = (player_x-100, player_y)
            elif direction == 2:
                pink_target = (player_x, player_y-100)
            else:
                pink_target = (player_x, player_y+100)

    else:
        pink_target = return_target

    if not clyde.dead:
        if 340 < clyd_x < 560 and 340 < clyd_y < 500:
            clyd_target = (400, 100)
        else:
            clyd_target = (player_x, player_y)
    else:
        clyd_target = return_target

    return [blink_target, ink_target, pink_target, clyd_target]
