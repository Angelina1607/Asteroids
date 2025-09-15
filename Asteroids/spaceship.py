from PIL import Image, ImageTk
import math

class Spaceship:
    def __init__(self, canvas):
        self.canvas = canvas
        self.angle = 0
        self.speed = 0
        self.x = 500
        self.y = 309
        self.ship_image = ImageTk.PhotoImage(Image.open("ship.png"))
        self.fire_ship_image = ImageTk.PhotoImage(Image.open("ship_with_fire.png"))
        self.rocket_image = ImageTk.PhotoImage(Image.open("blast.png"))
        self.ship_img = None
        self.fire_ship_img = None

    def generate_fire_ship(self, x, y):

        self.fire_ship_img = self.canvas.create_image(x, y, image=self.fire_ship_image)
        self.rotate(0)

    def generate_ship(self, x, y):
        self.ship_img = self.canvas.create_image(x, y, image=self.ship_image)
        self.rotate(0)

    def move(self):
        self.x -= self.speed * math.sin(math.radians(self.angle%360))
        self.y -= self.speed * math.cos(math.radians(self.angle%360))
        self.wrap_around()
        if self.speed >= 0.2:
            self.speed -= 0.2
        else: self.speed = 0

        if self.speed > 0:
            if self.ship_img:
                self.canvas.delete(self.ship_img)
                self.ship_img = None
            if self.fire_ship_img is None:
                self.generate_fire_ship(self.x, self.y)
            self.canvas.coords(self.fire_ship_img, self.x, self.y)
        if self.speed == 0:
            if self.fire_ship_img:
                self.canvas.delete(self.fire_ship_img)
                self.fire_ship_img = None
            if self.ship_img is None:
                self.generate_ship(self.x, self.y)
            self.canvas.coords(self.ship_img, self.x, self.y)

    def wrap_around(self):
        if self.x > 1000:
            self.x = 0
        elif self.x < 0:
            self.x = 1000
        if self.y > 618:
            self.y = 0
        elif self.y < 0:
            self.y = 618

    def rotate(self, angle):
        self.angle += angle
        if self.ship_img:
            self.ship_image = ImageTk.PhotoImage(Image.open("ship.png").rotate(self.angle, expand=True))
            self.ship_img = self.canvas.create_image(self.x, self.y, image=self.ship_image)
        if self.fire_ship_img:
            self.fire_ship_image = ImageTk.PhotoImage(Image.open("ship_with_fire.png").rotate(self.angle, expand=True))
            self.fire_ship_img = self.canvas.create_image(self.x, self.y, image=self.fire_ship_image)

    def accelerate(self):
        if self.speed < 7:
            self.speed += (7-self.speed)



class Blast:
    def __init__(self, canvas, ship_x, ship_y, ship_angle):
        self.canvas = canvas
        self.x = ship_x-30*math.sin(math.radians(ship_angle%360))
        self.y = ship_y-30*math.cos(math.radians(ship_angle%360))
        self.angle = ship_angle
        self.blast_image = ImageTk.PhotoImage(Image.open("blast.png").rotate(ship_angle, expand=True))
        self.blast_img = self.canvas.create_image(self.x, self.y, image=self.blast_image)

    def move(self):
        self.canvas.coords(self.blast_img, self.x, self.y)
        self.x -= 15 * math.sin(math.radians(self.angle%360))
        self.y -= 15 * math.cos(math.radians(self.angle % 360))

    def check_collision_with_asteroid(self, asteroid_x, asteroid_y):
        if asteroid_x-20<=self.x<=asteroid_x+20 and asteroid_y-20<=self.y<=asteroid_y+20: return True
