from datatypes import Board, Cell


def initialize_board(num_rows: int, num_cols: int) -> Board:
    """
    Initialize a board with all cells set to (0, 0).
    
    Args:
        num_rows: Number of rows in the board
        num_cols: Number of columns in the board
    
    Returns:
        A Board with all cells initialized to (0.0, 0.0)
    """
    board = []
    for _ in range(num_rows):
        row = []
        for _ in range(num_cols):
            row.append((0.0, 0.0))
        board.append(row)
    return board


def sum_cells(*cells: Cell) -> Cell:
    """
    Sum an arbitrary number of Cell variables element-wise.

    Args:
        *cells (tuple[float, float]): Any number of Cell tuples (A, B),
        where A represents the concentration of the predator and
        B represents the concentration of the prey.

    Returns:
        tuple[float, float]: A single Cell (A_sum, B_sum) corresponding
        to the sum of the 0th and 1st elements across all input cells.
    """
    # Initialize totals
    total_a = 0.0
    total_b = 0.0
    # Iterate through all Cell tuples and sum each element
    for cell in cells:
        total_a += cell[0]
        total_b += cell[1]
    return (total_a, total_b)


def change_due_to_reactions(current_cell: tuple[float, float],
                            feed_rate: float,
                            kill_rate: float) -> tuple[float, float]:
    """
    Compute the change in a cell's concentrations due to Gray-Scott reactions.

    Args:
        current_cell (tuple[float, float]): Current cell concentrations (A, B),
            where A is the predator concentration and B is the prey concentration.
        feed_rate (float): The feed rate (f), controlling the input of A.
        kill_rate (float): The kill rate (k), controlling the removal of B.

    Returns:
        tuple[float, float]: A Cell (delta_A, delta_B) representing the change due to the reactions.
    """
    # Initializing the constant + given values
    a, b = current_cell
    r = 1.0
    # Computing the Gray–Scott equations for reaction changes
    delta_a = feed_rate * (1 - a) - r * a * (b ** 2)
    delta_b = -kill_rate * b + r * a * (b ** 2)
    return (delta_a, delta_b)


def in_field(board: list[list[float]], row: int, col: int) -> bool:
    """
    Checks whether the given row and column indices lie within the valid range of the board.

    Args:
        board (list[list[float]]): A 2D grid representing the current concentration values.
        row (int): The row index to check.
        col (int): The column index to check.

    Returns:
        bool: True if the index (row, col) is within the board's bounds, return False otherwise.
    """
    # Checks negative indices
    if row < 0 or col < 0:
        return False
    # Checks upper bound
    if row >= len(board) or col >= len(board[0]):
        return False
    return True


def change_due_to_diffusion(current_board: list[list[tuple[float, float]]],
                            row: int,
                            col: int,
                            prey_diffusion_rate: float,
                            predator_diffusion_rate: float,
                            kernel: list[list[float]]) -> tuple[float, float]:
    """
    Compute the change in concentration (delta) of both particles (A and B) in a given cell
    due to diffusion based on the Gray-Scott model.

    Args:
        current_board (list[list[tuple[float, float]]]): 2D list of cells, each cell is the tuple (A, B).
        row (int): Row index of the target cell.
        col (int): Column index of the target cell.
        prey_diffusion_rate (float): Diffusion rate for the prey species (A).
        predator_diffusion_rate (float): Diffusion rate for the predator species (B).
        kernel (list[list[float]]): 3×3 list of floats representing diffusion weights.

    Returns:
        tuple[float, float]: The change (delta_A, delta_B) due to calculated diffusion for this cell.
    """
    # Initialize variables to calculate accumulation
    delta_a = 0.0
    delta_b = 0.0
    # Iterate through the 3×3 neighborhood, only add if exist
    for di in (-1, 0, 1):
        for dj in (-1, 0, 1):
            ni = row + di
            nj = col + dj
            # Check if the neighbors exist on the board here
            if in_field(current_board, ni, nj):
                neighbor = current_board[ni][nj]
                weight = kernel[di + 1][dj + 1]
                delta_a += neighbor[0] * weight
                delta_b += neighbor[1] * weight
    # Update per respective diffusion rates
    delta_a *= prey_diffusion_rate
    delta_b *= predator_diffusion_rate
    return (delta_a, delta_b)


