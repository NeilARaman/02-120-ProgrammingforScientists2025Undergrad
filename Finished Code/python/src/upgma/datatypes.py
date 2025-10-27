from dataclasses import dataclass
from typing import Self

# three things: distance matrix alias,
# node declaration,
# tree declaration


@dataclass
class Node:
    """
    Represents a node in a phylogenetic tree.
    
    Attributes:
        num (int): numeric ID for the node 
        age (float): represents its "age" from the leaves 
        label (str): species name for leaves, ancestor name for internal nodes 
        child1: the first child node, or None if it doesn't exist
        child2: the second child node, or None if it doesn't exist
    """

    num: int = 0
    age: float = 0.0
    label: str = ""
    child1: Self | None = None # this allows us to have a child attribute that is a Node
    child2: Self | None = None

    # we would like to do this ...
    # child1: Node = None 
    # child2: Node = None
    # but this is a "recursive" class definition, and Python doesn't allow it :(

# alias declarations 

DistanceMatrix = list[list[float]]

Tree = list[Node]