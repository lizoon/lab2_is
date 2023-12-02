
def convert_from_ascii(maze):
    maze = maze.strip().replace("|", "3").replace("+", "6").replace("-", "4").replace(".", "2").replace("=", "1")
    m = []
    for l in maze.splitlines():
        if not l:
            pass
        row = list(map(int, l))
        m.append(row)
    #list(map(int, maze.splitlines()))

    return m

