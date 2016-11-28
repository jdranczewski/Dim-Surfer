import pygame
import math
import time

class Player():
    def __init__(self, w, h):
        self.x = 0
        self.y = 0
        self.x_speed = 0
        self.y_speed = 0
        self.acceleration = 0.3
        self.decceleration = 0.95
        self.width = w
        self.height = h
        self.vertices = [[self.x, self.y], [self.x + self.height, self.y], [self.x + self.height, self.y + self.width],
                         [self.x, self.y + self.width]]

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), [self.x, self.y, self.width, self.height])

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

    def update(self, mouse_z):
        diff = mouse_z-self.z
        if abs(diff)>50:
            diff = 50*abs(diff)/diff
        self.z += diff*0.1

    def draw(self, screen):
        drawing = self.data[math.floor(self.z)]
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
    player = Player(20, 20)
    x_speed = 0
    y_speed = 0

    # -------- Main Program Loop -----------
    while not done:
        # Event Processing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_speed = -1
                elif event.key == pygame.K_RIGHT:
                    x_speed = 1
                elif event.key == pygame.K_UP:
                    y_speed = -1
                elif event.key == pygame.K_DOWN:
                    y_speed = 1
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                    y_speed = 0
                elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_speed = 0
        pos = pygame.mouse.get_pos()
        mouse_x = pos[0]
        mouse_y = pos[1]

        # Game logic
        level.update(mouse_y)

        # Drawing
        screen.fill((255,255,255))
        level.draw(screen)
        player.draw(screen)

        # Update the screen
        pygame.display.flip()

        # Set the maximum framerate to 60fps
        clock.tick(60)

    # Close the window
    pygame.quit()


if __name__ == "__main__":
    main()