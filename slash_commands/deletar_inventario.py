from shared_functions import load_inventory, save_inventory
from disnake.ext import commands

class DeleteInvCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='deletar_inventario', description="[ADMIN] Delete o inventario de um jogador!")
    @commands.has_permissions(administrator=True)
    async def deletar_inventario(self, ctx, jogador):
        inventory = load_inventory()

        jogador = jogador.capitalize()

        if jogador in inventory:
            del inventory[jogador]
            save_inventory(inventory)
            await ctx.send(f"Inventário de {jogador} deletado com sucesso.")
        else:
            await ctx.send(f"Inventário para {jogador} não existe ou já foi deletado.")

def setup(bot):
    bot.add_cog(DeleteInvCog(bot))