class Problem:
    def __init__ (self, discrete_matrix):
        self.problem_description = discrete_matrix

    def initial(self):
        #print("Problems: ",self.problem_description)
        initial_position = (0,0)
        for i, x in enumerate(self.problem_description):
            if "s" in x:
                return (i, x.index("s"))

    def actions(self, state):
        actions = []
        y, x = state
        if ( y - 1 > 0 ):
            if( self.problem_description[y - 1][x] == "0"):
                actions.append("up")
        if ( x - 1 > 0 ):
            if( self.problem_description[y][x - 1] == "0"):
                actions.append("left")
        if ( y + 1 < len(self.problem_description) ):
            if( self.problem_description[y + 1][x] == "0"):
                actions.append("down")
        if ( x + 1 < len(self.problem_description[0]) ):
            if( self.problem_description[y][x + 1] == "0"):
                actions.append("right")
        return actions


    def result(self, state,action):
        y, x = state
        if( action == "up" ):
            y = y - 1
            return  (y, x)
        elif( action == "left" ):
            x = x - 1
            return  (y, x)
        elif( action == "down" ):
            y = y + 1
            return  (y, x)
        elif( action == "right" ):
            x = x + 1
            return  (y, x)

    def goal_test(self, state):
        y, x = state
        if ( self.problem_description[y][x] == "g" ):
            return True
        else:
            return False

    def step_cost(self, state, action, state_1):
        return 1 

    def path_cost(self, states):
        return ( len(states) -1 )