import terminalio
import displayio
from adafruit_display_text import label
import math
import random

shot_timeout = 0.3
frame_sleep = 0.02
enemy_timeout = 4.0
max_shots = 3
game_over = False;

shots = []
time_since_shot = shot_timeout
enemies = []
time_since_enemy = enemy_timeout
score = 0
lives = 3

about = displayio.Group()
about_group = displayio.Group(scale=1, x=int(display.width*0.5), y=display.height - 20)
about_area = label.Label(terminalio.FONT, text="A", color=0xFFFFFF)
about_group.append(about_area)
about.append(about_group)

score_group = displayio.Group(scale=1, x=0, y=5)
score_area = label.Label(terminalio.FONT, text="{:08d}".format(score), color=0xFFFFFF)
score_group.append(score_area)
about.append(score_group)

lives_group = displayio.Group(scale=1, x=display.width, y=5)
lives_area = label.Label(terminalio.FONT, text="AAA", color=0xFFFFFF, label_direction="RTL")
lives_group.append(lives_area)
about.append(lives_group)

display.show(about)

def UpdateScore(label):
    label.text = "{:08d}".format(score)

def Shoot():
    shot_group = displayio.Group(scale=1, x=about_group.x, y=about_group.y - 3)
    shot_area = label.Label(terminalio.FONT, text="*", color=0xFFFFFF)
    shot_group.append(shot_area)
    about.append(shot_group)
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
                RemoveEnemy(enemy)
                RemoveShot(shot)
                UpdateScore(score_area)
    return lose_life

def DistanceBetweenGroups(a, b):
    return math.sqrt(pow(a.x - b.x, 2) + pow(a.y - b.y, 2))

def RemoveShot(shot):
    about.remove(shot)
    shots.remove(shot)

def SpawnEnemy():
    enemy_group = displayio.Group(scale=1, x=random.randint(10, display.width-10), y=0)
    enemy_area = label.Label(terminalio.FONT, text="X", color=0xFFFFFF)
    enemy_group.append(enemy_area)
    about.append(enemy_group)
    enemies.append(enemy_group)

def RemoveEnemy(enemy):
    about.remove(enemy)
    enemies.remove(enemy)

while(not game_over):
    time_since_shot = time_since_shot + frame_sleep
    time_since_enemy = time_since_enemy + frame_sleep
    direction = 0
    if BTN_X.value == False and about_group.x > 5:
        direction = -1
    if BTN_Y.value == False and about_group.x < display.width - 5:
        direction = 1
    if BTN_B.value == False:
        if(time_since_shot >= shot_timeout and len(shots) < max_shots):
            Shoot()
            time_since_shot = 0
    about_group.x = about_group.x + direction
    MoveShots()
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
            about.append(gameover_group)
            about.remove(about_group)
    if(time_since_enemy >= enemy_timeout):
        SpawnEnemy()
        time_since_enemy = 0
        if(enemy_timeout > 0.8):
            enemy_timeout = enemy_timeout * 0.9
    time.sleep(frame_sleep)
    score = score + 10

time.sleep(2)
