import os
import re
from flask import Flask, request, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.secret_key = 'supersecretkey'
app.config['MAX_CONTENT_PATH'] = 1000000  # Maximum file size in bytes

def parse_chess_results(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    results = []
    player_pattern = re.compile(r'^\s*(\d+)\s+([^\d]+?)\s+(\d+)\s+(\w*)\s+(\w+)\s+(\d+\.\d)\s+\|(.+)\|')

    for line in lines:
        match = player_pattern.match(line)
        if match:
            pos, name, rating, title, fed, points, rounds = match.groups()
            round_results = rounds.strip().split()
            parsed_results = []
            for result in round_results:
                match_result = re.match(r'([+=-])([WB])(\d+)', result)
                if match_result:
                    outcome, color, opponent = match_result.groups()
                    parsed_results.append({
                        'outcome': outcome,
                        'color': color,
                        'opponent': int(opponent)
                    })
            player_data = {
                'Pos': int(pos),
                'Name': name.strip(),
                'Rtg': int(rating),
                'T': title.strip(),
                'Fed': fed,
                'Pts': float(points),
                'Rounds': parsed_results
            }
            results.append(player_data)
    
    return results

def get_player_results(results, position):
    player_results = None
    for player in results:
        if player['Pos'] == position:
            player_results = player
            break
    
    if not player_results:
        return f"No player found with position {position}"
    
    opponent_info = []
    for i, round_info in enumerate(player_results['Rounds']):
        opponent_position = round_info['opponent']
        opponent = next((p for p in results if p['Pos'] == opponent_position), None)
        if opponent:
            opponent_info.append({
                'round': i + 1,
                'opponent_name': opponent['Name'],
                'opponent_position': opponent['Pos'],
                'result': round_info['outcome'],
                'color': round_info['color']
            })
    
    return opponent_info

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If user does not select file, browser also submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            position = int(request.form['position'])
            parsed_results = parse_chess_results(filepath)
            player_results = get_player_results(parsed_results, position)
            return render_template('player_results.html', position=position, results=player_results)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

