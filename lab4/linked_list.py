from __future__ import annotations
from dataclasses import dataclass
from typing import Final
import random

@dataclass
class LinkedListNode[T]:
    value_: Final[T]
    next_: Final[LinkedListNode[T]]



class LinkedList[T]:
    __head: LinkedListNode[T] | None = None
    
    def __traverse_to_node_of(self, index: int) -> LinkedListNode[T] | None:
        if self.__head is None:
            return None
        
        pos = 0
        current = self.__head
        while pos < index and current.next_ is not None:
            current = current.next_
            pos += 1
        
        return current

    def set_node(self, index: int, value: T) -> None:
        node = self.__traverse_to_node_of(index)
        
        if node is not None:
            node.value_ = value

    def get_node(self, index: int) -> LinkedListNode[T] | None:
        return self.__traverse_to_node_of(index)

    def insert_node(self,index: int,value: T) -> None:
        pass

    def remove_node(self,index: int) -> None:
        pass

    def size(self) -> int:
        pass

    def push_back(self,value: T) -> None:
        pass

def generate_random_list(length: int):
    result = []

    for i in range(0,length):
        result.append(random.randint(0,10000))
    return result

def generate_Random_linked_list(length: int):
    result = LinkedList()

    for i in range(0,length):
        # result.append(random.randint(0,10000))
        pass

    return result

def main():
    pass

if __name__ == "__main__":
    main()
