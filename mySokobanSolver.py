
'''

    2019 CAB320 Sokoban assignment

The functions and classes defined in this module will be called by a marker script.
You should complete the functions and classes according to their specified interfaces.

You are not allowed to change the defined interfaces.
That is, changing the formal parameters of a function will break the
interface and triggers to a fail for the test of your code.

# by default does not allow push of boxes on taboo cells
SokobanPuzzle.allow_taboo_push = False

# use elementary actions if self.macro == False
SokobanPuzzle.macro = False

'''

# you have to use the 'search.py' file provided
# as your code will be tested with this specific file
import search
import sokoban
import itertools
import math
import copy

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -



def my_team():
    '''
    Return the list of the team members of this assignment submission as a list
    of triplet of the form (student_number, first_name, last_name)

    '''
    return [ (9956522, 'Nam', 'Nguyen'), (9809589, 'Dylan', 'Pryke-Watanabe'), (10008217, 'Texas', 'Barnes') ]

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def taboo_cells(warehouse):
    '''
    Identify the taboo cells of a warehouse. A cell inside a warehouse is
    called 'taboo' if whenever a box get pushed on such a cell then the puzzle
    becomes unsolvable.
    When determining the taboo cells, you must ignore all the existing boxes,
    simply consider the walls and the target cells.
    Use only the following two rules to determine the taboo cells;
     Rule 1: if a cell is a corner inside the warehouse and not a target,
             then it is a taboo cell.
     Rule 2: all the cells between two corners inside the warehouse along a
             wall are taboo if none of these cells is a target.

    @param warehouse: a Warehouse object

    @return
       A string representing the puzzle with only the wall cells marked with
       an '#' and the taboo cells marked with an 'X'.
       The returned string should NOT have marks for the worker, the targets,
       and the boxes.
    '''

    ##Floor check

    x_wall = list(zip(*warehouse.walls))[0]
    y_wall = list(zip(*warehouse.walls))[1]
    max_x = max(x_wall) + 1
    max_y = max(y_wall) + 1
    perm_x = list(range(max_x))
    perm_y = list(range(max_y))
    all_xy = list(itertools.product(perm_x,perm_y))

    floor = []

    for coord in all_xy:
        row = coord[0]
        wall_at_row = [wall for wall in warehouse.walls if wall[0] == row]
        wall_column = list(zip(*wall_at_row))[1]
        if coord[1] < max(wall_column) and coord[1] > min(wall_column):
            floor.append(coord)



    ##Corner check

    corners = []
    next_walls = []
    print(warehouse.targets)


    for cells in floor:
        x, y = cells[0], cells[1]
        if cells not in warehouse.worker and cells not in warehouse.targets and cells not in warehouse.boxes:
            if (x + 1, y) in warehouse.walls and (x, y + 1) in warehouse.walls:
                corners.append(cells)

            elif (x + 1, y) in warehouse.walls and (x, y - 1) in warehouse.walls:
                corners.append(cells)

            elif (x - 1, y) in warehouse.walls and (x, y - 1) in warehouse.walls:
                corners.append(cells)

            elif (x - 1, y) in warehouse.walls and (x, y + 1) in warehouse.walls:
                corners.append(cells)

        ## Wall Check
        if cells not in warehouse.worker and cells not in warehouse.targets and cells not in warehouse.boxes:
            if (x + 1, y) in warehouse.walls:
                next_walls.append(cells)

            if (x - 1, y) in warehouse.walls:
                next_walls.append(cells)

            if (x, y + 1) in warehouse.walls:
                next_walls.append(cells)

            if (x, y - 1) in warehouse.walls:
                next_walls.append(cells)

    print(corners)


    ##Remove floor cells in the same row or column as target
    for target in warehouse.targets:
        next_walls = [next for next in next_walls if next[0] != target[0] and next[1] != target[1]]

    map = ""
    for y in range(max_y):
        for x in range(max_x):
            if (x,y) in warehouse.walls:
                map += "#"
            elif (x,y) in corners:
                map += "X"
            elif (x,y) in next_walls:
                map += "X"
            else:
                map += " "
        if y < max_y - 1:
            map += "\n"

    return map

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#Function to check if there is an adjacent cell
def cell_adjacent(cell, direction):

    if direction == "Left":
        return(cell[0] - 1, cell[1])

    elif direction == "Right":
        return(cell[0] + 1, cell[1])

    elif direction == "Up":
        return(cell[0], cell[1] - 1)

    elif direction == "Down":
        return(cell[0], cell[1] + 1)

