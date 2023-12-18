from shared_functions import load_inventory, save_inventory
from disnake.ext import commands

class EditInvCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

@commands.slash_command(name='editar_inventario', description="Edite o inventario de seu personagem")
async def editar_inventario(ctx, jogador, item, quantidade: int):
    inventory = load_inventory()
    if FileNotFoundError in inventory:
       await ctx.response.send_message("Estamos com problemas internos e por isso não podemos cadastrar, carregar ou mexer nos inventarios.")

    jogador = jogador.capitalize()
    
    if jogador not in inventory:
        await ctx.send(f"Inventário para {jogador} não encontrado.")
        return

    if jogador.lower() == str(ctx.author).lower():
        inventory[jogador][item] = quantidade
        save_inventory(inventory)
        await ctx.send(f"{item} adicionado ao seu inventário com quantidade {quantidade}.")
    else:
        await ctx.send("Você só pode editar o seu próprio inventário.")
        
def setup(bot):
    bot.add_cog(EditInvCog(bot))