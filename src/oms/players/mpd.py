import asyncio
import os

from mpd.asyncio import MPDClient

from .player import Player


class MPD(Player):
    def __init__(self, host="127.0.0.1", port="6600"):
        """
        Initiate an MPD player.
        Arguments:
        -----------
        host : str
            The IP for the MPD server.
        port : str
            The port for the MPD server.

        """
        self.host = os.environ.get("MPD_HOST", host)
        self.port = int(os.environ.get("MPD_PORT", port))

    async def _connect(self):
        client = MPDClient()
        await client.connect(self.host, self.port)
        return client

    def get_queue(self):
        return asyncio.run(self._get_queue())

    def _enqueue(self, queue):
        asyncio.run(self._async_enqueue(queue))

    def daemon(self, callback):
        asyncio.run(self._daemon(callback))

    async def _get_queue(self):
        client = await self._connect()
        try:
            queue = self.Queue()
            for entry in await client.playlistinfo():
                queue.songs.append(
                    Player.Song(
                        path=entry["file"],
                        albumartist=entry["albumartist"],
                        album=entry["album"],
                    )
                )
            status = await client.status()
            if "elapsed" in status:
                queue.position = float(status["elapsed"])
            if "song" in status:
                queue.index = int(status["song"])
            return queue
        finally:
            client.disconnect()

    async def _async_enqueue(self, queue):
        if not queue.songs:
            return
        client = await self._connect()
        try:
            await client.clear()
            for song in queue.songs:
                await client.add(song.path)
            await client.seek(queue.index, queue.position)
        finally:
            client.disconnect()

    async def _daemon(self, callback):
        client = await self._connect()
        try:
            async for _ in client.idle(["playlist", "player"]):
                callback(await self._get_queue())
        finally:
            client.disconnect()
