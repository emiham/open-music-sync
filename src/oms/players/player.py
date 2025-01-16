from abc import ABC, abstractmethod


class Player(ABC):
    """
    Parent class for different players.
    """

    class Queue:
        def __init__(self) -> None:
            """
            Initiate a queue.
            Attributes:
            -----------
            index : int
                Index of the song in the queue, i.e. 0 for the first song.
            position : float
                Playback position in seconds.
            songs : list
                List of songs, contains paths and optionally other metadata.

            """
            self.index: int = 0
            self.position: float = 0.0
            self.songs: list[Player.Song] = []

    class Song:
        def __init__(self, path: str, albumartist: str = "", album: str = "") -> None:
            """
            Initiate a song.

            Arguments:
            -----------
            path : str
                Path to the music file, relative to the music directory.
            albumartist : str
                Album Artist field from tag.
            album : str
                Album field from tag.
            """
            self.path = path
            self.albumartist = albumartist
            self.album = album

    @abstractmethod
    def get_queue(self) -> Queue:
        """Return a Queue object with the current queue."""

        return self.Queue()

    @abstractmethod
    def enqueue(self, queue: Queue) -> None:
        """
        Replace the current queue with a new one, and seek to the new index and
        position.

        Arguments:
        ----------
        queue : Queue
            The new queue.
        """

    def print_queue(self) -> None:
        """Print the current queue."""
        queue: Player.Queue = self.get_queue()

        print(f"index: {queue.index}")

        minutes = int(queue.position // 60)
        seconds = int(queue.position % 60)
        print(f"position: {queue.position} ({minutes:02d}:{seconds:02d})")

        for song in queue.songs:
            if song.albumartist and song.album:
                print(f"{song.albumartist} - {song.album}: {song.path}")
            else:
                print(song.path)
