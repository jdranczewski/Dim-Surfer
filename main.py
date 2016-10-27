import pygame
import math
import time


class Player():
    def __init__(self, w, h):
        self.x = 0
        self.y = 0
        self.width = w
        self.height = h
        self.vertices = []

    def update(self, x, y):
        self.x = x
        self.y = y
        # We need to have a list off all the player's corners for the projection process
        self.vertices = [[self.x, self.y], [self.x+self.height, self.y], [self.x+self.height, self.y + self.width], [self.x, self.y+self.width]]

    def project(self, normal):
        # Comments to the projection process are placed in the Polygon class
        projected = []
        for vect in self.vertices:
            dp = vect[0] * normal[0] + vect[1] * normal[1]
            projected_v = [normal[0] * dp, normal[1] * dp]
            projected_l = math.sqrt(projected_v[0] ** 2 + projected_v[1] ** 2)
            sign_p = projected_v[0] * normal[0] + projected_v[1] * normal[1]
            projected.append(math.copysign(projected_l, sign_p))
        return [min(projected), max(projected), sign_p]

    def draw(self, screen):
        pygame.draw.rect(screen, (0,0,0), [self.x, self.y, self.width, self.height])

class Polygon():
    def __init__(self, vert):
        self.vertices = vert

    def collide(self, player):
        start = time.clock()
        # We check whether the player is colliding with the polygon
        collided = 0
        checked = []
        # We check every face
        for i in range(len(self.vertices)):
            nexti = (i+1) % len(self.vertices)
            # Using vector substraction we obtain the vector representing the face...
            vector = [self.vertices[nexti][0]-self.vertices[i][0], self.vertices[nexti][1]-self.vertices[i][1]]
            # ...its lenght...
            len_v = math.sqrt(vector[0]**2+vector[1]**2)
            # ... and convert it to a unit vector
            unit_v = [vector[0]/len_v, vector[1]/len_v]
            # Then we calculate the vector perpendicular to it, which represents the normal axis
            normal = [-unit_v[1], unit_v[0]]
            checked.append(normal)
            # We project sprites onto the axis
            me_p = self.project(normal)
            player_p = player.project(normal)
            # And check for overlap
            if (me_p[1] < player_p[0]) or (me_p[0]>player_p[1]):
                collided = 0
                # Thanks to the rules of the Separating Axes Theorem
                # we can stop checking when there is no overlap on at least one of the axes
                break
            else:
                collided = 1
        # We return the correct screen colour
        print(time.clock()-start)
        if collided:
            return (0,255,0)
        else:
            return  (255,255,255)

    def project(self, normal):
        projected = []
        # We project every vortex onto the normal vector
        for vect in self.vertices:
            dp = vect[0]*normal[0] + vect[1]*normal[1]
            projected_v = [normal[0]*dp, normal[1]*dp]
            projected_l = math.sqrt(projected_v[0]**2 + projected_v[1]**2)
            # We need to calculate the dot product of the projected vector and the normal vector,
            # because the length of the projected vector will always be positive,
            # and we want it to be negative if the projected vector faces in the opposite direction
            sign_p = projected_v[0] * normal[0] + projected_v[1] * normal[1]
            projected.append(math.copysign(projected_l, sign_p))
        # We return the min and max vector length - the boundaries of the projection
        return [min(projected), max(projected), sign_p]

    def draw(self, screen):
        pygame.draw.polygon(screen, (255,0,0), self.vertices)

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
    player = Player(20,20)
    polygon = Polygon([[100,100],[100,200],[200,200]])

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
        player.update(mouse_x, mouse_y)
        colour = polygon.collide(player)

        # Drawing
        screen.fill(colour)
        polygon.draw(screen)
        player.draw(screen)

        # Update the screen
        pygame.display.flip()

        # Set the maximum framerate to 60fps
        clock.tick(60)

    # Close the window
    pygame.quit()


if __name__ == "__main__":
    main()