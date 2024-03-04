'''
Resolution in the program is 1280x720
This is my own version of Asteroids built in tkinter
Required files:
 - AsteroidsMain.py (this one)
 - leaderboard.py
 - playerprefs.txt
The other txt files will create themselves as and when needed
'''
import leaderboard  # imports leaderboard.py - non standard library as I created it
import tkinter as tk
from tkinter import Canvas as cv
import math
from PIL import Image, ImageTk
import random


class Constants:  # Class of constants - used to be able to have easy access to any whenever required
    WINDOWHEIGHT = 720  # Each constant is simply named and in all capitals for easy recognition
    WINDOWWIDTH = 1280
    MIDPOINTX = WINDOWWIDTH / 2  # Created the midpoint constants as it was quicker to access like this
    MIDPOINTY = WINDOWHEIGHT / 2
    FIRESPEED = 15
    FRAMERATE = 60  # Controls the framerate the game runs on
    ACCELERATION = -80
    DECELERATION = 2.5
    SPEED = 0.05
    SPEEDCAP = 100
    BULLETSPEED = 3
    MAXBULLETS = 4
    MAXASTEROIDSPEED = 3  # N.B. no speed metric - just used on an individual level due to simplistic nature of the game
    MINASTEROIDSPEED = 1
    ASTEROIDSPEED = 3
    EXPLOSIONLENGTH = 16
    LASERSPEED = 3
    SAUCERSPAWNTIME = 30
    SAUCERSPEED = 4


class Saucer:
    def __init__(self, curIteration):  # Instantiation function, taking in the current iteration of the saucer
        self.health = math.ceil(curIteration / 2)  # The health is set to half the current iteration but always rounded
        # up, i.e. when curIteration = 1, health = 0.5 but rounded up to 1
        self.sprite = ImageTk.PhotoImage(Image.open("Images/Saucer.png"))  # Sets the sprite to the image
        # N.B. the PIL library used here as a quick way to keep the image properly in memory, so it doesn't disappear
        self.pos = [random.randint(0, Constants.WINDOWWIDTH), random.randint(0, Constants.WINDOWHEIGHT)]
        # Above sets the position of the saucer to anywhere within bounds
        self.scoreGiven = 1000 * curIteration  # Sets the score that will be given on destruction based on the iteration
        self.startPos = [self.pos[0], self.pos[1]]  # Sets the starting position to be the position generated
        self.endPos = [random.randint(0, Constants.WINDOWWIDTH), random.randint(0, Constants.WINDOWHEIGHT)]
        # Above generates a random end position for the saucer to travel between
        self.returning = False  # Sets returning to false - i.e. will be going from start to end
        x = self.startPos[0] - self.endPos[0]  # Finds the difference in x
        y = self.startPos[1] - self.endPos[1]  # Finds the difference in Y
        if x != 0:  # Make sure there are no divide by 0 errors
            angle = math.atan2(y, x)  # Uses inverse tan to be able to find the angle of travel for the asteroid
        else:
            if y > 0:  # if x = 0, it will check if y is positive or negative and set the angle accordingly
                angle = 0
            else:
                angle = math.pi
        vecX = math.cos(angle) * -1  # Uses more trigonometry to find the X and Y vectors
        vecY = math.sin(angle) * -1  # Lines below set the velocity of the asteroid, different speeds so random is used
        self.velocity = [vecX * Constants.SAUCERSPEED, vecY * Constants.SAUCERSPEED]  # Sets the velocity
        self.cvObj = gC.create_image(self.pos[0], self.pos[1], image=self.sprite)  # Creates the canvas object

    def Fire(self, pPosX, pPosY):  # Function to fire a laser from the saucer
        pPosX += random.randint(-15, 15)  # Creates some variance in the shots, meaning that the saucers aren't deadly
        pPosY += random.randint(-10, 11)  # accurate with fast lasers - makes the game more fun
        axisDistances = [self.pos[0] - pPosX, self.pos[1] - pPosY]  # Checks the distances on both axes from the player
        angleOfFire = 0  # Creates the angleOfFire variable as a fail-safe in case it doesn't get assigned
        if axisDistances[1] != 0:  # If the distance for the y-axis isn't 0
            angleOfFire = math.atan2(axisDistances[0], axisDistances[1])
            # The above does the inverse tan of x/y - can only be done when y != 0 as otherwise a
            # divide by 0 error is thrown
        else:  # If y is 0
            if axisDistances[0] > 0:  # Checks to see which if the x distance is > 0
                angleOfFire = math.pi / 2  # If it is then the angle of fire is pi/2
            else:  # Otherwise
                angleOfFire = math.pi * (3/2)  # The angle of fire is 3pi/2
        vecX = math.sin(angleOfFire) * -1  # Creates the vectors required
        vecY = math.cos(angleOfFire) * -1  # Multiplied by negative 1 in order for the vectors to work properly
        lasers.append(Laser(vecX, vecY, self.pos[0], self.pos[1]))  # Creates a laser and add it to the list


class Laser:
    def __init__(self, vecX, vecY, posX, posY):  # Takes a few values when created
        self.velocity = [vecX * Constants.LASERSPEED, vecY * Constants.LASERSPEED]
        # Above sets the velocity using the vectors
        self.pos = [posX, posY]  # Sets the laser's position
        self.cvObj = gC.create_oval(posX, posY, posX + 10, posY + 10, fill="#32CD32")  # Creates the green oval object



class Asteroid:  # The class for the asteroids - used to instantiate each asteroid every time it's created
    def __init__(self, size, entryType):  # Runs whenever a new asteroid is instantiated
        self.size = size  # Gets the size from the arguments
        if size == 3:  # (Large)
            spriteNum = random.randint(1, 4)  # Choose a sprite
            self.sprite = tk.PhotoImage(file="Images/Obstacles/LargeAsteroid" + str(spriteNum) + ".png")
            self.width = 48  # Set the geometry
            self.height = 48
            self.health = 3  # Set the health
            self.scoreGiven = 10  # Set the amount of score given when destroyed
        elif size == 2:  # (Medium)
            spriteNum = random.randint(1, 4)
            self.sprite = tk.PhotoImage(file="Images/Obstacles/MediumAsteroid" + str(spriteNum) + ".png")
            self.width = 32
            self.height = 32
            self.health = 2
            self.scoreGiven = 5
        elif size == 1:  # (Small)
            spriteNum = random.randint(1, 4)
            self.sprite = tk.PhotoImage(file="Images/Obstacles/SmallAsteroid" + str(spriteNum) + ".png")
            self.width = 16
            self.height = 16
            self.health = 1
            self.scoreGiven = 3  # Line below sets a random destination location on screen to calculate velocity
        destination = [random.randint(0, Constants.WINDOWWIDTH), random.randint(0, Constants.WINDOWHEIGHT)]
        if entryType == "Vertical":  # Decides what side of the screen to enter from - given as an argument
            r = random.randint(1, 2)  # Chooses top or bottom
            if r == 1:  # Selection and vector location to prove that
                self.pos = [random.randint(0, Constants.WINDOWWIDTH), -20]
            else:
                self.pos = [random.randint(0, Constants.WINDOWWIDTH), Constants.WINDOWHEIGHT + 20]
        else:  # Same for horizontal
            r = random.randint(1, 2)
            if r == 1:
                self.pos = [-20, random.randint(0, Constants.WINDOWHEIGHT)]
            else:
                self.pos = [Constants.WINDOWWIDTH + 20, random.randint(0, Constants.WINDOWHEIGHT)]
        x = self.pos[0] - destination[0]  # Starts the vector calculations to find the velocity
        y = self.pos[1] - destination[1]  # Current position minus destination gives the sides
        if x != 0:  # Make sure there are no divide by 0 errors
            angle = math.atan(y/x)  # Uses inverse tan to be able to find the angle of travel for the asteroid
        else:
            if y > 0:  # if x = 0, it will check if y is positive or negative and set the angle accordingly
                angle = 0
            else:
                angle = math.pi
        vecX = math.sin(angle)  # Uses more trigonometry to find the X and Y vectors
        vecY = math.cos(angle)  # Lines below set the velocity of the asteroid, different speeds so random is used
        self.velocity = [random.randint(Constants.MINASTEROIDSPEED, Constants.MAXASTEROIDSPEED) * vecX,
                         random.randint(Constants.MINASTEROIDSPEED, Constants.MAXASTEROIDSPEED) * vecY]
        # Creates the canvas object:
        self.cvObj = gC.create_image(self.pos[0], self.pos[1], image=self.sprite, tags="asteroid")


