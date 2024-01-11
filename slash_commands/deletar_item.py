from shared_functions import *
from disnake.ext import commands

class DeleteItemCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='deletar_item', description="Delete um item do inventario de seu personagem")
    @commands.guild_only()
    async def deletar_item(ctx, jogador, item, quantidade):
        inventory = load_inventory()
        if FileNotFoundError in inventory:
            await ctx.response.send_message("Estamos com problemas internos e por isso não podemos cadastrar, carregar ou mexer nos inventarios.")

        jogador = ctx.author.nick.title() if ctx.author.nick else ctx.author.display_name.title()
        
        if jogador not in inventory:
            await ctx.send(f"Inventário para {jogador} não encontrado.")
            return

        if jogador.lower() == str(ctx.author).lower():
            if jogador in inventory:
                if item in inventory[jogador]:
                    del inventory[jogador][item]
                    save_inventory(inventory)
                    await ctx.send(f"{item} deletado do seu inventário.")
                else:
                    await ctx.send(f"Item não encontrado.")
                    return
            else:
                await ctx.response.send_message(f"Inventario de {jogador} não encontrado.")
        else:
            await ctx.send("Você só pode editar o seu próprio inventário.")
            
def setup(bot):
    bot.add_cog(DeleteItemCog(bot))