# ==MODRON OFICIAL==
# PARA UTILIZA-LO É NECESSARIO TER UMA CONTA NA PLATAFORMA DISCORD
import discord
import numpy as np
from discord.ext import commands
from token_modron_alpha import TOKEN_MOV as TOKEN

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Entramos como {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    # --------------------------- DADO RODANDO NORMALMENTE COM NUMERO E SOMA ---------------------------#
    if 'd' in message.content:
        split_message = message.content.split('d')
        if len(split_message) >= 2:
            if '+' in split_message[1]:
                dice_type, *bonus_list = split_message[1].split('+')
                bonus = sum(int(b) for b in bonus_list)
            elif '-' in split_message[1]:
                dice_type, *penalty_list = split_message[1].split('-')
                penalty = sum(int(p) for p in penalty_list)
                bonus = -penalty
            else:
                dice_type = split_message[1]
                bonus = 0
            if split_message[0].isnumeric():
                dice_number = int(split_message[0])
            else:
                dice_number = 1
            rolls = sorted(np.random.choice(np.arange(1, int(dice_type) + 1)) for _ in range(dice_number)) #alteração de biblioteca (RANDOM PARA NUMPY)
            total_roll = sum(rolls) + bonus
            roll_str = f"{dice_number}d{dice_type}"
            if bonus > 0:
                roll_str += f" + {bonus}"
            elif bonus < 0:
                roll_str += f"{bonus}"
            roll_results = f"[{', '.join(str(roll) for roll in rolls)}]"
            if 1 in rolls or int(dice_type) in rolls:
                roll_results = f"[{', '.join(f'**{roll}**' if roll == 1 or roll == int(dice_type) else str(roll) for roll in rolls)}]"
            await message.reply(f"`` {total_roll} `` ⟵ {roll_results} {roll_str}")

    # ---------------------------------EASTER EGG PIKA----------------------------------------------
    '''Algo bacana por aqui'''

bot.run(TOKEN)