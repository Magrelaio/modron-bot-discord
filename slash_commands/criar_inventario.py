from shared_functions import load_inventory, save_inventory
from disnake.ext import commands

class CreateInvCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
    @commands.slash_command(name='criar_inventario', description="[ADMIN] Crie um inventario para um jogador!")
    async def criar_inventario(self, ctx, jogador):
        inventory = load_inventory()
        jogador = jogador.title()

        if jogador not in inventory:
            inventory[jogador] = {}
            save_inventory(inventory)
            await ctx.send(f"Inventário para {jogador} criado com sucesso.")
        else:
            await ctx.send(f"Inventário para {jogador} já existe.")

def setup(bot):
    bot.add_cog(CreateInvCog(bot))