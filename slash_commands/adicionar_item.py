from shared_functions import load_inventory, save_inventory
from disnake.ext import commands

class AddItemCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
    @commands.slash_command(name='adicionar_item', description="Edite o inventario de um jogador")
    async def adicionar_item(ctx, jogador=None, item=None, quantidade=None):
        inventory = load_inventory()
        if FileNotFoundError in inventory:
            await ctx.response.send_message("Estamos com problemas internos e por isso não podemos cadastrar, carregar ou mexer nos inventarios.")

        if ctx.author.guild_permissions.administrator:
            if not jogador:
                await ctx.send("Por favor, especifique o jogador cujo inventário você deseja editar.")
                return
        else:
            jogador = ctx.author.display_name.title()

        if jogador not in inventory:
            await ctx.send(f"Inventário para {jogador} não encontrado.")
            return

        if not item or not quantidade:
            await ctx.send("Por favor, especifique o item e a quantidade.")
            return
        
        try:
            quantidade = int(quantidade)
        except ValueError:
            await ctx.send("A quantidade deve ser um número inteiro.")
            return

        inventory[jogador][item] = quantidade
        save_inventory(inventory)
        await ctx.send(f"{quantidade} {item} adicionado ao inventário de {jogador}.")

def setup(bot):
    bot.add_cog(AddItemCog(bot))