from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    # test '/'
    def test_home(self):
        with app.test_client() as client:
            res = client.get('/')
            html = res.get_data(as_text=True)
            
            self.assertEqual(res.status_code, 200)
            self.assertIn('<button  id="start-button">Start!</button>', html)


    # test '/game'
    def test_game(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['gameboard'] = [['P', 'E', 'Q', 'G', 'T'],['S', 'H', 'O', 'D', 'Q'],['H', 'M', 'R', 'T', 'E'],['F', 'U', 'M', 'V', 'W'],['P', 'M', 'P', 'A', 'I']]
                change_session['score'] = 0

            res = client.get('/game')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<button id="submit-guess">Submit!</button>', html)
            self.assertEqual(session['score'], 0)

    # test '/score'
    def test_score(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['score'] = 5
            res = client.get('/score')
            self.assertEqual(res.json['score'], 5)

    # test '/check' with valid word
    def test_check_valid(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['gameboard'] = [['P', 'E', 'Q', 'G', 'T'],['S', 'H', 'O', 'D', 'Q'],['H', 'M', 'R', 'T', 'E'],['F', 'U', 'M', 'V', 'W'],['P', 'M', 'P', 'A', 'I']]
                change_session['score'] = 0
            res = client.get('/check?guess=she')
            self.assertEqual(res.json['result'], 'ok')
            self.assertEqual(res.json['score'], 1)

    # test '/check' with invalid word
    def test_check_invalid(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['gameboard'] = [['P', 'E', 'Q', 'G', 'T'],['S', 'H', 'O', 'D', 'Q'],['H', 'M', 'R', 'T', 'E'],['F', 'U', 'M', 'V', 'W'],['P', 'M', 'P', 'A', 'I']]
                change_session['score'] = 0
            res = client.get('/check?guess=abcd')
            self.assertEqual(res.json['result'], 'not-word')
            self.assertEqual(res.json['score'], 0)

    # test '/check' with valid word not on board
    def test_check_not_on_board(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['gameboard'] = [['P', 'E', 'Q', 'G', 'T'],['S', 'H', 'O', 'D', 'Q'],['H', 'M', 'R', 'T', 'E'],['F', 'U', 'M', 'V', 'W'],['P', 'M', 'P', 'A', 'I']]
                change_session['score']=0
            res = client.get('/check?guess=egg')
            self.assertEqual(res.json['result'], 'not-on-board')
            self.assertEqual(res.json['score'], 0)