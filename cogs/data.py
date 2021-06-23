from discord.ext import commands

class Data(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

    
  @commands.command(name="price", aliases=['p'])
  async def fetch_price(self, ctx):
    await ctx.channel.send("Current Price")

  @commands.command(name='convert', aliases=['cv'])
  async def convert_currencies(self, ctx):
    await ctx.channel.send("Converted Price")