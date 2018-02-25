import math
from problem import *
from sets import Set
# Breadth First Search
def remove_choice(paths):
    return  min(paths, key = len)

# Depth First Search 
def remove_choice2(paths):
    return  max(paths, key = len)

# A*
def remove_choice3(paths):
    pass


 #Heuristic shortest distance between two points 
def heuristic1(problem, state):
    discrete_matrix = problem.problem_description
    final_position = (0,0)
    for i, x in enumerate(discrete_matrix):
            if "g" in x:
                final_position = (i ,x.index("g"))
                break
    x2, y2 = final_position
    x1, y1 = state

    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2) 
    return distance

# Heuristic, steps to reach goal with no limmitations 
def heuristic2(problem, state):
    discrete_matrix = problem.problem_description
    final_position = (0, 0)
    for i, x in enumerate(discrete_matrix):
            if "g" in x:
                final_position = (i ,x.index("g"))
                break
    x2, y2 = final_position
    x1, y1 = state
    total_blocks = abs((y2 - y1) + (x2 - x1))
    return total_blocks

def graph_search(problem): 
    frontier = [[ problem.initial ]]
    explored = Set([])

    while True:
        if len(frontier):
            path = remove_choice(frontier)
            s = path[-1]
            explored.add(s)

            if problem.goal_test(s):
                return path

            for a in problem.actions(s):
                result = problem.result(s, a)

                if result not in explored:
                    new_path = []
                    new_path.extend( path )
                    new_path.append( problem.result(s, a) )
                    frontier.append(new_path)

        else: 
            return False
