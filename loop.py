user_data = {'762662833094656011': {'name': 'nimingdehaoyou_agf', 'guesses': [41, 88, 5, 76], 'user_avg': 52.5}, '373052955949268992': {'name': 'kcnkvs', 'guesses': [70, 75], 'user_avg': 72.5}}

# result 
# Rankings by average number of guesses:
# 1. name (52)
# 2. tina (72.5)

counter = 1
for key, value in user_data.items():
    #do nothing with key
    username = value['name']
    avg = value['user_avg']
    msg = f"{counter}. {username} ({avg})"
    counter += 1
    print(msg)


#Rank by smallest guess to largest guess

# Create a list of tuples containing (user_id, name, user_avg)
leaderboard_data = [(user_id, info['name'], info['user_avg']) for user_id, info in user_data.items()]
print(leaderboard_data)

# Sort the list based on user_avg (which is the third element in each tuple)
sorted_users = sorted(user_data, key=lambda x: x[2], reverse=True)
print(sorted_users)

def find_avg(user_data):
    leaderboard = []
    counter = 1
    sorted_data = dict(sorted(user_data.items(), key=lambda item: item[1]['user_avg']))
    for key, value in sorted_data.items():
        username = value['name']
        avg = value['user_avg']
        msg = f"{counter}. {username} ({avg})"
        leaderboard.append(msg)
        counter += 1
    return "\n".join(leaderboard)

print(find_avg(user_data))

