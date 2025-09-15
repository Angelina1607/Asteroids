import tkinter as tk
from tkinter import *
import time
from PIL import Image, ImageTk
from spaceship import Spaceship, Blast
from asteroids import Asteroid

class Game:
    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(master, width=1000, height=618)
        self.sky_image = tk.PhotoImage(file='sky.png')
        self.screensaver_image = tk.PhotoImage(file='screensaver.png')
        self.canvas.pack()

        self.lives = 3
        self.score = 0
        self.loss = False

        self.asteroids = []
        self.ship = None

        self.display_lives = None
        self.display_score = None

        self.explosion_image = ImageTk.PhotoImage(Image.open("explosion.png"))
        self.explosion_of_ship_img = None
        self.time_explosion_of_ship = time.time()

        self.blast = None
        self.blast_live = None

        self.explosion_of_blast_img = None
        self.time_explosion_of_blast = time.time()

        self.show_start_screen()

        self.canvas.bind("<Button-1>", self.start_game)
        self.master.bind("<space>", self.shoot)
        self.master.bind("<Left>", self.rotate_left)
        self.master.bind("<Right>", self.rotate_right)
        self.master.bind("<Up>", self.accelerate)

    def show_start_screen(self):
        self.canvas.create_image(1, 1, anchor='nw', image=self.screensaver_image)

    def start_game(self, event):
        if 442 < event.x < 716 and 192 < event.y < 426:
            self.canvas.delete("all")
            self.canvas.create_image(1, 1, anchor='nw', image=self.sky_image)
            self.update_score_and_lives()
            self.generate_ship()
            self.generate_asteroids()
            self.game_loop()

    def update_score_and_lives(self):
        self.display_lives = self.canvas.create_text(100, 20, text=f"Lives: {self.lives}", anchor=NW, fill='green', font='Arial 18')
        self.display_score = self.canvas.create_text(900, 20, text=f"Score: {self.score}", anchor=NE, fill='green', font='Arial 18')

    def generate_ship(self):
        self.ship = Spaceship(self.canvas)

    def generate_asteroids(self):
        if len(self.asteroids) < 20:
            for _ in range(20-len(self.asteroids)):  # Generate 5 asteroids
                asteroid = Asteroid(self.canvas)
                self.asteroids.append(asteroid)

    def game_loop(self):
        self.game_over()
        if not self.loss:
            if self.blast:
                self.blast.move()
                for asteroid in self.asteroids:
                    if (self.blast and self.blast.check_collision_with_asteroid(asteroid.x, asteroid.y)
                            and self.check_blast_live()):
                        self.asteroids.remove(asteroid)
                        self.time_explosion_of_blast = time.time()
                        self.explosion_of_blast_img = self.canvas.create_image(
                            (asteroid.x + self.blast.x) / 2,
                            (asteroid.y + self.blast.y) / 2, image=self.explosion_image)
                        self.blast_live=None
                        self.blast = None
                        self.score += 100
            self.check_blast_live()
            self.check_collision()
            self.canvas.delete(self.display_lives)
            self.canvas.delete(self.display_score)
            self.update_score_and_lives()
            self.generate_asteroids()
            self.delete_explosion_of_ship()
            self.delete_explosion_of_blast()
            self.ship.move()
            for asteroid in self.asteroids:
                asteroid.move()
            self.master.after(50, self.game_loop)

    def shoot(self, event):
        if not self.blast:
            self.blast_live = time.time()
            self.blast = Blast(self.canvas, self.ship.x, self.ship.y, self.ship.angle)

    def check_blast_live(self):
        if self.blast_live and self.blast and time.time() - self.blast_live < 1:
            return True
        else:
            self.blast_live = None
            self.blast = None

    def rotate_left(self, event):
        self.ship.rotate(10)

    def rotate_right(self, event):
        self.ship.rotate(-10)

    def accelerate(self, event):
        self.ship.accelerate()

    def check_collision(self):
        coordinates = []
        for asteroid in self.asteroids:
            coordinates.append([asteroid.x, asteroid.y])
            if (asteroid.x-25 <= self.ship.x <= asteroid.x+25
                    and asteroid.y-25 <= self.ship.y <= asteroid.y+25):
                self.lives -= 1
                self.generate_ship()
                self.asteroids.remove(asteroid)
                self.time_explosion_of_ship = time.time()
                self.explosion_of_ship_img = self.canvas.create_image(
                    (self.ship.x+asteroid.x*30)/31, (self.ship.y+asteroid.y*30)/31,
                    image=self.explosion_image)

    def delete_explosion_of_ship(self):
        if self.time_explosion_of_ship is not None:
            if time.time() - self.time_explosion_of_ship > 0.5:
                if self.explosion_of_ship_img is not None:
                    self.canvas.delete(self.explosion_of_ship_img)
                    self.time_explosion_of_ship = None

    def delete_explosion_of_blast(self):
        if self.time_explosion_of_blast is not None:
            if time.time() - self.time_explosion_of_blast > 0.3:
                if self.explosion_of_blast_img is not None:
                    self.canvas.delete(self.explosion_of_blast_img)
                    self.time_explosion_of_blast = None

    def game_over(self):
        if self.lives == 0:
            self.loss = True
            self.canvas.create_image(1, 1, anchor='nw', image=self.screensaver_image)
            self.canvas.create_text(100, 20, text=f"Lives: {self.lives}", anchor=NW, fill='green', font='Arial 18')
            self.canvas.create_text(900, 20, text=f"Score: {self.score}", anchor=NE, fill='green', font='Arial 18')
            self.canvas.create_text(500, 100, text=f"GAME OVER", fill='red', font='Algerian 30 bold')



