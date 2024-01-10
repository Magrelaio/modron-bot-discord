from shared_functions import *
from disnake.ext import commands

class SeeOneInvCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='ver_inventario', description="Veja o inventario de um unico jogador!")
    async def ver_inventario(ctx, jogador):
        jogador = jogador.capitalize()
        inventory = load_inventory()
        if FileNotFoundError in inventory:
            await ctx.response.send_message("Estamos com problemas internos e por isso não podemos cadastrar, carregar ou mexer nos inventarios.")

        inventarios_str = (f"Inventário de {jogador}:\n{formatar_inventario(inventario)}" for jogador, inventario in inventory.items)
        if inventarios_str == '':
            await ctx.send(f"Nenhum inventário para este jogador encontrado! Experimente o comando /HELP caso precise de ajuda!")
            return
        await ctx.send(f"Inventário de {jogador}:\n{inventarios_str}")

def setup(bot):
    bot.add_cog(SeeOneInvCog(bot))