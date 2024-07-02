from Stack import *
from Queue import *
from PriorityQueue import *
from enum import Enum
from typing import List, NamedTuple, Optional
from typing import Union
import random

################################################################################
class Contents(str, Enum):
    ''' create an enumeration to define what the visual contents of a Cell are;
        using str as a "mixin" forces all the entries to be strings; using an
        enum means no cell entry can be anything other than the options here
    '''
    EMPTY   = " "
    START   = "S" #"S"
    GOAL    = "G" #"G"
    BLOCKED = "░" #"X"
    PATH    = "*" #"*"

################################################################################
class Position(NamedTuple):
    ''' just allows us to use .row and .col rather than the less-easy-to-read
        [0] and [1] for accessing values'''
    row: int
    col: int

################################################################################
class Cell:
    ''' class that allows us to use Cell as a data type -- an ordered triple
        of row, column, & cell contents
        (see Contents class enumeration above)
    '''
    def __init__(self, row: int, col: int, contents: Contents):
        self._position:  Position = Position(row, col)
        self._contents:  Contents = contents
        self._parent:    'Cell'   = None    # parent of this Cell during exploration
        self._g: int  = 0
        self._h: int = 0

    def getPosition(self) -> Position:
        ''' method to return the (row,col) Position of this cell
        Returns:
            a Position object containing the cell's row and column
        '''
        return Position(self._position.row, self._position.col)

    def getParent(self) -> 'Cell':
        ''' method to return the parent of this Cell object as determined during
            maze exploration
        Returns:
            a Cell object corresponding to the cell that considered this cell
            during the exploration process
        '''
        return self._parent

    def markOnPath(self) -> None:
        ''' method to identify this cell as being on the path from source
            to goal
        '''
        self._contents = Contents.PATH

    def isBlocked(self) -> bool:
        ''' Boolean method to indicate whether this cell contains a block
        Returns:
            True if the cell is blocked (cannot be explored), False o/w
        '''
        return self._contents == Contents.BLOCKED

    def isGoal(self) -> bool:
        ''' Boolean method to indicate whether this cell is the goal
        Returns:
            True if the cell is the maze goal, False o/w
        '''
        return self._contents == Contents.GOAL

    def setCost(self, item: int) -> None:
        self._g = item

    def getCost(self) -> int:
        return self._g

    def setHeuristic(self, item: int) -> None:
        self._h = item

    def getHeuristic(self) -> int:
        return self._h


    def __str__(self) -> str:
        ''' creates and returns a string representation of this cell
        Returns:
            a string identifying the cell's row, col, and cell contents
        '''
        contents = "[EMPTY]" if self._contents == Contents.EMPTY else self._contents
        #return f"({self._position.row}, {self._position.col}): {contents}"
        string = f"({self._position.row}, {self._position.col}): {contents} "
        if self._parent is not None: string += f"({self._parent._position.row}, {self._parent._position.col})"
        return string

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other: 'Cell') -> bool:
        ''' Boolean method to indicate whether a given Cell is equal to this Cell
        Returns:
            True if this Cell and the other Cell are the same, False o/w
        '''
        return self._position.row == other._position.row and \
               self._position.col == other._position.col and \
               self._contents == other._contents

