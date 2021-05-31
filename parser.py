def read(filename):
    file = open(filename)

    dim = int(file.readline())
    grid = []

    for i in range(dim**2):
        line = file.readline().split('\n')[0].split(' ')
        for j in range(dim**2):
            if int(line[j]) != 0:
                grid.append((i, j, int(line[j])))

    file.close()

    return dim, grid


if __name__ == "__main__":
    n, initial_grid = read('sudoku_16_16_1.txt')
    print(n)
    print(initial_grid)
