import sys
import tkinter as tk
from tkinter import filedialog

def read_instructions(filename,number_of_columns,number_of_rows,debug=False):
    """
    Reads movement instructions from a file with debug output.
    """
    if debug:
        print("debug mode is on")
    try:
        with open(filename, 'r') as file:
            # Read and process the starting coordinates
            start_coords = file.readline().strip().split(',')
            
            # Debug output for raw input
            # print("\nDebug Information:")
            # print(f"Raw coordinates from file: {start_coords}")
            
            # Convert to integers with validation
            if len(start_coords) != 2:
                message="Error: Invalid coordinate format. Expected 2 numbers separated by comma."
                return_package=dict(rc=4, message=message, route_data=None)
                return return_package
                
            try:
                start_x = int(start_coords[0])
                start_y = int(start_coords[1])
                
                # Debug output for converted coordinates
                # print(f"Converted coordinates:")
                # print(f"start_x = {start_x} (type: {type(start_x)})")
                # print(f"start_y = {start_y} (type: {type(start_y)})")
                
                # Validate coordinate ranges (assuming 10x10 grid)
                if not (0 <= start_x <= number_of_columns-1 and 0 <= start_y <= number_of_rows-1):
                    return_package=dict(rc=4, message="starting coordinates out of range",route_data=None)
                    return return_package
                
            except ValueError:
                return_package=dict(rc=4, message="Starting coordinates invalid",route_data=None)
                return return_package
            
            # Read and validate directions
            directions = [direction.strip().lower() for direction in file.readlines()]
            # print("\nDirections read from file:")
            # print(directions)
            
            # Validate directions
            valid_directions = {'north', 'south', 'east', 'west', 
                              'northeast', 'northwest', 'southeast', 'southwest',
                              'n', 's', 'e', 'w', 'ne', 'nw', 'se', 'sw'}
            invalid_directions = [d for d in directions if d not in valid_directions]
            if invalid_directions:
                return_package=dict(rc=4, message="Directions invalid",route_data=None)
                return return_package
            route_data = dict(start_x=start_x, start_y=start_y, directions=directions)
            return_package = dict(route_data=route_data, rc=0, message="Instructions read successfully")
            return return_package
            
    except FileNotFoundError:
        message = f"Error: File {filename} not found"
        return_package = dict(rc=4, message=message, route_data=None)
        return return_package
    except Exception as e:
        message = f"Error reading file: {str(e)}"
        return_package=dict(rc=4, message=message, route_data=None)
        return return_package

"""# Test the function
def test_coordinate_reading():
    print("Testing coordinate reading...")
    
    # Replace this with your actual file path
    #file_path = "D:\\Development\\DT_Squad_learning\\instructions.txt"
    
    result = read_instructions(file_path)
    
    if result:
        (start_x, start_y), directions = result
        print("\nFinal Results:")
        print(f"Starting position: ({start_x}, {start_y})")
        print(f"Number of directions read: {len(directions)}")
        print("All tests completed.")
    else:
        print("Failed to read instructions.")

# Run the test
if __name__ == "__main__":
    test_coordinate_reading()"""

def get_validated_integer(prompt, min_value=None, max_value=None):
    """
    Prompts user for an integer within the specified range.
    Continues prompting until valid input is received.
    
    Args:
        prompt (str): The prompt to display to the user
        min_value (int, optional): Minimum acceptable value (inclusive)
        max_value (int, optional): Maximum acceptable value (inclusive)
    
    Returns:
        int: Validated integer within range
    """
    while True:
        try:
            # Get user input and convert to integer
            user_input = input(prompt)
            value = int(user_input)
            
            # Check if value is within range (if ranges were provided)
            if min_value is not None and value < min_value:
                print(f"Error: Input must be at least {min_value}.")
                continue
                
            if max_value is not None and value > max_value:
                print(f"Error: Input must be at most {max_value}.")
                continue
                
            # If we get here, input is valid
            return value
            
        except ValueError:
            print("Error: Please enter a valid integer.")

def mark_starting_position(grid, start_x, start_y):
    """
    Places a '0' at the starting position in the grid
    """
    grid[start_y][start_x] = '0'
    return grid

