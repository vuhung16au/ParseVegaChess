import re

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

def print_round(results, round_number):
    pairings = []
    
    for player in results:
        for i, round_info in enumerate(player['Rounds']):
            if i + 1 == round_number:
                opponent_position = round_info['opponent']
                opponent = next((p for p in results if p['Pos'] == opponent_position), None)
                if opponent:
                    pairings.append({
                        'player': player['Name'],
                        'opponent': opponent['Name'],
                        'result': round_info['outcome'],
                        'color': round_info['color']
                    })
    
    if not pairings:
        print(f"No pairings found for round {round_number}")
        return
    
    print(f"Pairings for round {round_number}:")
    for pairing in pairings:
        print(f"{pairing['player']} vs {pairing['opponent']} ({pairing['color']}, result: {pairing['result']})")


# filename = '2024citySydneyBlitz.txt'
filename = '2024NSWRapid.txt'
parsed_results = parse_chess_results(filename)

# Print the pairing for a round
# round_number = int(input("Enter the round number: "))
# print_round(parsed_results, round_number)

# print all players
# for result in parsed_results:
#     print(result)
    
# pos_list = [1, 2, 3, 4, 10, 20]

# for position in pos_list:
#    print("player " + str(position) + ":")
#    player_results = get_player_results(parsed_results, position)
#     for result in player_results:
#         print(result)

position = int(input("Enter the player number: "))

print("player " + str(position) + ":")
player_results = get_player_results(parsed_results, position)
for result in player_results:
    print(result)
