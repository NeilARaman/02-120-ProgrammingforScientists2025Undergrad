import os
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1") # hide pygame support prompt
import sys
import time
import imageio
import pygame

from serial import create_board, simulate_sandpiles
from drawing import animate_boards_parallel


def main() -> None:
    """CLI Call:
        python3 main.py <board_width> <num_coins> <random|central> <cell_width>
        try python3 main.py 50 4000 central 10 
        try python3 main.py 300 20000 central 4 # comment serial out
    """
    # Parse command line arguments
    if len(sys.argv) != 5:
        print("Usage: python3 main.py <board_width> <num_coins> <random|central> <cell_width>")
        sys.exit(1)
    
    board_width = int(sys.argv[1])
    num_coins = int(sys.argv[2])
    placement = sys.argv[3].lower()
    cell_width = int(sys.argv[4])
    
    # Validate placement argument
    if placement not in ["random", "central"]:
        print("Placement must be 'random' or 'central'")
        sys.exit(1)
    
    center = (placement == "central")
    
    # Initialize pygame
    pygame.init()
    
    print(f"Creating {board_width}x{board_width} board with {num_coins} coins ({placement} placement)...")
    initial_board = create_board(board_width, board_width, num_coins, center=center)
    
    # Run serial simulation
    print("\n=== Serial Simulation ===")
    start_time = time.time()
    serial_boards = simulate_sandpiles(initial_board)
    serial_time = time.time() - start_time
    print(f"Serial simulation completed in {serial_time:.2f} seconds")
    print(f"Generated {len(serial_boards)} generations")
    
    # Render animation
    print("\n=== Rendering Animation ===")
    start_time = time.time()
    frames = animate_boards_parallel(serial_boards, cell_width)
    render_time = time.time() - start_time
    print(f"Rendered {len(frames)} frames in {render_time:.2f} seconds")
    
    # Write video
    print("Writing sandpile.mp4...")
    imageio.mimsave("sandpile.mp4", frames, fps=30, codec='libx264')
    
    print("\nDone! Created sandpile.mp4")
    pygame.quit()


if __name__ == "__main__":
    main()
