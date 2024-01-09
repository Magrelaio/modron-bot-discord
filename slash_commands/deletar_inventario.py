from shared_functions import *
from disnake.ext import commands

class DeleteInvCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='deletar_inventario', description="[ADMIN] Delete o inventario de um jogador!")
    @commands.has_permissions(administrator=True)
    async def criar_inventario(self, ctx, jogador):
        inventory = load_inventory()

        jogador = jogador.capitalize()

        if jogador not in inventory:
            inventory[jogador] = {}
            save_inventory(inventory)
            await ctx.send(f"Inventário para {jogador} criado com sucesso.")
        else:
            await ctx.send(f"Inventário para {jogador} já existe.")

def setup(bot):
    bot.add_cog(DeleteInvCog(bot))