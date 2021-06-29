from discord.ext import commands
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json, os, pprint, discord
from money import Money

class Data(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  def generate_trend_string(self, trend):
        if trend >= 1:
          trend_string = f'''
          ``css
          {trend}%
          ```
          '''
          return trend_string
        elif trend < -1:
          trend_string = f'''
          ``diff
          {trend}%
          ```
          '''
          return trend_string
        else:
          return f'{trend}%'

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

      name = data['data'][str.upper(symbol)]['name']

      trend_1h = round(data['data'][str.upper(symbol)]['quote'][str.upper(currency)]['percent_change_1h'], 2)
      trend_24h = round(data['data'][str.upper(symbol)]['quote'][str.upper(currency)]['percent_change_24h'], 2)
      trend_7d = round(data['data'][str.upper(symbol)]['quote'][str.upper(currency)]['percent_change_7d'], 2)
      trend_30d = round(data['data'][str.upper(symbol)]['quote'][str.upper(currency)]['percent_change_30d'], 2)
      trend_90d = round(data['data'][str.upper(symbol)]['quote'][str.upper(currency)]['percent_change_90d'], 2)

      last_updated = data['data'][str.upper(symbol)]['quote'][str.upper(currency)]['last_updated']

      price = Money(amount = data['data'][str.upper(symbol)]['quote'][str.upper(currency)]['price'], currency = str.upper(currency))

      #### Create the initial embed object ####
      embed=discord.Embed(title=f"{name} Overview", url="https://realdrewdata.medium.com/", description="This is an embed that will show how to build an embed and the different components", color=0x109319)

      # Add author, thumbnail, fields, and footer to the embed
      #embed.set_author(name="Crypto Bot", url="https://twitter.com/RealDrewData", icon_url="https://cdn.discordapp.com/avatars/856799677751885835/64a0cc5b3b99b999c1b7acd08e1a502b.webp?size=128")

      embed.add_field(name="Field 1 Title", value="This is the value for field 1. This is NOT an inline field.", inline=False)
      embed.add_field(name="1h Trend", value=f"{self.generate_trend_string(trend_1h)}", inline=True)
      embed.add_field(name="24h Trend", value=f"{self.generate_trend_string(trend_24h)}", inline=True)
      embed.add_field(name="7d Trend", value=f"{self.generate_trend_string(trend_7d)}", inline=True)
      embed.add_field(name="30d Trend", value=f"{self.generate_trend_string(trend_30d)}", inline=True)
      embed.add_field(name="90d Trend", value=f"{self.generate_trend_string(trend_90d)}", inline=True)

      embed.set_footer(text=f"This Bot does not deliver real time data, because the used API is not updating exactly to the second. Last update was at {last_updated}")

      
      await ctx.channel.send(embed=embed)

      pprint.pprint(data)

    except (ConnectionError, Timeout, TooManyRedirects) as e:
      print(e)

    
    

