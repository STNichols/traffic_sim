# -*- coding: utf-8 -*-
"""
Created on Fri Jan  1 16:08:47 2021

@author: Sean
"""

import pygame
import numpy as np
from math import copysign

from car import Car

WHITE_LINE = (255, 255, 255)
YELLOW_LINE = (255, 255, 0)

class TrafficSim:
    """
    Simulation of various traffic interactions and how they propagate at
    scale
    """
    
    def __init__(self):
        """ """
        
        pygame.init()
        pygame.display.set_caption("Traffic Simulator")
        self.width = 1500 # 25 car lengths
        self.height = 300 # 10 car widths
        """
        For instance:
            1, 0.5 is first lane down, back of car touching starting edge
            49, 1.5 is second lane down, front of car touching finishing edge
        """
        
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.ticks = 60
        self.exit = False
        
        # Setup pixel occupation matrix
        self.pom = np.zeros((self.width, self.height))
                
    def run(self):
        """ """
        
        ppu = 30
        
        mcar = Car(1, 0.5)
        
        # Create library of cars that are driving
        car_lib = []
        for cid in np.arange(10):
            car_lib.append(Car(1, 0.5 + cid))

        while not self.exit:
            dt = self.clock.get_time() / 1000

            # Event queue
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True
            
            # User input
            pressed = pygame.key.get_pressed()

            if pressed[pygame.K_UP]:
                if mcar.velocity.x < 0:
                    mcar.acceleration = mcar.brake_deceleration
                else:
                    mcar.acceleration += 1 * dt
            elif pressed[pygame.K_DOWN]:
                if mcar.velocity.x > 0:
                    mcar.acceleration = -mcar.brake_deceleration
                else:
                    mcar.acceleration -= 1 * dt
            elif pressed[pygame.K_SPACE]:
                if abs(mcar.velocity.x) > dt * mcar.brake_deceleration:
                    mcar.acceleration = -copysign(mcar.brake_deceleration, mcar.velocity.x)
                else:
                    mcar.acceleration = -mcar.velocity.x / dt
            else:
                if abs(mcar.velocity.x) > dt * mcar.free_deceleration:
                    mcar.acceleration = -copysign(mcar.free_deceleration, mcar.velocity.x)
                else:
                    if dt != 0:
                        mcar.acceleration = -mcar.velocity.x / dt
            mcar.acceleration = max(-mcar.max_acceleration, min(mcar.acceleration, mcar.max_acceleration))

            if pressed[pygame.K_RIGHT]:
                mcar.steering -= 30 * dt
            elif pressed[pygame.K_LEFT]:
                mcar.steering += 30 * dt
            else:
                mcar.steering = 0
            mcar.steering = max(-mcar.max_steering, min(mcar.steering, mcar.max_steering))

            # Prepare next screen
            self.screen.fill((0, 0, 0))
            
            # Draw traffic lines
            for lane in np.arange(11):
                pygame.draw.line(self.screen, WHITE_LINE,
                                 (0, lane * ppu),
                                 (1500, lane * ppu),
                                 1)
            pygame.draw.line(self.screen, YELLOW_LINE,
                                 (0, self.height / 2),
                                 (1500, self.height / 2),
                                 1)
            
            # Update my car
            mcar.update(dt)
            rotated = pygame.transform.rotate(mcar.image, mcar.angle)
            rect = rotated.get_rect()
            self.screen.blit(rotated, mcar.position * ppu - (rect.width / 2, rect.height / 2))
            
            # Update library of cars
            for car in car_lib:
                car.update(dt)
                rotated = pygame.transform.rotate(car.image, car.angle)
                rect = rotated.get_rect()
                self.screen.blit(rotated, car.position * ppu - (rect.width / 2, rect.height / 2))


            pygame.display.flip()
            self.clock.tick(self.ticks)
            
        pygame.quit()


if __name__ == '__main__':
    ts = TrafficSim()
    ts.run()
