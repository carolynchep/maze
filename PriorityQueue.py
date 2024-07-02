# see https://medium.com/@steveYeah/using-generics-in-python-99010e5056eb
from typing import Generic, TypeVar

K = TypeVar("K", int, float, str)  # allows variable K to be used to represent a generic type
V = TypeVar("V")
E = TypeVar("E")  # used to represent Entry

import heapq
import random
import string

class EmptyError(Exception):
    ''' class extending Exception to better document stack errors '''
    def __init__(self, message: str):
        self.message = message

class Entry(Generic[K,V]):
    def __init__(self, priority: K, data: V):
        self._key   = priority
        self._value = data
    def __str__(self):  return f"({self._key},{self._value})"
    def __eq__(self, other):
        return self._key == other._key and self._value == other._value
    def __lt__(self, other):
        return self._key < other._key
    # not the Pythonic way to use __repr__ but allows us to print list of Entry
    def __repr__(self):
        key = f"'{self._key}'"   if isinstance(self._key,   str) else f"{self._key}"
        val = f"'{self._value}'" if isinstance(self._value, str) else f"{self._value}"
        return f"({key},{val})"

class PriorityQueue(Generic[E]):
    slots = ('_container')

    def __init__(self):
        self._container: list[Entry] = list()

    def __len__(self) -> int:
        return len(self._container)

    def is_empty(self) -> bool:
        return len(self._container) == 0

    def insert(self, key: K, item: V) -> None:
        #create a new entry with key and item
        #insert the entry into the heap
        new_entry = Entry(key, item)
        heapq.heappush(self._container, new_entry)


    def remove_min(self) -> Entry:
        if len(self._container) == 0:
            raise EmptyError("can't remove from empty heap")
        else:
            return heapq.heappop(self._container)


    def min(self) -> Entry:
        if len(self._container) == 0:
            raise EmptyError("can't remove from empty heap")
        else:
            return self._container[0]

def main():
    heap = [1,2,3,4,5,6,7,8,9]
    #hq.heapify(heap)
    print(len(heap))
    print(heap)

    pq = PriorityQueue()
    pq.insert(5, 'task1')
    pq.insert(3, 'task2')
    pq.insert(6, 'task3')
    pq.insert(2, 'task4')

    print(f"Priority Queue: {pq._container}")
    print(f"Minimum element: {pq.min()}")

    print("Removing elements:")
    while not pq.is_empty():
        print(pq.remove_min())

if __name__ == "__main__":
    main()
