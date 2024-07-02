# see https://medium.com/@steveYeah/using-generics-in-python-99010e5056eb
from typing import Generic, TypeVar
from LinkedList import *

T = TypeVar("T")  # allows variable T to be used to represent a generic type

class EmptyError(Exception):
    ''' class extending Exception to better document stack errors '''
    def __init__(self, message: str):
        self.message = message

class Queue(Generic[T]):
    ''' class to implement a queue ADT using a Python list'''

    __slots__ = ("_data")           # will be a Python list

    def __init__(self):
        self._data: list[T] = LinkedList()    # typing _data to be a list of type T

    def __len__(self) -> int:
        ''' allows the len function to be called using an Queue object, e.g.,
               queue = Queue()
               print(len(queue))
        Returns:
            number of elements in the queue, as an integer
        '''
        return len(self._data)

    def push(self, item: T) -> None:
        ''' pushes a given item of arbitrary type onto the queue
        Parameters:
            item: an item of arbitrary type
        Returns:
            None
        '''
        self._data.add_right(item)
        #self._data.append(item)

    def pop(self) -> T:
        ''' removes the leftmost element from the queue and returns that element
        Returns:
            the leftmost item, of arbitrary type
        Raises:
            EmptyError exception if the queue is empty
        '''
        if len(self._data) == 0:
            raise EmptyError('Error in Queue.pop(): stack is empty')
        return self._data.remove_left() # calling Python list pop()

    def top(self) -> T:
        ''' returns the topmost element from the stack without modifying the stack
        Returns:
            the topmost item, of arbitrary type
        Raises:
            EmptyError exception if the stack is empty
        '''
        if len(self._data) == 0:
            raise EmptyError('Error in Queue.top(): stack is empty')
        #return self._data[-1]
        return self._data._tail.data

    def is_empty(self) -> bool:
        ''' indicates whether the stack is empty
        Returns:
            True if the stack is empty, False otherwise
        '''
        return len(self._data) == 0

    def __str__(self) -> str:
        ''' returns an str implementation of the Queue '''
        string = " <- "
        #string = "---top---\n"
        a = self._data._head
        while a != None:
            string += f"{a.data} "
            a = a.next

            #for i in range(len(self._data) - 1, -1, -1):
            #string += str(self._data[i]) + "\n"
        #string += "---bot---"
        string += "<-"
        return string

def main():
    MyQueue = Queue()
    MyQueue.push(11)
    MyQueue.push(33)
    MyQueue.push(40)
    print(MyQueue)
    #MyQueue.pop()
    print("The removed element")
    print(MyQueue.pop())
    print("the top function")
    print(MyQueue.top())
    #print(MyQueue)



if __name__ == "__main__":
    main()
