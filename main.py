import random

# Global constants for board dimensions
ROWS = 5
COLS = 7

# Sith Lords
VADER = 'V'
MAUL = 'M'
SITH_LORDS = (VADER, MAUL)

# Lightsaber parts
KYBER = 'K'
LENS = 'L'
POWER = 'P'
HILT = 'H'
LIGHTSABER_PARTS = (KYBER, LENS, POWER, HILT)

# Board characters
EMPTY = ' '
JEDI = 'J'
UNVISITED = chr(9608)  # '█'

# Move commands
UP = 'u'
DOWN = 'd'
LEFT = 'l'
RIGHT = 'r'


def create_board():
    board = []
    for row in range(ROWS):
        board_row = []
        for col in range(COLS):
            # Each location is a tuple: (occupant, visited)
            board_row.append((EMPTY, False))
        board.append(board_row)
    return board


def find_empty_position(board):
    empty_positions = []
    for row in range(ROWS):
        for col in range(COLS):
            occupant, visited = board[row][col]
            if occupant == EMPTY:
                empty_positions.append((row, col))
    
    if empty_positions:
        return random.choice(empty_positions)
    return None


def place_sith_lords(board):
    for sith in SITH_LORDS:
        row, col = find_empty_position(board)
        occupant, visited = board[row][col]
        board[row][col] = (sith, visited)


def place_lightsaber_parts(board):
    for part in LIGHTSABER_PARTS:
        row, col = find_empty_position(board)
        occupant, visited = board[row][col]
        board[row][col] = (part, visited)


def place_jedi(board):
    row, col = find_empty_position(board)
    occupant, visited = board[row][col]
    board[row][col] = (occupant, True)  # Mark as visited
    return (row, col)


def display(board, jedi_pos, moves, collected_parts, slain_sith):
    jedi_row, jedi_col = jedi_pos
    
    for row in range(ROWS):
        line = ""
        for col in range(COLS):
            occupant, visited = board[row][col]
            
            if row == jedi_row and col == jedi_col:
                line += JEDI
            elif visited:
                if occupant in slain_sith or occupant in collected_parts:
                    line += occupant
                elif occupant in SITH_LORDS or occupant in LIGHTSABER_PARTS:
                    line += occupant
                else:
                    line += EMPTY
            else:
                line += UNVISITED
        print(line)
    
    print(f"Collected Lightsaber Parts ({len(collected_parts)}/{len(LIGHTSABER_PARTS)}): {sorted(collected_parts)}")
    print(f"Slain Sith Lords ({len(slain_sith)}/{len(SITH_LORDS)}): {sorted(slain_sith)}")
    print(f"Position: {jedi_pos} Moves: {moves}")


def move(board, jedi_pos, direction):
    row, col = jedi_pos
    
    if direction == UP:
        new_row, new_col = row - 1, col
    elif direction == DOWN:
        new_row, new_col = row + 1, col
    elif direction == LEFT:
        new_row, new_col = row, col - 1
    elif direction == RIGHT:
        new_row, new_col = row, col + 1
    else:
        raise ValueError("Invalid direction")
    
    if new_row < 0 or new_row >= ROWS or new_col < 0 or new_col >= COLS:
        raise ValueError("Move is off the board")
    
    occupant, visited = board[new_row][new_col]
    board[new_row][new_col] = (occupant, True)
    
    return ((new_row, new_col), occupant)


def main():
    print(f"Sith Lords: {SITH_LORDS}")
    print(f"Lightsaber Parts: {LIGHTSABER_PARTS}")
    print("May The Force Be With You!")
    
    board = create_board()
    place_sith_lords(board)
    place_lightsaber_parts(board)
    jedi_pos = place_jedi(board)
    
    moves = 0
    collected_parts = []
    slain_sith = []
    
    display(board, jedi_pos, moves, collected_parts, slain_sith)
    
    while True:
        command = input("> ").strip().lower()
        
        if command == 'q':
            print("Goodbye!")
            break
        
        if command in (UP, DOWN, LEFT, RIGHT):
            try:
                new_pos, occupant = move(board, jedi_pos, command)
                jedi_pos = new_pos
                moves += 1
                
                if occupant in SITH_LORDS:
                    if len(collected_parts) == len(LIGHTSABER_PARTS):
                        if occupant not in slain_sith:
                            print(f"You have slain Sith Lord {occupant}!")
                            slain_sith.append(occupant)
                    else:
                        display(board, jedi_pos, moves, collected_parts, slain_sith)
                        print("You have encountered a Sith Lord before")
                        print("rebuilding your lightsaber and have been slain.")
                        print("Goodbye!")
                        break
                
                elif occupant in LIGHTSABER_PARTS:
                    if occupant not in collected_parts:
                        print(f"You found lightsaber part {occupant}!")
                        collected_parts.append(occupant)
                        
                        if len(collected_parts) == len(LIGHTSABER_PARTS):
                            print("You have collected all lightsaber parts and now the")
                            print("hunted has become the hunter!")
                
                display(board, jedi_pos, moves, collected_parts, slain_sith)
                
                if len(slain_sith) == len(SITH_LORDS):
                    print("All Sith Lords have been disposed of. You win!")
                    print("Goodbye!")
                    break
                
            except ValueError:
                print("Invalid move!")
                display(board, jedi_pos, moves, collected_parts, slain_sith)


if __name__ == "__main__":
    main()