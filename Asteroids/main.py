import tkinter as tk
from game import Game

class Main:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Asteroids Game")
        self.game = Game(self.root)
        self.root.mainloop()

if __name__ == "__main__":
    Main()

