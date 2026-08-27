import pygetwindow as gw

def move_window(window_title, x, y):
    """
    Move the window with the given title to the specified coordinates.

    :param window_title: Title of the window to move.
    :param x: X-coordinate to move the window to.
    :param y: Y-coordinate to move the window to.
    """
    try:
        # Get the window object by title
        window = gw.getWindowsWithTitle(window_title)[0]
        # Move the window to the specified coordinates
        window.moveTo(x, y)
        print(f"Moved {window_title} to ({x}, {y})")
    except IndexError:
        print(f"Window with title '{window_title}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")