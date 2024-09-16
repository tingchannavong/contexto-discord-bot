# A discord app to collect Contexto game statistics from users, store it as json file, create a leaderboard, delete user data, . Take inspiration from function of wordle bot. 
# To-do: divide members by guild, To work on guild and servers like worldle bot. Make global variables so can change name easier i.e. glob_var_name = 'ct_hint_avg'

import discord
from discord.ext import commands
import json
import os
import re
import plotly.graph_objects as go
import plotly.express as px

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

def calc_avg_guess(user, guess_type):
    """Takes a discord user id, guess type (name of dictionary key for contexto|letroso guesses) and calculate average guess by sum of guesses list/guess number."""
    average_guesses = sum(user_data[str(user.id)][guess_type]) / len(user_data[str(user.id)][guess_type]) 
    return average_guesses

def calc_avg_hint(user, hint_type):
    """Takes a discord user id and calculate average Contexto hints."""
    average_hints = sum(user_data[str(user.id)][hint_type]) / len(user_data[str(user.id)][hint_type])
    return average_hints

def count_game_no(user, game_type):
    """Takes a discord user id and game type (contexto|letroso guesses) and calculate number of games played."""
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

def extract_last_three_numbers(text):
    """To get contexto averages close, medium, far-off."""
    # Split the string by periods and get the last part
    last_part = text.split('.')[-1].strip()

    # Use regular expression to find all numbers (1-3 digits) in the last part
    numbers = re.findall(r'\b\d{1,3}\b', last_part)
    # numbers[-3]

    # Return the last three numbers (or fewer if there aren't three)
    return numbers

def convert_to_int(extracted):
    new_list = []
    for i in extracted:
        converted = int(i)
        new_list.append(converted)
    return new_list

