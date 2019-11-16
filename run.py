import numpy as np
import sys
import random
import matplotlib.pyplot as plot
import matplotlib.animation as animation



dx = [-1, 0, 1, 1, 1, 0, -1, -1]
dy = [1, 1, 1, 0, -1, -1, -1, 0]

def place_exists(n, x, y):
        return x >= 0 and y >= 0 and x < n and y < n

def is_satisfied(Map, x, y):
    neighbours = {1:0, 2:0} # первый элемент - колво соседей agent1, второй элемент - agent2

    # пробегаемся по всем соседям одного элемента. Считаем сколько соседей разного вида агентов, считаем процет и чекаем с R
    for i in range(1,3):
        for k in range(len(dx)):
            if place_exists(len(Map), x + dx[k], y + dy[k]) and Map[x + dx[k]][y + dy[k]] == i:
                neighbours[i] += 1
    # нам нужен процент каждого агента относительно всех соседей
    total = sum(neighbours.values())
    if total > 0:
        for i in range(1,3):
            neighbours[i] = neighbours[i] * 100.0 / total

    t = Map[x][y]
    # isn't sutisfied cz very little amount type of agent around 
    if neighbours[t] < quantity[t]:
        return False
        
    return True


def find_positions(Map, x, y):
    n = len(Map)
    t = Map[x][y]
    Map[x][y] = 0
    available = []
    # формируем список доступных мест
    for i in range(n):
        for j in range(n):
            if Map[i][j] == 0 and ((i,j) not in available): #доступные места: где нолик
                Map[i][j] = t
                available.append((i, j))
                Map[i][j] = 0 
    Map[x][y] = t
    return available


def make_step(frame, image, Map):
    global moved
    moved = 0
    def cant_move(list):
        for x, y in list:
            available = find_positions(Map, x, y)
            if len(available) > 0:
                return False
        return True

    n = len(Map)
    unhappy = [(i, j) for i in range(n) for j in range(n) if Map[i][j] != 0 and not is_satisfied(Map, i, j)]
    
    if cant_move(unhappy):
        sys.exit()
        print('Deadlock')
        return None

    while len(unhappy) > 0:
        x, y = random.choice(unhappy)
        available = find_positions(Map, x, y)
        
        while len(available) == 0:
            x, y = random.choice(unhappy)
            available = find_positions(Map, x, y)
        
        X_new, Y_new = random.choice(available)
        Map[X_new][Y_new] = Map[x][y]
        Map[x][y] = 0
        unhappy.remove((x,y))
        moved += 1
    
    print(moved)
    image.set_data(Map)
    return image

    
def random_Map(n, sizes):
    '''
    Aimed to fill Map with size nxn.
    Filled by 3 types: 0  (empty spaces), 1 and 2 (two agents)
    '''
    Map = [[0 for i in range(n)] for j in range(n)]
    coords = [(i, j) for i in range(n) for j in range(n)]
    
    for t in range(1,3): # Номер агента 0(первый), 1(второй)
        # тут процесс заполнения сетки: у нас сетка 30 на 30, по 440 агентов => 20 пустых
        for _ in range(sizes[t-1]):
            x, y = random.choice(coords)
            coords.remove((x, y))
            Map[x][y] = t
 
    return Map

def run(n, sizes):
    # тут просто идёт рисование сетки
    Map = random_Map(n, sizes)

    fig, ax = plot.subplots()
    plot.axis('off')
    #fig.set_size_inches(14,11)
    
    ax.set_title(f'Schelling’s Model with R = {R}')
    image = ax.imshow(Map)
    ani = animation.FuncAnimation(fig, make_step, frames=10, fargs=(image, Map), interval=10)
    ani.save('Scheling_R {}.gif'.format(R), fps=10, dpi=300)
    plot.show()

def two_agents(R):
    n = 30 #размер 100x100 
    sizes = [400, 400]
    global quantity
    quantity = {1: R * 100, 2: R * 100}
    
    return (n, sizes)

if __name__ == '__main__':
    R = 6/8
    n, sizes = two_agents(R)
    run(n, sizes)
