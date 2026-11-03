import argparse
import os
import tomllib

from xdg_base_dirs import xdg_config_home

from oms.players.jellyfin import Jellyfin
from oms.players.mpd import MPD
from oms.players.player import Player
from oms.players.subsonic import Subsonic

from .constants import APP_NAME, PLAYERS


def _create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d", "--daemon", help="Run in daemon mode", action="store_true"
    )
    parser.add_argument(
        "source_player",
        choices=PLAYERS,
        help="Player to load queue from",
    )
    parser.add_argument(
        "target_player", nargs="?", choices=PLAYERS, help="Player to play on"
    )
    return parser


def _create_player(player_type: str, config):
    """
    Creates a player to read queue from or send queue to.

    Arguments:
    ----------
    player_type : str
        One of "MPD", "Subsonic", or "Jellyfin".
    config : dict
        Dictionary with configuration options.

    Returns:
    --------
        Player: the newly initiated player.
    """
    player: Player
    if player_type == "MPD":
        player = MPD(**config["MPD"])
    elif player_type == "Subsonic":
        player = Subsonic(**config["Subsonic"])
    elif player_type == "Jellyfin":
        player = Jellyfin(**config["Jellyfin"])

    return player


def load_config(filename="config.toml"):
    """
    Load a TOML configuration file from the XDG config directory.

    Arguments:
    ----------
    filename : str
        The name of the config file to load.

    Returns:
    --------
        dict: The configuration data.
    """
    path = os.path.join(xdg_config_home(), APP_NAME, filename)

    if not os.path.exists(path):
        raise FileNotFoundError(f"Config file '{path}' not found.")

    with open(path, "rb") as config_file:
        config = tomllib.load(config_file)

    return config


def main():
    """Runs the program."""
    parser = _create_parser()
    args = parser.parse_args()

    config = load_config()
    source_player = _create_player(args.source_player, config)

    if args.daemon:
        if not args.target_player:
            parser.error("daemon mode requires a target player")

        target_player = _create_player(args.target_player, config)

        try:
            source_player.daemon(target_player.enqueue)
        except NotImplementedError:
            parser.error(f"{args.source_player} does not support daemon mode")
        except KeyboardInterrupt:
            pass

    elif args.target_player:
        target_player = _create_player(args.target_player, config)
        target_player.enqueue(source_player.get_queue())

    else:
        source_player.print_queue()


if __name__ == "__main__":
    main()
