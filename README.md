# gdw-breakout

Inspired by this old-ass [StackExchange post](https://gamedev.stackexchange.com/questions/854/what-are-good-games-to-earn-your-wings-with), here's my attempt at creating a Breakout clone!

_You need to have Python 3.11 and [poetry](https://python-poetry.org) installed in your computer first._

After cloning this repo, run the following command to set everything up:

```shell
$ poetry update
```

Then run this to start the game:

```shell
$ poetry run python breakout.py
```

Enjoy!

## Creating an executable file

If you wish to create an executable file for this game, run the following command:

```shell
$ poetry run pyinstaller breakout.spec
```

You will find the new executable file in the `dist` folder.

## Audio credits

- Background song is &ldquo;Like A Cake&rdquo; by Andrey Avkhimovich. [Listen on Jamendo](https://www.jamendo.com/track/1199570/like-a-cake)
- Ball bounce on paddle was extracted from [this sound](https://freesound.org/people/DanielRousseau/sounds/366780/) from Freesound user `DanielRousseau`.
- Bell sound when ball speed increases was extracted from [this sound](https://freesound.org/people/cdrk/sounds/495484/) from Freesound user `cdrk`.
- Sound when paddle shrinks was extracted from [this sound](https://freesound.org/people/OTBTechno/sounds/136772/) from Freesound user `OTBTechno`.
- Rewind sound when game resets was derived from [this sound](https://freesound.org/people/crunchymaniac/sounds/687272/) from Freesound user `crunchymaniac`.
- Sound when keys are pressed in menus was extracted from [this sound](https://freesound.org/people/Freezeman/sounds/153210/) from Freesound user `Freezeman`.