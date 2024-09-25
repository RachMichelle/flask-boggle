from boggle import Boggle
from flask import Flask, render_template, session, request, jsonify

app = Flask(__name__)
app.config["SECRET_KEY"] = "bogglegame"

boggle_game = Boggle()

@app.route('/')
def show_home():
    """home screen with start button, creates new gameboard"""

    game_board = boggle_game.make_board()
    session['gameboard'] = game_board
    score = 0
    session['score'] = score

    return render_template('home.html')

@app.route('/game')
def show_game():
    """creates boggle board on screen adn starts game"""

    game_board = session['gameboard']

    score = session['score']
    print(score)

    return render_template('game.html', game_board = game_board, score=score)

@app.route('/score')
def get_score():
    """gets score from session (primarily for page load on refresh)"""

    score = session['score']
    return jsonify({'score': score})

@app.route('/check')
def check_answer():
    """check if entered word is valid--only add to score if result=ok"""

    word = request.args['guess']
    
    game_board = session['gameboard']

    score = session['score']

    res =  boggle_game.check_valid_word(game_board, word)

    if res == 'ok':
        score += 1
        session['score'] = score

    return jsonify({'result' : res, 'score': score})