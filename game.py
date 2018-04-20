"""
This is an experiment by Bradley Robinson

I want to create a game that is episodic in nature, but without a narrative thread that connects each episode.
In other words, I want an engine that allows for short story type games that share mechanics

"""
import random, sys
import pygame
import pygame.midi
import pygame.mixer
import music
from game_state import ColorChanger
from game_sprites import Player, Explosion
from level import Text, opposite_color

pygame.init()
pygame.midi.init()
pygame.mixer.init()
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
note_choice = [70, 72, 75, 77, 75, 73, 72, 80, 82, 90, 97, 96]
random_player = music.Musical(note_choice, modifier=music.shuffle_notes)
# TODO: this is for experimentation, please move this somewhere else
# TODO: have a message data type that is customizable
messages = [' ', 'hello?', ' ', 'hello?', ' ',
            "hi!", ' ', "hello?", ' ', "anyone?",
            "anyone?"]
first_text = Text(24, messages, size, True)
hello_wav = pygame.mixer.Sound("hello.wav")

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
        if frames % 38 == 0:
            random_player.play_note(midi_player, instrument=random.randint(0, 12))
    return direction


def start_game():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return True
    return False


def generate_controlled_explosion(location, color):
    return Explosion(location, size, random.randint(10, 50), color)

def generate_random_explosion():
    return Explosion((random.randint(10, size[0]-10),
                      random.randint(10, size[1]-10)), size,
                     color=[random.randint(0, 254) for _ in range(3)])

steady_sequence = music.create_repetitive_chords([[63, 65], [63,66,69], [63, 65, 68], [63, 65, 68, 70]], 5)
steady_player = music.Musical(steady_sequence, modifier=music.reverse_notes)

volume = 0.1
echo_sound = pygame.mixer.Sound("stretchedecho.ogg")
pygame.mixer.set_num_channels(12)
echo_sound.set_volume(0.1)
echo_sound.play(20)
change_text_counter = 0
change_sound_counter = 0
change_sound_max = 580
current_text_color = (0, 0, 0)
explosions = []
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
        player.move(movement[0], movement[1], size=size, change_by=0)
        player.draw(screen)
        frames += 1
        change_text_counter += 1
        change_sound_counter += 1
        if frames >= 61:
            steady_player.play_notes(midi_player, 8)
            explosions.append(generate_controlled_explosion(
                player.location, player.color.get_colors()
            ))
            frames = 0
        if change_text_counter >= 481:
            change_text_counter = 0
            current_text_color = opposite_color(background.get_colors())
            first_text.render(current_text_color, screen, True)
            explosions.append(generate_random_explosion())
        else:
            first_text.render(current_text_color, screen, False)
        if change_sound_counter >= change_sound_max:
            if volume < 1.0:
                volume += .05
            echo_sound.set_volume(volume)
            hello_wav.play(fade_ms=100)
            hello_wav.set_volume(volume)
            if change_sound_max > 30:
                change_sound_max -= 30
            change_sound_counter = 0

        for explosion in explosions:
            explosion.draw(screen)
            if len(explosion.boxes) == 0:
                explosions.remove(explosion)

        pygame.display.flip()
