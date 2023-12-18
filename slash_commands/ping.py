import disnake
from disnake.ext import commands

class PingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="ping", description="Mede o ping do bot em MS")
    async def ping(self, ctx: disnake.ApplicationCommandInteraction):
        latency = self.bot.latency * 1000
        await ctx.response.send_message(f"Ping: {latency:.2f}ms")
        
def setup(bot):
    bot.add_cog(PingCog(bot))