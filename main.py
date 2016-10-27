import pygame

def main():
    pygame.init()

    # Set the width and height of the screen [width,height]
    size = [700, 500]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("My Game")

    # Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # -------- Main Program Loop -----------
    while not done:
        # Event Processing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        # Game logic

        # Drawing
        screen.fill((255, 255, 255))

        # Update the screen
        pygame.display.flip()

        # Set the maximum framerate to 60fps
        clock.tick(60)

    # Close the window
    pygame.quit()


if __name__ == "__main__":
    main()