class SokobanPuzzle(search.Problem):
    '''
    An instance of the class 'SokobanPuzzle' represents a Sokoban puzzle.
    An instance contains information about the walls, the targets, the boxes
    and the worker.

    Your implementation should be fully compatible with the search functions of
    the provided module 'search.py'.

    Each instance should have at least the following attributes
    - self.allow_taboo_push
    - self.macro

    When self.allow_taboo_push is set to True, the 'actions' function should
    return all possible legal moves including those that move a box on a taboo
    cell. If self.allow_taboo_push is set to False, those moves should not be
    included in the returned list of actions.

    If self.macro is set True, the 'actions' function should return
    macro actions. If self.macro is set False, the 'actions' function should
    return elementary actions.


    '''
    '''

            "INSERT YOUR CODE HERE"

        Revisit the sliding puzzle and the pancake puzzle for inspiration!

        Note that you will need to add several functions to
        complete this class. For example, a 'result' function is needed
        to satisfy the interface of 'search.Problem'.
    '''


    def __init__(self, warehouse):
        self.warehouse = warehouse
        self.initial = ((warehouse.worker),) + tuple(warehouse.boxes)
        self.targets = warehouse.targets
        self.taboo_list = taboo_cells(warehouse)
        self.macro = False
        self.allow_taboo_push = False;  
        
    # function for the availible actions
    def actions(self, state):
        """
        Return the list of actions that can be executed in the given state.

        As specified in the header comment of this class, the attributes
        'self.allow_taboo_push' and 'self.macro' should be tested to determine
        what type of list of actions is to be returned.
        """
        # actions = ['Left', 'Down', 'Right', 'Up']
        actions = []

        if self.allow_taboo_push:
            adjacent_cell_up = cell_adjacent(state[0], "Up")
            adjacent_cell_down = cell_adjacent(state[0], "Down")
            adjacent_cell_left = cell_adjacent(state[0], "Left")
            adjacent_cell_right = cell_adjacent(state[0], "Right")

            # check if valid cell is above.
            if adjacent_cell_up not in self.warehouse.walls and adjacent_cell_up not in state[1:]:
                actions += ("Up")
            elif adjacent_cell_up in state[1:]:
                adjacent_box_up = cell_adjacent(adjacent_cell_up, "Up")
                if adjacent_box_up not in self.taboo_list and adjacent_box_up not in self.warehouse.walls and adjacent_box_up not in state[1:]:
                    actions+= ("Up")

            # check if valid cell is below.
            if adjacent_cell_down not in self.warehouse.walls and adjacent_cell_down not in state[1:]:
                actions += ("Down")
            elif adjacent_cell_down in state[1:]:
                adjacent_box_down = cell_adjacent(adjacent_cell_down, "Down")
                if adjacent_box_down not in self.taboo_list and adjacent_box_down not in self.warehouse.walls and adjacent_box_down not in state[1:]:
                    actions+= ("Down")

            # check if valid cell is to the left
            if adjacent_cell_left not in self.warehouse.walls and adjacent_cell_left not in state[1:]:
                actions += ("Left")
            elif adjacent_cell_left in state[1:]:
                adjacent_box_left = cell_adjacent(adjacent_cell_left, "Left")
                if adjacent_box_left not in self.taboo_list and adjacent_box_left not in self.warehouse.walls and adjacent_box_left not in state[1:]:
                    actions+= ("Left")

            # check if valid cell is to the right
            if adjacent_cell_right not in self.warehouse.walls and adjacent_cell_right not in state[1:]:
                actions += ("Right")
            elif adjacent_cell_right in state[1:]:
                adjacent_box_right = cell_adjacent(adjacent_cell_right, "Right")
                if adjacent_box_right not in self.taboo_list and adjacent_box_right not in self.warehouse.walls and adjacent_box_right not in state[1:]:
                    actions+= ("Right")

            return actions

        elif self.allow_taboo_push:
            #for the elementary with no macro
        # if !self.macro or self.allow_taboo_push:
            adjacent_cell_up = cell_adjacent(state[0], "Up")
            adjacent_cell_down = cell_adjacent(state[0], "Down")
            adjacent_cell_left = cell_adjacent(state[0], "Left")
            adjacent_cell_right = cell_adjacent(state[0], "Right")

            # check if valid cell is above.
            if adjacent_cell_up not in self.warehouse.walls and adjacent_cell_up not in state:
                actions += ("Up")
            elif adjacent_cell_up in state:
                adjacent_box_up = cell_adjacent(adjacent_cell_up, "Up")
                if adjacent_box_up not in self.warehouse.walls and adjacent_box_up not in state:
                    actions+= ("Up")

            # check if valid cell is below.
            if adjacent_cell_down not in self.warehouse.walls and adjacent_cell_down not in state:
                actions += ("Down")
            elif adjacent_cell_down in state:
                adjacent_box_down = cell_adjacent(adjacent_cell_down, "Down")
                if adjacent_box_down not in self.warehouse.walls and adjacent_box_down not in state:
                    actions+= ("Down")

            # check if valid cell is to the left
            if adjacent_cell_left not in self.warehouse.walls and adjacent_cell_left not in state:
                actions += ("Left")
            elif adjacent_cell_left in state:
                adjacent_box_left = cell_adjacent(adjacent_cell_left, "Left")
                if adjacent_box_left not in self.warehouse.walls and adjacent_box_left not in state:
                    actions+= ("Left")

            # check if valid cell is to the right
            if adjacent_cell_right not in self.warehouse.walls and adjacent_cell_right not in state:
                actions += ("Right")
            elif adjacent_cell_right in state:
                adjacent_box_right = cell_adjacent(adjacent_cell_right, "Right")
                if adjacent_box_right not in self.warehouse.walls and adjacent_box_right not in state:
                    actions+= ("Right")

            return actions

    # function for checm
    def result(self, state, action):
        # assert the action is doable in the current state
        assert action in self.actions(state)
        new_state = ()
        new_state = copy.deepcopy(state)

        # Check if worker is pushing a box
        if cell_adjacent(state[0], action) in state[1:]:
            i = 1
            #find box being pushed
            for box in state[1:]:
                # get direction and new position of box
                if cell_adjacent(state[0], action) == box:
                    new_state_list = list(new_state)
                    new_state_list[i] = cell_adjacent(box, action)
                    new_state = tuple(new_state_list)
                    break
                i += 1

            new_state_list = list(new_state)
            # move the worker to where the box used to be before being pushed
            new_state_list[0] = cell_adjacent(state[0], action)
            new_state = tuple(new_state_list)

        # if not pushing a box update the position
        else:
            new_state_list = list(new_state)
            # move the worker
            new_state_list[0] = cell_adjacent(state[0], action)
            new_state = tuple(new_state_list)

        # add the worker, then the box locations.
        new_state = (new_state[0],) + tuple(sorted(new_state[1:]))

        # return the new state of the puzzle
        return new_state

    # check if the goal state is reached
    def goal_test(self, state):
        # test how many boxes are on targets
        num_box_on_target = 0
        for box in state[1:]:
            if box in self.targets:
                num_box_on_target += 1

        # return if all boxes are on targets.
        if num_box_on_target == len(state)-1:
            return True
        else:
            return False

    # return the value of the shortest length
    def value(self, state):

        # assert that there are an equal number of targets and boxes
        assert(len(state)-1 == len(self.targets))

        # variables used 
        value = 0
        first = True
        dist = 0
        boxes = []
        boxes = copy.deepcopy(state[1:])
        list_of_targets = []
        list_of_targets = copy.deepcopy(self.warehouse.targets)
        min_dist = 0

        box_targets_dist = []
        temp_list = []

        # get box and target coordinates and find distance from each other
        for box in boxes:
            # get box x and y
            box_x = box[0]
            box_y = box[1]

            for target in target_list:
                # get target x and y
                target_x = target[0]
                target_y = target[1]

                # use pythag to find distance
                distance = math.sqrt((box_x - target_x)**2 + (box_y - target_y)**2)

                temp += box
                temp += target
                temp += [distance,]
                box_targets_distance += [temp,]
                temp = []

        # Goes through the different distances and finds the shortest distance for each box
        while box_targets_distance:
            temp_trio = box_targets_distance[0]

            for i in range(0, len(box_targets_distance)):
                if i == 0:
                    min_distance = box_targets_distance[0][4]
                if box_targets_distance[i][4] < min_distance:
                    min_distance = box_targets_distance[i][4]
                    temp_trio = box_targets_distance[i]

            # Add the minimal distance to value
            value += min_distance

            # Loops until the shortest distance for each box is found.
            i = 0
            while i < len(box_targets_distance):
                trio = box_targets_distance[i]
                if (trio[0] == temp_trio[0] and trio[1] == temp_trio[1]) or (trio[2] == temp_trio[2] and trio[3] == temp_trio[3]):
                    box_targets_distance.remove(trio)
                    i -= 1
                i += 1

        # return the value
        return value


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def check_action_seq(warehouse, action_seq):
    '''

    Determine if the sequence of actions listed in 'action_seq' is legal or not.

    Important notes:
      - a legal sequence of actions does not necessarily solve the puzzle.
      - an action is legal even if it pushes a box onto a taboo cell.

    @param warehouse: a valid Warehouse object

    @param action_seq: a sequence of legal actions.
           For example, ['Left', 'Down', Down','Right', 'Up', 'Down']

    @return
        The string 'Failure', if one of the action was not successul.
           For example, if the agent tries to push two boxes at the same time,
                        or push one box into a wall.
        Otherwise, if all actions were successful, return
               A string representing the state of the puzzle after applying
               the sequence of actions.  This must be the same string as the
               string returned by the method  Warehouse.__str__()
    '''

    ##         "INSERT YOUR CODE HERE"

    raise NotImplementedError()


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def solve_sokoban_elem(warehouse):
    '''
    This function should solve using elementary actions
    the puzzle defined in a file.

    @param warehouse: a valid Warehouse object

    @return
        If puzzle cannot be solved return the string 'Impossible'
        If a solution was found, return a list of elementary actions that solves
            the given puzzle coded with 'Left', 'Right', 'Up', 'Down'
            For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
            If the puzzle is already in a goal state, simply return []
    '''

    ##         "INSERT YOUR CODE HERE"

    raise NotImplementedError()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def can_go_there(warehouse, dst):
    '''
    Determine whether the worker can walk to the cell dst=(row,column)
    without pushing any box.

    @param warehouse: a valid Warehouse object

    @return
      True if the worker can walk to cell dst=(row,column) without pushing any box
      False otherwise
    '''



    if warehouse.worker == dst:
        return True
    else:
        
        x, y = zip(*warehouse.walls)

        x_size, y_size = 1 + max(x), 1 + max(y)

        # add the starting position to the frontier
        explored_locations = []
        frontier = [warehouse.worker]
        
        # get the maximum values of the x and y in the warehouse
        x_wall = list(zip(*warehouse.walls))[0]
        y_wall = list(zip(*warehouse.walls))[1]
        max_x = list(range(max(x_wall) + 1))
        max_y = list(range(max(y_wall) + 1))
        all_xy = list(itertools.product(max_x,max_y))


        for cell in frontier:

            # check if the cell being explored is not a wall, box, outside the map or previously explored
            if cell not in all_xy and cell not in warehouse.boxes and cell not in explored_locations and cell[0] > 0 and cell[0] < x_size and cell[1] > 0 and cell[1] < y_size:
                # check if the cell is the target and return true if so
                if tuple(cell) == dst:
                    return True

                temp_cell = cell_adjacent(cell, "Up")
                if temp_cell not in warehouse.walls and temp_cell not in warehouse.boxes and temp_cell not in explored_locations and temp_cell[0] > 0 and temp_cell[0] < x_size and temp_cell[1] > 0 and temp_cell[1] < y_size:
                    frontier +=  [list(cell_adjacent(cell, "Up"))]

                temp_cell = cell_adjacent(cell, "Down")
                if temp_cell not in warehouse.walls and temp_cell not in warehouse.boxes and temp_cell not in explored_locations and temp_cell[0] > 0 and temp_cell[0] < x_size and temp_cell[1] > 0 and temp_cell[1] < y_size:
                    frontier +=  [list(cell_adjacent(cell, "Down"))]

                temp_cell = cell_adjacent(cell, "Left")
                if temp_cell not in warehouse.walls and temp_cell not in warehouse.boxes and temp_cell not in explored_locations and temp_cell[0] > 0 and temp_cell[0] < x_size and temp_cell[1] > 0 and temp_cell[1] < y_size:
                    frontier +=  [list(cell_adjacent(cell, "Left"))]

                temp_cell = cell_adjacent(cell, "Right")
                if temp_cell not in warehouse.walls and temp_cell not in warehouse.boxes and temp_cell not in explored_locations and temp_cell[0] > 0 and temp_cell[0] < x_size and temp_cell[1] > 0 and temp_cell[1] < y_size:
                    frontier +=  [list(cell_adjacent(cell, "Right"))]    

        explored_locations += [cell]
        
    return False



# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def solve_sokoban_macro(warehouse):
    '''
    Solve using macro actions the puzzle defined in the warehouse passed as
    a parameter. A sequence of macro actions should be
    represented by a list M of the form
            [ ((r1,c1), a1), ((r2,c2), a2), ..., ((rn,cn), an) ]
    For example M = [ ((3,4),'Left') , ((5,2),'Up'), ((12,4),'Down') ]
    means that the worker first goes the box at row 3 and column 4 and pushes it left,
    then goes to the box at row 5 and column 2 and pushes it up, and finally
    goes the box at row 12 and column 4 and pushes it down.

    @param warehouse: a valid Warehouse object

    @return
        If puzzle cannot be solved return the string 'Impossible'
        Otherwise return M a sequence of macro actions that solves the puzzle.
        If the puzzle is already in a goal state, simply return []
    '''

    ##         "INSERT YOUR CODE HERE"

    raise NotImplementedError()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
