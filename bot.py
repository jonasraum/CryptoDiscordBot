import os
from discord.ext import commands
import cogs.data as data, cogs.graph as graph


bot = commands.Bot(command_prefix = '!')
client_token = os.environ['TOKEN']
COGS = [data.Data, graph.Graph]

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

def add_cogs(bot):
    for cog in COGS:
        bot.add_cog(cog(bot))

def run():
  add_cogs(bot)
  bot.run(client_token)

