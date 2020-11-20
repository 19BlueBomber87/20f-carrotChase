# EG16-11-complete game
#ROB MILLS CHAPTER 15

import pygame

import random

import sys

class Sprite:
    '''
    A sprite in the game. Can be sub-classed
    to create sprites with particular behaviours
    '''
    def __init__(self, image, game):
        '''
        Initialize a sprite
        image is the image to use to draw the sprite
        default position is origin (0,0)
        game is the game that contains this sprite
        '''
        self.image = image
        self.position = [0, 0]
        self.game = game
        self.reset()

    def update(self):
        '''
        Called in the game loop to update
        the status of the sprite.
        Does nothing in the super class
        '''
        pass

    def draw(self):
        '''
        Draws the sprite on the screen at its
        current position
        '''
        self.game.surface.blit(self.image, self.position)

    def intersects_with(self,target):
        '''
        Returns True if this sprite intersects with
        the one supplied as a parameter
        '''
        max_x = self.position[0] + self.image.get_width()
        max_y = self.position[1] + self.image.get_height()

        target_max_x = target.position[0] + target.image.get_width()
        target_max_y = target.position[1] + target.image.get_height()

        if max_x < target.position[0]:
            return False

        if max_y < target.position[1]:
            return False
        
        if self.position[0] > target_max_x:
            return False
        
        if self.position[1] > target_max_y:
            return False
        
        # if we get here the sprites intersect
        return True

    def reset(self):
        '''
        Called at the start of a new game to
        reset the sprite
        '''
        pass


class Hare(Sprite):
    '''
    Player controlled Hare object that can be steered
    around the screen by the player
    '''

    def reset(self):
        '''
        Reset the hare position and stop any movement
        Set the movement speed back to the start speed
        '''
        self.movingUp = False
        self.movingDown = False
        self.movingLeft = False
        self.movingRight = False
        self.position[0] = (self.game.width - self.image.get_width())/2
        self.position[1] = (self.game.height - self.image.get_height())/2
        self.movement_speed=[20,20]
        
    def update(self):
        '''
        Update the hare position and then stop it moving off
        the screen.
        '''
        if self.movingUp:
            self.position[1] = self.position[1] - (self.movement_speed[1])
        if self.movingDown:
            self.position[1] = self.position[1] + (self.movement_speed[1])
        if self.movingLeft:
            self.position[0] = self.position[0] - (self.movement_speed[0])
        if self.movingRight:
            self.position[0] = self.position[0] + (self.movement_speed[0])

        if self.position[0] < 0:
            self.position[0]=0
        if self.position[1] < 0:
            self.position[1]=0
        if self.position[0] + self.image.get_width() > self.game.width:
            self.position[0] = self.game.width - self.image.get_width()
        if self.position[1] + self.image.get_height() > self.game.height:
            self.position[1] = self.game.height - self.image.get_height()

        
    def StartMoveUp(self):
        'Start the hare moving up'
        self.movingUp = True
        
    def StopMoveUp(self):
        'Stop the hare moving up'
        self.movingUp = False
        
    def StartMoveDown(self):
        'Start the hare moving down'
        self.movingDown = True
        
    def StopMoveDown(self):
        'Stop the hare moving down'
        self.movingDown = False

    def StartMoveLeft(self):
        'Start the hare moving left'
        self.movingLeft = True
        
    def StopMoveLeft(self):
        'Stop the hare moving left'
        self.movingLeft = False

    def StartMoveRight(self):
        'Start the hare moving right'
        self.movingRight = True
        
    def StopMoveRight(self):
        'Stop the hare moving right'
        self.movingRight = False

class Carrot(Sprite):
    '''
    The carrot provides a target for the hare
    When reset it moves to a different random place
    on the screen
    '''
    def __init__(self, image, game, captured_sound):
        super().__init__(image, game)
        self.captured_sound = captured_sound
        
    def reset(self):
        self.position[0] = random.randint(0,
                self.game.width-self.image.get_width())
        self.position[1] = random.randint(0,
                self.game.height-self.image.get_height())

    def update(self):
        if self.intersects_with(game.hare_sprite):
            self.captured_sound.play()
            self.reset()
            self.game.score += 10 

class Lynx(Sprite):
    def __init__(self, image, game, entry_delay):
        super().__init__(image, game)
        self.entry_delay = entry_delay

    def update(self):

        self.entry_count = self.entry_count + 1
        if self.entry_count < self.entry_delay:
            return
        
        if game.hare_sprite.position[0] > self.position[0]:
            self.x_speed = self.x_speed + self.x_accel
        else:
            self.x_speed = self.x_speed - self.x_accel
        self.x_speed = self.x_speed * self.friction_value
        self.position[0] = self.position[0] + self.x_speed

        if game.hare_sprite.position[1] > self.position[1]:
            self.y_speed = self.y_speed + self.y_accel
        else:
            self.y_speed = self.y_speed - self.y_accel
        self.y_speed = self.y_speed * self.friction_value
        self.position[1] = self.position[1] + self.y_speed
    
        if self.intersects_with(game.hare_sprite):
            self.game.end_game()
    def reset(self):
        self.entry_count = 0
        self.friction_value = 0.99
        self.x_accel = 0.2
        self.y_accel = 0.2
        self.x_speed = 0
        self.y_speed = 0
        self.position = [200, -200]
