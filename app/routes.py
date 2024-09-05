from flask import render_template, request, session
from app import app
import random


def knight_path(start, end):
    def valid_moves(x, y):
        return [(x + 2, y + 1), (x + 2, y - 1), (x - 2, y + 1), (x - 2, y - 1),
                (x + 1, y + 2), (x + 1, y - 2), (x - 1, y + 2), (x - 1, y - 2)]

    def coord_to_square(x, y):
        return chr(x + 97) + str(y + 1)

    def square_to_coord(square):
        return ord(square[0]) - 97, int(square[1]) - 1

    start_x, start_y = square_to_coord(start)
    end_x, end_y = square_to_coord(end)

    queue = [(start_x, start_y, [start])]
    visited = set()

    while queue:
        x, y, path = queue.pop(0)
        if (x, y) == (end_x, end_y):
            return path

        if (x, y) not in visited:
            visited.add((x, y))
            for nx, ny in valid_moves(x, y):
                if 0 <= nx < 8 and 0 <= ny < 8:
                    queue.append((nx, ny, path + [coord_to_square(nx, ny)]))

    return None


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/knight_game', methods=['GET', 'POST'])
def knight_game():
    if request.method == 'POST':
        user_moves = int(request.form['user_moves'])
        correct_moves = session.get('correct_moves')
        square_a = session.get('square_a')
        square_b = session.get('square_b')
        path = session.get('path')

        if user_moves == correct_moves:
            message = f"Correct! The Knight can move from {square_a} to {square_b} in {correct_moves} move{'s' if correct_moves != 1 else ''}."
            return render_template('result.html', correct=True, message=message,
                                   square_a=square_a, square_b=square_b,
                                   correct_moves=correct_moves, piece="Knight",
                                   game_type='knight_game', path=path)
        else:
            error_message = "Incorrect. Try again!"
            return render_template('knight_game.html', square_a=square_a, square_b=square_b, message=error_message)

    files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    ranks = ['1', '2', '3', '4', '5', '6', '7', '8']
    square_a = random.choice(files) + random.choice(ranks)
    square_b = random.choice(files) + random.choice(ranks)

    while square_b == square_a:
        square_b = random.choice(files) + random.choice(ranks)

    path = knight_path(square_a, square_b)
    correct_moves = len(path) - 1

    session['correct_moves'] = correct_moves
    session['square_a'] = square_a
    session['square_b'] = square_b
    session['path'] = path

    return render_template('knight_game.html', square_a=square_a, square_b=square_b)

@app.route('/bishop_game', methods=['GET', 'POST'])
def bishop_game():
    if request.method == 'POST':
        user_moves = int(request.form['user_moves'])
        correct_moves = session.get('correct_moves')
        square_a = session.get('square_a')
        square_b = session.get('square_b')

        if user_moves == correct_moves:
            if correct_moves == -1:
                message = f"Correct! The Bishop cannot move from {square_a} to {square_b} because it cannot change square colors."
            else:
                message = f"Correct! The Bishop can move from {square_a} to {square_b} in {correct_moves} move{'s' if correct_moves != 1 else ''}."
            return render_template('result.html', correct=True, message=message,
                                   square_a=square_a, square_b=square_b,
                                   correct_moves=correct_moves, piece="Bishop",
                                   game_type='bishop_game')
        else:
            error_message = "Incorrect. Try again!"
            return render_template('bishop_game.html', square_a=square_a, square_b=square_b, message=error_message)

    files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    ranks = ['1', '2', '3', '4', '5', '6', '7', '8']
    square_a = random.choice(files) + random.choice(ranks)
    square_b = random.choice(files) + random.choice(ranks)

    while square_b == square_a:
        square_b = random.choice(files) + random.choice(ranks)

    file_diff = abs(files.index(square_a[0]) - files.index(square_b[0]))
    rank_diff = abs(int(square_a[1]) - int(square_b[1]))

    if file_diff == rank_diff:
        correct_moves = 1
    elif (file_diff + rank_diff) % 2 == 0:
        correct_moves = 2
    else:
        correct_moves = -1  # Impossible move

    session['correct_moves'] = correct_moves
    session['square_a'] = square_a
    session['square_b'] = square_b

    return render_template('bishop_game.html', square_a=square_a, square_b=square_b)



@app.route('/color_game', methods=['GET', 'POST'])
def color_game():
    if request.method == 'POST':
        user_color = request.form['color']
        correct_color = session.get('correct_color')
        square = session.get('square')

        if user_color == correct_color:
            message = f"Correct! {square} is {correct_color}."
            return render_template('result.html', correct=True, message=message,
                                   square_a=square, correct_color=correct_color,
                                   piece="Square", game_type='color_game')
        else:
            error_message = "Incorrect. Try again!"
            return render_template('color_game.html', square=square, message=error_message)

    # Generate a random square
    files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    ranks = ['1', '2', '3', '4', '5', '6', '7', '8']
    square = random.choice(files) + random.choice(ranks)

    # Determine the correct color
    file_index = files.index(square[0])
    rank_index = int(square[1]) - 1
    correct_color = 'black' if (file_index + rank_index) % 2 == 0 else 'white'  # Fixed color determination

    # Store the correct answer in the session
    session['correct_color'] = correct_color
    session['square'] = square

    return render_template('color_game.html', square=square)