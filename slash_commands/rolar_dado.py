'''Isso daqui é basicamente inutil já que só dá mais trabalho e etc, mas achei um codigozinho interessante pra guardar'''
# @bot.slash_command(name="rolar_dado", description="Rola um dado com o número especificado de lados")
# async def rolar_dado(ctx: disnake.ApplicationCommandInteraction, lados: int):
#     if lados <= 1:
#         await ctx.response.send_message("O número de lados do dado deve ser maior que 1.")
#         return
#     resultado = np.random.randint(1, lados + 1)
#     await ctx.response.send_message(f"Resultado do dado de {lados} lados: {resultado}")
#     bot.add_command(rolar_dado)