# A discord app to collect Contexto game statistics from users, store it as json file, create a leaderboard, delete user data, . Take inspiration from function of wordle bot. 
# To-do: -take hints into account -switch case: customize msgs based on guess no. today  
# -take the colored guess & data visualize pie chart avg?

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

def calc_avg_guess(user):
    """Takes a discord user id and calculate average guess by sum of guesses list/guess number."""
    average_guesses = sum(user_data[str(user.id)]['guesses']) / len(user_data[str(user.id)]['guesses']) 
    return average_guesses

def calc_avg_hint(user):
    """Takes a discord user id and calculate average hints."""
    average_hints = sum(user_data[str(user.id)]['hints']) / len(user_data[str(user.id)]['hints'])
    return average_hints

# Function to find leaderboard by looping through userdata, while sorting from smallest to largest average guesses.
def make_leaderboard(user_data):
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

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if "played contexto.me" in message.content.lower():
        try:
            # Handle contexto guesses
            guesses = int(message.content.split("and got it in")[1].split("guesses")[0].strip()) 
            user = message.author

            if str(user.id) in user_data:
                user_data[str(user.id)]['guesses'].append(guesses)
            else:
                user_data[str(user.id)] = {'name': user.name, 'guesses': [guesses]}

            average_guesses = calc_avg_guess(user)

            user_data[str(user.id)]['user_avg'] = average_guesses  # Update each user average guess

            save_user_data()  # Save data after each update
            # I want to send a customize message based on number of guesses
            await message.channel.send(f"{user.name}, Good job!")

            # Handle contexto hints
            if "hints" in message.content.lower():
                hints = int(message.split("guesses and")[1].split("hints")[0])
                if str(user.id) in user_data:
                    user_data[str(user.id)]['hints'].append(hints)
                else:
                    user_data[str(user.id)] = {'name': user.name, 'hints': [hints]}

                average_hints = calc_avg_hint(user) 
                user_data[str(user.id)]['avg_hints'] = average_hints # Update each user average hint
                save_user_data()  # Save data after each update
            else:
                pass

            # I want to send a customize message based on number of guesses
            await message.channel.send(get_custom_message(user_data[str(user.id)]['user_avg']))

        except (ValueError, IndexError):
            await message.channel.send("I couldn't parse your guesses. Please make sure your message is in the correct format.")

    await bot.process_commands(message)

@bot.command()
async def myscore(ctx, user: discord.User = None): 
    user = user or ctx.author 
    if str(user.id) in user_data:
        average_guesses = calc_avg_guess(user)
        if user_data[str(user.id)]['hints'] in user_data:
            average_hints = calc_avg_hint(user)
            await ctx.send(f"{user.name}'s average guesses: {average_guesses:.2f} and hints: {average_hints}..")
        else:
            await ctx.send(f"{user.name}'s average guesses: {average_guesses:.2f}.")
    else:
        await ctx.send(f"No data for {user.name} yet.")

@bot.command()
async def avg(ctx, user: discord.User = None):
    """!avg use this bot command to find average number of guesses and display the leaderboard."""
    user = user or ctx.author
    if user_data == {}:
        await ctx.send(f"No data for the leaderboard.")
    else:
        leaderboard = make_leaderboard(user_data)
        await ctx.send(f"Contexto rankings by average number of guesses:\n{leaderboard}")

@bot.command()
async def deletemydata(ctx, user: discord.User = None):
    """!deletemydata use this bot command to delete all user data."""
    user = user or ctx.author
    try:    
        if str(user.id) in user_data:
            del user_data[str(user.id)]
            save_user_data()
            await ctx.send(f"Data for {user.name} has been deleted.")
    except KeyError:
        await ctx.send(f"No data for {user.name}.")
   
bot.run('your bot token')