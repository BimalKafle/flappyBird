import sys
import random
import pygame
from flappy.player import Player
from flappy.pipe import Pipe
from flappy.base import Base
from flappy.bird_agent import BirdAgent
from flappy.config import (
    FPS,
    SCREENWIDTH,
    SCREENHEIGHT,
    PLAYER_START_X,
    PLAYER_START_Y,
    PIPE_DISTANCE_X,
    GROUNDY
)

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Flappy Bird")
        self.clock=pygame.time.Clock()
        self.screen=pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))

        self.sprites=self.load_sprites()
        self.sounds=self.load_sounds()

        self.player=None
        self.base=None
        self.pipes=[]
        self.score=0



    def load_sprites(self):
        return {
            'numbers':tuple(
                pygame.image.load(f'gallery/sprites/{i}.png').convert_alpha() for i in range(10)
            ),
            'message':pygame.image.load('gallery/sprites/welcome.png').convert_alpha(),
            'base':pygame.image.load('gallery/sprites/base.png').convert_alpha(),
            'pipe': (
                pygame.transform.rotate(pygame.image.load('gallery/sprites/pipe.png').convert_alpha(), 180),
                pygame.image.load('gallery/sprites/pipe.png').convert_alpha()
            ),
            'background': pygame.image.load('gallery/sprites/background.png').convert(),
            'player': pygame.image.load('gallery/sprites/bird.png').convert_alpha()
        }
    
    def load_sounds(self):
         return {
            'die': pygame.mixer.Sound('gallery/audio/die.wav'),
            'hit': pygame.mixer.Sound('gallery/audio/hit.wav'),
            'point': pygame.mixer.Sound('gallery/audio/point.wav'),
            'swoosh': pygame.mixer.Sound('gallery/audio/swoosh.wav'),
            'wing': pygame.mixer.Sound('gallery/audio/wing.wav')
        }
    
    def spawn_pipe(self, offset_x=0):
        
        new_pipe_x = SCREENWIDTH + offset_x
        return Pipe(new_pipe_x, sprites=self.sprites)
    
    def reset(self):
        self.player = Player(PLAYER_START_X, PLAYER_START_Y, sprites=self.sprites, sounds=self.sounds)
        self.base = Base(sprites=self.sprites)

        first_pipe = self.spawn_pipe(offset_x=200)
        second_pipe = self.spawn_pipe(offset_x=200 + PIPE_DISTANCE_X)

        self.pipes = [first_pipe, second_pipe]

        self.score = 0

    def welcome_screen(self):
        player_x=PLAYER_START_X
        player_y=PLAYER_START_Y
        message_x=(SCREENWIDTH-self.sprites['message'].get_width())/2
        message_y=SCREENHEIGHT*0.13

        while True:
            for event in pygame.event.get():
                if(event.type==pygame.QUIT or (event.type==pygame.KEYDOWN and event.key == pygame.K_ESCAPE)):
                     pygame.quit()
                     sys.exit()
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_UP):
                    return 
            self.screen.blit(self.sprites['background'], (0, 0))
            self.screen.blit(self.sprites['message'], (message_x, message_y))
            self.screen.blit(self.sprites['base'], (0, GROUNDY))
            self.screen.blit(self.sprites['player'], (player_x, player_y))

            pygame.display.update()
            self.clock.tick(FPS)

    def run(self):
        
        while True:
            self.welcome_screen()
            self.reset()
            self.main_game()

    def game_over_screen(self):
        game_over_font = pygame.font.SysFont('Arial', 50)
        restart_font = pygame.font.SysFont('Arial', 25)
        
        game_over_surface = game_over_font.render('Game Over!', True, (255, 0, 0))
        restart_surface = restart_font.render('Press Space to Restart', True, (255, 255, 255))
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    return  # Restart the game
            
            self.screen.blit(self.sprites['background'], (0, 0))
            self.base.draw(self.screen)
            self.player.draw(self.screen)

            # Draw game over messages
            self.screen.blit(game_over_surface, (SCREENWIDTH // 2 - game_over_surface.get_width() // 2, SCREENHEIGHT // 3))
            self.screen.blit(restart_surface, (SCREENWIDTH // 2 - restart_surface.get_width() // 2, SCREENHEIGHT // 2))

            pygame.display.update()
            self.clock.tick(FPS)

    def main_game(self):
        
        while True:
            self.handle_events()
            self.update_game_state()
            self.draw()

            pygame.display.update()
            self.clock.tick(FPS)

            if self.check_collision():
                self.sounds['hit'].play()
                self.game_over_screen()
                return  # Exit the current game and show welcome screen again

    def handle_events(self):
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_UP):
                self.player.flap()

    def update_game_state(self):
        self.player.move()
        self.base.move()

        for pipe in self.pipes:
            pipe.move()

        # Get the last pipe in the list
        last_pipe = self.pipes[-1]

        # Check if the last pipe has moved far enough to spawn a new one
        if last_pipe.x < SCREENWIDTH - PIPE_DISTANCE_X:
            new_pipe = self.spawn_pipe(offset_x=0)  # Spawn just off the right edge
            self.pipes.append(new_pipe)

        # Remove the pipe if it's off-screen
        if self.pipes[0].is_off_screen():
            self.pipes.pop(0)

        self.update_score()

    def update_score(self):
        player_mid_x=self.player.x+self.sprites['player'].get_width()/2

        for pipe in self.pipes:
            pipe_mid_x=pipe.x+self.sprites['pipe'][0].get_width()/2
            if(pipe_mid_x<=player_mid_x<pipe_mid_x+4):
                self.score+=1
                self.sounds['point'].play()

    def check_collision(self):
        
        player_rect = self.player.get_rect()

        # Ground and ceiling collision
        if self.player.y > GROUNDY - 25 or self.player.y < 0:
            return True

        # Pipe collision
        for pipe in self.pipes:
            if player_rect.colliderect(pipe.get_upper_rect()) or player_rect.colliderect(pipe.get_lower_rect()):
                return True

        return False

    def draw(self):
       
        self.screen.blit(self.sprites['background'], (0, 0))

        for pipe in self.pipes:
            pipe.draw(self.screen)

        self.base.draw(self.screen)
        self.player.draw(self.screen)
        
        # Draw score
        score_str = str(self.score)
        total_width = 0
        number_height = self.sprites['numbers'][0].get_height()

        # Calculate total width of the score to center it
        for digit in score_str:
            total_width += self.sprites['numbers'][int(digit)].get_width()

        x_offset = (SCREENWIDTH - total_width) / 2

        for digit in score_str:
            digit_surface = self.sprites['numbers'][int(digit)]
            self.screen.blit(digit_surface, (x_offset, SCREENHEIGHT * 0.12))
            x_offset += digit_surface.get_width()


    def check_collision_single(self, player, pipes):
        player_rect = player.get_rect()

        # Ground and ceiling collision
        if player.y > GROUNDY - 25 or player.y < 0:
            return True

        # Pipe collision
        for pipe in pipes:
            if player_rect.colliderect(pipe.get_upper_rect()) or player_rect.colliderect(pipe.get_lower_rect()):
                return True

        return False


    def run_generation(self, population_size):
        agents = [BirdAgent() for _ in range(population_size)]
        birds = [Player(PLAYER_START_X, PLAYER_START_Y, sprites=self.sprites, sounds=self.sounds) for _ in agents]
        
        base = Base(sprites=self.sprites)
        pipes = [self.spawn_pipe(offset_x=200), self.spawn_pipe(offset_x=200 + PIPE_DISTANCE_X)]
        
        alive_agents = population_size
        generation_score = 0
        
        while alive_agents > 0:
            # ✅ Process events (MUST run to prevent freezing)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            # ✅ Loop through agents
            for i, agent in enumerate(agents):
                if not agent.alive:
                    continue  # Skip dead birds
                
                # ✅ Get the next pipe for the bird
                next_pipe = pipes[0] if pipes[0].x + self.sprites['pipe'][0].get_width() >= birds[i].x else pipes[1]
                pipe_gap_top = next_pipe.upper_y + self.sprites['pipe'][0].get_height()
                pipe_gap_bottom = next_pipe.lower_y
                pipe_gap_center = (pipe_gap_top + pipe_gap_bottom) / 2

                # ✅ Normalize inputs
                inputs = [
                    birds[i].y / SCREENHEIGHT,
                    birds[i].vel_y / 10,
                    (next_pipe.x - birds[i].x) / SCREENWIDTH,
                    pipe_gap_center / SCREENHEIGHT
                ]

                # ✅ Decide if flap
                if agent.decide(inputs):
                    birds[i].flap()

                birds[i].move()

                # ✅ Check collisions
                if self.check_collision_single(birds[i], pipes):
                    agent.alive = False
                    alive_agents -= 1
                else:
                    agent.score += 1
            
            # ✅ Move pipes and base (THIS WAS OUTSIDE THE LOOP)
            base.move()
            for pipe in pipes:
                pipe.move()
            
            # ✅ Add new pipes if needed
            if pipes[-1].x < SCREENWIDTH - PIPE_DISTANCE_X:
                pipes.append(self.spawn_pipe(offset_x=0))
            
            # ✅ Remove off-screen pipes
            if pipes[0].is_off_screen():
                pipes.pop(0)
            
            # ✅ DRAW EVERYTHING (Fixing Black Screen)
            self.screen.blit(self.sprites['background'], (0, 0))

            for pipe in pipes:
                pipe.draw(self.screen)

            base.draw(self.screen)

            # ✅ Draw only alive birds
            for i, bird in enumerate(birds):
                if agents[i].alive:
                    bird.draw(self.screen)

            # ✅ Update the screen (THIS WAS MISSING IN THE LOOP)
            pygame.display.update()
            self.clock.tick(FPS)
        
        # ✅ Assign fitness scores AFTER simulation
        for agent in agents:
            agent.fitness = agent.score  

        return agents  # ✅ Return the agents with their fitness after one generation


    def evolve_population(self, population_size=10, generations=10):
        # ✅ Create initial random population
        agents = [BirdAgent() for _ in range(population_size)]

        # ✅ Loop through multiple generations
        for generation in range(generations):
            print(f"\n=== Generation {generation + 1} ===")

            # ✅ Run one generation and evaluate fitness
            agents = self.run_generation(population_size=population_size)

            # ✅ Sort agents by fitness (best first)
            agents.sort(key=lambda a: a.fitness, reverse=True)

            # ✅ Log best agent info
            best_agent = agents[0]
            print(f"Best Fitness: {best_agent.fitness}")
            print(f"Best Weights: {best_agent.weights}")

            # ✅ Select top performers (elitism)
            survivors = agents[:population_size // 2]  # Keep the top 50%

            # ✅ Create next generation by breeding
            next_generation = survivors.copy()  # Keep the best birds

            while len(next_generation) < population_size:
                # Pick two random parents from survivors
                parent1 = random.choice(survivors)
                parent2 = random.choice(survivors)

                # Create a child through crossover
                child = BirdAgent.crossover(parent1, parent2)

                # Mutate the child to introduce variation
                child.mutate(mutation_rate=0.1)  # Try increasing mutation if they get stuck!

                # Add child to next generation
                next_generation.append(child)

            # ✅ Set up the new generation
            agents = next_generation



    def run_agent(self, agent):
       
        # Initialize the player and game objects
        bird = Player(PLAYER_START_X, PLAYER_START_Y, sprites=self.sprites, sounds=self.sounds)
        base = Base(sprites=self.sprites)
        pipes = [self.spawn_pipe(offset_x=200), self.spawn_pipe(offset_x=200 + PIPE_DISTANCE_X)]

        score = 0
        alive = True

        while alive:
            # Process events (to handle quit)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Get the next pipe (same logic as before)
            next_pipe = pipes[0] if pipes[0].x + self.sprites['pipe'][0].get_width() >= bird.x else pipes[1]
            pipe_gap_top = next_pipe.upper_y + self.sprites['pipe'][0].get_height()
            pipe_gap_bottom = next_pipe.lower_y
            pipe_gap_center = (pipe_gap_top + pipe_gap_bottom) / 2

            # Inputs to the agent (same as before)
            inputs = [
                bird.y / SCREENHEIGHT,
                bird.vel_y / 10,
                (next_pipe.x - bird.x) / SCREENWIDTH,
                pipe_gap_center / SCREENHEIGHT
            ]

            # Let the agent decide whether to flap
            if agent.decide(inputs):
                bird.flap()

            # Move bird, pipes, and base
            bird.move()
            base.move()
            for pipe in pipes:
                pipe.move()

            # Add new pipes if needed
            if pipes[-1].x < SCREENWIDTH - PIPE_DISTANCE_X:
                pipes.append(self.spawn_pipe(offset_x=0))

            # Remove pipes off-screen
            if pipes[0].is_off_screen():
                pipes.pop(0)

            # Check for collision
            if self.check_collision_single(bird, pipes):
                alive = False
                print(f"Final Score: {score}")
                self.sounds['die'].play()
                break

            # Update score
            player_mid_x = bird.x + self.sprites['player'].get_width() / 2
            for pipe in pipes:
                pipe_mid_x = pipe.x + self.sprites['pipe'][0].get_width() / 2
                if pipe_mid_x <= player_mid_x < pipe_mid_x + 4:
                    score += 1
                    self.sounds['point'].play()

            # Draw the screen
            self.screen.blit(self.sprites['background'], (0, 0))

            for pipe in pipes:
                pipe.draw(self.screen)

            base.draw(self.screen)
            bird.draw(self.screen)

            # Draw the score
            score_str = str(score)
            total_width = 0
            for digit in score_str:
                total_width += self.sprites['numbers'][int(digit)].get_width()

            x_offset = (SCREENWIDTH - total_width) / 2

            for digit in score_str:
                digit_surface = self.sprites['numbers'][int(digit)]
                self.screen.blit(digit_surface, (x_offset, SCREENHEIGHT * 0.12))
                x_offset += digit_surface.get_width()

            pygame.display.update()
            self.clock.tick(FPS)
