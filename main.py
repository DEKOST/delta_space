from flask import Flask, jsonify, session, render_template
from flask_cors import CORS
import random
import time

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
CORS(app)

# Временное "хранилище" данных (для демо)
players = {}


class SpaceEngine:
    @staticmethod
    def generate_jump():
        events = {
            'black_hole': {'fuel': -20, 'score': 50, 'text': "🕳️ Гравитационная аномалия!"},
            'fuel_station': {'fuel': 30, 'score': 20, 'text': "⛽ Заправка у космической станции"},
            'asteroid': {'fuel': -10, 'score': 100, 'text': "☄️ Пролет через астероидный пояс"},
            'empty': {'fuel': -5, 'score': 10, 'text': "🌌 Тишина и спокойствие"}
        }
        event = random.choice(list(events.keys()))
        return {
            **events[event],
            'coordinates': {
                'x': random.randint(-100, 100),
                'y': random.randint(-100, 100)
            }
        }


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/start', methods=['POST'])
def start_game():
    player_id = str(random.randint(1000, 9999))
    session['player_id'] = player_id
    players[player_id] = {
        'fuel': 100,
        'score': 0,
        'position': {'x': 0, 'y': 0}
    }
    return jsonify({
        'status': 'ready',
        'fuel': 100,
        'position': players[player_id]['position']
    })


@app.route('/jump', methods=['POST'])
def make_jump():
    player_id = session.get('player_id')
    if not player_id or player_id not in players:
        return jsonify({'error': 'Игра не начата'}), 400

    jump_data = SpaceEngine.generate_jump()
    players[player_id]['fuel'] = max(0, players[player_id]['fuel'] + jump_data['fuel'])
    players[player_id]['score'] += jump_data['score']
    players[player_id]['position'] = jump_data['coordinates']

    # Имитация задержки связи
    time.sleep(1.5)

    return jsonify({
        **jump_data,
        'total_fuel': players[player_id]['fuel'],
        'total_score': players[player_id]['score']
    })


@app.route('/leaderboard')
def leaderboard():
    return jsonify([
        {'name': f'Player_{i}', 'score': 10000 - i * 1000}
        for i in range(1, 6)
    ])


if __name__ == '__main__':
    app.run(debug=True)