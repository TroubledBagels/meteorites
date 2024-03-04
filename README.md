# Meteorites
## Description
This was a challenge I set myself to be able to create a game in the python tkinter package, one which does not have any physics built in.
For this, I decided to create my version of Asteroid, the classic game that everyone knows.

For this, I had to:
- Create the physics
- Create the collision
- Program all functionality
- Make it fun

This was made in the Autumn 2022, and my commenting style was a bit much at the time. Hopefully from my submission, you can see that it has changed since.

## Changelog

### Reading Variables
There are a few types of variables:
1. Regular variables are typed in camelCase
2. Constants are typed in CAPITALS
3. Functions are typed in PascalCase

This allows me to easily and quickly recognise variables when I need to.

N.B. Blackboard is my Uni's main course website, and is a part of this as I wanted to add a "boss key"

### 03/11/22 - 18:10
Working on the train so lack of pushes
Main changes:
- Added Constants() to be able to store all the constants required for the program
- Added main menu
- Added way to view leaderboard from AsteroidsMain.py
- Added options menu
- Added ways to navigate between menus
- Added name entry box on main menu
- Added options to change difficulty on options menu
- Added method to change controls
- Added fonts.txt which is just a list of usable fonts within tkinter
- Added Controls() class to store different controls
- Added a way to refresh the options menu once the controls have changed
- Added key press and release detection for within the options menu
- Added a function to save the options before returning to the main menu
- Created multiple frames for the different sections of my program
- Changed font in leaderboard.py

### 04/11/22 - 15:07
- Finished the options menu, so it contains both difficulty and controls
- Added a playerprefs.txt file that stores the options so between sessions you won't have to change all your options back
- Fixed an error where difficulty wasn't changing correctly

### 05/11/22 - 16:15
- Added name validation and first canvas to the program
- Created a method for deceleration, but still need to get the calculations right
- Implemented the acceleration of the ship
- Setup possibilities for easier implementation of rotation of the ship
- Added rotation to the ship - not displayed on image yet
- Rotation works however the maths for keeping speed down don't yet

### 06/11/22 - 20:00
- Sorted velocity and movement incl. rotation
- Added bullets
- Added bullet movement
- Added bullet cap
- Added fire rate
- Implemented F3X cheat code
- Created many asteroid sprites
- Created asteroid class
- Added some asteroid logic
- Started collision with asteroids

### 09/11/22 - 20:30
- Added explosion "animation"
- Added collision with asteroids
- Added loss of life function
- Added bullet collision with asteroids
- Added increase in score from asteroid destruction with bullets

### 10/11/22 - 18:00
- Finished death screen
- Added checklist.md
- Fixed some bugs with the leaderboard in the case that there are less than 5 entries
- Added the changes that come with difficulty
- Added god mode
- Added save game feature
- Added load game
- Added pause screen
- Added boss key and all logic with it

### 11/11/22 - 18:30
- **Lots** of comments

### 12/11/22 - 10:15
- Added a clear leaderboard option to the leaderboard frame

### 25/11/22 - 16:30
- Added saucers
- Added saucer aim variation
- Added saucer lasers
- Added saucer movement
- Added player wrap around
- Error handling for if playerprefs doesn't exist
- Error handling for if leaderboard.txt doesn't exist