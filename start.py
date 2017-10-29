from Framework import matrix, menu

matrix = matrix.MatrixSimulator()

menu = menu.Menu(matrix)

while 1:
    menu.update(matrix.get_keys())
    menu.draw()
