# eclyssia.py
Python3 Wrapper for [Eclyssia-api (Eclyssia-api)](https://eclyssia-api.tk/) using [aiohttp](https://github.com/aio-libs/aiohttp)<br>
## Installation
### Using pip
```
pip install eclyssia
```
### Using git
```
pip install git+https://github.com/Zenrac/eclyssia.py
```

### Requirements: <br>
- Python3+<br>
- [aiohttp](https://github.com/aio-libs/aiohttp) <br>
- asyncio<br>

## Examples: <br>
Pluggable Client for Discord bots<br>
```py
from discord.ext.commands import Bot
from eclyssia import Client

bot = Bot(command_prefix='=')
Client.pluggable(bot=bot, token="PassWord123")

@bot.command()
async def triggered(ctx):
    image = await bot.eclyssia.get_image(image_type='triggered', url=ctx.author.avatar_url_as(format='png'))
    await ctx.send(file=image)
```
Without Pluggable Client<br>
```py
from discord.ext.commands import Bot
from eclyssia import Client

bot = Bot(command_prefix='=')
eclyssia = Client(token="PassWord123")

@bot.command()
async def triggered(ctx):
    image = await eclyssia.get_image(image_type='triggered', url=ctx.author.avatar_url_as(format='png'))
    await ctx.send(file=image)
```
Generated image<br>
```py
await eclyssia.get_image(image_type='presidentialalert', text=TextHere)
```
Get BytesIO instead of discord.File<br>
```py
file = await eclyssia.get_image(image_type='triggered', url=URLHERE, discordfile=False)
# file type is BytesIO instead of discord.File
```
Get image variants<br>
```py
file = await eclyssia.get_image(image_type='triggered', url=URLHERE, type=1)
# file image is type 1 instead of type 0.
```
## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
