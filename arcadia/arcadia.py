# -*- coding: utf-8 -*-

import aiohttp
import asyncio

from .errors import NotFound, Forbidden, InvalidEndPoint

try:
    import discord
except ImportError:
    _discord = False
else:
    if discord.__version__ != '1.0.0a':
        _discord = False
    else:
        _discord = True


class Client:
    def __init__(self, token: str = '', bot=None, loop=None, aiosession=None):
        self._headers = {
            "User-Agent": "Arcadia.py (GitHub: Zenrac)",
            "Authorization": token
        }

        self.url = "https://arcadia-api.xyz/api/v1"
        self._loop = loop or asyncio.get_event_loop()
        self.session = aiosession if aiosession else aiohttp.ClientSession(loop=self.loop)
        self.retry = 0
        self.endpoints = []
        asyncio.ensure_future(self.get_endpoints())

    @property
    def loop(self) -> asyncio.AbstractEventLoop:
        return self._loop

    @classmethod
    def pluggable(cls, bot, token: str = "", *args, **kwargs):
        """
        Pluggable version of Client. Inserts Client directly into your Bot client.
        Called by using `bot.arcadia`

        Parameters

        bot: discord.ext.commands.Bot or discord.ext.commands.AutoShardedBot
            Your Bot client from discord.py

        token: str
            Your token from arcadia-api.xyz
        """

        if hasattr(bot, 'arcadia'):
            return bot.arcadia
        bot.arcadia = cls(token, bot=bot, *args, **kwargs)
        return bot.arcadia

    async def get_endpoints(self):
        try:
            async with self.session.get(self.url) as response:
                json = await response.json()
                if not isinstance(json['endpoints'], dict):
                    self.endpoints = json['endpoints']
                else:
                    endpoints = []
                    for endpoint in json['endpoints'].values():
                        endpoints += endpoint
                    self.endpoints = endpoints
                await response.release()
        except (aiohttp.ClientError, asyncio.TimeoutError):
            self.retry += 1
            await asyncio.sleep(min(self.retry*5, 60))
            await self.get_endpoints()

    async def get_image(self, image_type: str, url: str = None, urlbis: str = None,
        text: str = None, type: int = 0, discordfile: bool = True, timeout: int = 300):
        """
        Basic get_image function using aiohttp
        Returns a Discord File if discordfile parameter is True and discord.py rewrite library is installed.
        Otherwise returns BytesIO.

        ----------
        Parameters

        image_type: str
            A valid image type from the list of available endpoints in the documentation : https://arcadia-api.xyz/

        url : str, default to None
            The image url parameter

        urlbis : str, default to None
            The second image.

        text : str, default to None
            Allows to get generated image from an endpoint.

        type : int, default to 0
            Some endpoint have multiple variants to the same image, type allows to get a specific one.

        discordfile : bool, default to True
            If enabled, try to return a discord.File object

        timeout : int, default to 300
            Time before the request is canceled if there is no answer.
        """
        if self.endpoints and image_type.lower() not in self.endpoints:
            raise InvalidEndPoint('This is not a valid endpoint, please see the list of available endpoints on arcadia-api.xyz.')

        async with self.session.get('{}/{}{}{}{}'.format(self.url, image_type.lower(), '?url={}'.format(url) if url else '', '{}text={}'.format('&' if url else '?', text) if text else '',
                                                         '&urlbis={}'.format(urlbis) if urlbis else '','&type={}'.format(type) if type else ''), headers=self._headers, timeout=timeout) as response:
            if response.status == 403:
                raise Forbidden('You are not allowed to access this resource.')
            elif response.status != 200:
                raise NotFound('This resource does not exist or you are not allowed to access.')
            ext = response.content_type.split('/')[-1]
            img = await response.read()
            await response.release()

        if _discord and discordfile:
            return discord.File(img, filename="image.{}".format(ext))

        return img
