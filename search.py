

from problem import *
import sys
import time

algorithms = {
    'bfs': lambda frontier, problem, heuristics_function : min(frontier, key = len),
    'dfs': lambda frontier, problem, heuristics_function : max(frontier, key = len),
    'a_star': lambda frontier, problem, heuristics_function: a_star(frontier, problem, heuristics_function)
}


# Quitamos el camino de la frontera conforme al criterio del algoritmo implementado. 
def remove_choice(frontier, algorithm, problem, heuristics_function = None):
    selected_path = algorithms[algorithm](frontier, problem, heuristics_function)

    if (selected_path in frontier):
        frontier.remove(selected_path)

    return selected_path

def a_star(frontier, problem, heuristics_function):
    f_list = [
        (problem.path_cost(path) + heuristics_function(path[-1]), path)
        for path in frontier
    ]

    # Returnar el segundo elemento de la tupla denotada por el menor valor
    # en el primer elemento
    #print(f_list)
    return min(f_list, key = lambda tuple : tuple[0])[1]

def graph_search(problem, algorithm, heuristics_function = None):
    frontier = [[problem.initial()]]
    explored = set([])
    currentIterationIndex = 0
    maxIterations = None
    debug = True

    while True:
        if len(frontier):
            debug and print('---- Iteración ' + str(currentIterationIndex))
            debug and debug_print_frontier(frontier)
            debug and debug_print_frontier(explored)

            #t1 = time.time()
            chosen_path = remove_choice(frontier, algorithm, problem, heuristics_function)
            #t2 = time.time()

            #print("time: ", str(t2-t1))
            debug and print('Chosen path:\n ', chosen_path)

            end_of_path = chosen_path[-1]
            explored.add(end_of_path)

            if (maxIterations and currentIterationIndex == maxIterations):
                debug and print('Force quitting')
                sys.exit()

            if problem.goal_test(end_of_path):
                return chosen_path

            for action in problem.actions(end_of_path):
                result = problem.result(end_of_path, action)

                if result not in explored:
                    new_path = []
                    new_path.extend(chosen_path)
                    new_path.append(problem.result(end_of_path, action))
                    frontier.append(new_path)

            currentIterationIndex += 1
        else:
            return False

def debug_print_frontier(frontier):
    print('Current frontier\n[')
    for path in frontier:
        print('  ' + str(path))
    print(']')