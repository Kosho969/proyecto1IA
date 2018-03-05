import math

# Inicio Framework del problema.
class Problem:
    def __init__ (self, discrete_matrix):
        self.problem_description = discrete_matrix
        self.goals = self.goal_()
        if (not self.initial()):
            print(self.initial())
            raise ValueError('No se encontró estado inicial en la discretización')
        print(self.initial())

    # Devuelve la tupla (x, y) del punto de partida rojo, identificado
    # como 's' en los colores de problem_description
    def initial(self):
        initial_position = (0, 0)
        for i, x in enumerate(self.problem_description):
            if 's' in x:
                return (i, x.index('s'))

    # Devuelve las acciones válidas a partir de una tupla
    # (x, y)
    def actions(self, state):
        actions = []
        y, x = state

        if (y - 1 >= 0):
            if (self.is_valid_state(self.problem_description[y - 1][x])):
                actions.append('up')

        if (x - 1 >= 0):
            if (self.is_valid_state(self.problem_description[y][x - 1])):
                actions.append('left')

        if (y + 1 < len(self.problem_description)):
            if (self.is_valid_state(self.problem_description[y + 1][x])):
                actions.append('down')

        if (x + 1 < len(self.problem_description[0])):
            if (self.is_valid_state(self.problem_description[y][x + 1])):
                actions.append('right')

        return actions

    def is_valid_state(self, state):
        return state == '0' or state == 'g'

    # A devuelve la tupla (x, y) resultante de aplicar
    # action sobre un estado, es decir sobre una tupla
    # (x_o, y_o) inicial
    def result(self, state, action):
        y, x = state

        if (action == 'up'):
            y = y - 1
            return (y, x)

        elif (action == 'left'):
            x = x - 1
            return (y, x)

        elif (action == 'down'):
            y = y + 1
            return (y, x)

        elif (action == 'right'):
            x = x + 1
            return (y, x)

    # Verificamos que haya una meta
    def goal_test(self, state):
        y, x = state
        if (self.problem_description[y][x] == 'g'):
            return True
        return False

    # Costo de dar un paso en nuestra matriz
    def step_cost(self, state, action, state_1):
        return 1

    # Costo de uno de los caminos
    def path_cost(self, states):
        return (len(states) - 1)

# FIN Framework

    # Obtener arreglo con las metas 
    def goal_(self):
        initial_position = (0, 0)
        goals = []
        for i, x in enumerate(self.problem_description):
            if 'g' in x:
                goals.append((i, x.index('g')))
        return goals

    # Heuristic shortest distance between two points
    def shortest_distance_heuristic(self, state):
        if len(self.goals) == 0:
            return 0
        discrete_matrix = self.problem_description
        distances = []
        for goal in self.goals:
            final_position = goal
            x2, y2 = final_position
            x1, y1 = state
            distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            distances.append(distance)
        return min(distances)

    # Heuristic steps to reach goal with no limmitations 
    def steps_to_reach_goal_heuristic(self, state):
        if len(self.goals) == 0:
            return 0
        discrete_matrix = self.problem_description
        steps = []
        for goal in self.goals:
            final_position = goal
            x2, y2 = final_position
            x1, y1 = state
            total_blocks = abs((y2 - y1) + (x2 - x1))
            steps.append(total_blocks)

        return min(steps)
