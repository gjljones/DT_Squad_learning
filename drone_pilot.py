from drone_pilot_functions import (
    read_instructions,
    mark_starting_position,
    track_movement,
    get_direction_offset,
)

if __name__ == "__main__":
    # you need to define the path to file of instructions here
    file_path = "D:\\Development\\DT_Squad_learning\\instructions.txt"

    # This section creates the blank grid that will be worked with later
    rows = []
    number_of_columns = 10
    number_of_rows = 10
    for row_index in range(number_of_rows):
        line=[]
        for column_index in range(number_of_columns):
            line.append('.')
        rows.append(line)

    result = read_instructions(file_path,number_of_columns,number_of_rows)
        
    if result:
        (start_x, start_y), directions = result
            
        # Mark starting position
        rows = mark_starting_position(rows, start_x, start_y)
    #    print("\nGrid with starting position marked:")

    rows=track_movement(rows,start_x,start_y,directions)

    # This section will print the grid having constructed it using the previous functions.
    for row in rows:
        print(' '.join(row))
