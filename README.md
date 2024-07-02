# Solving Mazes Using Depth-First Search, Breadth-First Search, & A*

**BFS**

**Breadth-First Search** is an algorithm that searches a tree data structure for a node by exploring all nodes at the present depth prior to moving on to the next depth level, used in a
queue. 

In a maze:

Searches the closest
elements to the starting
location are searched first
and finds the shortest
solution path

Finds the shortest path in
terms of actions only but
not necessarily the
least-cost path

**DFS**

**Depth- First-Search** is an
algorithm for traversing
tree or graph data
structures using the stack

DFS in maze:

From the current position,
the algorithm first explores N,S,E,W
positions and evaluates
whether the positions are
blocked and already
explored.

It also records
its parent and from the
current position, all the
potential next position is
pushed onto the stack.


The new current position
is popped from the stack
and evaluated again until
the goal is reached.

**A***

**A* algorithm** is an an
informed search
algorithm that uses the
priorityqueue.

A* aims to find a path to
the goal having the
smallest cost

g(n) is the cost from start to the goal

h(n) is the estimated cost
calculated by the
Euclidian or the
Manhattan distance
f(n) = g(n) + h(n)

A* Algorithm works by
vertices in the graph,
which start with the
object’s starting point and
then repeatedly examines
the next unexamined
vertex, adding its vertices
to the set of vertices that
will be examined.
(https://www.mygreatlear
ning.com/blog/a-search-a
lgorithm-in-artificial-intelli
gence/ )
Finds the shortest path
with the least cost

Implemented Sample Code: 
(find the attached file Maze.py)
```python
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
        ''' method to perform a star (using a PriorityQueue) to implement maze searching
        Returns:
            a Cell object corresponding to the Maze goal, or None if no goal
            can be found
        '''
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
```

## Expected Output
![dfs](https://github.com/carolynchep/maze/assets/152312583/253f7ba3-7660-48c8-8d91-731d21fb88a9)
![bfs](https://github.com/carolynchep/maze/assets/152312583/87c755cc-f0b4-44cf-a320-bedb34d5d442)
![atar](https://github.com/carolynchep/maze/assets/152312583/338e89b3-217e-494e-8736-a2a8c0092a58)


