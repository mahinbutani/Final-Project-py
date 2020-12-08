#Mahin Butani (Freshman)
#12/07/2020
#CIS 1051

import tkinter
from random import *
class Simon() :
    def __init__(self, master) :
        # Configure tkinter.Tk with some basic settings.
        self.master = master
        self.master.minsize(640, 480)
        self.master.resizable(False, False)
        self.master.title("Mahin Says")
        self.master.update() # Complete any outstanding tkinter tasks.

        # Create the canvas to be used to draw the rectangles that make up the game. Have it take up the entire window.
        self.game_canvas = tkinter.Canvas(self.master, width = self.master.winfo_width(), height = self.master.winfo_height(), highlightthickness = 0)
        self.game_canvas.pack()

        # Set up the four colors that will be used throughout the game.
        self.game_colors = ("#ff4d4d", "#4d4dff", "#4dff4d", "#faffa3")
        self.simon_colors = ("red", "blue", "green", "yellow")
        self.current_colors = [color for color in self.game_colors]

        self.rectangle_ids = []

        # Sequence of the colors for the current game and the position in the sequence for use when showing it to the user.
        self.sequence = [choice(self.game_colors)]
        self.sequence_position = 0

        self.draw_canvas()

        self.start_sequence()

        self.master.mainloop()

        # Show the sequence to the player, so the player can repeat it.
    def start_sequence(self) :
        # Pass the current color of the sequence to the flash function.
        self.flash(self.sequence[self.sequence_position])
        # Check that we have not reached the end of the sequence.
        if(self.sequence_position < len(self.sequence) - 1) :
            # Since we haven't reached the end of the sequence increment the postion and schedule a callback.
            self.sequence_position += 1
            self.master.after(1250, self.start_sequence)
        else :
            self.sequence_position = 0 # Reset the position for next round.

        # Flash a single rectangle once. Used to indicate it is apart of the sequence to the player.
    def flash(self, color) :
        index = self.game_colors.index(color) # Find the position in the tuple that the specified color is at.
        if self.current_colors[index] == self.game_colors[index] : # Use the position of the color specified to compare if the current color on screen matches the idle one.
            # If so set the current color equal to that of the tinted color.
            self.current_colors[index] = self.simon_colors[index]
            self.master.after(1000, self.flash, color) # Call this function again in 1 seconds time to revert back to the idle color
        else :
            self.current_colors[index] = self.game_colors[index] # Revert the current color back to the idle color.
        self.draw_canvas() # Draw the canvas to reflect this change to the player.

    def check_choice(self) :
        color = self.game_colors[self.rectangle_ids.index(self.game_canvas.find_withtag("current")[0])]
        if(color == self.sequence[self.sequence_position]) :
            if(self.sequence_position < len(self.sequence) - 1) :
                self.sequence_position += 1
            else :
                self.master.title("Mahin Says - Score: {}".format(len(self.sequence))) # Update the score.
                # Reached the end of the sequence append new color to sequence and play that.
                self.sequence.append(choice(self.game_colors))
                self.sequence_position = 0
                self.start_sequence()
        else :
            # Game Over for the player as they got the sequence wrong reset the game back to level one.
            self.master.title("Mahin Says - Game Over! | Final Score: {}".format(len(self.sequence)))
            self.sequence[:] = [] # Empty the list of sequences
            self.sequence.append(choice(self.game_colors)) # Add the first sequence of the new game to the list of sequences.
            self.sequence_position = 0
            self.start_sequence()

    def draw_canvas(self) :
        self.rectangle_ids[:] = [] # Empty out the list of ids.
        self.game_canvas.delete("all") # Clean the frame ready for the new one
        for index, color in enumerate(self.current_colors) : # Iterate over the colors in the list drawing each of the rectangles their respective place.
            if index <= 1 :
                self.rectangle_ids.append(self.game_canvas.create_rectangle(index * self.master.winfo_width(), 0, self.master.winfo_width() / 2, self.master.winfo_height() / 2, fill = color, outline = color))
            else :
                self.rectangle_ids.append(self.game_canvas.create_rectangle((index - 2) * self.master.winfo_width(), self.master.winfo_height(), self.master.winfo_width() / 2, self.master.winfo_height() / 2, fill = color, outline = color))
        for id in self.rectangle_ids :
            self.game_canvas.tag_bind(id, '<ButtonPress-1>', lambda e : self.check_choice())

def main() :
    root = tkinter.Tk()
    gui = Simon(root)

if __name__ == "__main__" : main()
