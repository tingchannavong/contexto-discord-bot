user_data = {'762662833094656011': {'name': 'nimingdehaoyou_agf', 'guesses': [41, 88, 5, 76], 'user_avg': 52.5}, '373052955949268992': {'name': 'kcnkvs', 'guesses': [70, 75], 'user_avg': 72.5}}

message = "I played contexto.me #717 and got it in 1 guesses."


# Function to determine switch case
def get_custom_message(guesses_count):
    if guesses_count > 100:
        return "Yer had a good run~"
    elif 75 < guesses_count <= 100:
        return "Maybe you need more hints..."
    elif 45 < guesses_count <= 75:
        return "Good job!"
    elif 15 < guesses_count <= 45:
        return "You're performing as well as an AI."
    else:
        return "Wow, you are god-like!"
    
print(get_custom_message(user_data['762662833094656011']['user_avg']))

guesses = int(message.split("and got it in")[1].split("guesses")[0].strip()) 
try:
    hints = int(message.split("guesses and")[1].split("hints")[0]) 
    print(hints)
    #save hints data
except IndexError:
    pass