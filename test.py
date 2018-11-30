import pygame
import synthEngine as se
from synthEngine import Note


mySynth = se.synth() # initialize the synth / makes new synth object
pygame.init()
width, height = (200, 300)
screen = pygame.display.set_mode((width, height))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (30, 30, 30)


# se.synth(5) --> makes a synth object with 5 oscillators
# defaults to 2 if no parameters ar given
mySynth.sources[0]  # each oscillator can be accessed through array
mySynth.sources[0].form = se.Wave.SAW  # can either be saw, sin, or square
mySynth.sources[1].play(Note.C, 2)  # play raw oscilliscope sound


def loop():
    # The button is just a rect.
    button = pygame.Rect(0, 100, 200, 200)
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            # This block is executed once for each MOUSEBUTTONDOWN event.
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mySynth.play(Note.A)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mySynth.release(Note.A)

        screen.fill(WHITE)
        pygame.draw.rect(screen, GRAY, button)
        pygame.display.update()


loop()
pygame.quit()
