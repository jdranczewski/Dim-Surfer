import pygame
import math

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
        self.vertices = [[self.x, self.y], [self.x+self.height, self.y], [self.x+self.height, self.y + self.width], [self.x, self.y+self.width]]

    def project(self, normal):
        projected = []
        for vect in self.vertices:
            dp = vect[0] * normal[0] + vect[1] * normal[1]
            projected_v = [normal[0] * dp, normal[1] * dp]
            projected_l = math.sqrt(projected_v[0] ** 2 + projected_v[1] ** 2)
            projected.append(projected_l)
        return [min(projected), max(projected)]

    def draw(self, screen):
        pygame.draw.rect(screen, (0,0,0), [self.x, self.y, self.width, self.height])

class Polygon():
    def __init__(self, vert):
        self.vertices = vert

    def collide(self, player):
        collided = 0
        for i in range(len(self.vertices)):
            nexti = (i+1)%len(self.vertices)
            vector = [self.vertices[nexti][0]-self.vertices[i][0], self.vertices[nexti][1]-self.vertices[i][1]]
            len_v = math.sqrt(vector[0]**2+vector[1]**2)
            unit_v = [vector[0]/len_v, vector[1]/len_v]
            normal = [-unit_v[1], unit_v[0]]
            me_p = self.project(normal)
            player_p = player.project(normal)
            if (me_p[1] < player_p[0]) or (me_p[0]>player_p[1]):
                collided = 0
                break
            else:
                collided = 1
        if collided:
            return (0,255,0)
        else:
            return  (255,255,255)

    def project(self, normal):
        projected = []
        for vect in self.vertices:
            dp = vect[0]*normal[0] + vect[1]*normal[1]
            projected_v = [normal[0]*dp, normal[1]*dp]
            projected_l = math.sqrt(projected_v[0]**2 + projected_v[1]**2)
            projected.append(projected_l)
        return [min(projected), max(projected)]

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
    polygon = Polygon([[100,100],[200,200],[300,100]])

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