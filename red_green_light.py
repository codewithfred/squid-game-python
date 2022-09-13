from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random
import sys

app = Ursina()

player = FirstPersonController()
player.cursor.visible = False

Sky()

ground = Entity(
    model = 'plane',
    texture = 'grass',
    collider = 'mesh',
    scale = (600, 10, 600)
)

losing_ground = Entity(
    model = 'plane',
    texture = 'assets/lava.jpg',
    collider = 'mesh',
    scale = (600, 10, 600),
    position = (0, -100, 0)
)

doll = Entity(
    model = 'assets/doll.obj',
    color = color.black,
    scale = 4,
    position = (0, 0, 50)
)

left_eye = Entity(
    model = 'sphere',
    color = color.red,
    scale = 0.2,
    position = (-0.3, 13, 49.05)
)

right_eye = Entity(
    model = 'sphere',
    color = color.red,
    scale = 0.2,
    position = (0.3, 13, 49.05)
)

line = Entity(
    model = 'cube',
    color = color.red,
    scale = (600, 0.1, 1),
    position = (0, 0, 40)
)

def turn_front():
    current_y = doll.rotation_y
    doll.animate_rotation_y(current_y + 180, duration = random.randint(1, 2))
    invoke(turn_back, delay = 3)
 
def turn_back():
    current_y = doll.rotation_y
    doll.animate_rotation_y(current_y - 180, duration = random.randint(1, 2))
    invoke(turn_front, delay = 3)

turn_front()

time_left = Text(
    size = 2 * Text.size,
    text = f'Time: {00}\t',
    position = (0.5, 0.4)
)
time_left.create_background()

def set_time(sec):
    time_left.text = f'Time: {sec}\t'
    if sec == 0 and player.z < 40:
        destroy(ground)
        destroy(time_left)
        lose_text = Text(
            scale = 3,
            text = 'GAME OVER',
            color = color.red,
            position = (-0.21, 0, 0)
        )
        window.exit_button.visible = True
        mouse.locked = False
    if sec > 0:
        invoke(set_time, sec - 1, delay = 1)

set_time(50)

def update():
    walking = held_keys['w'] or held_keys['a'] or held_keys['s'] or held_keys['d']
    if doll.rotation_y == 180.0:
        if player.z < 40:
            if walking or player.y > 0 or not mouse.velocity == Vec3(0, 0, 0):
                destroy(ground)
                destroy(time_left)
                lose_text = Text(
                    scale = 3,
                    text = 'GAME OVER',
                    color = color.red,
                    position = (-0.21, 0, 0)
                )
                window.exit_button.visible = True
                mouse.locked = False

def input(key):
    if key == 'escape':
        quit()

app.run()