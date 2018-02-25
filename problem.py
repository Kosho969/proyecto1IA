class Problem:
    def __init__ (self, discrete_matrix):
        self.problem_description = discrete_matrix
        # TODO: Verificar que que la matriz discreta tenga un inicio,
        # de lo contrario gracefully avisar
        if (not self.initial()):
            raise ValueError('No se encontró estado inicial en la discretización')

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

        if (y - 1 > 0):
            if (self.problem_description[y - 1][x] == '0'):
                actions.append('up')

        if (x - 1 > 0):
            if (self.problem_description[y][x - 1] == '0'):
                actions.append('left')

        if (y + 1 < len(self.problem_description)):
            if (self.problem_description[y + 1][x] == '0'):
                actions.append('down')

        if (x + 1 < len(self.problem_description[0])):
            if (self.problem_description[y][x + 1] == '0'):
                actions.append('right')

        return actions

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

    def goal_test(self, state):
        y, x = state

        if (self.problem_description[y][x] == 'g'):
            return True

        return False

    def step_cost(self, state, action, state_1):
        return 1

    def path_cost(self, states):
        return (len(states) -1)
