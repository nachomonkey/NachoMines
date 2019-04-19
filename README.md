# NachoMines
*A simple python-made minesweeper game using pygame*
## Requires
* Python 3.6 or greater
* pygame

## Installation
### Linux

**Using Pip**

	sudo pip3 install git+https://github.com/nachomonkey/NachoMines

**Using Git**

	git clone https://github.com/nachomonkey/NachoMines
	cd NachoMines
	sudo python3 setup.py install

## Launching the game

The **setup.py** script installs the "nachomines" python module, a "nachomines" console script, and a .desktop file on linux machines.

**Using Python**

	python3 -m nachomines
**Using the console script**

	nachomines

**Using the .desktop file**

An application by the name "NachoMines" should be found in the "Games" section of your application menu

## Gameplay and Controls
* Press <**Esc**> or <**Q**> to exit
### Main Menu

* The "Grid Subdivisions" drop-down menu selects the size of the game board
* The "Mine Density" drop-down menu controls the chance in percentage of a square containing a mine.

### Game
Hover over the blocks using the cursor. Right-click to flag a block.
Left-click to show an empty square and the empty squares near it.

# License
Uses the MIT License. See the LICENSE file for further detail.