import requests

from .player import Player


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
        self.headers = {"Authorization": f'MediaBrowser Token="{token}"'}
        self.music_directory = music_directory

    def get_queue(self) -> Player.Queue:
        queue = self.Queue()

        sessions = requests.get(f"{self.host}/Sessions", headers=self.headers).json()

        # TODO Handle multiple sessions
        for session in sessions:
            if "NowPlayingItem" not in session:
                continue

            ids = [entry["Id"] for entry in session.get("NowPlayingQueue", [])]
            print(ids)

            # It seems that this list is not populated when only playing one item.
            # TODO Look deeper into this. Tested with 3:30 in Houston on Finamp.
            if len(ids) == 0:
                ids = [session["NowPlayingItem"]["Id"]]

            items = requests.get(
                f"{self.host}/Items",
                params={"Ids": ",".join(ids), "Fields": "Path"},
                headers=self.headers,
            ).json()["Items"]
            paths = {item["Id"]: item["Path"] for item in items}

            for i, item_id in enumerate(ids):
                queue.songs.append(
                    Player.Song(
                        path=paths[item_id].replace(f"{self.music_directory}/", "")
                    )
                )
                if item_id == session["NowPlayingItem"]["Id"]:
                    queue.index = i

            if "PlayState" in session and "PositionTicks" in session["PlayState"]:
                queue.position = session["PlayState"]["PositionTicks"] / 10000000

        return queue

    def enqueue(self, queue: Player.Queue) -> None:
        super().enqueue(queue)
        raise NotImplementedError
