# -*- coding: utf-8 -*-

import aiohttp
import asyncio
import logging

from io import BytesIO
from .errors import NotFound, Forbidden, InvalidEndPoint

try:
    import discord
except ImportError:
    _discord = False
else:
    _discord = True

log = logging.getLogger('arcadia')


class Client:
    def __init__(self, token: str = '', bot=None, loop=None, aiosession=None):
        self._headers = {
            "User-Agent": "Arcadia.py (GitHub: Zenrac)",
            "Authorization": token
        }

        self.url = "https://eclyssia-api.tk/api/v1"
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
            Your token from eclyssia-api.tk
        """

        if hasattr(bot, 'arcadia'):
            return bot.arcadia
        bot.arcadia = cls(token, bot=bot, *args, **kwargs)
        return bot.arcadia

    async def get_endpoints(self, bypass=False):
        """Tries to fetch the available endpoints of the API."""
        if self.retry != 0 and not bypass:  # We don't want several loop of this to run
            return
        try:
            async with self.session.get(self.url) as response:
                json = await response.json()
                if not json.get('endpoints', False):
                    log.info('Failed to get endpoints...')
                    return 
                if not isinstance(json['endpoints'], dict):
                    self.endpoints = json['endpoints']
                else:
                    endpoints = []
                    for endpoint in json['endpoints'].values():
                        endpoints += endpoint
                    self.endpoints = endpoints
                log.info("Got list of {} endpoints, arcadia is ready to use.".format(len(self.endpoints)))
                self.retry = 0
                await response.release()
        except (aiohttp.ClientError, asyncio.TimeoutError):
            self.retry += 1
            wait = min(self.retry*5, 60)
            log.info("Failed to get endpoints, trying again in {}seconds".format(wait))
            await asyncio.sleep(wait)
            await self.get_endpoints(bypass=True)
        except RuntimeError:
            log.info('Session is closed... Can\'t fetch information from arcadia.')
            return  # Session is closed. Useless to try again.

    async def get_image(self, image_type: str, url: str = None, discordfile: bool = True, timeout: int = 300, **args):
        """
        Basic get_image function using aiohttp
        Returns a Discord File if discordfile parameter is True and discord.py rewrite library is installed.
        Otherwise returns BytesIO.

        ----------
        Parameters

        image_type: str
            A valid image type from the list of available endpoints in the documentation : https://docs.eclyssia-api.tk/

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

        For other parameters, see https://docs.eclyssia-api.tk/
        """
        if self.endpoints and image_type.lower() not in self.endpoints:
            log.info('Found a not known endpoint, trying to update list of available endpoint.')
            asyncio.ensure_future(self.get_endpoints())  # In case of infinite loop of try / except better not to await
            await asyncio.sleep(1)  # Waiting to get_endpoints() to finish with a normal speed connexion
            if self.endpoints and image_type.lower() not in self.endpoints:
                raise InvalidEndPoint('This is not a valid endpoint, please see the list of available endpoints on https://docs.eclyssia-api.tk/.')

        final_url = '{}/{}'.format(self.url, image_type.lower())

        # Allows no kwargs when calling funct by specifying the two most communs
        # e.g we can do get_image('triggered', 'urlhere.com') without specifying url='urlhere.com'
        params = {}
        if url:
            params['url'] = url
        params.update(args)

        log.debug("Requesting image from url: {}".format(final_url))

        async with self.session.get(final_url, headers=self._headers, params=params, timeout=timeout) as response:
            if response.status == 403:
                raise Forbidden('You are not allowed to access this resource.')
            elif response.status != 200:
                raise NotFound('This resource does not exist or you are not allowed to access. ({})'.format(response.status))
            ext = response.content_type.split('/')[-1]
            img = BytesIO(await response.read())
            await response.release()

        if _discord and discordfile:
            return discord.File(img, filename="image.{}".format(ext))

        return img
