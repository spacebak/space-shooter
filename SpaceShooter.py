import terminalio
import displayio
from adafruit_display_text import label
import math
import random

# Static variables
frame_sleep = 0.02
max_shots = 3
shot_timeout = 0.3
enemy_spawn_multiplier = 0.9
enemy_spawn_minimum_time = 1.0;

# Dynamic variables
score = 0
lives = 3
enemy_timeout = 4.0
game_over = False;
shots = []
enemies = []
time_since_shot = shot_timeout
time_since_enemy = enemy_timeout

# Game elements setup
player = displayio.Group()
player_group = displayio.Group(scale=1, x=int(display.width*0.5), y=display.height - 20)
player_area = label.Label(terminalio.FONT, text="A", color=0xFFFFFF)
player_group.append(player_area)
player.append(player_group)

score_group = displayio.Group(scale=1, x=0, y=5)
score_area = label.Label(terminalio.FONT, text="{:08d}".format(score), color=0xFFFFFF)
score_group.append(score_area)
player.append(score_group)

lives_group = displayio.Group(scale=1, x=display.width, y=5)
lives_area = label.Label(terminalio.FONT, text="AAA", color=0xFFFFFF, label_direction="RTL")
lives_group.append(lives_area)
player.append(lives_group)

display.show(player)

def UpdateScore(label):
    label.text = "{:08d}".format(score)

def Shoot():
    shot_group = displayio.Group(scale=1, x=player_group.x, y=player_group.y - 3)
    shot_area = label.Label(terminalio.FONT, text="*", color=0xFFFFFF)
    shot_group.append(shot_area)
    player.append(shot_group)
    shots.append(shot_group)

def MoveShots():
    for shot in shots:
        shot.y = shot.y - 2
        if(shot.y < 0):
            RemoveShot(shot)

def MoveEnemies():
    lose_life = False
    for enemy in enemies:
        enemy.y = enemy.y + 1
        if(enemy.y > display.height):
                lose_life = True
                RemoveEnemy(enemy)
        for shot in shots:
            if(DistanceBetweenGroups(enemy, shot) < 5):
                score = score + 1000 - enemy.y * 10 
                RemoveEnemy(enemy)
                RemoveShot(shot)
                UpdateScore(score_area)
    return lose_life

def DistanceBetweenGroups(a, b):
    return math.sqrt(pow(a.x - b.x, 2) + pow(a.y - b.y, 2))

def RemoveShot(shot):
    player.remove(shot)
    shots.remove(shot)

def SpawnEnemy():
    enemy_group = displayio.Group(scale=1, x=random.randint(10, display.width-10), y=0)
    enemy_area = label.Label(terminalio.FONT, text="X", color=0xFFFFFF)
    enemy_group.append(enemy_area)
    player.append(enemy_group)
    enemies.append(enemy_group)

def RemoveEnemy(enemy):
    player.remove(enemy)
    enemies.remove(enemy)

# Gameloop
while(not game_over):
    time_since_shot = time_since_shot + frame_sleep
    time_since_enemy = time_since_enemy + frame_sleep
    direction = 0
    if BTN_X.value == False and player_group.x > 5:
        direction = -1
    if BTN_Y.value == False and player_group.x < display.width - 5:
        direction = 1
    if BTN_B.value == False:
        if(time_since_shot >= shot_timeout and len(shots) < max_shots):
            Shoot()
            time_since_shot = 0
    player_group.x = player_group.x + direction
    MoveShots()

    # Test if enemy crosses bottom line
    if(MoveEnemies()):
        lives = lives - 1
        lives_string = ""
        while len(lives_string) < lives:
            lives_string = lives_string + "A"
        lives_area.text = lives_string
        if(lives < 1):
            gameover_group = displayio.Group(scale=1, x=int(display.width * 0.5), y=int(display.height * 0.5))
            gameover_area = label.Label(terminalio.FONT, text="GAME OVER", color=0xFFFFFF)
            gameover_group.append(gameover_area)
            player.append(gameover_group)
            player.remove(player_group)
            game_over = True

    # Test if we should spawn a new enemy
    if(time_since_enemy >= enemy_timeout):
        time_since_enemy = 0
        SpawnEnemy()
        if(enemy_timeout > enemy_spawn_minimum_time):
            enemy_timeout = enemy_timeout * enemy_spawn_multiplier
    time.sleep(frame_sleep)

time.sleep(2)
