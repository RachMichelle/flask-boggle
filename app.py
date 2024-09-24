from boggle import Boggle
from flask import Flask, render_template, session, request, jsonify

app = Flask(__name__)
app.config["SECRET_KEY"] = "bogglegame"

boggle_game = Boggle()

@app.route('/')
def show_home():
    """home screen with start button"""
    return render_template('home.html')

@app.route('/game')
def show_game():
    """creates new boggle board to start game"""
    game_board = boggle_game.make_board()

    session['gameboard'] = game_board
    score=0

    return render_template('game.html', game_board = game_board, score=score)

@app.route('/check')
def check_answer():
    word = request.args['guess']
    
    game_board = session['gameboard']

    res =  boggle_game.check_valid_word(game_board, word)

    return jsonify({'result' : res})