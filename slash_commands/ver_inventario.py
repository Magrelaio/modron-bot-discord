from shared_functions import *
from disnake.ext import commands

class SeeOneInvCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    from shared_functions import load_inventory, formatar_inventario
from disnake.ext import commands

class SeeOneInvCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
    @commands.slash_command(name='ver_inventario', description='Visualiza o inventário de um jogador')
    async def ver_inventario(self, ctx, jogador):
        inventory = load_inventory()
        jogador = jogador.title()
        if jogador in inventory:
            player_inventory = inventory[jogador]
            formatted_inventory = formatar_inventario(player_inventory)
            await ctx.send(f"Inventário de {jogador}:\n{formatted_inventory}")
        else:
            await ctx.send(f"Inventário para {jogador} não existe.")

def setup(bot):
    bot.add_cog(SeeOneInvCog(bot))