# see https://medium.com/@steveYeah/using-generics-in-python-99010e5056eb
from typing import Generic, TypeVar
from LinkedList import *

T = TypeVar("T")  # allows variable T to be used to represent a generic type

class EmptyError(Exception):
    ''' class extending Exception to better document stack errors '''
    def __init__(self, message: str):
        self.message = message

class Stack(Generic[T]):
    ''' class to implement a stack ADT using a Python list '''

    __slots__ = ("_data")

    def __init__(self):
        self._data: list[T] = LinkedList()   # typing _data to be a list of type T

    def __len__(self) -> int:
        ''' allows the len function to be called using an ArrayStack object, e.g.,
               stack = ArrayStack()
               print(len(stack))
        Returns:
            number of elements in the stack, as an integer
        '''
        return len(self._data)

    def push(self, item: T) -> None:
        ''' pushes a given item of arbitrary type onto the stack
        Parameters:
            item: an item of arbitrary type
        Returns:
            None
        '''
        self._data.add_right(item)
        #self._data.append(item)

    def pop(self) -> T:
        ''' removes the topmost element from the stack and returns that element
        Returns:
            the topmost item, of arbitrary type
        Raises:
            EmptyError exception if the stack is empty
        '''
        if len(self._data) == 0:
            raise EmptyError('Error in ArrayStack.pop(): stack is empty')
        return self._data.remove_right()  # calling Python list pop()

    def top(self) -> T:
        ''' returns the topmost element from the stack without modifying the stack
        Returns:
            the topmost item, of arbitrary type
        Raises:
            EmptyError exception if the stack is empty
        '''
        if len(self._data) == 0:
            raise EmptyError('Error in ArrayStack.top(): stack is empty')
        return self._data._tail

    def is_empty(self) -> bool:
        ''' indicates whether the stack is empty
        Returns:
            True if the stack is empty, False otherwise
        '''
        return len(self._data) == 0

    def __str__(self) -> str:
        ''' returns an str implementation of the ArrayStack '''
        string = "---top---\n"
        a = self._data._tail
        while a != None:
            #print(f"{a.data}")
            string += f"{a.data}\n"
            a = a.prev
            #print(f"{a.data}")
            #string += f"{a.data} + \n"
            #string += str(self._data[i]) + "\n"
        string += "---bot---"
        return string

def main():
    MyStack = Stack()
    MyStack.push(11)
    MyStack.push(33)
    MyStack.push(40)
    MyStack.push(23)
    MyStack.push(10)
    print(MyStack)
    print("The length of the stack:")
    print(len(MyStack))


    print("Popping the top element of the stack:")
    print(MyStack.pop())
    print(MyStack)

    print("Checking if the stack is empty:")
    print(MyStack.is_empty())

    print("Popping all elements to empty the stack:")
    MyStack.pop()
    MyStack.pop()
    MyStack.pop()
    MyStack.pop()
    print(MyStack)

    print("Checking if the stack is empty:")
    print(MyStack.is_empty())


if __name__ == "__main__":
    main()
