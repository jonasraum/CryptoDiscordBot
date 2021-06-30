from discord.ext import commands
import pandas_datareader as pandas
import matplotlib.pyplot as plt
import datetime as dt
import discord

class Graph(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  @commands.command(name="graph", aliases=['g'])
  async def create_graph(self, ctx, symbol, currency, days):
    start = dt.date.today() - dt.timedelta(days = int(days))
    end = dt.date.today()
    data = pandas.DataReader(f"{str.upper(symbol)}-{str.upper(currency)}", "yahoo", start, end)

    plt.plot(data['Adj Close'])
    plt.show()
    await ctx.channel.send(file=discord.File('Figure_1.png'))

    print(data)
