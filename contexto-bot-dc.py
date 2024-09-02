# A discord app to collect Contexto game information and store it.

import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Dictionary to store users and their guesses
user_data = {}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Example message format to capture: "I played contexto.me #715 and got it in 24 guesses."
    if "played contexto.me" in message.content.lower():
        try:
            # Extracting the number of guesses from the message
            guesses = int(message.content.split("and got it in")[1].split("guesses")[0].strip())
            user = message.author

            # Log user guesses
            if user.id in user_data:
                user_data[user.id]['guesses'].append(guesses)
            else:
                user_data[user.id] = {'name': user.name, 'guesses': [guesses]}

            # Calculate the average guesses
            average_guesses = sum(user_data[user.id]['guesses']) / len(user_data[user.id]['guesses'])

            # Send a message with the updated average
            await message.channel.send(
                f"{user.name}, your average guesses so far: {average_guesses:.2f}"
            )

        except (ValueError, IndexError):
            await message.channel.send("I couldn't parse your guesses. Please make sure your message is in the correct format.")

    await bot.process_commands(message)

@bot.command()
async def avg(ctx, user: discord.User = None):
    """Command to check the average guesses for a specific user."""
    user = user or ctx.author  # Default to the message author if no user is specified
    if user.id in user_data:
        average_guesses = sum(user_data[user.id]['guesses']) / len(user_data[user.id]['guesses'])
        await ctx.send(f"{user.name}'s average guesses: {average_guesses:.2f}")
    else:
        await ctx.send(f"No data for {user.name} yet.")

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot.run('YOUR_BOT_TOKEN')


