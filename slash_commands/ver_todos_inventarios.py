from shared_functions import load_inventory, formatar_inventario
from disnake.ext import commands

class SeeAllInvCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
    @commands.slash_command(name='ver_todos_inventarios', description='Veja todos os inventarios cadastrados ao mesmo tempo.')
    async def ver_todos_inventarios(ctx):
        inventory = load_inventory()
        if FileNotFoundError in inventory:
            await ctx.response.send_message("Estamos com problemas internos e por isso não podemos cadastrar, carregar ou mexer nos inventarios.")

        inventarios_str = "\n\n".join([f"Inventário de {jogador}:\n{formatar_inventario(inventario)}" for jogador, inventario in inventory.items()])
        if inventarios_str == '':
            await ctx.send(f"Nenhum inventário encontrado! Experimente o comando /HELP caso precise de ajuda!")
            return
        await ctx.send(f"Inventários existentes:\n{inventarios_str}")

def setup(bot):
    bot.add_cog(SeeAllInvCog(bot))