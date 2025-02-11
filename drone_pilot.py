import sys

# This section creates the blank grid that will be worked with later
rows = []
number_of_columns = 10
number_of_rows = 10
for row_index in range(number_of_rows):
    line=[]
    for column_index in range(number_of_columns):
        line.append('.')
    rows.append(line)
# rows[5][5] = "X"

# you need to define the path to file of instructions here
file_path = "D:\\Development\\DT_Squad_learning\\instructions.txt"

def read_instructions(filename):
    """
    Reads movement instructions from a file with debug output.
    """
    try:
        with open(filename, 'r') as file:
            # Read and process the starting coordinates
            start_coords = file.readline().strip().split(',')
            
            # Debug output for raw input
            # print("\nDebug Information:")
            print(f"Raw coordinates from file: {start_coords}")
            
            # Convert to integers with validation
            if len(start_coords) != 2:
                print("Error: Invalid coordinate format. Expected 2 numbers separated by comma.")
                return None
                
            try:
                start_x = int(start_coords[0])
                start_y = int(start_coords[1])
                
                # Debug output for converted coordinates
                # print(f"Converted coordinates:")
                # print(f"start_x = {start_x} (type: {type(start_x)})")
                # print(f"start_y = {start_y} (type: {type(start_y)})")
                
                # Validate coordinate ranges (assuming 10x10 grid)
                if not (0 <= start_x <= number_of_columns-1 and 0 <= start_y <= number_of_rows-1):
                    print(f"Warning: Coordinates out of range for a {number_of_columns}x{number_of_rows} grid!")
                    print(f"X coordinate {start_x} should be between 0 and 9")
                    print(f"Y coordinate {start_y} should be between 0 and 9")
                    sys.exit(1)
                
            except ValueError:
                print("Error: Coordinates must be valid numbers")
                return None
            
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
                print(f"\nWarning: Invalid directions found: {invalid_directions}")
                sys.exit(1)
            
            return (start_x, start_y), directions
            
    except FileNotFoundError:
        print(f"Error: File {filename} not found")
        return None
    except Exception as e:
        print(f"Error reading file: {str(e)}")
        return None

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

result = read_instructions(file_path)
    
if result:
    (start_x, start_y), directions = result
        
    # Mark starting position
    rows = mark_starting_position(rows, start_x, start_y)
#    print("\nGrid with starting position marked:")

rows=track_movement(rows,start_x,start_y,directions)

# This section will print the grid having constructed it using the previous functions.
for row in rows:
    print(' '.join(row))
