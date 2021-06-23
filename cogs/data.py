from discord.ext import commands
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json, os, pprint
from money import Money

class Data(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  @commands.command(name="price", aliases=['p'])
  async def fetch_price(self, ctx):
    await ctx.channel.send("Current Price")

  @commands.command(aliases=['ov'])
  async def overview(self, ctx, symbol, currency = "EUR"):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    parameters = {
      "symbol": symbol,
      "convert": currency
    }
    headers = {
      'Accepts': 'application/json',
      'X-CMC_PRO_API_KEY': os.environ['CMC API Key']
    }
    session = Session()
    session.headers.update(headers)

    try:
      response = session.get(url, params=parameters)
      data = json.loads(response.text)

      price = Money(amount = data['data'][str.upper(symbol)]['quote'][str.upper(currency)]['price'], currency = str.upper(currency))
      await ctx.channel.send(price)

      print(price)

    except (ConnectionError, Timeout, TooManyRedirects) as e:
      print(e)