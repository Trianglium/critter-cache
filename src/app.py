import pygame
import config as gc

from pygame import display, event, image
from time import sleep
from animal import Animal

def find_index(x, y):
    row = y // gc.IMAGE_SIZE
    col = x // gc.IMAGE_SIZE
    index = row * gc.NUM_TILES_SIDE + col
    return index

pygame.init()

display.set_caption("Critter Cache")
screen = display.set_mode((512, 512))
matched = image.load('other_assets/matched.png')


running = True
tiles = [Animal(i) for i in range(0, gc.NUM_TILES_TOTAL)]
current_images = []
score = 0

while running:
    current_events = event.get()

    for e in current_events:
        if e.type == pygame.QUIT:
            running = False

    if e.type == pygame.KEYDOWN:
        if e.key == pygame.K_ESCAPE:
            running = False

    if e.type == pygame.MOUSEBUTTONDOWN:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        index = find_index(mouse_x, mouse_y)
        if index not in current_images:
            current_images.append(index)
        if len(current_images) > 2:
            current_images = []

    screen.fill(gc.BG_DARK)
    total_skipped = 0

    for _, tile in enumerate(tiles):
        image_i = tile.image if tile.index in current_images else tile.box
        if not tile.skip:
            screen.blit(image_i, (tile.col * gc.IMAGE_SIZE + gc.MARGIN, tile.row * gc.IMAGE_SIZE + gc.MARGIN))
        else:
            total_skipped += 1

    display.flip()

    if len(current_images) == 2:
        idx1, idx2 = current_images
        if tiles[idx1].name == tiles[idx2].name:
            tiles[idx1].skip = True
            tiles[idx2].skip = True
            sleep(0.4)
            screen.blit(matched, (0, 0))
            display.flip()
            sleep(0.4)
            current_images = []

        elif tiles[idx1].name != tiles[idx2].name:
            sleep(0.4)
            display.flip()
            current_images = []
            print("Opps! Not a match!")
        display.flip()

    if total_skipped == len(tiles):
        running = False


print("Goodbye")
