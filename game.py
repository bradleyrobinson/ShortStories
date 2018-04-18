"""
This is an experiment by Bradley Robinson

I want to create a game that is episodic in nature, but without a narrative thread that connects each episode.
In other words, I want an engine that allows for short story type games that share mechanics

"""
from collections import deque
import random, sys
import pygame
import pygame.midi
from game_state import ColorChanger
from game_sprites import Player

pygame.init()
pygame.midi.init()
midi_player = pygame.midi.Output(0)

size = (480, 480)
screen = pygame.display.set_mode(size)
BLACK = (0, 0, 0)
add_color = [True, False, False]
increase = 1
clock = pygame.time.Clock()
background = ColorChanger()
player = Player()
direction = [0, 0]
frames = 0

# TODO: Move this where it makes sense
right_down = 0
left_down = 0
up_down = 0
down_down = 0
def move_player():
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                direction[0] = 0
            if event.key == pygame.K_RIGHT:
                direction[0] = 0
            if event.key == pygame.K_UP:
                direction[1] = 0
            if event.key == pygame.K_DOWN:
                direction[1] = 0
        # TODO: figure out how to make sure it always works properly
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                direction[0] = -2
            if event.key == pygame.K_RIGHT:
                direction[0] = 2
            if event.key == pygame.K_UP:
                direction[1] = -2
            if event.key == pygame.K_DOWN:
                direction[1] = 2
    if direction[0] != 0 or direction[1] != 0:
        play_random_note()
    return direction

def start_game():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return True
    return False

note_choice = [70, 72, 75, 77, 75, 73, 72, 80, 82, 90, 97, 96]
note_queue = deque(note_choice)
def play_random_note():
    try:
        if frames % 40 == 0:
            midi_player.set_instrument(random.randint(0, 12))
            note = note_queue.popleft()
            midi_player.note_on(note, 127)
    except:
        midi_player.note_on(random.choice(note_choice), 127)

full_sequence = []
for i in range(13):
    if i > 8:
        full_sequence.append([63, 65, 68])
    elif i > 4:
        full_sequence.append([63, 66, 69])
    else:
        full_sequence.append([63])

song_queue = deque(full_sequence)
current_instrument = 8
def play_steady_note():
    midi_player.set_instrument(current_instrument)
    notes = song_queue.popleft()
    for note in notes:
        midi_player.note_on(note, 127)
    if len(song_queue) == 0:
        return True
    return False

started = False
while 1:
    if not started:
        started = start_game()
        screen.fill(background.get_colors())
    else:
        direction = move_player()
        clock.tick(61)
        background.change_color()
        screen.fill(background.get_colors())
        movement = move_player()
        player.move(movement[0], movement[1], size, frames)
        player.draw(screen)
        pygame.display.flip()
        frames += 1
        if len(note_queue) == 0:
            random.shuffle(note_choice)
            note_queue = deque(note_choice)
        if frames >= 61:
            if play_steady_note():
                full_sequence.reverse()
                song_queue = deque(full_sequence)
            frames = 0
