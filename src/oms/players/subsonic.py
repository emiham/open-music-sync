from .player import Player
from ..constants import APP_NAME
import requests


class Subsonic(Player):
    def __init__(self, host: str, user: str, password: str) -> None:
        """
        Initiate a Subsonic player.
        Arguments:
        -----------
        host : str
            The URL for the Subsonic server.
        user : str
            Username for the user to sync the queue for.
        password : str
            Password for the user to sync the queue for.

        """
        self.host: str = host
        self.params = {
            "u": user,
            "p": password,
            "v": "1.16.1",
            "c": APP_NAME,
            "f": "json",
        }

    def get_queue(self) -> Player.Queue:
        queue = self.Queue()

        response = requests.get(
            f"{self.host}/rest/getPlayQueue", params=self.params
        ).json()["subsonic-response"]

        if response:
            play_queue = response["playQueue"]
            if play_queue:
                current = play_queue["current"]
                if "position" in play_queue:
                    queue.position = float(play_queue["position"]) / 1000
                for i, entry in enumerate(play_queue["entry"]):
                    if current in entry.values():
                        queue.index = i
                    queue.songs.append(Player.Song(path=entry["path"]))

        return queue

    def enqueue(self, queue: Player.Queue) -> None:
        song_ids = []

        # Unfortunately we can't query by MBID or path, so we have to search a
        # bit to find the right song
        for queued_song in queue.songs:
            song_found = False
            artists = requests.get(
                f"{self.host}/rest/search3",
                params={"query": f"{queued_song.albumartist}"} | self.params,
            ).json()["subsonic-response"]["searchResult3"]["artist"]

            artist_ids = [artist["id"] for artist in artists]

            for artist_id in artist_ids:
                if song_found:
                    break
                albums = requests.get(
                    f"{self.host}/rest/getArtist",
                    params={"id": artist_id} | self.params,
                ).json()["subsonic-response"]["artist"]["album"]

                for album in albums:
                    if song_found:
                        break
                    if album["album"] == queued_song.album:
                        songs = requests.get(
                            f"{self.host}/rest/getAlbum",
                            params={"id": album["id"]} | self.params,
                        ).json()["subsonic-response"]["album"]["song"]

                        for song in songs:
                            if song["path"] == queued_song.path:
                                song_ids.append(song["id"])
                                song_found = True

        current_id = song_ids[queue.index]

        response = requests.get(
            f"{self.host}/rest/savePlayQueue",
            params={
                "id": song_ids,
                "current": current_id,
                "position": int(queue.position * 1000),
            }
            | self.params,
        ).json()["subsonic-response"]

        if not response["status"] == "ok":
            raise Exception(response)
