from datatypes import Node, Tree, DistanceMatrix

def upgma(mtx: DistanceMatrix, species_names: list[str]) -> Tree:
    """
    Build a phylogenetic tree using the UPGMA algorithm.

    Given a distance matrix and species names, iteratively merges the closest
    clusters and updates the matrix using cluster-size–weighted averages.
    The resulting tree has `n` leaves (the species) and `n-1` internal nodes.

    Args:
        mtx (DistanceMatrix): Square symmetric matrix of pairwise distances.
        species_names (list[str]): Names of the species, in the same order as `mtx`.

    Returns:
        Tree: A list of `Node` objects representing the full UPGMA tree.
              Conventionally, the last node (index -1) is the root.
    """
    #TODO: Implement
    pass


def assert_square_matrix(mtx: DistanceMatrix) -> None:
    """
    Validate that a distance matrix is square.

    Args:
        mtx (DistanceMatrix): The matrix to validate.

    Raises:
        ValueError: If the matrix is not square.
    """
    #TODO: Implement
    pass


def assert_same_number_species(mtx: DistanceMatrix, species_names: list[str]) -> None:
    """
    Validate that the number of species matches the matrix dimension.

    Args:
        mtx (DistanceMatrix): Square distance matrix.
        species_names (list[str]): Species labels.

    Raises:
        ValueError: If their sizes do not match.
    """
    #TODO: Implement
    pass


def add_row_col(row: int, col: int, cluster_size1: int, cluster_size2: int, mtx: DistanceMatrix) -> DistanceMatrix:
    """
    Add a new cluster (row/column) to the matrix via size-weighted averaging.

    Computes distances from the new merged cluster to each existing cluster
    using a weighted average by cluster sizes, then appends this as a new
    row/column at the end of the matrix.

    Args:
        row (int): Index of the first merged cluster (row < col).
        col (int): Index of the second merged cluster.
        cluster_size1 (int): Number of leaves in the first cluster.
        cluster_size2 (int): Number of leaves in the second cluster.
        mtx (DistanceMatrix): The current distance matrix.

    Returns:
        DistanceMatrix: The matrix with the new cluster appended as the last row/column.
    """
    #TODO: Implement
    pass

def delete_clusters(clusters: list[Node], row: int, col: int) -> list[Node]:
    """
    Remove two cluster representatives at indices `row` and `col`.

    This is used after we merge those two clusters into a new one.

    Args:
        clusters (list[Node]): Active cluster representatives.
        row (int): Index of the first cluster (row < col).
        col (int): Index of the second cluster.

    Returns:
        list[Node]: Updated list of cluster representatives with the two removed.
    """
    #TODO: Implement
    pass


def delete_row_col(mtx: DistanceMatrix, row: int, col: int) -> DistanceMatrix:
    """
    Delete two rows and two columns (row/col) from the matrix.

    This is used after appending the new merged cluster at the end.

    Args:
        mtx (DistanceMatrix): The distance matrix.
        row (int): The first row/column index to delete (row < col).
        col (int): The second row/column index to delete.

    Returns:
        DistanceMatrix: The matrix with the specified rows/columns removed.
    """
    #TODO: Implement
    pass


def find_min_element(mtx: DistanceMatrix) -> tuple[int, int, float]:
    """
    Find the indices (i, j) of the smallest strictly upper-triangular entry.

    Args:
        mtx (DistanceMatrix): A square matrix with size >= 2.

    Returns:
        tuple[int, int, float]: (row_index, col_index, min_value) with col_index > row_index.

    Raises:
        ValueError: If the matrix is smaller than 2x2.
    """
    #TODO: Implement
    pass


def initialize_tree(species_names: list[str]) -> Tree:
    """
    Initialize a tree container for UPGMA with labeled leaves and internal nodes.

    Creates a list of 2n - 1 nodes:
      - The first n nodes (0..n-1) are leaves labeled by species_names.
      - The remaining n - 1 nodes (n..2n-2) are internal nodes labeled as ancestors.

    Args:
        species_names (list[str]): Species labels.

    Returns:
        Tree: The preallocated list of `Node` objects used by UPGMA.
    """
    #TODO: Implement
    pass


def initialize_clusters(t: Tree) -> list[Node]:
    """
    Extract the initial cluster representatives (the leaves) from the tree.

    Args:
        t (Tree): The full node list allocated for UPGMA.

    Returns:
        list[Node]: The first n nodes of `t`, corresponding to the leaves.
    """
    #TODO: Implement
    pass