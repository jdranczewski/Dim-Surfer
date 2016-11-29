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

    def update(self, x_speed, y_speed, collided, y_ev):
        self.x_speed += x_speed * self.acceleration
        self.y_speed += 0.1
        if collided and y_speed < 0 and y_ev < 0:
            self.y_speed = -10
        self.x_speed *= self.decceleration
        self.y_speed *= self.decceleration
        self.x += self.x_speed
        self.y += self.y_speed
        # We need to have a list off all the player's corners for the projection process
        self.vertices = [[self.x, self.y], [self.x + self.height, self.y], [self.x + self.height, self.y + self.width],
                         [self.x, self.y + self.width]]

    def collision_displace(self, x, y):
        self.x += x
        self.y += y

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), [self.x, self.y, self.width, self.height])

def project(polygon, normal):
    projected = []
    for vect in polygon:
        dp = vect[0] * normal[0] + vect[1] * normal[1]
        projected_v = [normal[0] * dp, normal[1] * dp]
        projected_l = math.sqrt(projected_v[0] ** 2 + projected_v[1] ** 2)
        sign_p = projected_v[0] * normal[0] + projected_v[1] * normal[1]
        projected.append(math.copysign(projected_l, sign_p))
    return [min(projected), max(projected)]

def calculateEjection(normal, polygon, player, out_v, out_v_val):
    # We calculate projections of both the polygon and the player onto the normal vector
    polygon_p = project(polygon, normal)
    player_p = project(player, normal)
    collided = 0
    # We check whether there is overlap
    if (polygon_p[1] < player_p[0]) or (polygon_p[0] > player_p[1]):
        collided = 0
    else:
        if (polygon_p[1] - player_p[0]) >= 0:
            out_v_val.append(polygon_p[1] - player_p[0])
            out_v.append([(polygon_p[1] - player_p[0]) * normal[0], (polygon_p[1] - player_p[0]) * normal[1]])
        if (polygon_p[0] - player_p[1]) <= 0:
            out_v_val.append(player_p[1] - polygon_p[0])
            out_v.append([(polygon_p[0] - player_p[1]) * normal[0], (polygon_p[0] - player_p[1]) * normal[1]])
        collided = 1
    return collided

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

    def collide(self, player):
        for polygon in self.data[math.floor(self.z)]:
            # We start by assuming that there is no overlap
            collided = 0
            # We create an empty list of ejection vectors
            out_v = []
            # And their values for easy comparision
            out_v_val = []

            # We then calculateEjection() to calculate the ejection vectors.
            # It also returns a boolenan that tells us whether the objects are actually overlaping on that axis
            # We start with the x axis:
            calculateEjection([1,0], polygon, player.vertices, out_v, out_v_val)

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
        collide = level.collide(player)
        # player.collision_displace(collide[1][0], collide[1][1])

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