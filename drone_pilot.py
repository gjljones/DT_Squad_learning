from drone_pilot_functions import (
    read_instructions,
    get_validated_integer,
    mark_starting_position,
    track_movement,
    get_direction_offset,
    select_file,
    get_grid
)

if __name__ == "__main__":

    # This section creates the blank grid that will be worked with later
    rows = []
    number_of_columns = 15
    number_of_rows = 10
    rows = get_grid(number_of_columns, number_of_rows)

    file_path = select_file()

    result = read_instructions(file_path,number_of_columns,number_of_rows)

    route_points = result['route_data']

    if route_points:
        start_x= route_points['start_x']
        start_y= route_points['start_y']
        directions = route_points['directions']
            
        # Mark starting position
        rows = mark_starting_position(rows, start_x, start_y)
    #    print("\nGrid with starting position marked:")

    rows=track_movement(rows,start_x,start_y,directions)

    # This section will print the grid having constructed it using the previous functions.
    for row in rows:
        print(' '.join(row))
