import random
from datatypes import Board
from helper_functions import contains, deep_copy_board, num_cols, num_rows, make_empty_board

def create_board(r: int,
                 c: int,
                 pile: int,
                 center: bool = True,
                 num_piles: int = 1) -> Board:
    """Create an r x c board and place grains either centrally or randomly.

    Args:
        r: Number of rows.
        c: Number of columns.
        pile: Number of grains (must be positive).
        center: If True, place all grains at center. If False, use random placement.
        num_piles: When center=False, number of random cells receiving pile/num_piles grains.

    Returns:
        A board with grains placed according to the mode selected.
    """
    if pile <= 0:
        raise ValueError("Error: stack size must be positive.")

    if not center and num_piles <= 0:
        raise ValueError("Error: num_piles must be positive for random placement.")

    # Start with an empty board
    b = make_empty_board(r, c)

    if center:
        # Place all grains in the center cell
        center_row = r // 2
        center_col = c // 2
        b[center_row][center_col] = pile
        return b

    # Otherwise: random placement across num_piles random locations
    grains_per_pile = pile // num_piles

    for _ in range(num_piles):
        row = random.randrange(r)
        col = random.randrange(c)
        b[row][col] = grains_per_pile

    return b

def simulate_sandpiles(initial_board: Board) -> list[Board]:
    """
    Run the sandpile simulation until convergence.
    
    Parameters:
        initial_board: The starting configuration.
    
    Returns:
        list[Board]: All boards from initial to final stable state.
    """
    # Define variables
    final_boards = [deep_copy_board(initial_board)]
    current_board = deep_copy_board(initial_board)
    # Keep updating until stable
    while not is_converged(current_board):
        # Apply one update step
        current_board = update(current_board)
        # Add board to history
        final_boards.append(deep_copy_board(current_board))
    return final_boards


def is_converged(b: Board) -> bool:
    """
    Check whether the board has reached a stable configuration.
    
    Parameters:
        b: The current sandpile board.
    
    Returns:
        bool: True if no cell has 4 or more coins, False otherwise.
    """
    # Check every cell on the board
    for row in b:
        for cell in row:
            # If any cell can still topple, not converged
            if cell >= 4:
                return False
    # All cells are stable
    return True


def update(b: Board) -> Board:
    """
    Perform one update step of the sandpile simulation.
    
    Parameters:
        b: The current sandpile board.
    
    Returns:
        Board: A new board after one update step.
    """
    # Define variables
    rows = num_rows(b)
    cols = num_cols(b)
    new_board = []
    # Update each cell
    for r in range(rows):
        new_row = []
        for c in range(cols):
            old_value = b[r][c]
            coins_out = number_of_coins_out(b, r, c)
            coins_in = number_of_coins_in(b, r, c)
            new_value = old_value - coins_out + coins_in
            new_row.append(new_value)
        new_board.append(new_row)
    return new_board


def number_of_coins_out(b: Board, r: int, c: int) -> int:
    """
    Return the number of coins that cell (r, c) sends to its neighbors.
    
    Parameters:
        b: The current sandpile board.
        r: Row index of the cell.
        c: Column index of the cell.
    
    Returns:
        int: Total number of coins sent out.
    """
    return (b[r][c] // 4) * 4

def number_of_coins_in(b: Board, r: int, c: int) -> int:
    """
    Return the number of coins that cell (r, c) receives from its neighbors.
    
    Parameters:
        b: The current sandpile board.
        r: Row index of the cell.
        c: Column index of the cell.
    
    Returns:
        int: Total number of coins received from all neighbors.
    """
    # Define variables
    total_coins = 0
    neighbors = [
        (r - 1, c),  # North
        (r + 1, c),  # South
        (r, c - 1),  # West
        (r, c + 1)   # East
    ]
    # Check each neighbor
    for nr, nc in neighbors:
        # Check if in bounds
        if 0 <= nr < len(b) and 0 <= nc < len(b[0]):
            # Add coins from this neighbor
            total_coins += b[nr][nc] // 4
    return total_coins

