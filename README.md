# Cyberlab

Requirements: python 3, pygame.

**$python main.py**

## Controls:
* Arrow keys for movement
* F11 toggles fullscreen

## Editing tools:

**$python util/tiled2json.py**
Imports map from [Tiled](http://www.mapeditor.org/)

Usage:
* Load the tileset using *assets/spritesheet.ong*
* Make a new map
* Save the map as .json
* Run the script to convert in the internal map format

**$python util/txt2json.py**
Converts the map in readable txt format to json format