class Explosion:  # Class for explosions
    def __init__(self, posX, posY, size):  # Instantiation function
        img = Image.open("Images/Explosions/explosion.png")  # uses PIL to open the image ready for sizing
        x = 0
        y = 0
        if size == 1:  # Takes the size of the asteroid that was destroyed and gets the dimensions of the asteroid
            x = 16
            y = 16
        elif size == 2:
            x = 32
            y = 32
        elif size == 3:
            x = 48
            y = 48
        resizedImage = img.resize((x, y), Image.ANTIALIAS)  # Resizes the image with antialiasing
        self.explosionSprite = ImageTk.PhotoImage(resizedImage)  # Sets sprite variable to be the image
        # N.B. if a constant reference to the image isn't kept, tkinter won't display it correctly as (I assume)
        # It gets removed from memory at the end of the function
        self.explosion = gC.create_image(posX, posY, image=self.explosionSprite)  # Instantiates the image
        self.explosionTimer = 0  # Sets the timer to 0 - used for a seemingly asynchronous process
        # I looked into both threading and async.io but this seemed to be the most consistent


class Player:
    def __init__(self, posX=Constants.MIDPOINTX, posY=Constants.MIDPOINTY):  # Instantiation function
        self.pos = [posX, posY]  # Sets the position if given, if not automatically goes to centre screen
        self.lives = 5  # Sets the amount of lives
        self.godMode = False  # Sets the god mode boolean
        self.fireSpeed = Constants.FIRESPEED  # Sets the fire speed
        self.velocity = [0, 0]  # Sets the player velocity
        self.sprite = tk.PhotoImage(file="Images/Ship/ship0.png")  # Grabs the image just using regular tkinter
        # Line below creates the canvas object
        self.cvObj = gC.create_image(self.pos[0], self.pos[1], image=self.sprite, tags="player")
        self.rot = 0  # Sets the rotation
        self.bulletCap = Constants.MAXBULLETS  # Sets the cap on the bullets
        # Things like the bullet cap had to be done here due to MAXBULLETS being within the Constants class and
        # me wanting to create cheat codes that affect them

        cheatCodes = True  # As python doesn't have a way to section out code to be able to collapse it like in
        if cheatCodes:  # languages like C#, I tried out an if statement like this however it didn't help as much
            if pName == "LIV": # as I thought
                self.lives = 10
            if pName == "GOD":  # Checks the name of the player
                self.godMode = True  # Applies the appropriate cheat
            if pName == "F3X":
                self.fireSpeed = self.fireSpeed / 3
                self.bulletCap = self.bulletCap * 3


class Bullet:
    def __init__(self, angle):  # Runs on instantiation of each bullet
        self.vecX = math.sin(math.radians(angle))  # Uses trigonometry to get the vectors
        self.vecY = math.cos(math.radians(angle))
        self.velocity = [self.vecX * Constants.BULLETSPEED, self.vecY * Constants.BULLETSPEED]  # Sets velocity
        self.cvObj = gC.create_oval(player.pos[0] - 5, player.pos[1] - 5, player.pos[0] + 5, player.pos[1] + 5,
                                    fill="cyan", tags="bullet")  # Creates the canvas object
        self.pos = [player.pos[0]-5, player.pos[1]-5, player.pos[0]+5, player.pos[1]+5]  # Sets the position
        # N.B. almost all pos variables for each object are used only for collision detection


class LifeImage:  # A class solely for the images you see in the top left - done so they won't disappear due to
    def __init__(self, x, y):  # the strange tkinter quirk with images I mentioned earlier
        self.img = tk.PhotoImage(file="Images/Ship/ship180.png")  # Gets the image
        self.cvObj = gC.create_image(x, y, image=self.img)  # Creates the object


class Controls:  # A class for controls that I had to set up an object for due to the scope of where they're required
    def __init__(self, fB, fBC, rL, rLC, rR, rRC, f, fC, p, pC, bk, bC):
        self.fireButton = fB  # The parameters here are used to update the controls
        self.fireChar = fBC  # Each parameter will update a single variable within the object
        self.rotLeft = rL  # This is done so the controls will always be accessible
        self.rotLChar = rLC
        self.rotRight = rR
        self.rotRChar = rRC
        self.forward = f
        self.forwardChar = fC
        self.pause = p
        self.pauseChar = pC
        self.bossKey = bk
        self.bossChar = bC


