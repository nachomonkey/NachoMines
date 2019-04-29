# NachoMines
*A simple python-made minesweeper game using pygame*
## Requires
* Python 3.6 or greater
* pygame
* Monospace font (recommended)

## Installation
### Linux

**Using Pip**

```bash
sudo pip3 install git+https://github.com/nachomonkey/NachoMines
```

**Using Git**

```bash
git clone https://github.com/nachomonkey/NachoMines
cd NachoMines
sudo python3 setup.py install
```

## Launching the game

The **setup.py** script installs the "nachomines" python module, a "nachomines" console script, and a .desktop file on linux machines.

**Using Python**

```bash
python3 -m nachomines
```
**Using the console script**

```bash
nachomines
```

**Using the .desktop file**

An application by the name "NachoMines" should be found in the "Games" section of your application menu

## Gameplay and Controls
* Press <**Esc**> or <**Q**> to exit
### Main Menu

* The "Grid Subdivisions" drop-down menu selects the size of the game board
* The "Mine Density" drop-down menu controls the chance in percentage of a square containing a mine.
* The "Theme" drop-down menu decides if you want a light or dark color theme during gameplay.

### Game
Hover over the blocks using the cursor. Right-click to flag a block.
Left-click to show an empty square and the empty squares near it.

Win by flagging all of the mines.

# License
Uses the MIT License. See the LICENSE file for further detail.