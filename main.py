# MODRON ALPHA (VERSÃO DE TESTE)
'''Adicionar coisa pra deletar o numero mais baixo das rolagens (dificil)
    Adicionar algo que mude a vida dos players (comando para subtrair a vida atual(tambem dificil)
    Adicionar porcentagem do numero total do dado
    inventario do Dojo - em progresso
    rodar dados em fileira (como o # de um outro bot)
'''

import disnake 
from disnake.ext import commands
import os
from shared_functions import *
from functools import reduce
from token_modron_alpha import TOKEN_MAV as TOKEN

intents = disnake.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='', intents= intents)

@bot.event
async def on_ready():
    print(f'Entramos como {bot.user}')
    load_inventory()

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    content = message.content.strip().lower()
    
    if content.startswith(tuple("abcefghijklmnopqrstuvwxyzABCEFGHIJKLMNOPQRSTUVWXYZ")):
        return
    
    if content.endswith(tuple("abcdefghijklmnopqrstuvwxyzABCEFGHIJKLMNOPQRSTUVWXYZ")):
        return

    if 'd' in message.content:
        resultado = processar_rolagem(message.content)

        if isinstance(resultado, str):
            await message.reply(resultado)
            return
        
        if resultado is not None:

            dice_number, dice_type, operador, bonus = resultado
            rolls, total_roll, roll_str = processar_expressao(dice_number, dice_type, operador, bonus)

            roll_results = f"[{', '.join(str(roll) for roll in rolls)}]"
            if 1 in rolls or dice_type in rolls:
                roll_results = f"[{', '.join(f'**{roll}**' if roll == 1 or roll == dice_type else str(roll) for roll in rolls)}]"

            await message.reply(f"`` {total_roll} `` ⟵ {roll_results} {roll_str}")
        else:
            await message.reply("Expressão inválida ou não reconhecida.")

for filename in os.listdir('./slash_commands'):
    if filename.endswith('.py'):
        print(f"Carregando extensão: {filename}")
        bot.load_extension(f'slash_commands.{filename[:-3]}')
bot.run(TOKEN)