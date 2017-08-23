# Cyberlab

Requirements: python 3, pygame.

**$python main.py**

## Controls:

### Menu:

* Up/Down keys to select option
* Enter to choose option

### Game:

* Arrow keys for movement
* Look at the door and press Enter to open/close it
* E or G to pickup items, Q to drop
* F11 toggles fullscreen

## Editing tools:

### Tiled

**$python util/tiled2json.py**
Imports map from [Tiled](http://www.mapeditor.org/)

Usage:
* Load the tileset using *assets/spritesheet.png*
* Make a new map
* Save the map as .json
* Run the script to convert in the internal map format

#### How to add story triggers
* Add a new objects layer
* Selects a rectangular area
* Add a custom property called text
* The value of that property would be the displayed text

### Plain old ascii art

**$python util/txt2json.py**
Converts the map in readable txt format to json format

### Compiling into executable
**python -m pip install cx_Freeze --upgrade** to install cx_Freeze module

**python setup.py build**

It will create *build* folder with binaries.