def make_pie_chart(user):
    """Make a pie chart to visualize contexto guesses in 3 categories: close, medium or far-off guesses. Save as png and return the image."""
    #Create labels and colors"
    labels = ['Close Guesses', 'Medium Guesses', 'Far Off Guesses']
    colors = ['#00FF00', '#ADD8E6', '#FF9999']

    #Calculate percentages
    total = sum(user_data[str(user.id)]['pie_dict'].values())
    percentage = [f'{(each/total)*100:.1f}%' for each in user_data[str(user.id)]['pie_dict'].values()]

    # Create the pie chart
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values= list(user_data[str(user.id)]['pie_dict'].values()),
        textinfo='label+percent',
        hoverinfo='label+percent+value',
        marker=dict(colors=colors, line=dict(color='#000000', width=2)),
        textposition='inside',
        insidetextorientation='radial'
    )])

    # Update layout
    fig.update_layout(
        title={
            'text': f"{user_data[str(user.id)]['name']}'s Average Contexto Guesses Visualized",
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        showlegend=True,
        legend_title="Categories",
        font=dict(size=14)
    )

    # Save the figure as an image
    fig.write_image("pie.png")

    # Show the plot
    fig.show()

#MAIN COMMANDS
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# Flag to track message processing
processed_messages = set()

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Unique message identifier (can use message ID or combination of user ID and message content)
    message_id = (message.author.id, message.content)
    user = message.author

    # Avoid processing the same message more than once
    if message_id in processed_messages:
    	await message.channel.send("You've already submitted today's score.")
    	return

    if "played contexto.me" in message.content.lower():
        try:
            # Handle the case where user gave up
            if "gave up" in message.content.lower():
                await message.channel.send("I'm sorry you gave up! Your efforts won't be recorded today. Please try again next time :) ")
                return

            # Handle contexto guesses
            guesses = int(message.content.split("and got it in")[1].split("guesses")[0].strip()) 

            # Initialize user data if not exists, then add only relevant game
            if str(user.id) not in user_data:
                user_data[str(user.id)] = {'name': user.name, 'guesses': [], 'ct_avg':0, 'hints': [], 'avg_hints': 0, 'lt_guesses':[], 'lt_avg':0, 'cn_guesses':[], 'cn_avg':0, 'cn_hints':[], 'cn_hints_avg':0}

            #Add Today's guess to the list
            user_data[str(user.id)]['guesses'].append(guesses)
            average_guesses = calc_avg_guess(user, 'guesses')
            user_data[str(user.id)]['ct_avg'] = average_guesses  # Update each user average guess

            #Save the guess details for visualization
            user_data[str(user.id)]['pie_dict'] = {'close_avg': 0, 'med_avg': 0, 'far_avg': 0}
            pie_list = convert_to_int(extract_last_three_numbers(message.content.lower()))

           # Declare mapping
            user_data[str(user.id)]['pie_dict']['close_avg'] += pie_list[0]
            user_data[str(user.id)]['pie_dict']['med_avg'] += pie_list[1]
            user_data[str(user.id)]['pie_dict']['far_avg'] += pie_list[2]

            # Handle contexto hints
            if "hint" in message.content.lower():
                hints = int(message.content.split("guesses and")[1].split("hint")[0])
                if 'hints' in user_data[str(user.id)]:
                    user_data[str(user.id)]['hints'].append(hints)
                else:
                    user_data[str(user.id)] = {'name': user.name, 'hints': [hints]}

                average_hints = calc_avg_hint(user,'hints') 
                user_data[str(user.id)]['avg_hints'] = average_hints # Update each user average hint
            else:
                pass

            save_user_data()  # Save data after each update

            # Send a customize message based on number of guesses
            await message.channel.send(get_custom_message(guesses))

            # Mark message as processed
            processed_messages.add(message_id)

        except (ValueError, IndexError):
            await message.channel.send("I couldn't parse your guesses. Please make sure your message is in the correct format.")

    if "played conexo.ws" in message.content.lower():
        try:
            # Handle conexo guesses
            guesses = int(message.content.split("and got it in")[1].split("guesses")[0].strip()) 

            # Initialize user data if not exists
            if str(user.id) not in user_data:
                user_data[str(user.id)] = {'name': user.name, 'guesses': [], 'ct_avg':0, 'hints': [], 'avg_hints': 0, 'lt_guesses':[], 'lt_avg':0, 'cn_guesses':[], 'cn_avg':0, 'cn_hints':[], 'cn_hints_avg':0}
           
            #Add Today's guess to the list
            user_data[str(user.id)]['cn_guesses'].append(guesses)
            average_guesses = calc_avg_guess(user, 'cn_guesses')
            user_data[str(user.id)]['cn_avg'] = average_guesses  # Update each user average guess

            # Handle conexo hints
            if "hint" in message.content.lower():
                hints = int(message.content.split("guesses and")[1].split("hint")[0])
                user_data[str(user.id)]['cn_hints'].append(hints)
                average_hints = calc_avg_hint(user,'cn_hints') 
                user_data[str(user.id)]['cn_hints_avg'] = average_hints # Update each user average hint
            else:
                pass

            save_user_data()  # Save data after each update

            # Send a customize message based on number of guesses
            await message.channel.send("Thank you for submitting your score~")

            # Mark message as processed
            processed_messages.add(message_id)

        except (ValueError, IndexError):
            await message.channel.send("I couldn't parse your guesses. Please make sure your message is in the correct format.")

    if "played letroso.com" in message.content.lower():
        try:
            # Handle letroso guesses
            lt_guesses = int(message.content.split("and got it in")[1].split("guesses")[0].strip()) 

            # Initialize user data if not exists
            if str(user.id) not in user_data:
                user_data[str(user.id)] = {'name': user.name, 'guesses': [], 'ct_avg':0, 'hints': [], 'avg_hints': 0, 'lt_guesses':[], 'lt_avg':0, 'cn_guesses':[], 'cn_avg':0, 'cn_hints':[], 'cn_hints_avg':0}
         
            user_data[str(user.id)]['lt_guesses'].append(lt_guesses)
            lt_avg = calc_avg_guess(user, 'lt_guesses')
            user_data[str(user.id)]['lt_avg'] = lt_avg  # Update each user average guess

            save_user_data()  # Save data after each update

            await message.channel.send('Good job!')

            # Mark message as processed
            processed_messages.add(message_id)

        except (ValueError, IndexError):
            await message.channel.send("I couldn't parse your guesses. Please make sure your message is in the correct format.")

    await bot.process_commands(message)

@bot.command()
async def myscore(ctx, user: discord.User = None): 
    user = user or ctx.author 
    if str(user.id) in user_data:
        #Collect info about Contexto stats for each player
        ct_average = user_data[str(user.id)]['ct_avg'] 
        ct_games_played = count_game_no(user, 'guesses')
        average_hints = user_data[str(user.id)]['avg_hints']

        #Collect info about Letroso stats for each player
        lt_average = user_data[str(user.id)]['lt_avg'] 
        lt_games_played = count_game_no(user, 'lt_guesses')

        #Collect info about Conexo stats for each player
        cn_average = user_data[str(user.id)]['cn_avg'] 
        cn_games_played = count_game_no(user, 'cn_guesses')
        cn_hints_avg = user_data[str(user.id)]['cn_hints_avg']

        await ctx.send(f"""{user.name} scores are:
        Contexto ~ played {ct_games_played} games with average guesses: {ct_average:.2f} and used hints: {average_hints}
        Letroso ~ played {lt_games_played} games with average guesses: {lt_average:.2f}
        Conexo ~ playeed {cn_games_played} games with average guesses: {cn_average:.2f} and used hints: {cn_hints_avg}""")
    else:
        await ctx.send(f"No data for {user.name} yet.")

@bot.command()
async def ctavg(ctx, user: discord.User = None):
    """!ctavg use this bot command to find average number of guesses and display the Contexto leaderboard."""
    user = user or ctx.author
    if user_data == {}:
        await ctx.send(f"No data for the leaderboard.")
    else:
        leaderboard = make_leaderboard(user_data, 'ct_avg', 'avg_hints')
        await ctx.send(f"Contexto rankings by average number of guesses:\n{leaderboard}")

@bot.command()
async def ltavg(ctx, user: discord.User = None):
    """!ltavg use this bot command to find average number of guesses and display the Letroso leaderboard."""
    user = user or ctx.author
    if user_data == {}:
        await ctx.send(f"No data for the leaderboard.")
    else:
        leaderboard = make_leaderboard(user_data, 'lt_avg','avg_hints')
        await ctx.send(f"Letroso rankings by average number of guesses:\n{leaderboard}")

@bot.command()
async def cnavg(ctx, user: discord.User = None):
    """!cnavg use this bot command to find average number of guesses and display the Conexo leaderboard."""
    user = user or ctx.author
    if user_data == {}:
        await ctx.send(f"No data for the leaderboard.")
    else:
        leaderboard = make_leaderboard(user_data, 'cn_avg', 'cn_hints_avg')
        await ctx.send(f"Conexo rankings by average number of guesses:\n{leaderboard}")

@bot.command()
async def deletemydata(ctx, user: discord.User = None):
    """!deletemydata use this bot command to delete your specific user data."""
    user = user or ctx.author
    try:    
        if str(user.id) in user_data:
            del user_data[str(user.id)]
            save_user_data()
            await ctx.send(f"Data for {user.name} has been deleted.")
    except KeyError:
        await ctx.send(f"No data for {user.name}.")

@bot.command()
async def cleardata(ctx, user: discord.User = None):
    """!clearall use this bot command to delete all users data."""
    user = user or ctx.author
    user_data.clear()
    save_user_data()
    await ctx.send(f"All users' data has been deleted.")

@bot.command()
async def ctpie(ctx, user: discord.User = None):
    """!ctpie - use this bot command to see your Contexto guesses visualized in a pie chart."""
    user = user or ctx.author
    try:    
        if str(user.id) in user_data:
            make_pie_chart(user)

            # Send the image to Discord
            with open("pie.png", "rb") as f:
                picture = discord.File(f)
                await ctx.send("Here is your pie chart:", file=picture)

            # Clean up the image after sending it
            os.remove("pie.png")

    except KeyError:
        await ctx.send(f"No data for {user.name}.")

@bot.command()
async def invitelink(ctx):
    """!invitelink use this bot command to generate an OAuth URL to invite the bot with specific permissions."""

    # Set permissions according to the Contexto discord bot's need
    permissions = discord.Permissions(
    	create_events=True,
        create_instant_invite=True,
        create_expressions=True,
        create_public_threads=True,
        create_private_threads=True,
        view_channel=True,
        send_messages=True,
        send_messages_in_threads=True,
        send_tts_messages=True,  
        embed_links=True,
        attach_files=True,
        read_message_history=True,
        mention_everyone=True,
        add_reactions=True,
        use_external_emojis=True,
        use_external_stickers=True,
        use_embedded_activities=True,
        use_application_commands=True,
        use_external_apps=True,
        connect=True,
        speak=True,
        request_to_speak=True,
        use_voice_activation=True,
        change_nickname=True,
        use_soundboard=True,
        use_external_sounds=True,
    )
    
    # Generate OAuth URL with specific permissions
    oauth_url = discord.utils.oauth_url(bot.user.id, permissions=permissions)
    
    # Send the OAuth invite URL in the current channel
    await ctx.send(f"Invite the contexto bot using this URL: {oauth_url}")

@bot.command()
async def helpme(ctx, user: discord.User = None):
    """!helpme use this bot command to ask for all available commands."""
    user = user or ctx.author
    await ctx.send("""!helpme ~to see this message 
        !myscore ~to see your stats 
        !ctavg ~to see Contexto's server rankings by average number of guesses 
        !ltavg ~to see Letroso's server rankings by average number of guesses 
        !cnavg ~to see Conexo's server rankings by average number of guesses 
        !deletemydata ~to remove all your scores from this game bot""")
   
bot.run('your bot token')
