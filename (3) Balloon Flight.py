import pgzrun
import pygame
import pgzero
import random
import time
from random import randint
from pgzero.builtins import Actor

WIDTH = 800
HEIGHT = 600
GRAVITY_STRENGTH = 1
life = 5

balloon = Actor('balloon')
balloon.pos = 400, 300

bird = Actor('bird-up')
bird.pos = randint(800, 1600), randint(10, 200)

house = Actor('house')
house.pos = randint(800, 1600), 460

house2 = Actor('house')
house2.pos = randint(800, 1600), 460

tree = Actor('tree')
tree.pos = randint(800, 1600), 450

tree2 = Actor('tree')
tree2.pos = randint(800, 1600), 450

bird_up = True
up = False
game_over = False
score = 0
number_of_updates = 0
level = 1

scores = []


def update_high_scores():
    global score, scores
    filename = (r'high-scores.txt')
    scores = []
    with open(filename, 'r') as file:
        line = file.readline()
        high_scores = line.split()
        for high_score in high_scores:
            if(score > int(high_score)):
                scores.append(str(score) + ' ')
                score = int(high_score)
            else:
                scores.append(str(high_score) + ' ')
    with open(filename, 'w') as file:
        for high_score in scores:
            file.write(high_score)


def display_high_scores():
    screen.draw.text('GAME OVER', (350, 100), color='black')
    screen.draw.text('Score: ' + str(score), (350, 120), color='black')
    #screen.draw.text('High Scores', (350, 150), color='black')
    y = 175
    position = 1
    
    for high_score in scores:
        screen.draw.text(str(position) + ". " + high_score, (350, y), color="black")
        y += 25
        position += 1


def draw():
    screen.blit('background', (0,0))
    if not game_over:
        balloon.draw()
        bird.draw()
        house.draw()
        house2.draw()
        tree.draw()
        tree2.draw()
        screen.draw.text('Score: ' + str(score), (700, 5), color='black')
        screen.draw.text("Lives: " + str(life), (700, 20), color="black")
        if level < 6:
            screen.draw.text("Level: " + str(level), (700, 35), color="black")
        else:
            screen.draw.text("Level: CRAZY", (700, 35), color="black")
    else:
        display_high_scores()


def on_mouse_down():
    global up
    up = True
    balloon.y -= 50


def on_mouse_up():
    global up
    up = False

def life_count():
    global life
    if life > 0:
        life -= 1
    else:
        game_over = True

def flap():
    global bird_up
    if bird_up:
        bird.image = 'bird-down'
        bird_up = False
    else:
        bird.image = 'bird-up'
        bird_up = True


def update():
    global game_over, score, number_of_updates, level, speed, speedbird

    if level != 8:
        speed = 2 + level
        speed2 = speed
        speedbird = speed * 2
    else:
        speed = 10
        speed2 = 12
        speedbird = 19

    if score == 10:
        level = 2
    elif score == 20:
        level = 3
    elif score == 30:
        level = 4
    elif score == 40:
        level = 5
    elif score == 50:
        level = 8

    if life > 0:
        if not up:
            balloon.y += GRAVITY_STRENGTH  # gravity
        if bird.x > 0:
            bird.x -= speedbird
            if number_of_updates == 9:
                flap()
                number_of_updates = 0
            else:
                number_of_updates += 1
        else:
            bird.x = randint(800, 1600)
            bird.y = randint(10, 200)
            score += 1
            number_of_updates = 0

        if house.right > 0:
            house.x -= speed
        else:
            house.x = randint(800, 1600)
            score += 1

        if house2.right > 0:
           house2.x -= speed2
        else:
           house2.x = randint(800, 1600)
           score += 1

        if tree.right > 0:
            tree.x -= speed
        else:
            tree.x = randint(800, 1600)
            score += 1

        if tree2.right > 0:
            tree2.x -= speed2
        else:
            tree2.x = randint(800, 1600)
            score += 1

        if balloon.top < 0 or balloon.bottom > 560:
            #game_over = True
            #update_high_scores()
            balloon.pos = 400, 300
            life_count()

        if (balloon.collidepoint(bird.x, bird.y) or
                balloon.collidepoint(house.x, house.y) or
                balloon.collidepoint(tree.x, tree.y)):
            #game_over = True
            #update_high_scores()
            balloon.pos = 400, 300
            life_count()
    else:
        game_over = True

pgzrun.go()