class HareChase:
    '''
    Plays the amazing carrot chase game
    '''
    
    def display_message(self, message,y_pos):
        '''
        Displays a message on the screen
        The first argument is the message text
        The second argument is the vertical position
        of the text
        The text is drawn centered on the screen
        It is drawn with a black shadow
        '''
        shadow = self.font.render(message,True,(0,0,0))
        text = self.font.render(message,True,(0,0,255))
        text_position = [self.width/2 -text.get_width()/2, y_pos]
        self.surface.blit(shadow,text_position)
        text_position[0] += 2
        text_position[1] += 2
        self.surface.blit(text,text_position)

    def update_game(self):
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return
                elif e.key == pygame.K_UP:
                    self.hare_sprite.StartMoveUp()
                elif e.key == pygame.K_DOWN:
                    self.hare_sprite.StartMoveDown()
                elif e.key == pygame.K_LEFT:
                    self.hare_sprite.StartMoveLeft()
                elif e.key == pygame.K_RIGHT:
                    self.hare_sprite.StartMoveRight()
            elif e.type == pygame.KEYUP:
                if e.key == pygame.K_UP:
                    self.hare_sprite.StopMoveUp()
                elif e.key == pygame.K_DOWN:
                    self.hare_sprite.StopMoveDown()
                elif e.key == pygame.K_LEFT:
                    self.hare_sprite.StopMoveLeft()
                elif e.key == pygame.K_RIGHT:
                    self.hare_sprite.StopMoveRight()

        for sprite in self.sprites:
            sprite.update()


    def draw_game(self):
        for sprite in self.sprites:
            sprite.draw()
        status = 'Score' + str(game.score)
        self.display_message(status,0)

    def start_game(self):
        for sprite in self.sprites:
            sprite.reset()
        self.score = 0
        self.game_running = True
    
    def end_game(self):
        self.game_running = False
        if self.score > self.top_score:
            self.top_score = self.score

    def update_start(self):
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif e.key == pygame.K_RETURN:
                    self.start_game()

    def draw_start(self):
        self.start_background_sprite.draw()
        self.display_message(message='Top Score: ' + str(self.top_score),y_pos=0)
        self.display_message(message='Welcome to Carrot Chase',y_pos=150)
        self.display_message(message='Steer the Snowshoe Hare to',y_pos=250)
        self.display_message(message='Capture the carrots!',y_pos=300)
        self.display_message(message='<@:D BEWARE THE HUNGRY LYNX <@:D',y_pos=350)
        self.display_message(message='Arrow keys to move', y_pos=450)
        self.display_message(message='Press the Enter key to play', y_pos=500)
        self.display_message(message='Press Escape to exit', y_pos=550)

    def play_game(self):
        '''
        Starts the game playing
        Will return when the player exits
        the game.
        '''
        init_result = pygame.init()
        if init_result[1] != 0:
            print('pygame not installed properly')
            return

        self.width = 1400
        self.height = 650
        self.size = (self.width, self.height)

        self.font = pygame.font.Font(None, 60)

        start_background_image = pygame.image.load('startBackground.png')
        self.start_background_sprite = Sprite(image=start_background_image,
                                            game=self)

        self.sprites = []

        self.surface = pygame.display.set_mode(self.size)
        pygame.display.set_caption('Hare Chase')
        background_image = pygame.image.load('background.png')
        self.background_sprite = Sprite(image=background_image,
                                        game=self)

        self.sprites.append(self.background_sprite) # append sprites

        carrot_image = pygame.image.load('carrot.png')
        carrot_eat_sound = pygame.mixer.Sound('crunch.wav')

        
        for i in range(20):
            carrot_sprite = Carrot(image=carrot_image,
                        game=self,captured_sound=carrot_eat_sound)
            self.sprites.append(carrot_sprite) #append sprites

        hare_image = pygame.image.load('hare.png')
        self.hare_sprite = Hare(image=hare_image,
                                        game=self)


        self.sprites.append(self.hare_sprite) #append sprties

        lynx_image = pygame.image.load('lynx.png')

        for entry_delay in range(0,3000,300):
            lynx_sprite= Lynx(image=lynx_image,
                                    game=self,
                                    entry_delay=entry_delay)
            self.sprites.append(lynx_sprite)

        clock = pygame.time.Clock()        
        
        self.score = 0
        self.top_score = 0
        self.end_game()

        self.game_active = True

        while self.game_active:
            clock.tick(60)
            if self.game_running:
                self.update_game()
                self.draw_game()
            else:
                self.update_start()
                self.draw_start()
            pygame.display.flip()


game = HareChase()
game.play_game()
