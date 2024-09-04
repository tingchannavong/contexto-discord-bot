# A discord app to collect Contexto game statistics from users, store it as json file and create a leaderboard. Also Deletemydata, take inspiration from function of wordle bot.
import discord
from discord.ext import commands
import json
import os

# File path for the JSON file
DATA_FILE = "user_data.json"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Load user data from JSON file if it exists
def load_user_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return {}

# Save user data to JSON file
def save_user_data():
    with open(DATA_FILE, "w") as file:
        json.dump(user_data, file, indent=4)

# Initialize user data from the file
user_data = load_user_data()

# Function to find leaderboard by looping through userdata, while sorting from smallest to largest average guesses.
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

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if "played contexto.me" in message.content.lower():
        try:
            guesses = int(message.content.split("and got it in")[1].split("guesses")[0].strip()) #This parsing needs more variety for 100 with hints etc.
            user = message.author

            if str(user.id) in user_data:
                user_data[str(user.id)]['guesses'].append(guesses)
                #logging
                print(user_data)
            else:
                user_data[str(user.id)] = {'name': user.name, 'guesses': [guesses]}

            average_guesses = sum(user_data[str(user.id)]['guesses']) / len(user_data[str(user.id)]['guesses'])

            # Update each user average guess
            user_data[str(user.id)]['user_avg'] = average_guesses

            save_user_data()  # Save data after each update
            
            #LOGGING
            print(user_data)

            await message.channel.send(
                f"{user.name}, your average guesses so far: {average_guesses:.2f}"
            )

        except (ValueError, IndexError):
            await message.channel.send("I couldn't parse your guesses. Please make sure your message is in the correct format.")

    await bot.process_commands(message)

@bot.command()
async def myscore(ctx, user: discord.User = None): 
    user = user or ctx.author 
    if str(user.id) in user_data:
        average_guesses = sum(user_data[str(user.id)]['guesses']) / len(user_data[str(user.id)]['guesses']) 
        await ctx.send(f"{user.name}'s average guesses: {average_guesses:.2f}")
    else:
        await ctx.send(f"No data for {user.name} yet.")

@bot.command()
async def avg(ctx, user: discord.User = None):
    """!avg use this bot command to find average number of guesses and display the leaderboard."""
    user = user or ctx.author
    leaderboard = find_avg(user_data)
    await ctx.send(f"Rankings by average number of guesses:\n{leaderboard}")

bot.run('Your bot token')