def get_direction_offset(direction):
    """
    Converts cardinal direction to x,y coordinate changes
    """
    direction_mapping = {
        'north': (0, -1),
        'south': (0, 1),
        'east': (1, 0),
        'west': (-1, 0),
        'northeast': (1, -1),
        'northwest': (-1, -1),
        'southeast': (1, 1),
        'southwest': (-1, 1),
        'n': (0, -1),
        's': (0, 1),
        'e': (1, 0),
        'w': (-1, 0),
        'ne': (1, -1),
        'nw': (-1, -1),
        'se': (1, 1),
        'sw': (-1, 1)
    }
    return direction_mapping.get(direction.lower(), (0, 0))

def track_movement(rows, start_x, start_y, directions):
    """
    Tracks movement through the grid, marking each position with a number
    """
    current_x, current_y = start_x, start_y
    # Start with 0 for the starting position
    move_number = 0
    
    # Mark starting position
    rows[current_y][current_x] = str(move_number)
    
    # print(f"\nStarting at position ({current_x}, {current_y})")
    
    # Process each direction
    for direction in directions:
        # Get the x,y changes for this direction
        dx, dy = get_direction_offset(direction)
        
        # Calculate new position
        new_x = current_x + dx
        new_y = current_y + dy
        
        # Check if new position is within grid bounds
        if 0 <= new_x < len(rows[0]) and 0 <= new_y < len(rows):
            move_number += 1
            current_x, current_y = new_x, new_y
            rows[current_y][current_x] = str(move_number)
            # print(f"Move {move_number}: {direction} to position ({current_x}, {current_y})")
        else:
            print(f"Warning: Move {move_number + 1} in direction {direction} would go out of bounds - check directions and start again")
            return rows
    
    return rows

def get_grid(number_of_columns, number_of_rows):
    # This section creates the blank grid that will be worked with later
    rows = []
    for row_index in range(number_of_rows):
        line=[]
        for column_index in range(number_of_columns):
            line.append('.')
        rows.append(line)
    return rows

def select_file():
    """
    Opens a file dialog to let the user select an instruction file
    Returns the selected file path or None if canceled
    """
    root = tk.Tk()
    root.attributes('-topmost', True)  # Make window stay on top
    root.withdraw()  # Hide the main window
    
    file_path = filedialog.askopenfilename(
        title="Select Instruction File",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        parent=root # set the parent window
    )

    root.destroy()
    
    if file_path:
        print(f"Selected file: {file_path}")
        return file_path
    else:
        print("No file selected. Program terminating.")
        sys.exit(1)

if __name__ == "__main__":
    number_of_columns = get_validated_integer("how many columns do you want in the grid?", 5, 20)
    number_of_rows = get_validated_integer("how many rows do you want in the grid?", 5, 20)
    rows=get_grid(number_of_columns,number_of_rows)

    # add some error comparisons
    # comparison 1 correct number of rows
    if len(rows) == number_of_rows:
        print("Test 1 passed")
    else:
        print("Test 1 failed")
    # comparison 2 correct number of columns
    if len(rows[1]) == number_of_columns:
        print("Test 2 passed")
    else:
        print("Test 2 failed")
    # comparison 3 correct notation in each columns of every row
    test_worked = True
    for row in rows:
        for column in row:
            if not column == '.':
                test_worked = False
                break
    if test_worked:
        print("Test 3 passed")
    else:
        print("Test 3 failed, reinstall universe and reboot from start")

    # you need to define the path to file of instructions here
#    file_path = "D:\\Development\\DT_Squad_learning\\instructions.txt"
    file_path=select_file()
    
    result = read_instructions(file_path,number_of_columns, number_of_rows)
#    result = read_instructions(file_path,number_of_columns, number_of_rows, debug=True)

    # check if there is an error
    if result['rc'] == 0:
        print("no errors continuing with processing")
        route_points = result['route_data']
    else:
        print(f"error in instructions file; code = {result['rc']}; error message; {result['message']}")
        sys.exit(1)
        

    if route_points:
        start_x= route_points['start_x']
        start_y= route_points['start_y']
        directions = route_points['directions']
            
        # Mark starting position
        rows = mark_starting_position(rows, start_x, start_y)
    #    print("\nGrid with starting position marked:")

    # add test 4 to ensure that there is only a single 0 in the grid
    test_worked = True
    count_zeros = 0
    for row in rows:
        for column in row:
            if column == '0':
                count_zeros += 1
    if not count_zeros==1:
        test_worked=False
    if test_worked:
        print("Test 4 passed")
    else:
        print("Test 4 failed, incorrect number of starting positions in grid")     

    rows=track_movement(rows,start_x,start_y,directions)

    # This section will print the grid having constructed it using the previous functions.
    for row in rows:
        print(' '.join(row))
