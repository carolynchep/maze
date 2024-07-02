# see https://medium.com/@steveYeah/using-generics-in-python-99010e5056eb
from typing import Generic, TypeVar
T = TypeVar("T")  # allows variable T to be used to represent a generic type

class Node(Generic[T]):
    #represents one of the nodes
    def __init__(self, data: T):
        self.data: T      = data
        self.next: Optional('Node') = None  # eventually another Node
        self.prev: Optional('Node') = None

class LinkedList(Generic[T]):

    def __init__(self) -> None:
        self._head: Optional(Node[T]) = None   # the head pointer in the linked list
        self._tail: Optional(Node[T]) = None   # the tail pointer in the linked list
        self._count = 0

    def add_left(self, item: T) -> None:
        ''' adds the given T-type data item as part of a new Node to the left
            of the linked list... remember to reset the head pointer, and, when
            appropriate, the tail pointer
        Parameters:
            item: a type T data item to be included as the data in the inserted Node
        Returns:
            nothing
        '''
        new_node = Node(item)
        #handle adding left on empty list
        if self._head is None:
            self._tail = new_node
            self._head =new_node

        else:
            new_node.next = self._head
            self._head.prev = new_node
            self._head = new_node
        self._count +=1
        #print(self._count)


    def add_right(self, item: T) -> None:
        ''' adds the given T-type data item as part of a new Node to the right
            of the linked list... remember to reset the tail pointer, and, when
            appropriate, the head pointer
        Parameters:
            item: a type T data item to be included as the data in the inserted Node
        Returns:
            nothing
        '''
        new_node = Node(item)
        #handle adding right on empty list
        if self._tail is None:
            self._head = new_node
            self._tail =new_node


        else:
            new_node.prev = self._tail
            self._tail.next = new_node
            self._tail = new_node
        self._count +=1


    def remove_left(self) -> T:
        ''' removes the first Node in the linked list, returning the data item
            inside that Node...  Remember to handle the special case of an
            empty list (what should the head and tail pointers be in that case?)
            and remember to update the head & tail pointer(s) when appropriate.
        Returns:
            a T type data item extracted from the removed Node
        '''
        if self._head is None:
            return None #raise the error

        elif self._count == 1:
            leftNode = self._head.data
            self._head = None
            self._tail = None
            self._count = self._count -1
            return leftNode


        else:
            leftNode = self._head.data
            self._head = self._head.next
            self._head.prev = None
            self._count = self._count - 1
            return leftNode



    def remove_right(self) -> T:
        ''' removes the last Node in the linked list, returning the data item
            inside that Node...  Remember to handle the special case of an
            empty list (what should the head and tail pointers be in that case?)

            Note: This one is trickier because you always have to walk (almost)
            all the way through the list in order to know what the new tail
            should be.

            Remember to update the head & tail pointer(s) when appropriate.

        Returns:
            a T type data item extracted from the removed Node
        '''
        if self._head is None:
            return None

        elif self._count == 1:
            rightNode = self._head.data
            self._head = None
            self._tail = None
            self._count = 0
            return rightNode

        else:
            rightNode = self._tail.data
            self._tail = self._tail.prev
            self._tail.next = None
            self._count = self._count - 1
            return rightNode


    def __str__(self):
        ''' returns a str representation of the linked list data
        Returns:
            an str representation of the linked list, showing head pointer
                and data tiems
        '''
        str_ = "head->"

        # start out at the head Node, and walk through Node by Node until we
        # reach the end of the linked list (i.e., the ._next entry is None)
        ptr_ = self._head
        while ptr_ is not None:
            str_ += "[" + str(ptr_.data) + "]->"
            ptr_ = ptr_.next  # move ptr_ to the next Node in the linked list

        if self._head != None: str_ = str_[:-2]
        str_ += "<-tail"
        return str_

    def __len__(self):
        return self._count

def main():
    # create a LinkedList and try out some various adds and removes
    ll = LinkedList()
    print(ll)
    ll.add_right(8)
    print(ll)
    print(len(ll))
    ll.add_right(6)
    print(ll)
    ll.add_right(7)
    print(ll)
    ll.add_left(5)
    print(ll)
    ll.remove_left()
    print(ll)
    ll.remove_right()
    print(ll)



    #print(f"Removing from left: {ll.remove_left()}")
    #print(ll)

    #for i in range(3):
        #print(f"Removing from right: {ll.remove_right()}")
        #print(ll)

if __name__ == "__main__":
    main()