def GameLoop():  # Main game loop of the entire game
    global gameTicks  # Global variables that control certain parts - gameTicks acts as a counter for every frame
    global scoreboard  # Scoreboard to allow the updates
    global score  # Score variable to be updated
    global canFire  # Check if the player can fire - True/False
    global asteroids  # The array full of asteroids
    global bullets  # The array full of bullets
    global saucerIteration  # Amount of saucers spawned

    gameTicks += 1  # Increases the timer each frame

    spawner = random.randint(300 * difficulty, 1000)  # Chooses a random number that will spawn the asteroids
    if 950 <= spawner < 975:  # The smaller asteroids have a 25 point range for each type making it most common
        asteroids.append(Asteroid(1, "Vertical"))  # Adds an object to asteroids with the size and direction
    elif 925 <= spawner < 950:
        asteroids.append(Asteroid(1, "Horizontal"))  # Same as above but different direction
    elif 975 <= spawner < 982:  # Medium asteroids have a 7/8 point range in order to make them less common
        asteroids.append(Asteroid(2, "Vertical"))
    elif 982 <= spawner < 990:  # Slightly larger range than above in order to keep it as a multiple of 5 between them
        asteroids.append(Asteroid(2, "Horizontal"))
    elif 990 <= spawner < 995:  # Large asteroids have a 5 point range to make them the least common
        asteroids.append(Asteroid(3, "Vertical"))
    elif 995 <= spawner < 1000:
        asteroids.append(Asteroid(3, "Horizontal"))

    angle = player.rot  # Gets the angle of the player
    vecX = math.sin(math.radians(angle))  # Calculates the vectors of each direction - making sure to use the
    vecY = math.cos(math.radians(angle))  # radian value of the angle as math.cos and math.sin require that
    if angle == 90 or angle == 270:  # If the angle is 90 or 270 deg it will set vecY to 0 as
        vecY = 0  # the value of math.cos will always not be exactly 0
    if angle == 0 or angle == 180:  # Same with the x-axis for 0 and 180 deg and vecX
        vecX = 0

    speed = math.sqrt(player.velocity[0] ** 2 + player.velocity[1] ** 2)  # finds the speed of the player by getting
    # the absolute value (essentially getting the magnitude of the vector by a rearrangement a^2 = b^2 + c^2
    if not accelerating and speed <= Constants.SPEEDCAP // 1:  # Checks if the player is accelerating or not and is less
        # than the speed cap
        if player.velocity[1] > 0:  # Checks the direction of the y-velocity
            player.velocity[1] -= player.velocity[1] * (Constants.DECELERATION/player.velocity[1])
        elif player.velocity[1] < 0:  # Line above applies a deceleration formula
            player.velocity[1] += player.velocity[1] * (Constants.DECELERATION/player.velocity[1])
        if player.velocity[0] > 0:  # Does the same as above but with the x-velocity
            player.velocity[0] -= player.velocity[0] * (Constants.DECELERATION/player.velocity[0])
        elif player.velocity[0] < 0:
            player.velocity[0] += player.velocity[0] * (Constants.DECELERATION/player.velocity[0])

    speed = math.sqrt(player.velocity[0] ** 2 + player.velocity[1] ** 2)  # Recalculates speed
    if speed > Constants.SPEEDCAP:  # Checks if speed is going too fast
        if player.velocity[0] != 0:  # If the x-velocity isn't 0 it will set the velocity to the max speed times the
            player.velocity[0] = Constants.SPEEDCAP * vecX  # vector of the required direction
        if player.velocity[1] != 0:
            player.velocity[1] = Constants.SPEEDCAP * vecY

    for shot in bullets:  # Iterates through all bullets
        gC.move(shot.cvObj, Constants.BULLETSPEED * shot.velocity[0], Constants.BULLETSPEED * shot.velocity[1])
        # Moves the bullet
        shot.pos[0], shot.pos[1], shot.pos[2], shot.pos[3] = gC.coords(shot.cvObj)  # Gets the coordinates of the object
        if (shot.pos[2] < 0 or shot.pos[0] > Constants.WINDOWWIDTH or shot.pos[3] < 0 or
                shot.pos[1] > Constants.WINDOWHEIGHT):  # Checks if it's out of the bounds of the screen
            bullets.remove(shot)  # Destroys the object if it's out of bounds and then removes it from the list

    pPos = gC.bbox(player.cvObj)  # Gets the position of the player

    for shot in lasers:  # Iterates through all lasers
        lPos = gC.bbox(shot.cvObj)  # Gets the bounds of the laser
        # Checks for collision with the player
        if ((lPos[0]) in range(pPos[0], pPos[2]) or lPos[2] in range(lPos[0], lPos[2])
                and (lPos[1] in range(pPos[1], pPos[3]) or lPos[1] in range(pPos[1], pPos[3]))):
            if not player.godMode:  # If collision successful and the player isn't in god mode it removes a life
                RemoveLife()
            gC.itemconfigure(shot.cvObj, state="hidden")  # If successful then oval is hidden
            lasers.remove(shot)  # The shot is removed from the list
        # Below is how the laser is moved
        gC.move(shot.cvObj, Constants.LASERSPEED * shot.velocity[0], Constants.LASERSPEED * shot.velocity[1])

    for obst in asteroids:  # Iterates through all the asteroids in the list
        if obst.health == 0:  # If the asteroid is at 0 health
            score += obst.scoreGiven * difficulty  # Adds the score required by difficulty and size of the asteroid
            explosions.append(Explosion(obst.pos[0], obst.pos[1], obst.size))  # Adds an explosion to the list
            asteroids.remove(obst)  # Removes the object and the item from the list
            continue  # Continues to the next iteration
        gC.move(obst.cvObj, Constants.ASTEROIDSPEED * obst.velocity[0], Constants.ASTEROIDSPEED * obst.velocity[1])
        # Line above moves the asteroids via their velocity and the asteroid speed
        obst.pos[0], obst.pos[1] = gC.coords(obst.cvObj)  # Gets the coordinates of the object
        if (obst.pos[0] < -100 or obst.pos[0] > Constants.WINDOWWIDTH + 100 or obst.pos[1] < -100 or
                obst.pos[1] > Constants.WINDOWHEIGHT + 100):  # Checks if the asteroid is out of bounds
            asteroids.remove(obst)  # If it is OOB then it will destroy the object and remove the item from the list
        aPos = gC.bbox(obst.cvObj)  # Get the bounds of the asteroid and put it in a variable
        if ((pPos[0] in range(aPos[0], aPos[2]) or pPos[2] in range(aPos[0], aPos[2]))
                and (pPos[1] in range(aPos[1], aPos[3]) or pPos[3] in range(aPos[1], aPos[3]))):
            # Line above checks if the player is within the bounds of the asteroid
            if not player.godMode:  # Double-check the player isn't in God Mode
                RemoveLife()  # Removes a life if collision detected and not in God Mode
            explosions.append(Explosion(obst.pos[0], obst.pos[1], obst.size))  # Adds an explosion to the list
            # The Explosion class takes the parameters of the position and size of the asteroid in order to get
            # the correct size and location of the explosion
            asteroids.remove(obst)  # Destroys object and removes item from list
        for shot in bullets:  # Iterates through all bullets instantiated at the time
            sPos = gC.bbox(shot.cvObj)  # Gets the position of the bullet
            if ((sPos[0] in range(aPos[0], aPos[2]) or sPos[2] in range(aPos[0], aPos[2]))
                    and (sPos[1] in range(aPos[1], aPos[3]) or sPos[3] in range(aPos[1], aPos[3]))):
                # Checks if the shot is within the bounds of the asteroid
                gC.itemconfigure(shot.cvObj, state="hidden")  # Hides the bullet object
                bullets.remove(shot)  # Removes the bullet from the list
                obst.health -= 1  # Removes 1 from the health of the asteroid

    for expl in explosions:  # Iterates through all explosions
        expl.explosionTimer += 1  # Adds one to the timer within the object
        if expl.explosionTimer == Constants.EXPLOSIONLENGTH:  # If the object's timer reaches the explosion length const
            explosions.remove(expl)  # Remove from the list and destroy the explosion

    for obj in saucers:  # Iterated through all saucers
        if obj.health == 0:  # Checks if their health is 0
            score += obj.scoreGiven * difficulty  # If it is then adds a score
            explosions.append(Explosion(obj.pos[0], obj.pos[1], 2))  # Adds an explosion with size 2 to that location
            saucers.remove(obj)  # Removes the saucer
            continue  # Continues to next iteration as the object no longer exists
        gC.move(obj.cvObj, obj.velocity[0], obj.velocity[1])  # Moves the saucer
        sPos = gC.coords(obj.cvObj)  # Gets the new position of the saucer
        obj.pos = [sPos[0], sPos[1]]  # Sets the objects position to that
        if obj.returning:  # If the saucer is returning to the start position
            if (obj.startPos[0] in range(math.floor(sPos[0]) - 16, math.ceil(sPos[0]) + 16)  # If the saucer is back at
                    and obj.startPos[1] in range(math.floor(sPos[1]) - 16, math.ceil(sPos[1]) + 16)):  # the start pos
                obj.velocity[0] = obj.velocity[0] * -1  # Invert velocity
                obj.velocity[1] = obj.velocity[1] * -1
                obj.returning = False  # Set returning to false
        else:  # Otherwise to the same, but check if the saucer has reached the end pos
            if (obj.endPos[0] in range(math.floor(sPos[0]) - 16, math.ceil(sPos[0]))
                    and obj.endPos[1] in range(math.floor(sPos[1]) - 16, math.ceil(sPos[1]) + 16)):
                obj.velocity[0] = obj.velocity[0] * -1
                obj.velocity[1] = obj.velocity[1] * -1
                obj.returning = True
        for shot in bullets:  # Iterates through all bullets instantiated at the time
            bPos = gC.bbox(shot.cvObj)  # Gets the position of the bullet
            # Below is very long statement for checking collision with saucer, N.B. couldn't get the bbox() function to
            # work with the saucer for unknown reasons - therefore had to improvise. As the saucer is a 32x32px object,
            # to check the bounds only requires to add 16 and subtract 16 to get each side
            if ((bPos[0] in range(math.floor(sPos[0]) - 16, math.ceil(sPos[0]) + 16)
                 or bPos[2] in range(math.floor(sPos[0]) - 16, math.ceil(sPos[0]) + 16))
                    and (bPos[1] in range(math.floor(sPos[1]) - 16, math.ceil(sPos[1]) + 16)
                         or bPos[3] in range(math.floor(sPos[1]) - 16, math.ceil(sPos[1]) + 16))):
                # Checks if the shot is within the bounds of the saucer
                gC.itemconfigure(shot.cvObj, state="hidden")  # Hides the bullet object
                bullets.remove(shot)  # Removes the bullet from the list
                obj.health -= 1  # Removes 1 from the health of the saucers
        if random.randint(0, 50) == 0:  # 2% chance each frame that the saucer shoots a laser
            obj.Fire((pPos[0] + pPos[2]) / 2, (pPos[1] + pPos[3]) / 2)  # Actually shoots

    gC.move(player.cvObj, Constants.SPEED * player.velocity[0], Constants.SPEED * player.velocity[1])
    # Line above moves the player based on their velocity and the speed constant
    player.pos[0], player.pos[1] = gC.coords(player.cvObj)  # Updates the player's position
    if player.pos[0] < 0:  # Checks if player is off the left side of screen
        player.pos[0] = 1270  # Sets position to right side
        gC.moveto(player.cvObj, player.pos[0], player.pos[1])  # Moves object
    elif player.pos[0] > 1280:  # Repeats for right side
        player.pos[0] = 10
        gC.moveto(player.cvObj, player.pos[0], player.pos[1])
    if player.pos[1] < 0:  # Repeats for top side
        player.pos[1] = 710
        gC.moveto(player.cvObj, player.pos[0], player.pos[1])
    elif player.pos[1] > 720:  # Repeats for bottom side
        player.pos[1] = 10
        gC.moveto(player.cvObj, player.pos[0], player.pos[1])

    if gameTicks >= timeLastFired + player.fireSpeed:  # Checks how long since the player last fired and if it has
        canFire = True  # it allows the player to fire again

    if gameTicks % Constants.FRAMERATE == 0:  # Every second
        score = score * (1 + (0.0005 * difficulty))  # Multiply the score by a certain amount
    gC.itemconfig(scoreboard, text="Score: {0}".format(math.floor(score)))  # Updates the scoreboard with the new score

    if gameTicks % (Constants.FRAMERATE * Constants.SAUCERSPAWNTIME) == 0:
        # Above checks to see if it is time to spawn a saucer
        saucerIteration += 1  # Increased what number saucer this is as a total
        saucers.append(Saucer(saucerIteration))  # Creates a saucer and adds it to the list

    if player.lives > 0 and not paused:  # If the player isn't dead and the game isn't bored
        gC.after(1000 // Constants.FRAMERATE, lambda: GameLoop())
        # After a second divided by the frame rate restart the GameLoop() function
    elif player.lives == 0 and not paused:  # If the player is dead and the game isn't paused
        Die()  # Call the die function
    elif paused and not bossKey:  # If the game is paused, and it wasn't the boss key being pressed
        PauseMenu()  # Calls the pause menu
    elif paused and bossKey:  # If the game is paused, and the boss key was pressed
        BossKey()  # Call the boss key menu


def PauseMenu():  # The pause menu function called from the main game
    gameFrame.pack_forget()  # Unloads the gameFrame
    for widget in pauseFrame.winfo_children():  # Checks every child of pauseFrame
        widget.destroy()  # Removes each of the children
    pauseFrame.pack()  # Loads the pauseFrame
    pauseFrame.focus_set()  # Sets the focus to be the pauseFrame
    label = tk.Label(pauseFrame,
                     text="PAUSED\nSCORE IS: {}\nPRESS M FOR MENU\nPRESS S TO SAVE GAME THEN MENU\nPRESS {} FOR UNPAUSE".format(
                         math.floor(score), pControls.pauseChar), font=("Lucida Sans Typewrite", 40),
                     width=Constants.WINDOWWIDTH,
                     height=Constants.WINDOWHEIGHT, fg="#FFFFFF", bg="#000000")
    # The label above creates a black screen the size of the window with white text that says all the text above
    label.pack()  # Loads the label


def BossKey():  # Called from the main game when a key is pressed
    gameFrame.pack_forget()  # Unloads the gameFrame
    for widget in pauseFrame.winfo_children():  # Removes all children of the pauseFrame
        widget.destroy()
    pauseFrame.pack()  # Loads the pauseFrame
    pauseFrame.focus_set()  # Sets the focus of the pauseFrame
    label = tk.Label(pauseFrame, image=blackboardImage, width=Constants.WINDOWWIDTH, height=Constants.WINDOWHEIGHT)
    # The label above loads an image of blackboard the size of the window
    label.pack()  # Loads the label


def SaveGame():  # Save game function - called from pause menu or boss key image
    file = open("savedGame.txt", "w")  # Opens the savedGame.txt in write mode
    file.write(pName + "," + str(score) + "," + str(player.lives))  # Writes the required data
    MainMenu(pauseFrame)  # Calls the MainMenu() function passing in pauseFrame


def PauseKeyRelease(e):  # Function is called every time a key is released while in the pauseFrame
    global paused  # Globally called variables as they need to be updated everywhere
    global bossKey

    if e.keycode == pControls.pause:  # If the pause button is repressed
        paused = False  # Stop the pausing
        bossKey = False  # In case the boss key was pressed originally will reset that variable
        pauseFrame.pack_forget()  # Unload the pause menu
        gameFrame.pack()  # Load the game
        gameFrame.focus_set()  # Reset the focus to the game
        gC.after(1000 // Constants.FRAMERATE, lambda: GameLoop())  # Restarts the game loop
    elif e.char == "m":  # If the key was the m key
        for obj in gameFrame.winfo_children():  # Destroy all objects in gameFrame
            obj.destroy()
        bullets.clear()  # Clear the list of bullets
        asteroids.clear()  # Clear the list of asteroids
        explosions.clear()  # Clear the list of explosions
        livesList.clear()  # Clear the list of the life images
        lasers.clear()  # Clear the list of lasers
        saucers.clear()  # Clear the list of saucers
        paused = False  # Unpause
        bossKey = False  # Reset boss key variable
        MainMenu(pauseFrame)  # Return to MainMenu where pauseFrame will be unloaded
    elif e.char == "s":  # If the key was s
        for obj in gameFrame.winfo_children():  # Destroy all objects
            obj.destroy()
        bullets.clear()  # Clear all lists
        asteroids.clear()
        explosions.clear()
        livesList.clear()
        lasers.clear()
        saucers.clear()
        paused = False  # Unpause
        bossKey = False  # Reset boss key variable
        SaveGame()
    elif e.keycode == pControls.bossKey:  # If the boss key is re-pressed
        paused = False  # Unpause
        bossKey = False  # Reset boss key variable
        pauseFrame.pack_forget()  # Unload pause frame
        gameFrame.pack()  # Load game frame
        gameFrame.focus_set()  # Reset focus to gameFrame
        gC.after(1000 // Constants.FRAMERATE, lambda: GameLoop())  # Restart the game loop


def RemoveLife():  # Function to remove a life - called when a player is hit by an asteroid
    player.lives -= 1  # Removes the life from the player object
    if len(livesList) > 0:  # Checks there's more than 0 lives
        livesList.pop()  # Removes and destroy the last player life image in the list


def Die():  # Called when the player has no more lives
    gameFrame.pack_forget()  # Unloads the game frame
    for obj in gameFrame.winfo_children():  # Destroys all objects in the gameFrame
        obj.destroy()
    bullets.clear()  # Clears all the lists
    asteroids.clear()
    explosions.clear()
    livesList.clear()
    saucers.clear()
    lasers.clear()
    deathFrame.pack()  # Loads the death screen
    deathFrame.focus_set()  # Sets the focus to be the death screen
    label = tk.Label(deathFrame, text="GAME OVER\nSCORE WAS: {}\nPRESS M FOR MENU\nPRESS S TO SAVE THEN MENU".format(math.floor(score)),
                     font=("Impact", 40), width=Constants.WINDOWWIDTH, height=Constants.WINDOWHEIGHT,
                     fg="#FF0000", bg="#000000")
    # Label above creates a black screen the size of the window with red text saying the above
    label.pack()  # Loads the label


def DeathScreenKeyPress(e):  # Function is called every time a key is pressed on the death screen
    if e.char == "m":  # If the m key is pressed
        MainMenu(deathFrame)  # Return to the main menu with deathFrame being unloaded
    elif e.char == "s":  # If the s key is pressed
        SaveAndReturn(deathFrame)  # Go to the save function with the death screen being unloaded


def SaveAndReturn(frame):  # Function called on certain key press on death screen - takes the frame
    leaderboard.SaveScore("leaderboard.txt", pName, score)  # Saves the score using the leaderboard.py function
    MainMenu(frame)  # Returns to the main menu passing through the same frame


def StartGame():  # StartGame is called once the player enters a valid name
    global gC  # Global variable to store the canvas
    global player  # Global variable to store the player
    global scoreboard  # Global variable to store the scoreboard
    global saucerIteration
    menuFrame.pack_forget()  # Unload the menu
    gameFrame.pack()  # Load the game screen
    gameFrame.focus_set()  # Set the focus to the game screen
    gC, scoreboard = SetGUI()  # Set gC and scoreboard through the SetGUI function
    player = Player()  # Create the player object

    saucerIteration = 0  # Resets the saucer amount to 0

    lifeNum = 5  # Sets the number of lives to 5
    if pName == "LIV":  # Checks if the player is using the cheat code
        lifeNum = 10  # If so it sets the number of lives to 10
    for i in range(lifeNum):  # Iterates through the loop the same amount of times as how many lives there are
        x = 40 + (20 * i)  # Arbitrary values of spacing - each image placed 20px apart starting at 40
        y = 60  # Y height is 60 - just below the scoreboard
        livesList.append(LifeImage(x, y))  # Append the image to the list

    gC.pack()  # Load the canvas
    gC.after(1000 // Constants.FRAMERATE, lambda: GameLoop())  # Begin the game loop


def SetGUI():  # Called by the start-up functions of the game (start or load)
    canvas = cv(gameFrame, width=Constants.WINDOWWIDTH, height=Constants.WINDOWHEIGHT, bg="black")
    # Line above creates a black canvas that is the same dimensions as the window
    board = canvas.create_text(40, 20, fill="white", text="Score: 0")
    # Line above creates a text object that is the scoreboard for the game

    return canvas, board  # Returns both the canvas and the scoreboard


def GameKeyPress(e):  # This is called every time a key is pressed while the gameFrame is the foucs
    global player  # Global player due to the need to edit values within
    global accelerating  # Required to test whether the player is accelerating

    # Below checks if the keycode of the key pressed is the same as the controls for the player to move forward
    if e.keycode == pControls.forward:
        angle = player.rot  # Sets angle to be the player's rotation value
        vecX = math.sin(math.radians(angle))  # Sets the vectors using the same trigonometric functions
        vecY = math.cos(math.radians(angle))
        if angle == 90 or angle == 270:  # Reassigns the vectors in the case of the cardinal directions
            vecY = 0
        if angle == 0 or angle == 180:
            vecX = 0
        player.velocity[0] -= Constants.ACCELERATION * vecX  # Adds acceleration to the velocities
        player.velocity[1] -= Constants.ACCELERATION * vecY  # Negative is used here as (0, 0) is the top left
        # of the screen making it a slightly strange coordinate system
        accelerating = True  # Sets accelerating to be true
    if e.keycode == pControls.rotRight:  # If the keycode matches the right rotation key
        if player.rot - 9 == -9:  # Checks that the player rotation won't be moving out of bounds
            player.rot = 351  # If it will then set it to the correct rotation
        else:  # Otherwise it will just subtract 9 from the rotation
            player.rot -= 9
        player.sprite = tk.PhotoImage(file="Images/Ship/ship" + str(player.rot) + ".png")
        # Gets the photo image of the correctly angled ship and saves it to the sprite
        player.cvObj = gC.create_image(player.pos[0], player.pos[1], image=player.sprite)
        # Recreates the player canvas object to display the new rotation
        # N.B. For some reason image rotation on instantiated images is not supported in tkinter
    if e.keycode == pControls.rotLeft:  # If the keycode matches the left rotation key
        if player.rot + 9 == 360:  # Same as above but done for the opposite direction
            player.rot = 0
        else:
            player.rot += 9
        player.sprite = tk.PhotoImage(file="Images/Ship/ship" + str(player.rot) + ".png")  # Update sprite
        player.cvObj = gC.create_image(player.pos[0], player.pos[1], image=player.sprite)  # Create new image


def GameKeyRelease(e):  # Called every time a key is released on the main game screen
    global accelerating  # Global variable for accelerating required as is referenced elsewhere
    global bullets  # Global list for bullets as needs to be updated
    global timeLastFired  # Global variable for the last firing so the fire rate can be implemented
    global canFire  # Global boolean for whether the player can fire so the fire rate can't be bypassed
    global paused  # Global boolean for if the game is paused
    global bossKey  # Global boolean for if the game was paused with the boss key

    if e.keycode == pControls.forward:  # If forward is released
        accelerating = False  # Update accelerating to be false
    elif e.keycode == pControls.fireButton and len(bullets) < player.bulletCap and canFire:
        # The above checks if the fire button was released, there aren't more bullets than the player's bullet cap
        # and that the player can fire
        timeLastFired = gameTicks  # Sets the time last fired to the game time
        canFire = False  # Updates the boolean so the player can no longer fire
        bullets.append(Bullet(player.rot))  # Adds a bullet to the list
    elif e.keycode == pControls.pause:  # If the player released the pause button
        if not paused:  # If the game is not paused
            paused = True  # Pause the game
        else:  # Otherwise
            paused = False  # Unpause it
        # N.B. The else part of the statement is unnecessary but was included as a form of fail safe in case the
        # focus of the frames did not change correctly
    elif e.keycode == pControls.bossKey:  # If the player released the boss key
        if not paused:  # Same as above except updating the boss key boolean as well
            paused = True
            bossKey = True
        else:
            paused = False
            bossKey = False


def LoadGame():  # Load game can only be called from the main menu and loads the last saved game
    global gC  # Global canvas
    global player  # Global player variable
    global scoreboard  # Global scoreboard
    global pName  # Global player name so that it can be changed to match the saved game
    global score  # Global score so that it can be changed to match the saved data
    global saucerIteration  # Global value of saucers that have spawned
    menuFrame.pack_forget()  # Unload the menu
    gameFrame.pack()  # Load the game
    gameFrame.focus_set()  # Set the focus for the game - needed so that controls will go to the correct function

    file = open("savedGame.txt", "r")  # Opens the save file
    parts = file.read().split(",")  # Separates out the information for the list
    pName = parts[0]  # Sets the player name
    score = float(parts[1])  # Sets the score
    saucerIteration = 0  # Sets the amount of saucers back to 0

    gC, scoreboard = SetGUI()  # Creates the canvas and scoreboard through SetGUI
    player = Player()  # Creates the player object

    lifeNum = parts[2]  # Sets the number of lives to the saved data
    for i in range(int(lifeNum)):  # Iterates through that many times
        x = 40 + (20 * i)  # Set up the life image locations
        y = 60
        livesList.append(LifeImage(x, y))  # Generates the images

    gC.pack()  # Loads the canvas
    gC.after(1000 // Constants.FRAMERATE, lambda: GameLoop())  # Starts up the game loop


def ShowLeaderboard():
    lbFrame = leaderboard.GetLB("leaderboard.txt", window)
    # Uses the GetLB function of leaderboard.py to gete the frame
    menuFrame.pack_forget()  # Unloads the menu
    lbFrame.pack()  # Loads the leaderboard
    tk.Button(lbFrame, text="MAIN MENU", font=("Lucida Sans Typewriter", 16),
              command=lambda: MainMenu(lbFrame)).grid(row=7, columnspan=3, sticky=tk.W+tk.E)
    # Above is the return button at the bottom of the leaderboard
    # Below is a button to clear the leaderboard, calling ClearLeaderboard and passing in the leaderboard frame
    tk.Button(lbFrame, text="CLEAR LEADERBOARD", font=("Lucida Sans Typewriter", 16),
              command=lambda: ClearLeaderboard(lbFrame)).grid(row=8, columnspan=3, sticky=tk.W+tk.E)


def ClearLeaderboard(frame):  # Simple function to clear the leaderboard
    leaderboard.ClearBoard("leaderboard.txt")  # Calls ClearBoard from leaderboard.py
    MainMenu(frame)  # Returns to the main menu, passing in the leaderboard frame as an argument


def RefreshOptionsMenu():  # Function called when loading the options menu and when controls are changed
    for widget in optionsFrame.winfo_children():  # Deletes all previous children of the options menu
        widget.destroy()
    tk.Label(optionsFrame, text="OPTIONS", font=("Impact", 40)).grid(row=0, columnspan=3)
    # Above sets the title

    # Below creates a subtitle for the difficulty section of the menu
    tk.Label(optionsFrame, text="DIFFICULTY:", font=("Lucida Sans Typewriter", 20)).grid(row=1, columnspan=3)

    # Below creates labels for different radio buttons for the difficulty
    tk.Label(optionsFrame, text="EASY", font=("Lucida Sans Typewriter", 12)).grid(row=2, column=0)
    tk.Label(optionsFrame, text="MEDIUM", font=("Lucida Sans Typewriter", 12)).grid(row=2, column=1)
    tk.Label(optionsFrame, text="HARD", font=("Lucida Sans Typewriter", 12)).grid(row=2, column=2)

    diffVar = tk.IntVar()  # Creates a tkinter variable that can be changed with radio buttons
    diffVar.set(difficulty)  # Sets it to the current difficulty that is taken from the playerprefs.txt file
    dR1 = tk.Radiobutton(optionsFrame, variable=diffVar, value=1)  # Creates the first radio button
    dR1.grid(row=3, column=0)  # Sets the location
    dR2 = tk.Radiobutton(optionsFrame, variable=diffVar, value=2)  # Creates second radio button
    dR2.grid(row=3, column=1)  # Sets location
    dR3 = tk.Radiobutton(optionsFrame, variable=diffVar, value=3)  # Creates third radio button
    dR3.grid(row=3, column=2)  # Sets location
    # The value part of the tk.Radiobutton() function tells the program what to set the variable to

    # Below sets a subtitle for the controls section of the menu
    tk.Label(optionsFrame, text="CONTROLS:", font=("Lucida Sans Typewriter", 20)).grid(row=4, columnspan=3)
    # Creates the control message label at the bottom of the menu
    ctrlMessage = tk.Label(optionsFrame, text="", font=("Lucida Sans Typewrite", 15))
    ctrlMessage.grid(row=11, columnspan=3)  # Sets the location

    # Below creates the label for the first control
    tk.Label(optionsFrame, text="SHOOT:", font=("Lucida Sans Typewrite", 15)).grid(row=5, column=0, columnspan=2)
    # Below creates the button to change the first control and display the current one
    shootControl = tk.Button(optionsFrame, text=pControls.fireChar, font=("Lucida Sans Typewrite", 15),
                             command=lambda: ChangeControl(1, ctrlMessage))
    # Sets the location
    shootControl.grid(row=5, column=2)

    # Repeat of above for the next control
    tk.Label(optionsFrame, text="ROTATE LEFT:", font=("Lucida Sans Typewrite", 15)).grid(row=6, column=0, columnspan=2)
    rotLControl = tk.Button(optionsFrame, text=pControls.rotLChar, font=("Lucida Sans Typewrite", 15),
                            command=lambda: ChangeControl(2, ctrlMessage))
    rotLControl.grid(row=6, column=2)

    # Repeat
    tk.Label(optionsFrame, text="ROTATE RIGHT:", font=("Lucida Sans Typewrite", 15)).grid(row=7, column=0, columnspan=2)
    rotRControl = tk.Button(optionsFrame, text=pControls.rotRChar, font=("Lucida Sans Typewrite", 15),
                            command=lambda: ChangeControl(3, ctrlMessage))
    rotRControl.grid(row=7, column=2)

    # Repeat
    tk.Label(optionsFrame, text="FORWARD:", font=("Lucida Sans Typewrite", 15)).grid(row=8, column=0, columnspan=2)
    forwardControl = tk.Button(optionsFrame, text=pControls.forwardChar, font=("Lucida Sans Typewrite", 15),
                               command=lambda: ChangeControl(4, ctrlMessage))
    forwardControl.grid(row=8, column=2)

    # Repeat
    tk.Label(optionsFrame, text="PAUSE:", font=("Lucida Sans Typewrite", 15)).grid(row=9, column=0, columnspan=2)
    pauseControl = tk.Button(optionsFrame, text=pControls.pauseChar, font=("Lucida Sans Typewrite", 15),
                             command=lambda: ChangeControl(5, ctrlMessage))
    pauseControl.grid(row=9, column=2)

    # Repeat
    tk.Label(optionsFrame, text="BOSS KEY:", font=("Lucida Sans Typewrite", 15)).grid(row=10, column=0, columnspan=2)
    bossControl = tk.Button(optionsFrame, text=pControls.bossChar, font=("Lucida Sans Typewrite", 15),
                            command=lambda: ChangeControl(6, ctrlMessage))
    bossControl.grid(row=10, column=2)

    # Below creates a button to go back to the main menu, stopping by a different function first and retrieving
    # the value generated by the radio buttons to send through as well as the frame
    tk.Button(optionsFrame, text="MAIN MENU", font=("Lucida Sans Typewriter", 15), width=25, bg="#aaaaaa",
              command=lambda: SetOptions(optionsFrame, diffVar.get())).grid(row=12, columnspan=3)


def OptionsMenu():  # Called when the options menu button is pressed on the main meny
    RefreshOptionsMenu()  # Generates the options menu
    menuFrame.pack_forget()  # Unloads main menu
    optionsFrame.pack()  # Loads options menu
    optionsFrame.focus_set()  # Sets the focus to the options menu


def ChangeControl(controlNum, message):  # Called whenever a control button is pressed on the options menu
    global changing  # Required so the control that is being changed is known
    if controlNum == 1:  # Checks which control it is
        message.config(text="ENTER NEW CONTROL FOR SHOOT")  # Updates control message to the write thing
    elif controlNum == 2:
        message.config(text="ENTER NEW CONTROL FOR ROT LEFT")
    elif controlNum == 3:
        message.config(text="ENTER NEW CONTROL FOR ROT RIGHT")
    elif controlNum == 4:
        message.config(text="ENTER NEW CONTROL FOR FORWARD")
    elif controlNum == 5:
        message.config(text="ENTER NEW CONTROL FOR PAUSE")
    elif controlNum == 6:
        message.config(text="ENTER NEW CONTROL FOR BOSS KEY")
    changing = controlNum  # Sets changing to be the control number


def OptionsKeyRelease(e):  # Called whenever a key is released
    global changing  # Required to find which control needs updating
    global pControls  # Required the controls object to update the controls

    # N.B. Python 3.10 finally introduced a switch case statement, and unfortunately we can't use it as this is 3.9
    if changing == 1:  # Checks if there is a control being changed and which it is
        pControls.fireButton = e.keycode  # Sets the control to the inputted keycode
        if e.keycode == 32:  # Checks if the keycode is one that cannot be turned directly into a character
            pControls.fireChar = "SPACE"  # As if we tried that with space we'd just get " "
        elif e.keycode == 37:  # If it can't be turned to a character it is set to a string of what we expect to see
            pControls.fireChar = "LEFT"
        elif e.keycode == 38:
            pControls.fireChar = "UP"
        elif e.keycode == 39:
            pControls.fireChar = "RIGHT"
        elif e.keycode == 40:
            pControls.fireChar = "DOWN"
        else:  # If it can be converted to a character
            pControls.fireChar = e.char  # The character variable is set to the inputted character
        pControls.fireChar = pControls.fireChar.upper()  # It is then set to upper case to match the style
        changing = 0  # Changing is then set to 0
        RefreshOptionsMenu()  # The options menu is then refreshed
    elif changing == 2:  # Repeats for different controls
        pControls.rotLeft = e.keycode
        if e.keycode == 32:
            pControls.rotLChar = "SPACE"
        elif e.keycode == 37:
            pControls.rotLChar = "LEFT"
        elif e.keycode == 38:
            pControls.rotLChar = "UP"
        elif e.keycode == 39:
            pControls.rotLChar = "RIGHT"
        elif e.keycode == 40:
            pControls.rotLChar = "DOWN"
        else:
            pControls.rotLChar = e.char
        pControls.rotLChar = pControls.rotLChar.upper()
        changing = 0
        RefreshOptionsMenu()
    elif changing == 3:  # Repeats for different controls
        pControls.rotRight = e.keycode
        if e.keycode == 32:
            pControls.rotRChar = "SPACE"
        elif e.keycode == 37:
            pControls.rotRChar = "LEFT"
        elif e.keycode == 38:
            pControls.rotRChar = "UP"
        elif e.keycode == 39:
            pControls.rotRChar = "RIGHT"
        elif e.keycode == 40:
            pControls.rotRChar = "DOWN"
        else:
            pControls.rotRChar = e.char
        pControls.rotRChar = pControls.rotRChar.upper()
        changing = 0
        RefreshOptionsMenu()
    elif changing == 4:  # Repeats for different controls
        pControls.forward = e.keycode
        if e.keycode == 32:
            pControls.forwardChar = "SPACE"
        elif e.keycode == 37:
            pControls.forwardChar = "LEFT"
        elif e.keycode == 38:
            pControls.forwardChar = "UP"
        elif e.keycode == 39:
            pControls.forwardChar = "RIGHT"
        elif e.keycode == 40:
            pControls.forwardChar = "DOWN"
        else:
            pControls.forwardChar = e.char
        pControls.forwardChar = pControls.forwardChar.upper()
        changing = 0
        RefreshOptionsMenu()
    elif changing == 5:  # Repeats for different controls
        pControls.pause = e.keycode
        if e.keycode == 32:
            pControls.pauseChar = "SPACE"
        elif e.keycode == 37:
            pControls.pauseChar = "LEFT"
        elif e.keycode == 38:
            pControls.pauseChar = "UP"
        elif e.keycode == 39:
            pControls.pauseChar = "RIGHT"
        elif e.keycode == 40:
            pControls.pauseChar = "DOWN"
        else:
            pControls.pauseChar = e.char
        pControls.pauseChar = pControls.pauseChar.upper()
        changing = 0
        RefreshOptionsMenu()
    elif changing == 6:  # Repeats for different controls
        pControls.bossKey = e.keycode
        if e.keycode == 32:
            pControls.bossChar = "SPACE"
        elif e.keycode == 37:
            pControls.bossChar = "LEFT"
        elif e.keycode == 38:
            pControls.bossChar = "UP"
        elif e.keycode == 39:
            pControls.bossChar = "RIGHT"
        elif e.keycode == 40:
            pControls.bossChar = "DOWN"
        else:
            pControls.bossChar = e.char
        pControls.bossChar = pControls.bossChar.upper()
        changing = 0
        RefreshOptionsMenu()


def SetOptions(oF, diff=2):  # Called by a button when returning to the main menu from the options menu
    # Diff is set to 2 on the off chance that something goes wrong with the radio buttons
    global difficulty  # Accesses the global difficulty variable
    prefFile = open("playerprefs.txt", "w")  # Opens the playerprefs.txt file in write mode as it needs to overwrite
    # the data that is currently stored there
    prefString = (str(diff) + "," + str(pControls.fireButton) + "," + str(pControls.rotLeft) + "," + str(pControls.rotRight)
                  + "," + str(pControls.forward) + "," + str(pControls.pause) + "," + str(pControls.bossKey))
    # The above then creates a string with all the parts that need to be saved there and separates them with commas
    prefFile.write(prefString)  # The string is then wrtten to the file
    difficulty = diff  # Difficulty is then set to diff - which is the value of the radio buttons
    MainMenu(oF)  # Main menu is then called with the options frame passed through to it for unloading


def LoadPrefs():  # Load prefs is called on the booting of the game
    global difficulty  # Requires the reference to the global difficulty variable to update it
    global pControls  # Requires the reference to the player controls object to update the values
    try:  # Tests to see if the player prefs file exists
        prefFile = open("playerprefs.txt")  # Attempts to open the playerprefs.txt file in read mode
    except FileNotFoundError:  # If it doesn't exist, creates the file
        prefFile = open("playerprefs.txt", "w")  # Creates the file in write mode
        prefFile.write("2,32,37,39,38,80,66")  # Write in some default settings
        prefFile.close()  # Closes from write
        prefFile = open("playerprefs.txt", "r")  # Reopens in read
    else:  # If the file does exist
        prefFile = open("playerprefs.txt")  # Opens normally
    prefString = prefFile.read()  # Reads the file to a string
    prefArray = prefString.split(",")  # Separates it out at each comma
    fBC = ""  # Empty strings are made on the off chance that the file didn't save properly and so there is no value
    rLC = ""  # that can be set within the conditional statements ahead
    rRC = ""
    fC = ""
    pC = ""
    bC = ""
    for i in range(len(prefArray)):  # Iterates through the loop as many times as there are items in the array
        prefArray[i] = int(prefArray[i])  # Turns each value back into an integer data type

    if prefArray[1] == 32:  # Sets the characters like above in case there are values that can't be converted
        fBC = "SPACE"  # to characters
    elif prefArray[1] == 37:
        fBC = "LEFT"
    elif prefArray[1] == 38:
        fBC = "UP"
    elif prefArray[1] == 39:
        fBC = "RIGHT"
    elif prefArray[1] == 40:
        fBC = "DOWN"
    else:
        fBC = chr(int(prefArray[1]))

    if prefArray[2] == 32:  # Repeat
        rLC = "SPACE"
    elif prefArray[2] == 37:
        rLC = "LEFT"
    elif prefArray[2] == 38:
        rLC = "UP"
    elif prefArray[2] == 39:
        rLC = "RIGHT"
    elif prefArray[2] == 40:
        rLC = "DOWN"
    else:
        rLC = chr(int(prefArray[2]))

    if prefArray[3] == 32:  # Repeat
        rRC = "SPACE"
    elif prefArray[3] == 37:
        rRC = "LEFT"
    elif prefArray[3] == 38:
        rRC = "UP"
    elif prefArray[3] == 39:
        rRC = "RIGHT"
    elif prefArray[3] == 40:
        rRC = "DOWN"
    else:
        rRC = chr(int(prefArray[3]))

    if prefArray[4] == 32:  # Repeat
        fC = "SPACE"
    elif prefArray[4] == 37:
        fC = "LEFT"
    elif prefArray[4] == 38:
        fC = "UP"
    elif prefArray[4] == 39:
        fC = "RIGHT"
    elif prefArray[4] == 40:
        fC = "DOWN"
    else:
        fC = chr(int(prefArray[4]))

    if prefArray[5] == 32:  # Repeat
        pC = "SPACE"
    elif prefArray[5] == 37:
        pC = "LEFT"
    elif prefArray[5] == 38:
        pC = "UP"
    elif prefArray[5] == 39:
        pC = "RIGHT"
    elif prefArray[5] == 40:
        pC = "DOWN"
    else:
        pC = chr(int(prefArray[5]))

    if prefArray[6] == 32:  # Repeat
        bC = "SPACE"
    elif prefArray[6] == 37:
        bC = "LEFT"
    elif prefArray[6] == 38:
        bC = "UP"
    elif prefArray[6] == 39:
        bC = "RIGHT"
    elif prefArray[6] == 40:
        bC = "DOWN"
    else:
        bC = chr(int(prefArray[6]))

    difficulty = prefArray[0]  # Sets the difficulty to be whatever was saved in the file

    pControls = Controls(prefArray[1], fBC, prefArray[2], rLC, prefArray[3], rRC, prefArray[4], fC, prefArray[5], pC,
                         prefArray[6], bC)
    # Above sets the player's controls in the __init__ function of the Controls class


def ValidateEntry(e, errMsg):  # Called whenever the play game button is pressed
    global pName  # Calls the global reference to the player name
    name = e.get()  # e is the entry box passed through so the value is retrieved with the .get() function
    if len(name) == 3 and " " not in name:  # Checks the length of the name is 3 and there are no spaces
        pName = name  # If so then the name is accepted and set
        StartGame()  # Then start game is called
    else:  # Otherwise an error message is shown, and you must try to enter the name again
        errMsg.config(text="ENTER 3-LETTER NAME WITHOUT SPACES, NO MORE NO LESS")
        # The above line references errMsg which is passed into the function through the main menu


def MainMenu(prevFrame=None):  # The main menu function which takes a previous frame, if none is given it is assigned
    if prevFrame is not None:  # as a none value. If the frame variable is not None then it will unload the frame
        prevFrame.pack_forget()
    menuFrame.pack()  # Loads the menu frame
    menuFrame.focus_set()  # Sets the focus to the menu frame
    tk.Label(menuFrame, text="METEORITES", font=("Impact", 50)).grid(row=0, columnspan=2)  # Label creates the title
    # Below is the label for the name entry boc
    tk.Label(menuFrame, text="ENTER 3-LETTER NAME:", font=("Lucida Sans Typewriter", 20)).grid(row=1, column=0)
    # Below is the entry box and is assigned to the right of the label
    nameEntry = tk.Entry(menuFrame, font=("Lucida Sans Typewriter", 20))
    nameEntry.grid(row=1, column=1)

    # errMsg is located underneath that and originally sent to a blank string
    errMsg = tk.Label(menuFrame, text="", font=("Lucida Sans Typewriter", 15), fg="#FF0000")
    errMsg.grid(row=2, columnspan=2)
    # Below button calls the ValidateEntry function, passing in both the entry box and the errMsg label
    tk.Button(menuFrame, text="PLAY GAME", font=("Lucida Sans Typewriter", 15), width=25, bg="#aaaaaa",
              command=lambda: ValidateEntry(nameEntry, errMsg)).grid(row=3, columnspan=2)

    # Below button calls the LoadGame function
    tk.Button(menuFrame, text="LOAD GAME", font=("Lucida Sans Typewriter", 15), width=25, bg="#aaaaaa",
              command=lambda: LoadGame()).grid(row=4, columnspan=2)
    # Below button generates and displays the leaderboard
    tk.Button(menuFrame, text="LEADERBOARD", font=("Lucida Sans Typewriter", 15), width=25, bg="#aaaaaa",
              command=lambda: ShowLeaderboard()).grid(row=5, columnspan=2)
    # Below button transitions to the options menu
    tk.Button(menuFrame, text="OPTIONS", font=("Lucida Sans Typewriter", 15), width=25, bg="#aaaaaa",
              command=lambda: OptionsMenu()).grid(row=6, columnspan=2)


if __name__ == '__main__':  # Executes every time the program is run normally
    window = tk.Tk()  # Creates the window using tkinter
    window.title("Meteorites")  # Sets the title to be "Meteorites" - obvious play on asteroids
    window.geometry(str(Constants.WINDOWWIDTH) + "x" + str(Constants.WINDOWHEIGHT))  # Sets the geometry of the window
    menuFrame = tk.Frame(window)  # Creates the main menu frame
    gameFrame = tk.Frame(window)  # Creates the game frame
    optionsFrame = tk.Frame(window)  # Creates the options frame
    deathFrame = tk.Frame(window)  # Creates the death screen frame
    pauseFrame = tk.Frame(window)  # Creates the pause menu frame
    difficulty = 2  # Sets difficulty to 2 in the case of first boot and allows the global references
    pName = ""  # Sets the player name to nothing and allows global references
    gC = cv()  # Sets gC to be a canvas object, allows PyCharm to suggest parts and reduces annoying warnings
    scoreboard = gC.create_text(0, 0, text="")  # Creates a blank text object for scoreboard
    gameTicks = 0  # Sets the run timer to 0
    score = 0  # Sets the initial score to 0
    timeLastFired = 0  # Sets the initial time last fired to 0
    canFire = True  # Sets initial fire check to true

    asteroids = []  # Creates blank asteroid list
    accelerating = False  # Sets accelerating to false
    player = Player()  # Creates new player object - reduces warnings and allows global assignment
    pControls = Controls(0, "", 0, "", 0, "", 0, "", 0, "", 0, "") # Creates blank controls object
    LoadPrefs()  # Calls LoadPrefs to update controls

    # Below calls the function every time optionsFrame is in focus and a key is released and passes in the key event
    optionsFrame.bind("<KeyRelease>", lambda event: OptionsKeyRelease(event))

    # Below calls the function every time gameFrame is in focus and a key is pressed and passes in the key event
    gameFrame.bind("<KeyPress>", lambda event: GameKeyPress(event))
    # Same as the previous key release but for gameFrame
    gameFrame.bind("<KeyRelease>", lambda event: GameKeyRelease(event))

    # Same as previous key press but for deathFrame
    deathFrame.bind("<KeyPress>", lambda event: DeathScreenKeyPress(event))

    # Same as previous key release but for pauseFrame
    pauseFrame.bind("<KeyRelease>", lambda event: PauseKeyRelease(event))

    changing = 0  # Sets changing to 0
    bullets = []  # Creates empty bullet list
    explosions = []  # Creates empty explosions list
    livesList = []  # Create empty life images list
    paused = False  # Sets paused to be false
    bossKey = False  # Sets boss key to be false
    lasers = []  # Create empty lasers list
    saucers = []  # Create empty saucers list
    saucerIteration = 0  # Stores how many saucers have been spawned

    image = Image.open("Images/blackboard.jpg")  # Fetches the image of blackboard
    # Below scales the image to the window size using antialiasing
    scaledImage = image.resize((Constants.WINDOWWIDTH, Constants.WINDOWHEIGHT), Image.ANTIALIAS)
    # Sets blackboardImage to be the resized image
    blackboardImage = ImageTk.PhotoImage(scaledImage)

    MainMenu()  # Calls MainMenu() as the first function

    window.mainloop()  # Creates the window
