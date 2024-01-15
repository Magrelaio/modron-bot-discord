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
import os
from shared_functions import *
from functools import reduce
from token_modron_alpha import TOKEN_MAV as TOKEN

intents = disnake.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='', intents= intents)

def processar_expressao(dice_number=None, dice_type = int, operador = str, bonus = str):
    if int(dice_type) >= 201:
        return f'Número de lados muito alto! Tente um numero mais baixo por favor (máximo de 200)'
    
    if int(dice_type) <= 0:
        return 'Numero de lados inválido. Você precisa rolar um numero acima de 1!'

    rolls = sorted(np.random.choice(np.arange(1, int(dice_type) + 1)) for _ in range(dice_number))

    if int(dice_number) >= 26:
        return 'Numero de dados muito alto! tente um numero mais baixo por favor (máximo de 25)'

    if int(dice_number) <= 0:
        return 'Numero de dados inválido. Você precisa rolar um numero acima de 1! - ou deixe em branco como "d20"'

    roll_str = f"{dice_number}d{dice_type}"

    total_roll = sum(rolls) + abs(bonus) if operador == '+' else  sum(rolls)
        
    total_roll = sum(rolls) - abs(bonus) if operador == '-' else sum(rolls)
    
    total_roll = sum(rolls) * abs(bonus) if operador == '*' else sum(rolls)
    
    total_roll = sum(rolls) / abs(bonus) if operador == '/' else sum(rolls)
    
    roll_str += f"+ {bonus}"

    return total_roll, roll_str

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
            try:
                if '.' in split_message[1]:
                    dice_type, *decimal_list = split_message[1].split('.')
                    decimal_part = reduce(lambda x, y: x + '.' + y, decimal_list)
                    bonus = float(decimal_part)
                else:
                    dice_type, *bonus_list = split_message[1].split('+')
                    bonus = sum(float(b) for b in bonus_list)
            except ValueError:
                bonus = 0
            ##Container para criação de basicamente toda e qualquer alteração que será feita na questão de funcionalidade dos dados
            #para criação de expressões como "d20 + 5, d30 - 2 e afins
        if 'd' in message.content:
            split_message = message.content.split('d')
            if len(split_message) >= 2:
                try:
                    if dice_number == '':
                        dice_number = 0
                    dice_number = int(split_message[0])
                    dice_type, operador, bonus_str = separar_operadores(split_message[1])
                    bonus = float(bonus_str.replace(',', '.')) if bonus_str else 0
                except ValueError:
                    bonus = 0

                resultado = processar_expressao(dice_number, dice_type, operador, bonus)

                if isinstance(resultado, str):
                    await message.reply(resultado)
                    return

                total_roll, roll_str = resultado

                roll_results = f"[{', '.join(str(roll) for roll in processar_expressao.rolls)}]"
                if 1 in processar_expressao.rolls or int(dice_type) in processar_expressao.rolls:
                    roll_results = f"[{', '.join(f'**{roll}**' if roll == 1 or roll == int(dice_type) else str(roll) for roll in processar_expressao.rolls)}]"

                await message.reply(f"`` {total_roll} `` ⟵ {roll_results} {roll_str}")
        else:
            return

for filename in os.listdir('./slash_commands'):
    if filename.endswith('.py'):
        print(f"Carregando extensão: {filename}")
        bot.load_extension(f'slash_commands.{filename[:-3]}')
bot.run(TOKEN)