def update_cell(current_board: list[list[tuple[float, float]]],
                row: int,
                col: int,
                feed_rate: float,
                kill_rate: float,
                prey_diffusion_rate: float,
                predator_diffusion_rate: float,
                kernel: list[list[float]]) -> tuple[float, float]:
    """
    Update the concentrations of A and B for a single cell in the Gray-Scott model.

    Input:
        current_board (list[list[tuple[float, float]]]): 
            The current 2D array of concentrations (A, B).
        row (int): Row index of the cell.
        col (int): Column index of the cell.
        feed_rate (float): The rate at which new A particles are fed into the system.
        kill_rate (float): The rate at which existing B particles are removed from the system.
        prey_diffusion_rate (float): Diffusion rate of chemical A.
        predator_diffusion_rate (float): Diffusion rate of chemical B.
        kernel (list[list[float]]): 3x3 diffusion kernel.

    Output:
        tuple[float, float]: The new concentrations (A, B) for this cell after one update.
    """
    # Get the current cell's concentrations
    current_cell = current_board[row][col]
    # Calculate the diffusion changes
    diffusion_values = change_due_to_diffusion(current_board,
                                               row,
                                               col,
                                               prey_diffusion_rate,
                                               predator_diffusion_rate,
                                               kernel)
    # Calculate the Gray–Scott chemical reactions changes
    reaction_values = change_due_to_reactions(current_cell,
                                              feed_rate,
                                              kill_rate)
    # Add all the changes
    new_cell = sum_cells(current_cell, diffusion_values, reaction_values)
    return new_cell


def update_board(current_board: list[list[tuple[float, float]]],
                 feed_rate: float,
                 kill_rate: float,
                 prey_diffusion_rate: float,
                 predator_diffusion_rate: float,
                 kernel: list[list[float]]) -> list[list[tuple[float, float]]]:
    """
    Apply one full time step of the Gray-Scott model to a 2D board.

    Input:
        current_board (list[list[tuple[float, float]]]): 
            A 2D array where each element is a tuple (A, B)
            representing the concentrations of the two chemicals.
        feed_rate (float): The rate at which new A particles are fed into the system.
        kill_rate (float): The rate at which existing B particles are removed from the system.
        prey_diffusion_rate (float): The diffusion rate for chemical A.
        predator_diffusion_rate (float): The diffusion rate for chemical B.
        kernel (list[list[float]]): A 3x3 matrix of weights representing the diffusion kernel.

    Output:
        list[list[tuple[float, float]]]: 
            A 2D board representing updated concentrations after one time step.
    """
    # Initialize and set new dimensions
    rows = len(current_board)
    cols = len(current_board[0])
    # Initialize an empty board
    new_board = []
    # Make it the same size with cells of (0.0, 0.0)
    for _ in range(rows):
        row_list = []
        for _ in range(cols):
            row_list.append((0.0, 0.0))
        new_board.append(row_list)
    # Loop through each cell, update it with the update cell helper function
    for row in range(rows):
        for col in range(cols):
            new_board[row][col] = update_cell(
                current_board,
                row,
                col,
                feed_rate,
                kill_rate,
                prey_diffusion_rate,
                predator_diffusion_rate,
                kernel,
            )
    return new_board


def simulate_gray_scott(initial_board: list[list[tuple[float, float]]],
                        num_gens: int,
                        feed_rate: float,
                        kill_rate: float,
                        prey_diffusion_rate: float,
                        predator_diffusion_rate: float,
                        kernel: list[list[float]]) -> list[list[list[tuple[float, float]]]]:
    """
    Runs the Gray-Scott reaction-diffusion simulation over a specified number of generations.

    Input:
        initial_board (list[list[tuple[float, float]]]):
            The initial 2D grid of cells, where each cell stores (A, B) concentrations.
        num_gens (int):
            The total number of generations to simulate.
        feed_rate (float):
            The constant rate at which A is added to the system.
        kill_rate (float):
            The constant rate at which B is removed from the system.
        prey_diffusion_rate (float):
            The diffusion rate for A (prey chemical).
        predator_diffusion_rate (float):
            The diffusion rate for B (predator chemical).
        kernel (list[list[float]]):
            A 3×3 matrix representing diffusion weights that sum to zero.

    Output:
        list[list[list[tuple[float, float]]]]:
            A list of boards. The 0th board is the initial state,
            and each subsequent board represents the system after one additional time step.
    """
    # Initialize the list of boards
    boards = [initial_board]
    # Loop through the number of generations, updating based on the previous generation
    for gen in range(1, num_gens + 1):
        # Compute the next board generation
        prev_board = boards[gen - 1]
        next_board = update_board(prev_board,
                                  feed_rate,
                                  kill_rate,
                                  prey_diffusion_rate,
                                  predator_diffusion_rate,
                                  kernel)
        # Add the new list to the overall list
        boards.append(next_board)
    return boards
