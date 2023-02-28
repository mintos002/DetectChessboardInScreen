import tkinter as tk

# Create the main window
root = tk.Tk()

# Define the dimensions of the chess grid
WIDTH = 640
HEIGHT = 640
ROWS = 8
COLS = 8

# Define the colors of the grid
LIGHT_COLOR = "white"
DARK_COLOR = "gray"

# Define the piece names and their corresponding symbols
piece_names = {
    'black_king': 'k',
    'black_queen': 'q',
    'black_rook': 'r',
    'black_bishop': 'b',
    'black_knight': 'n',
    'black_pawn': 'p',
    'white_knight': 'N',
    'white_pawn': 'P',
    'white_king': 'K',
    'white_queen': 'Q',
    'white_rook': 'R',
    'white_bishop': 'B'
}

# Create the canvas to draw the grid on
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)

# Draw the squares of the chess grid
for row in range(ROWS):
    for col in range(COLS):
        x1 = col * (WIDTH / COLS)
        y1 = row * (HEIGHT / ROWS)
        x2 = (col + 1) * (WIDTH / COLS)
        y2 = (row + 1) * (HEIGHT / ROWS)
        color = LIGHT_COLOR if (row + col) % 2 == 0 else DARK_COLOR
        canvas.create_rectangle(x1, y1, x2, y2, fill=color)

# Create the piece selector
piece_frame = tk.Frame(root)
piece_frame.pack(side=tk.RIGHT)

selected_piece = tk.StringVar()
for piece_name in piece_names:
    tk.Radiobutton(piece_frame, text=piece_name, variable=selected_piece, value=piece_name).pack()

# Define the function to place a piece on the chessboard
pieces = {}
def place_piece(event):
    row = int(event.y / (HEIGHT / ROWS))
    col = int(event.x / (WIDTH / COLS))
    piece_symbol = piece_names[selected_piece.get()]
    pieces[(row, col)] = piece_symbol
    print(pieces)

def generate_fen_from_pieces(pieces):
    # Initialize an empty board
    board = [['' for _ in range(8)] for _ in range(8)]

    # Populate the board with the pieces
    for piece in pieces:
        row, col = piece['position']
        board[row][col] = piece['name']

    # Convert the board to FEN format
    fen = ''
    empty_count = 0
    for row in board:
        for square in row:
            if square == '':
                empty_count += 1
            else:
                if empty_count > 0:
                    fen += str(empty_count)
                    empty_count = 0
                fen += square
        if empty_count > 0:
            fen += str(empty_count)
            empty_count = 0
        fen += '/'

    # Remove the trailing slash and add the other FEN components
    fen = fen[:-1] + ' w KQkq - 0 1'

    return fen

fen = generate_fen_from_pieces(pieces)
print(fen)

# Bind the function to the canvas click event
canvas.bind("<Button-1>", place_piece)

# Pack the canvas and start the main event loop
canvas.pack()
root.mainloop()
