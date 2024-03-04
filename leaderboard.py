'''
This is a separate part to my main py file. Created as a way to be able to separate my code out as the main
AsteroidsMain.py file was already going to be very large and as this can be calculated on a separate file I deemed it
useful to be able to understand my code better.
Required files for game:
 - leaderboard.py
 - AsteroidsMain.py
 - playerprefs.txt
The other required files will be created as necessary
'''
import os  # Required for some file manipulation
import tkinter as tk  # Required to create the frame to return
import math  # Required for some operations within the program


def GetLB(fileLoc, window):  # This function is called and returns a frame containing leaderboard information
    try:  # Tests to see if the player prefs file exists
        file = open(fileLoc)  # Attempts to open the required file in read mode
    except FileNotFoundError:  # If it doesn't exist, creates the file
        file = open(fileLoc, "x")  # Creates the file in write mode
        file.close()  # Closes just in case
        file = open(fileLoc, "r")  # Reopens in read
    else:  # If the file does exist
        file = open(fileLoc)  # Opens normally
    leaderboardArray = []  # Creates an array to put the data in
    for line in file:  # Takes the data from the open file
        line = line.strip()  # Removes spaces and '\n's
        line = line.split(",")  # Splits it at every comma
        line[1] = int(line[1])  # Turns the second part of the array (the score) into a string
        leaderboardArray.append(line)  # Adds it to the leaderboard list
    sortedBoard = sorted(leaderboardArray, key=lambda x: x[1],reverse=True)  # Sorts it based on number in reverse order
    if len(leaderboardArray) < 5:  # Checks how large the array is
        maxRead = len(leaderboardArray)  # If it's too small for a top 5 it will take the whole list
    else:
        maxRead = 5  # Otherwise the maximum is set to 5 names
    top5 = sortedBoard[0:maxRead]  # Takes the top 5 of the leaderboard or however big it is
    lbFrame = tk.Frame(window)  # Creates a frame that answers to the inputted window
    lbFrame.pack()  # Packs said frame
    # Lines below create the main frame of the leaderboard in a table like format
    tk.Label(lbFrame, text="LEADERBOARD", font="Impact 30", fg="black").grid(row=0, columnspan=3, sticky=tk.W+tk.E)
    tk.Label(lbFrame, text="NAME", font=("Lucida Sans Typewriter", 14), fg="white", bg="black").grid(row=1, column=1)
    tk.Label(lbFrame, text="SCORE", font=("Lucida Sans Typewriter", 14), fg="white", bg="black").grid(row=1, column=2)
    tk.Label(lbFrame, text="1ST:", font=("Lucida Sans Typewriter", 20), fg="#FFD700").grid(row=2, column=0)
    tk.Label(lbFrame, text="2ND:", font=("Lucida Sans Typewriter", 18), fg="#C0C0C0").grid(row=3, column=0)
    tk.Label(lbFrame, text="3RD:", font=("Lucida Sans Typewriter", 16), fg="#CD7F32").grid(row=4, column=0)
    tk.Label(lbFrame, text="4TH:", font=("Lucida Sans Typewriter", 14), fg="black").grid(row=5, column=0)
    tk.Label(lbFrame, text="5TH:", font=("Lucida Sans Typewriter", 14), fg="black").grid(row=6, column=0)
    for i in range(maxRead):  # Iterates through the top 5 (or entire list) to give the names and scores
        # Below assigns them to labels within the table
        tk.Label(lbFrame, text=top5[i][0], font="Arial, 14").grid(row=i + 2, column=1)
        tk.Label(lbFrame, text=top5[i][1], font="Arial, 14").grid(row=i + 2, column=2)
    return lbFrame  # Returns the frame to the calling location


def SaveScore(fileLoc, pName, score):  # Simple score saving function
    file = open(fileLoc, "a")  # Opens the file in append mode
    file.write(pName + "," + str(math.floor(score)) + "\n")  # Writes the new line in at the end with the data


def ClearBoard(fileLoc):  # Slightly cheaty way of removing all contents
    os.remove(fileLoc)  # Deletes the file
    file = open(fileLoc, "x")  # Creates a new one with the same name
    print(type(file))
    # Could also have used write just to completely overwrite the file
