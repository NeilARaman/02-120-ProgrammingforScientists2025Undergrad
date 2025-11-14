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

    def is_leaf(self) -> bool:
        """
        Method that returns true if given node is a leaf and false otherwise.
        """
        # if it's child-free (a joy), then we are at a leaf 
        if self.child1 is None and self.child2 is None:
            return True
        # all other cases it's not a leaf
        return False


    # add our count_leaves() method here
    def count_leaves(self) -> int:
        """
        Count the number of leave nodes in the subtree rooted at this node.
        """
        # two cases are leaf or internal node 
        # base case: I'm at a leaf 
        if self.is_leaf():
            return 1
        # inductive step: find number of leaves beneath child 1, and add it to the number of leaves beneath child 2 
        # we might want to handle the case of an only child 
        leaves = 0
        if self.child1 is not None:
            leaves += self.child1.count_leaves()
        if self.child2 is not None:
            leaves += self.child2.count_leaves()
        return leaves
    
    def to_newick_ages(self) -> str:
        """
        Recursively serialize this subtree to Newick with branch lengths,
        where each branch length = parent.age - child.age.

        Returns:
            Newick string for this subtree (no trailing semicolon).
        """
        # Base case: leaf node
        if self.is_leaf():
            return self.label if self.label else f"N{self.num}"

        parts: list[str] = []

        # Process child1 if it exists
        if self.child1 is not None:
            bl1 = max(self.age - self.child1.age, 0.0)
            part1 = f"{self.child1.to_newick_ages()}:{bl1:.6f}"
            parts.append(part1)

        # Process child2 if it exists
        if self.child2 is not None:
            bl2 = max(self.age - self.child2.age, 0.0)
            part2 = f"{self.child2.to_newick_ages()}:{bl2:.6f}"
            parts.append(part2)

        inside = ",".join(parts)

        # Internal node: include label if present
        return f"({inside}){self.label}" if self.label else f"({inside})"

# alias declarations 

DistanceMatrix = list[list[float]]

Tree = list[Node]