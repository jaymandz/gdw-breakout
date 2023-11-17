# gdw-breakout

Inspired by this old-ass [StackExchange post](https://gamedev.stackexchange.com/questions/854/what-are-good-games-to-earn-your-wings-with), here's my attempt at creating a Breakout clone!

_You need to have Python 3.11 and [pipenv](https://pypi.org/project/pipenv/) installed in your computer first._

After cloning this repo, run the following command to set everything up:

```shell
$ pipenv update
```

_Windows users will need to download_ `pygame‑2.1.2‑cp310‑cp310‑win_amd64.whl` _from [this website](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pygame) first before running this command. I'm not putting it in this repo because it's not mine._

Then run this to start the game:

```shell
$ pipenv run python ./breakout.py
```

Enjoy!

## Update (November 17, 2023)

Last commits were on December 12, 2022. Whew!

Anyway, I tried setting this repo up in a Pearl Linux 13 system (which is based on Debian 12). I had to install the libraries listed below first. This should serve as a guide for Linux users who want to run this game on what to install first:

- `libfreetype6-dev`
- `libportmidi-dev`
- `libsdl2-dev`
- `libsdl2-image-dev`
- `libsdl2-mixer-dev`
- `libsdl2-ttf-dev`

Also, I had to downgrade the Python version to 3.10, as 3.11 had some problems compiling Pygame.
