import copy

# ---------- Global Structures ----------
class Square:
    def __init__(self, value=0, column=None, row=None, filled=False):
        self.value = value
        self.column = column
        self.row = row
        self.boxnum = ((row - 1) // 3) * 3 + ((column - 1) // 3) + 1
        self.bool_list = [filled] + [False] * 9


# ---------- Sudoku Board Initialization ----------
def create_empty_board():
    return [[None for _ in range(9)] for _ in range(9)]

def fill_initial_board(sdk):
    mode = input("Enter '1' to input row-by-row, '2' to paste all rows in one line separated by whitespace: ").strip()
    rows = []
    if mode == '1':
        print("Enter 9 rows of the Sudoku board, each with 9 digits (use 0 for empty cells):")
        while len(rows) < 9:
            line = input(f"Row {len(rows)+1}: ").strip()
            if len(line) == 9 and line.isdigit():
                rows.append(line)
            else:
                print("Invalid row. Please enter exactly 9 digits.")
    elif mode == '2':
        print("Paste 9 rows in a single line, separated by whitespace:")
        while True:
            raw = input("Input: ").strip()
            rows = raw.split()
            if len(rows) == 9 and all(len(row) == 9 and row.isdigit() for row in rows):
                break
            print("Invalid input. Please enter 9 rows, each with exactly 9 digits, separated by space.")
    else:
        raise ValueError("Invalid selection. Enter 1 or 2.")

    for i in range(9):
        for j in range(9):
            val = int(rows[i][j])
            filled = val != 0
            sdk[i][j] = Square(value=val, row=i+1, column=j+1, filled=filled)


def update_bool_lists(sdk):
    for i in range(9):
        for j in range(9):
            sq = sdk[i][j]
            if sq.bool_list[0]:
                sq.bool_list = [True] * 10
            else:
                row_vals = [sqr.value for sqr in sdk[sq.row - 1]]
                col_vals = [sdk[r][sq.column - 1].value for r in range(9)]
                box_vals = [sqr.value for sqr in get_box(sq.boxnum, sdk)]
                for val in set(row_vals + col_vals + box_vals):
                    if val != 0:
                        sq.bool_list[val] = True


# ---------- Helper Functions ----------
def get_box(boxnum, sdk):
    row_base = ((boxnum - 1) // 3) * 3
    col_base = ((boxnum - 1) % 3) * 3
    return [sdk[row_base + i][col_base + j] for i in range(3) for j in range(3)]

def get_row(rownum, sdk):
    return sdk[rownum - 1]

def get_col(colnum, sdk):
    return [sdk[i][colnum - 1] for i in range(9)]


def fill_square(sq, value, sdk):
    if sq.bool_list[0]:
        raise ValueError("Cannot fill a filled square.")
    if value in [sqr.value for sqr in get_row(sq.row, sdk) + get_col(sq.column, sdk) + get_box(sq.boxnum, sdk)]:
        raise ValueError("Value already exists in row/column/box.")
    sq.value = value
    sq.bool_list = [True] * 10
    for sqr in get_row(sq.row, sdk) + get_col(sq.column, sdk) + get_box(sq.boxnum, sdk):
        sqr.bool_list[value] = True


# ---------- Logic Methods ----------
def find_lone_candidates(sdk):
    results = []
    for region_func, label in [(get_box, 'box'), (get_row, 'row'), (get_col, 'col')]:
        for n in range(1, 10):
            for val in range(1, 10):
                squares = [sqr for sqr in region_func(n, sdk) if not sqr.bool_list[val]]
                if len(squares) == 1:
                    results.append((squares[0], val))
    return results

def solve_step(sdk):
    updated = False
    lone_candidates = find_lone_candidates(sdk)
    for sq, value in lone_candidates:
        try:
            fill_square(sq, value, sdk)
            #print(f"Filled ({sq.row},{sq.column}) with {value} [lone candidate]")
            updated = True
        except ValueError:
            continue
    return updated

def solve(sdk):
    while True:
        update_bool_lists(sdk)
        if not solve_step(sdk):
            break
    if all(sq.bool_list[0] for row in sdk for sq in row):
        print("Sudoku Solved deterministically!")
    else:
        #print("No further deterministic steps possible. Trying backtracking...")
        if solve_with_guessing(sdk):
            #print("Sudoku Solved with backtracking!")
            pass
        else:
            print("Sudoku could not be solved.")


# ---------- Backtracking Guess Logic ----------
def solve_with_guessing(sdk):
    update_bool_lists(sdk)
    if all(sq.bool_list[0] for row in sdk for sq in row):
        return True

    min_options = 10
    target_sq = None
    for row in sdk:
        for sq in row:
            if not sq.bool_list[0]:
                options = [i for i in range(1, 10) if not sq.bool_list[i]]
                if len(options) < min_options:
                    min_options = len(options)
                    target_sq = sq
                if min_options == 1:
                    break

    if not target_sq:
        return False

    for val in range(1, 10):
        if not target_sq.bool_list[val]:
            trial_sdk = copy.deepcopy(sdk)
            try:
                fill_square(trial_sdk[target_sq.row - 1][target_sq.column - 1], val, trial_sdk)
                if solve_with_guessing(trial_sdk):
                    # Copy solved board back
                    for i in range(9):
                        for j in range(9):
                            sdk[i][j].value = trial_sdk[i][j].value
                            sdk[i][j].bool_list = trial_sdk[i][j].bool_list.copy()
                    return True
            except:
                continue
    return False


def print_board(sdk):
    for i in range(9):
        if i in [3, 6]:
            print("------+-------+------")
        for j in range(9):
            val = sdk[i][j].value
            print('.' if val == 0 else val, end=' ' if (j+1) % 3 else ' | ')
        print()


# ---------- Run Example ----------
if __name__ == "__main__":
    sdk = create_empty_board()
    fill_initial_board(sdk)
    solve(sdk)
    print("\nFinal board:")
    print_board(sdk)