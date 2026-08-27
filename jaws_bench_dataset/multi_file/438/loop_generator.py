# loop_generator.py
# This file contains the function to generate a specified number of loops.

def generate_loops(num_loops):
    """
    Generates a specified number of loops.

    Args:
    num_loops (int): The number of loops to generate.
    """
    for i in range(num_loops):
        print(f"Loop {i + 1}:")
        for j in range(5):  # Example inner loop
            print(f"  Iteration {j + 1}")