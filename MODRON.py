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
from functools import reduce

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
    
    content = message.content.strip().lower()
    
    if content.startswith(tuple("abcefghijklmnopqrstuvwxyzABCEFGHIJKLMNOPQRSTUVWXYZ")):
        return
    
    if content.endswith(tuple("abcefghijklmnopqrstuvwxyzABCEFGHIJKLMNOPQRSTUVWXYZ")):
        return

    if 'd' in message.content:
        split_message = message.content.split('d')
        if len(split_message) >= 2:
            ##Container para criação de basicamente toda e qualquer alteração que será feita na questão de funcionalidade dos dados
            #para criação de expressões como "d20 + 5, d30 - 2 e afins"
            if '+' in split_message[1]:
                dice_type, *bonus_list = split_message[1].split('+')
                bonus = sum(int(b) for b in bonus_list)
            elif '-' in split_message[1]:
                dice_type, *penalty_list = split_message[1].split('-')
                penalty = sum(int(p) for p in penalty_list)
                bonus = -penalty
            elif '*' in split_message[1]:
                dice_type, *multiply_list = split_message[1].split('*')
                multiply = reduce(lambda x, y: x * int(y), multiply_list, 1)
                bonus = multiply
            #Fim da criação de expressões
            ##fim do container (oque esta abaixo disso será praticamente imutavel)
            else:
                dice_type = split_message[1]
                bonus = 0
                # if int(bonus) >= 100000001 IA COLOCAR LIMITADOR DE UM MILHÃO NO BONUS AHAHAHAH
                if int(dice_type) >= 201:
                    await message.reply('Número de lados muito alto! Tente um numero mais baixo por favor (máximo de 200)')
                    return
            if int(dice_type) <= 0:
                await message.reply('Numero de lados inválido. Você precisa rolar um numero acima de 1! - ou deixe em branco como "d20"')
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
    else:
        return


'''@bot.slash_command(name="rolar_dado", description="Rola um dado com o número especificado de lados")
async def rolar_dado(ctx: disnake.ApplicationCommandInteraction, lados: int):
    if lados <= 1:
        await ctx.response.send_message("O número de lados do dado deve ser maior que 1.")
        return
    resultado = np.random.randint(1, lados + 1)
    await ctx.response.send_message(f"Resultado do dado de {lados} lados: {resultado}")
    bot.add_command(rolar_dado)'''
#INICIO DAS SLASH COMMANDS

@bot.slash_command(name="ping", description="Mede o ping do bot em MS")
async def ping(ctx: disnake.ApplicationCommandInteraction):
    latency = bot.latency * 1000
    await ctx.response.send_message(f"Ping: {latency}ms")
    bot.add_command(name="ping")

@bot.slash_command(name="ver_todos_inventarios", description="Ver todos os itens do inventario de todos.")
async def ver_todos_inventarios(ctx: disnake.ApplicationCommandInteraction):
    with open("inventory.txt", "r", encoding='utf-8') as arquivo:
        inventario = arquivo.read()
    await ctx.response.send_message(f"{inventario}")
    bot.add_command(name="ver_todos_inventarios")

@bot.slash_command(name="ver_inventario", description="Ver todos os itens do inventario do personagem selecionado.")
async def ver_inventario(ctx: disnake.ApplicationCommandInteraction, personagem: str):
    # personagens = ["Fenyx", "Draque", "Ukkonen","Kyuma", "Murrdok", "Aloy"]
    # personagem = personagem.lower()
    # for personagem in personagens:
    #     inicio_inv_perso = inventario.find(personagens[Draque])
    if personagem.lower() == "draque":
        with open("inventory.txt", "r", encoding='utf-8') as arquivo:
            inventario = arquivo.read()
            Draque = inventario.split("Draque")
        await ctx.response.send_message(f"{Draque}")
        print(Draque)
    elif personagem.lower() == "ukkonen":
         with open("inventory.txt", "r", encoding='utf-8') as arquivo:
            inventario = arquivo.read()
            Ukkonen = inventario.split("Ukkonen")
    await ctx.response.send_message(f"{Ukkonen}")
    print(Ukkonen)
    bot.add_command(name="ver_inventario")

bot.run(TOKEN)