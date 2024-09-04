user_data = {'762662833094656011': {'name': 'nimingdehaoyou_agf', 'guesses': [41, 88, 5, 76], 'user_avg': 52.5}, '373052955949268992': {'name': 'kcnkvs', 'guesses': [70, 75], 'user_avg': 72.5}}

message = "I played contexto.me #717 and got it in 1 guesses and 1 hints"

guesses = int(message.split("and got it in")[1].split("guesses")[0].strip()) 
hints = int(message.split("guesses and")[1].split("hints")[0]) 

print(hints)
