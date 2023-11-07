# MODRON ALPHA (VERSÃO DE TESTE)
''' Adicionar coisa pra deletar o numero mais baixo das rolagens (dificil)
    Adicionar algo que mude a vida dos players (comando para subtrair a vida atual(tambem dificil)
    Adicionar porcentagem do numero total do dado
    Easter Egg (izi)
    inventario do Dojo
    rodar dados em fileira (como o # de um outro bot)
    '''

import disnake
from disnake.ext import commands
import numpy as np
from token_modron_alpha import TOKEN_MAV as TOKEN

intents = disnake.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='', intents= intents)

@bot.event
async def on_ready():
    print(f'Entramos como {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

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
            rolls = sorted(np.random.choice(np.arange(1, int(dice_type) + 1)) for _ in range(dice_number))
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

@bot.slash_command(name="ping", description="O bot fala pong")
async def ping(ctx: disnake.ApplicationCommandInteraction):
    await ctx.response.send_message("pong")

@bot.slash_command(name="rolar_dado", description="Rola um dado com o número especificado de lados")
async def rolar_dado(ctx: disnake.ApplicationCommandInteraction, lados: int):
    if lados <= 1:
        await ctx.response.send_message("O número de lados do dado deve ser maior que 1.")
        return
    resultado = np.random.randint(1, lados + 1)
    await ctx.response.send_message(f"Resultado do dado de {lados} lados: {resultado}")
    bot.add_command(rolar_dado)

'''@bot.slash_command(name="ping", description="Mede o ping do bot em MS")
async def ping(ctx: disnake.ApplicationCommandInteraction):
    latency = bot.latency * 1000
    await ctx.response.send_message(f"Ping: {latency:.2f}ms")
    bot.add_command(name="ping")'''

bot.run(TOKEN)