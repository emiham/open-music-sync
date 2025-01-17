# OpenMusicSync

Lets you seamlessly continue playback on different self-hosted music players.

## Supported players

### [MPD](https://www.musicpd.org/)

- Normal MPD installations work.
- Mopidy or any other implementations have not been tested.

### [Subsonic](https://www.subsonic.org/)

#### Servers

- [gonic](https://github.com/sentriz/gonic) works.
- [Navidrome](https://www.navidrome.org/) does not work, because it doesn't
expose real file paths.
- Other server implementations that expose real file paths should work, but so
far they are untested.

#### Clients

|                                                              | Platform | Saves queue | Loads queue                                                        |
|--------------------------------------------------------------|----------|-------------|--------------------------------------------------------------------|
| [airsonic-refix](https://github.com/tamland/airsonic-refix)  | Browser  | Yes         | Yes                                                                |
| [DSub2000](https://github.com/paroj/DSub2000)                | Android  | Yes         | Yes                                                                |
| [Tempo](https://github.com/CappielloAntonio/tempo)           | Android  | No          | No ([issue](https://github.com/CappielloAntonio/tempo/issues/336)  |
| [Youamp](https://github.com/siper/Youamp)                    | Android  | Yes         | No ([issue](https://github.com/siper/Youamp/issues/316))           |
| [Ultrasonic](https://gitlab.com/ultrasonic/ultrasonic)       | Android  | No          | No                                                                 |

 Open an issue if you've tried any other players so they can be added to this 
 list.

### [Jellyfin](https://jellyfin.org/)

> [!NOTE]  
> Currently you can only get the queue from Jellyfin, not the other way. This
> will be added in a future update.

#### Clients

- Jellyfin Web
- [Finamp](https://github.com/jmshrv/finamp)
- Open an issue if you've tried any other players so they can be added to this
  list.

### Others

Other players will be considered, open an issue and we can try to find out
what's possible.

## Installation

The different players need to store the same file paths for the music files.
If you point all players to the same music directory this should work, but if
you for some reason have different music directories for different players it
won't.

You need to create a configuration directory and file in your `XDG_CONFIG_HOME`
directory (usually `~/.config/OpenMusicSync/config.toml`). See
[Configuration](#-configuration) for an example configuration file.

## Usage

`open-music-sync source target`

Note that your current queue will be replaced without any prompts.

You can run the program with only a source argument to print the information
that would be sent to a target.

### Configuration

The structure should be as follows:
```toml
[MPD]
host = "127.0.0.1"
port = "6600"

[Subsonic]
host = "https://music.example.com"
user = "your_username"
password = "your_password"

[Jellyfin]
host = "https://jellyfin.example.com"
token = "your_jellyfin_api_token"
music_directory = "/home/your_username/music"
```

Substitute the values with your own.

The MPD section can be empty. It will then default to the `MPD_HOST` and
`MPD_PORT` environment variables, or `127.0.0.1` and `6600` respectively if the
environment variables are not set.

All values in the Subsonic and Jellyfin sections are mandatory, if you want to
use those players. If not, you can leave them empty.