################################################################################
class Maze:
    ''' class representing a 2D maze of Cell objects '''

    def __init__(self, rows: int = 20, cols: int = 20, prop_blocked: float = 0.2, \
                       start: Position = Position(0, 0), \
                       goal:  Position = Position(19, 19), \
                       debug: bool = False):
        ''' initializer method for a Maze object
        Parameters:
            rows:          number of rows in the grid
            cols:          number of columns in the grid
            prop_blocked:  proportion of cells to be blocked (between 0.0 and 1.0)
            start:         Position object indicating the (row,col) of the start cell
            goal:          Position object indicating the (row,col) of the goal cell
            debug:         whether to use one of the Maze examples from course slides
        '''
        try:
            float(prop_blocked)
        except:
            raise TypeError("prop_blocked argument must be a float between 0 and 1")
        else:
            if prop_blocked < 0 or prop_blocked > 1:
                raise ValueError("prop_blocked argument must be a float between 0 and 1")

        if not isinstance(start, Position) or not isinstance(goal, Position):
            raise ValueError("start and goal must both be Position objects")

        if debug:
            rows = 6; cols = 5;
            start = Position(5, 0)
            goal  = Position(0, 4)


        self._num_rows = rows
        self._num_cols = cols
        self._start    = Cell(start.row, start.col, Contents.START)
        self._goal     = Cell(goal.row,  goal.col,  Contents.GOAL)
        self._num_pushes = 0

        # create a rows x cols 2D list of Cell objects, intially all empty
        self._grid: list[list[Cell]] = \
            [ [Cell(r,c, Contents.EMPTY) for c in range(cols)] for r in range(rows) ]

        # set the start and goal cells (overriding two empty Cell objects from above)
        self._grid[start.row][start.col] = self._start
        self._grid[goal.row][goal.col]   = self._goal

        # put blocks at random spots in the grid, using given proportion;
        # start by creating a collapsed 1D version of the grid, then
        #   remove the start and goal, and then randomly pick cells to block;
        # note that we are using identical object references in both
        #   options and self._grid so that updates to options will be seen
        #   in self._grid (i.e., options is not a deep copy of cells);
        if not debug:
            options = [cell for row in self._grid for cell in row]
            options.remove(self._start)
            options.remove(self._goal)
            blocked = random.sample(options, k = round((rows * cols - 2) * prop_blocked))
            for b in blocked:
                b._contents = Contents.BLOCKED  # this is changing self._grid!
        else:
            # for example from slides
            pos = [(1,0),(1,3),(2,1),(2,4),(3,2),(5,1),(5,3),(5,4)]
            for p in pos:
                self._grid[p[0]][p[1]]._contents = Contents.BLOCKED

    def __str__(self) -> str:
        ''' creates a str version of the Maze, showing contents, with cells
            delimited by vertical pipes
        Returns:
            a str representation of the Maze
        '''
        maze_str = ""
        for row in self._grid:  # row : List[Cell]
            maze_str += "|" + "|".join([cell._contents for cell in row]) + "|\n"
        return maze_str[:-1]  # remove the final \n

    def getStart(self) -> Cell:
        ''' accessor method to return the Cell object corresponding to the Maze start
        Returns:
            the Cell object at the Maze start location
        '''
        return self._start

    def getGoal(self):
        ''' accessor method to return the Cell object corresponding to the Maze goal
        Returns:
            the Cell object at the Maze goal location
        '''
        return self._goal

    def getSearchLocations(self, search_cell: Cell) -> List[Cell]:
        ''' method to return a list of Cell objects of valid places to explore
            (i.e., not blocked and within the grid)
        Parameters:
            cell: the current Cell being explored
        Returns:
            a list of valid Cell objects (in N/S/W/E exploration) for further
            consideration
        '''
        cell_list =[]

        position = search_cell.getPosition()
        #checking to see if we can move to the north cell
        if position.row -1 >= 0 :
            cell = self._grid[position.row-1][position.col]
            if cell.isBlocked() or cell == self._start:
                pass
            else:
                cell_list.append(cell)

        #checking for the south cell
        if position.row +1 < self._num_rows:
            cell = self._grid[position.row+1][position.col]
            if cell.isBlocked() or cell == self._start:
                pass
            else:
                cell_list.append(cell)


        #checking for west cell
        if position.col - 1 >= 0:
            cell = self._grid[position.row][position.col-1]
            if cell.isBlocked() or cell == self._start:
                pass
            else:
                cell_list.append(cell)
        #checking for east cell
        if position.col +1 < self._num_cols:
            cell = self._grid[position.row][position.col+1]
            if cell.isBlocked() or cell == self._start:
                pass
            else:
                cell_list.append(cell)
        return cell_list


    def dfs(self) -> Union[Cell, None]:
        ''' method to perform DFS (using a stack) to implement maze searching
        Returns:
            a Cell object corresponding to the Maze goal, or None if no goal
            can be found
        '''
        #Use DFS + stack:
        #    stack: push new Cell objects to be explored
        #            (which will also keep track of the parent)
        #    list:  cells already explored
        mazeStack = Stack()
        current_cell = self.getStart()
        mazeStack.push(current_cell)

        visited_blocks = []
        visited_blocks.append(current_cell)
        self._num_pushes +=1


        while not mazeStack.is_empty():
            current_cell = mazeStack.pop()
            if current_cell.isGoal():
                print(f"The number of pushes:{self._num_pushes}")
                return current_cell


            valid_locals = self.getSearchLocations(current_cell)


            for i in range (len(valid_locals)):
                if valid_locals[i] not in visited_blocks:
                    mazeStack.push(valid_locals[i])
                    visited_blocks.append(valid_locals[i])
                    valid_locals[i]._parent = current_cell
                    self._num_pushes +=1

        print(f"The number of pushes:{self._num_pushes}")
        return None


    def bfs(self) -> Union[Cell, None]:
        ''' method to perform BFS (using a queue) to implement maze searching
        Returns:
            a Cell object corresponding to the Maze goal, or None if no goal
            can be found
        '''
        #Use BFS + queue:
        #    queue: push new Cell objects to be explored
        #            (which will also keep track of the parent)
        #    list:  cells already explored
        mazeQ = Queue()
        current_cell = self.getStart()
        mazeQ.push(current_cell)

        visited_blocks = []
        visited_blocks.append(current_cell)
        self._num_pushes +=1


        while not mazeQ.is_empty():
            current_cell = mazeQ.pop()
            if current_cell.isGoal():
                print(f"The number of pushes:{self._num_pushes}")
                return current_cell

            valid_locals = self.getSearchLocations(current_cell)


            for i in range (len(valid_locals)):
                if valid_locals[i] not in visited_blocks:
                    mazeQ.push(valid_locals[i])
                    visited_blocks.append(valid_locals[i])
                    valid_locals[i]._parent = current_cell
                    self._num_pushes += 1

        print(f"The number of pushes:{self._num_pushes}")
        return None



    def manhattan(self,othercell: Cell) -> int:
        goal = self.getGoal()
        position = goal.getPosition()
        otherpos = othercell.getPosition()
        rows = abs(position.row - otherpos.row)
        cols = abs(position.col - otherpos.col)

        cost = rows+cols
        return cost



    def a_star(self) -> 'Cell | None':
        to_explore = PriorityQueue()
        explored = dict()
        n = self.getStart()
        get_neighbors = self.getSearchLocations
        g= 0
        n.setCost(g)
        h = self.manhattan(n)
        n.setHeuristic(h)    # also keep track inside n
        f = g+h

        to_explore.insert(f, n)
        explored[n.getPosition()] = g  # {(r,c) : g(n)}
        self._num_pushes +=1


        while not to_explore.is_empty() :
            e = to_explore.remove_min()	# e is an Entry
            n = e._value         # n is a Cell
            if n == self.getGoal():
                print(f"The number of pushes:{self._num_pushes}")
                return n


            for m in self.getSearchLocations(n):
                updated_m_cost = n.getCost() + 1   	# cost is one step away from n
                if m.getPosition() not in explored or updated_m_cost < explored[m.getPosition()]:
                    m.setCost(updated_m_cost)
                    explored[m.getPosition()] = m.getCost()  # set the new/improved cost
                    h = self.manhattan(m)
                    m.setHeuristic(h)    # set heuristic
                    g= updated_m_cost
                    f = g+ h
                    to_explore.insert(f, m)
                    m._parent = n
                    # remember to update m's g(m), h(m) and parent
                    self._num_pushes +=1

        print(f"The number of pushes:{self._num_pushes}")
        return None




    def showPath(self, goal: Cell) -> None:
        ''' method to update the path from start to goal, identifying the steps
            along the way as belonging to the path (updating the cell via
            .markOnPath, which will change that cell's ._contents to
            Contents.PATH), printing the final resulting solutions
        Parameters:
            goal: a Cell object corresponding to the goal location
        Returns:
            nothing -- just updates the cells in the grid to identify those on the path
        '''

        path = []
        cell = goal
        while cell._parent is not None:
            path.append(cell)
            cell = cell._parent
        path.append(cell)  # should be the start

        path.reverse()

        for cell in path:
            if cell != self._start and cell != self._goal:
                cell.markOnPath()

        # print the maze, i.e., using __str__ which will show the solved maze
        print(self)

def main():
    seed = 46545
    random.seed(seed)
    m = Maze(debug = False)
    print(m)
    goal = m.dfs()
    print("This is dfs path")
    print(goal)
    if goal is not None:
        m.showPath(goal)

    random.seed(seed)
    m = Maze(debug = False)
    goal = m.bfs()
    print("This is bfs path")
    print(goal)
    if goal is not None:
        m.showPath(goal)

    random.seed(seed)
    m = Maze(debug = False)
    goal = m.a_star()
    print("This is a star path")
    print(f"goal cell:{goal}")
    if goal is not None:
        m.showPath(goal)


if __name__ == "__main__":
    main()
