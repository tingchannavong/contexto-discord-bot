# Helper functions to create leaderboard and track scores

def calc_avg_guess(user, guess_type, user_data):
    """Takes a discord user id, guess type (name of dictionary key for contexto|letroso guesses) and calculate average guess by sum of guesses list/guess number."""
    average_guesses = sum(user_data[str(user.id)][guess_type]) / len(user_data[str(user.id)][guess_type]) 
    return average_guesses

def calc_avg_hint(user, hint_type, user_data):
    """Takes a discord user id and calculate average Contexto hints."""
    average_hints = sum(user_data[str(user.id)][hint_type]) / len(user_data[str(user.id)][hint_type])
    return average_hints

def count_game_no(user, game_type, user_data):
    """Takes a discord user id and game type (contexto|letroso|conexo guesses) and calculate number of games played."""
    games_played = len(user_data[str(user.id)][game_type])
    return games_played 

# Function to find leaderboard by looping through userdata, while sorting from smallest to largest average guesses.
def make_leaderboard(user_data, game_type, hint_type):
    leaderboard = []
    counter = 1
    filtered_data = {k: v for k, v in user_data.items() if v[game_type] != 0}
    sorted_data = dict(sorted(filtered_data.items(), key=lambda item: item[1][game_type]))
    for key, value in sorted_data.items():
        username = value['name']
        avg = value[game_type]
        avg_hints = value[hint_type]
        if game_type == 'ct_avg' or game_type == 'cn_avg':
            msg = f"{counter}. {username} ({avg}) and uses ({avg_hints}) hints."
            leaderboard.append(msg)
        elif game_type == 'lt_avg':
            msg = f"{counter}. {username} ({avg})"
            leaderboard.append(msg)
        counter += 1
    return "\n".join(leaderboard)

def get_custom_message(guesses_count):
    if guesses_count > 100:
        return "Yer had a good run~"
    elif 75 < guesses_count <= 100:
        return "Maybe you need more hints..."
    elif 45 < guesses_count <= 75:
        return "Good job!"
    elif 15 < guesses_count <= 45:
        return "You're performing as well as an AI."
    elif guesses_count == 1:
        return "Let's be honest, are you cheating?"
    else:
        return "Wow, you are god-like!"