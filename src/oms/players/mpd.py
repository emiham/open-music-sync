import os
from mpd import MPDClient
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
        self.client = MPDClient()
        self.client.timeout = None
        self.client.idletimeout = None
        self.client.connect(
            os.environ.get("MPD_HOST", host),
            os.environ.get("MPD_PORT", port),
        )

    def get_queue(self):
        queue = self.Queue()

        for entry in self.client.playlistinfo():
            queue.songs.append(
                Player.Song(
                    path=entry["file"],
                    albumartist=entry["albumartist"],
                    album=entry["album"],
                )
            )

        if "elapsed" in self.client.status():
            queue.position = float(self.client.status()["elapsed"])

        if "song" in self.client.status():
            queue.index = int(self.client.status()["song"])

        self.client.disconnect()

        return queue

    def enqueue(self, queue):
        if len(queue.songs) > 0:
            self.client.clear()
            for song in queue.songs:
                self.client.add(song.path)

            self.client.seek(queue.index, queue.position)
            self.client.disconnect()
