# MODRON ALPHA (VERSÃO DE TESTE)
'''Adicionar coisa pra deletar o numero mais baixo das rolagens (dificil)
    Adicionar algo que mude a vida dos players (comando para subtrair a vida atual(tambem dificil)
    Adicionar porcentagem do numero total do dado
    inventario do Dojo - em progresso
    rodar dados em fileira (como o # de um outro bot)
'''

import disnake 
from disnake.ext import commands
import numpy as np
import json
import os
from functools import reduce
from token_modron_alpha import TOKEN_MAV as TOKEN #adicionado com merge por erros tecnicos

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
        split_message = message.content.split('d')
        if len(split_message) >= 2:
            ##Container para criação de basicamente toda e qualquer alteração que será feita na questão de funcionalidade dos dados
            #para criação de expressões como "d20 + 5, d30 - 2 e afins"
            if '+' in split_message[1]:
                try:
                    dice_type, *bonus_list = split_message[1].split('+')
                    bonus = sum(int(b) for b in bonus_list)
                except:
                    bonus = 0
            elif '-' in split_message[1]:
                try:
                    dice_type, *penalty_list = split_message[1].split('-')
                    penalty = sum(int(p) for p in penalty_list)
                    bonus = penalty
                except:
                    bonus = 0
            elif '*' in split_message[1]:
                try:
                    dice_type, *multiply_list = split_message[1].split('*')
                    multiply = reduce(lambda x, y: x * int(y), multiply_list, 1)
                    bonus = multiply
                except:
                    bonus = 1
            #Fim da criação de expressões
            else:
                dice_type = split_message[1]
                bonus = 0
                if int(dice_type) >= 201:
                    await message.reply('Número de lados muito alto! Tente um numero mais baixo por favor (máximo de 200)')
                    return
            if int(dice_type) <= 0:
                await message.reply('Numero de lados inválido. Você precisa rolar um numero acima de 1!')
                return
            if split_message[0].isnumeric():
                dice_number = int(split_message[0])
            else:
                try:
                    dice_number = 1
                except:
                    await message.reply('Numero de dado ou expressão invalida, tente novamente com numeros ou expressões validas; por exemplo: d20, d30 + 5, e afins \n Caso tenha dificuldade execute o comando "/FAQ"')
            rolls = sorted(np.random.choice(np.arange(1, int(dice_type) + 1)) for _ in range(dice_number))
            if int(dice_number) >= 26:
                await message.reply('Numero de dados muito alto! tente um numero mais baixo por favor (máximo de 25)')
                return

            if int(dice_number) <= 0:
                await message.reply('Numero de dados inválido. Você precisa rolar um numero acima de 1! - ou deixe em branco como "d20"')
                return
            total_roll = sum(rolls), bonus
            roll_str = f"{dice_number}d{dice_type}"
            if '+' in split_message[1]:
                total_roll = sum(rolls) + abs(bonus)
                roll_str += f"+ {bonus}"
            elif '-' in split_message[1]:
                total_roll = sum(rolls) - abs(bonus)
                roll_str += f"- {bonus}"
            elif '*' in split_message[1]:
                total_roll = sum(rolls) * abs(bonus)
                roll_str += f"* {bonus}"
            else:
                total_roll = sum(rolls)
            roll_results = f"[{', '.join(str(roll) for roll in rolls)}]"
            if 1 in rolls or int(dice_type) in rolls:
                roll_results = f"[{', '.join(f'**{roll}**' if roll == 1 or roll == int(dice_type) else str(roll) for roll in rolls)}]"
            await message.reply(f"`` {total_roll} `` ⟵ {roll_results} {roll_str}")
    else:
        return

for filename in os.listdir('./slash_commands'):
    if filename.endswith('.py'):
        print(f"Carregando extensão: {filename}")
        bot.load_extension(f'slash_commands.{filename[:-3]}')
bot.run(TOKEN)