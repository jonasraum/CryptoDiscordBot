from discord.ext import commands
import pandas_datareader as pandas
import matplotlib.pyplot as plt
import datetime as dt
import discord

class Graph(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  @commands.command(name="graph", aliases=['g'])
  async def create_graph(self, ctx, symbol, currency="EUR", days="7"):
    try:
      start = dt.date.today() - dt.timedelta(days=int(days))
      end = dt.date.today()
      data = pandas.DataReader(f"{str.upper(symbol)}-{str.upper(currency)}", "yahoo", start, end)

      plt.plot(data['Adj Close'])
      plt.xticks(rotation=45)
      plt.xlabel("Date")
      plt.ylabel("Price")
      plt.savefig("plot.png", bbox_inches="tight")
      plt.clf()

      await ctx.channel.send(file=discord.File('plot.png'))
    except:
      await ctx.channel.send("Your current request couldn't be processed. Check the valid syntax via `/help` or try again later.")

