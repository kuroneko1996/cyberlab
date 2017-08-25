# Cyberlab

Requirements: python 3, pygame.

**$python main.py**

## Controls:

### Menu:

* Up/Down keys to select option
* Enter to choose option

### Game:

* Arrow keys for movement. Numeric pad works too.
* Look at the door and press E or Enter to open/close it
* E or G to pickup items, Q to drop
* Space to close text messages
* F11 toggles fullscreen

You can change default key mapping in settings.py

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
**$python -m pip install cx_Freeze --upgrade** to install cx_Freeze module

**$python setup.py build**

It will create *build* folder with binaries.

## Development:


### In-game text
To put text on player's screen, append a message object
(you can make one with `message.make_message(text)`) to
`game.message_queue`.
This list contains all the messages that the player can
read at the moment. The message that the players sees is
the last text element in the list. When he presses space,
last message is removed from the list and the player sees
next message.

You can also make a text message that switches the picture
displayed on the players screen using
`message.make_message(text, True)`.
The picture would be switched after the players dismisses
the message.

### In-game images
To add an image on player's screen, append a `Sprite`
object to `game.picture_queue`.