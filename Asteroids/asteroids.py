import tkinter as tk
import random

class Asteroid:
    def __init__(self, canvas):
        self.canvas = canvas
        self.x = random.randint(0, 1000)
        self.y = random.randint(0, 618)
        self.asteroid_image = tk.PhotoImage(file='asteroid.gif')
        self.image = self.canvas.create_image(self.x, self.y, image=self.asteroid_image)
        self.speed_x = random.uniform(3, 6)

    def move(self):
        self.x -= self.speed_x
        if self.x < 0:
            self.x = 1000
        self.canvas.coords(self.image, self.x, self.y)
