user_data = {'762662833094656011': {'name': 'name', 'hints': [2], 'user_avg': 12.5, 'avg_hints': 2}, '373052955949268992': {'name': 'kcnkvs', 'guesses': [70, 75], 'user_avg': 72.5, 'avg_hints': 0}}

message = """I played contexto.me #717 and got it in 12 guesses.
🟩🟩 16
🟨🟨🟨 106
🟥🟥🟥🟥🟥 101"""

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

import re

def extract_last_three_numbers(text):
    # Split the string by periods and get the last part
    last_part = text.split('.')[-1].strip()
    
    # Use regular expression to find all numbers (1-3 digits) in the last part
    numbers = re.findall(r'\b\d{1,3}\b', last_part)
    
    # Return the last three numbers (or fewer if there aren't three)
    return numbers[-3:]

# Example usage
result = extract_last_three_numbers(message)
print(result)  # Output: ['15', '21', '41']