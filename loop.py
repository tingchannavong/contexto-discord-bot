user_data = {'762662833094656011': {'name': 'name', 'hints': [2], 'user_avg': 12.5, 'avg_hints': 2}, '373052955949268992': {'name': 'kcnkvs', 'guesses': [70, 75], 'user_avg': 72.5, 'avg_hints': 0}}

message = "I played contexto.me #717 and got it in 1 guesses and 2 hints."

# Handle contexto hints
if "hints" in message:
    hints = int(message.split("guesses and")[1].split("hint")[0])
    print(hints)
    if 'hints' in user_data[str('762662833094656011')]:
        user_data[str('762662833094656011')]['hints'].append(hints)
    else:
        user_data[str('762662833094656011')] = {'name': 'name', 'hints': [hints]}
        print(hints)

    user_data[str('762662833094656011')]['avg_hints'] = hints # Update each user average hint
    print(user_data)
else:
    print('hints dont exist')
    pass

def make_leaderboard(user_data):
    leaderboard = []
    counter = 1
    sorted_data = dict(sorted(user_data.items(), key=lambda item: item[1]['user_avg']))
    for key, value in sorted_data.items():
        username = value['name']
        avg = value['user_avg']
        avg_hints = value[avg_hints]
        msg = f"{counter}. {username} ({avg}) & uses ({avg_hints}) hints."
        leaderboard.append(msg)
        counter += 1
    return "\n".join(leaderboard)

leaderboard = make_leaderboard(user_data)
print(leaderboard)