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
          ```css
          {trend}%
          ```
          '''
          return trend_string
        elif trend < -1:
          trend_string = f'''
          ```
          {trend}%
          ```
          '''
          return trend_string
        else:
          return f'> {trend}%'

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
      slug = data['data'][str.upper(symbol)]['slug']

      print(name)

      trend_1h = round(data['data'][str.upper(symbol)]['quote'][str.upper(currency)]['percent_change_1h'], 2)
      trend_24h = round(data['data'][str.upper(symbol)]['quote'][str.upper(currency)]['percent_change_24h'], 2)
      trend_7d = round(data['data'][str.upper(symbol)]['quote'][str.upper(currency)]['percent_change_7d'], 2)
      trend_30d = round(data['data'][str.upper(symbol)]['quote'][str.upper(currency)]['percent_change_30d'], 2)
      trend_60d = round(data['data'][str.upper(symbol)]['quote'][str.upper(currency)]['percent_change_60d'], 2)
      trend_90d = round(data['data'][str.upper(symbol)]['quote'][str.upper(currency)]['percent_change_90d'], 2)

      last_updated = data['data'][str.upper(symbol)]['quote'][str.upper(currency)]['last_updated']

      price = Money(amount = data['data'][str.upper(symbol)]['quote'][str.upper(currency)]['price'], currency = str.upper(currency))


      embed=discord.Embed(title=f"{name} Overview", url=f"https://coinmarketcap.com/currencies/{slug}/", color=0x1289EA)
      
      embed.add_field(name="1h Trend", value=f"{trend_1h}%", inline=True)
      embed.add_field(name="24h Trend", value=f"{trend_24h}%", inline=True)
      embed.add_field(name="7d Trend", value=f"{trend_7d}%", inline=True)
      embed.add_field(name="30d Trend", value=f"{trend_30d}%", inline=True)
      embed.add_field(name="30d Trend", value=f"{trend_60d}%", inline=True)
      embed.add_field(name="90d Trend", value=f"{trend_90d}%", inline=True)

      embed.set_footer(text=f"This Bot does not deliver real time data, because the used API is not updating exactly to the second. Last update was at {last_updated}")

      
      await ctx.channel.send(embed=embed)

      pprint.pprint(data)

    except (ConnectionError, Timeout, TooManyRedirects) as e:
      print(e)

    
    

