import itertools
assignments = []
rows = 'ABCDEFGHI'
cols = '123456789'

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    print(values)
    print(box)
    print(value)
    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    nakedTwins = [[a,b] for a in boxes for b in boxes if a != b and values[a] == values[b] and b in peers[a] and len(values[a]) == 2 and len(values[b]) == 2]
    #remove duplicates if any
    
    # Eliminate the naked twins as possibilities for their peers
    for pair in nakedTwins:
        for eachUnit in units[pair[0]]:
            if pair[1] in eachUnit: # check if [A1,A2] are in same unit
                for box in eachUnit:
                    if box not in pair:
                        val = values[box]
                        for ch in values[pair[0]]:
                            val = val.replace(ch,'')
                        assign_value(values, box, val)
                        
    return values

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

# decode the string to a dictionary format
def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    assert len(grid) == 81 , "Invalid: string length != 81"
    i = 0
    dictionary = {}
    replacement = '123456789'
    
    for r in 'ABCDEFGHI':
        for c in '123456789':
            if grid[i] == '.':
                dictionary[r+c] = replacement
            else:
                dictionary[r+c] = grid[i]
            i+=1
    return dictionary

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            assign_value(values, peer, values[peer].replace(digit,''))
    return values

def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                assign_value(values,dplaces[0], digit)
    return values

def reduce_puzzle(values):
    stalled = False
    while not stalled:

        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])


        values = eliminate(values)
        
        values = naked_twins(values)
        #print("\n================================AFTER ELIMINATION====================================\n")
        #display(values)
        
        values = only_choice(values)
        #print("\n================================AFTER ONLY CHOICE====================================\n")
        #display(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])

        stalled = solved_values_before == solved_values_after
        #print("\n================================IS STALLED = ====================================\n")
        #print(stalled)
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and
    #print("\n===================SINCE STALLED USING RANDOM VALUE WITH MIN OCCURENCE============================\n")
    #print("GRID-" ,s)
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        #print("VALUE ASSIGNED = " + value)
        attempt = search(new_sudoku)
        #print("THIS ATTEMPT PASSED : " , attempt != False)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    return search(grid_values(grid))


boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units
# units = [[row],[col],[square]]
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)

# diagonal
diagonal = [rows[i]+cols[i] for i in range(0,9)]
#anti-diagonal
anti_diagonal = [rows[i]+cols[8-i] for i in range(0,9)]

for element in diagonal:
    units[element] = units[element]+[diagonal]
    
for element in anti_diagonal:
    units[element] = units[element]+[anti_diagonal]
   
# peers = [row+col+square]
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

if __name__ == '__main__':
    diag_sudoku_grid = '....9......8.6.5...9.5.2.8...1.4.9..74.6.9.23..9.2.4...1.9.8.4...6.1.8......5....'
    #'......8.68.........7..863.....8............8..8.5.9...1.8..............8.....8.4.'
    #'2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
 