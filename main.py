import pygame
import math
import time


class Level():
    def __init__(self, name):
        self.name = name
        self.data = self.obtain()
        self.z = 0

    def obtain(self):
        data = [[[]]]
        polygonI = 0
        zI = 0
        with open('level_data/' + self.name + ".txt", 'r') as f:
            for line in f:
                if line == "#\n":
                    data[zI].pop()
                    data.append([[]])
                    zI += 1
                    polygonI = 0
                elif line == "\n":
                    data[zI].append([])
                    polygonI += 1
                else:
                    data[zI][polygonI].append([float(x) for x in line.split(" ")])
            data.pop()
        f.closed
        return data

    def draw(self, screen, z):
        self.z = z
        drawing = self.data[self.z]
        for polygon in drawing:
            pygame.draw.polygon(screen, (255, 0, 0), polygon)

def main():
    pygame.init()

    # Set the width and height of the screen [width,height]
    size = [500, 500]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("My Game")

    # Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # Create sprites
    level = Level("workfile")
    print(len(level.data[354]))

    # -------- Main Program Loop -----------
    while not done:
        # Event Processing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        pos = pygame.mouse.get_pos()
        mouse_x = pos[0]
        mouse_y = pos[1]

        # Game logic

        # Drawing
        screen.fill((255,255,255))
        level.draw(screen, mouse_y)

        # Update the screen
        pygame.display.flip()

        # Set the maximum framerate to 60fps
        clock.tick(60)

    # Close the window
    pygame.quit()


if __name__ == "__main__":
    main()