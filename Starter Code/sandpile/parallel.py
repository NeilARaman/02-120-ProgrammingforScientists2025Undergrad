from datatypes import Board
import multiprocessing
from serial import (
    number_of_coins_in,
    number_of_coins_out,
    deep_copy_board
)
from helper_functions import num_rows, num_cols


def simulate_sandpiles_parallel(initial_board: Board,
                                num_procs: int | None = None) -> list[Board]:
    """
    Run the sandpile simulation using multiprocessing until it converges.
    
    Parameters:
        initial_board: The starting configuration.
        num_procs: Number of processes to use.
    
    Returns:
        list[Board]: All boards from the initial to final stable state.
    """
    # Default to number of CPU cores if not specified
    if num_procs is None:
        num_procs = multiprocessing.cpu_count()
    
    # Start with a list containing the initial board
    final_boards = [deep_copy_board(initial_board)]
    # Get the current board
    current_board = deep_copy_board(initial_board)
    
    # Keep updating until stable
    while not is_converged_multi_procs(current_board, num_procs):
        # Apply one update step
        current_board = update_multi_procs(current_board, num_procs)
        # Add this board to history
        final_boards.append(deep_copy_board(current_board))
    
    return final_boards


def _check_chunk_helper(args):
    """Helper function for Pool.map - checks if chunk has any cells >= 4"""
    board, start, end = args
    cols = len(board[0]) if board else 0
    
    for i in range(start, end):
        for j in range(cols):
            if board[i][j] >= 4:
                return False  # Found unstable cell
    return True  # All cells stable


def is_converged_multi_procs(b: Board, num_procs: int) -> bool:
    """
    Check if board is stable using multiprocessing.
    
    Parameters:
        b: The sandpile board.
        num_procs: Number of processes to use.
    
    Returns:
        bool: True if all cells < 4, False otherwise.
    """
    rows = num_rows(b)
    if rows == 0:
        return True
    
    # Make row chunks
    chunks = make_row_chunks(rows, num_procs)
    
    # Create arguments for each worker
    args_list = [(b, start, end) for start, end in chunks]
    
    # Use Pool to check chunks in parallel
    with multiprocessing.Pool(processes=num_procs) as pool:
        results = pool.map(_check_chunk_helper, args_list)
    
    # If all chunks are stable (all True), board is converged
    return all(results)


def _update_chunk_helper(args):
    """Helper function for Pool.map - updates a chunk of rows"""
    board, start, end = args
    cols = num_cols(board)
    updated_rows = []
    
    for i in range(start, end):
        new_row = []
        for j in range(cols):
            old_value = board[i][j]
            coins_out = number_of_coins_out(board, i, j)
            coins_in = number_of_coins_in(board, i, j)
            new_value = old_value - coins_out + coins_in
            new_row.append(new_value)
        updated_rows.append(new_row)
    
    return (start, updated_rows)


def update_multi_procs(b: Board, num_procs: int) -> Board:
    """
    Update the sandpile board using multiprocessing.
    
    Parameters:
        b: The current sandpile board.
        num_procs: Number of processes to use.
    
    Returns:
        Board: A new board after one update step.
    """
    rows = num_rows(b)
    if rows == 0:
        return []
    
    # Make row chunks for processing
    chunks = make_row_chunks(rows, num_procs)
    
    # Create arguments for each worker
    args_list = [(b, start, end) for start, end in chunks]
    
    # Use Pool to update chunks in parallel
    with multiprocessing.Pool(processes=num_procs) as pool:
        results = pool.map(_update_chunk_helper, args_list)
    
    # Sort results by row_start to ensure correct order
    results.sort(key=lambda x: x[0])
    
    # Assemble the complete new board
    new_board = []
    for row_start, updated_rows in results:
        for row in updated_rows:
            new_board.append(row)
    
    return new_board


def make_row_chunks(total_rows: int, num_procs: int) -> list[tuple[int, int]]:
    """
    Divide rows into chunks for parallel processing.
    
    Parameters:
        total_rows: Total number of rows to divide.
        num_procs: Number of processes/chunks desired.
    
    Returns:
        list[tuple[int, int]]: List of (start, end) pairs for each chunk.
    """
    num_chunks = min(num_procs, total_rows)
    chunk_size = total_rows // num_chunks
    chunks = []
    start = 0
    
    for i in range(num_chunks):
        # For the last chunk, extend to the end
        if i == num_chunks - 1:
            end = total_rows
        else:
            end = start + chunk_size
        chunks.append((start, end))
        start = end
    
    return chunks
