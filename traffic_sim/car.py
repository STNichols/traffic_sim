# -*- coding: utf-8 -*-
"""
Created on Fri Jan  1 16:08:47 2021

@author: Sean
"""

import os
import pygame
from math import sin, radians, degrees
from pygame.math import Vector2

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
CAR_IMAGE_PATH = os.path.join(CURRENT_PATH, "car.png")

class Car:
    """ A car that follows a set of physical laws """
    
    def __init__(
            self,
            x,
            y,
            angle=0.0,
            length=4,
            max_steering=30,
            max_acceleration=10.0,
            image=CAR_IMAGE_PATH
        ):
        """ Create a car """
        
        self.position = Vector2(x, y)
        self.velocity = Vector2(0.0, 0.0)
        self.angle = angle
        self.length = length
        self.max_acceleration = max_acceleration
        self.max_steering = max_steering
        self.max_velocity = 20
        self.brake_deceleration = 50
        self.free_deceleration = 2

        self.acceleration = 0.0
        self.steering = 0.0
        
        self.image = pygame.image.load(image)

    def update(self, dt):
        """ Update the car's physical parameters """
        
        self.velocity += (self.acceleration * dt, 0)
        self.velocity.x = max(-self.max_velocity, min(self.velocity.x, self.max_velocity))

        if self.steering:
            turning_radius = self.length / sin(radians(self.steering))
            angular_velocity = self.velocity.x / turning_radius
        else:
            angular_velocity = 0

        self.position += self.velocity.rotate(-self.angle) * dt
        self.angle += degrees(angular_velocity) * dt
