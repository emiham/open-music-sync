from .player import Player
import requests
from pprint import pprint


class Jellyfin(Player):
    def __init__(self, host: str, token: str, music_directory: str):
        """
        Initiate a Jellyfin player.
        Arguments:
        -----------
        host : str
            The URL for the Jellyfin server.
        token : str
            Your Jellyfin API token.
        music_directory : str
            The base directory where music is hosted on your server.

        """
        self.host = f"{host}"
        self.headers = {"X-Emby-Authorization": f"MediaBrowser Token={token}"}
        self.music_directory = music_directory

    def get_queue(self) -> Player.Queue:
        queue = self.Queue()
        indices = []

        sessions = requests.get(f"{self.host}/Sessions", headers=self.headers).json()

        # TODO Handle multiple sessions
        for session in sessions:
            if "NowPlayingItem" in session:
                queue.index = session["NowPlayingItem"]["IndexNumber"] - 1
            for item in session["NowPlayingQueueFullItems"]:
                queue.songs.append(
                    Player.Song(
                        path=item["Path"].replace(f"{self.music_directory}/", "")
                    )
                )
                indices.append(item["IndexNumber"])

            if "PlayState" in session:
                if "PositionTicks" in session["PlayState"]:
                    queue.position = session["PlayState"]["PositionTicks"] / 10000000

        queue.songs = [
            song for (_, song) in sorted(zip(indices, queue.songs), key=lambda x: x[0])
        ]

        return queue

    def enqueue(self, queue: Player.Queue) -> None:
        super().enqueue(queue)
