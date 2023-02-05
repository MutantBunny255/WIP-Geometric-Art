import pygame
import pygame.gfxdraw
import math
import time
import random

pygame.init()
#1200, 750
winW, winH = 1200, 750
win = pygame.display.set_mode((winW, winH), flags=pygame.SCALED, vsync=1)
surfaceW, surfaceH = winW*2, winH*2
surface = pygame.Surface((surfaceW, surfaceH))
fps = 60
layers = []


def addVect(vect1, vect2):
    return (vect1[0] + vect2[0], vect1[1] + vect2[1])

def subVect(vect1, vect2):
    return (vect1[0] - vect2[0], vect1[1] - vect2[1])

def vectLen(vect):
    return math.sqrt(vect[0]**2 + vect[1]**2)

def scaleVect(num, vect):
    return((vect[0]*num, vect[1]*num))

def multiplyVect(vect1, vect2):
    return((vect1[0]*vect2[0], vect1[1]*vect2[1]))

def rotateVect(angle, vect):
    return (vect[0]*math.cos(angle) - vect[1]*math.sin(angle), vect[0]*math.sin(angle) + vect[1]*math.cos(angle))
 
#allign vector to an imagindary grid composed of parallelograms with width of ihat and height of jhat
#also vector is positioned relative to the origin (in this case the center of the screen 350, 350)
def allignVect(vect, ihat, jhat, origin):
    return addVect((vect[0]*ihat[0] + vect[1]*jhat[0], vect[0]*ihat[1] + vect[1]*jhat[1]), origin)


class shape:
    #how a "shape" looks like
    #[[(x1, y1), (x2, y1), (x3, y3), ... ] , (R, G, B)]
    def __init__(self, points, color):
        self.points = points
        self.color = color

    #takes every point of the shape, rotates it around the (0,0), then moves it to its position
    def place(self, pos, angle):
        POINTS = []

        for point in self.points:
            POINTS.append(addVect(rotateVect(angle, point), pos))

        SHAPE = [POINTS, self.color]
        return SHAPE


    #circular place
    def circlePlace(self, layer, center, radius, divide):
        angle = 2*math.pi/divide
        theta = 0
        #figure out a "shift" value for when "divide" is odd and want to retain symmetry across the y-axis
        for i in range(divide):
            shapeCenter = addVect(center, (math.cos(theta)*radius, math.sin(theta)*radius))
            #return self.place(shapeCenter, theta)
            #cant return without exiting func, wa wa waa
            layer.vectors.append(self.place(shapeCenter, theta))
            theta += angle
        
            

class layer:
    def __init__(self, ihat, jhat, origin, vectors):
        self.ihat, self.jhat = ihat, jhat
        self.origin = origin
        self.vectors = vectors
        layers.append(self)

    def gridLines(self, color):
        #I just randomly chose 25
        amount = 25
        for y in range(-amount, amount):
            self.vectors.append([[(-amount, y), (amount, y)], color])
        for x in range(-amount, amount):
            self.vectors.append([[(x, -amount), (x, amount)], color])        

    def spin(self, clock, speed):
        self.ihat = rotateVect(speed, self.ihat)
        self.jhat = rotateVect(speed, self.jhat)

    #KEEP SIN GROW SPEED AT VALUES AROUND 0.01 (radians suck)
    def sinGrow(self, clock, amplitude):
        while amplitude >= 0.1:
            amplidute /= 10
        self.ihat = scaleVect(1 + math.sin(clock)*amplitude, self.ihat)
        self.jhat = scaleVect(1 + math.sin(clock)*amplitude, self.jhat)

    def draw(self):
        for shape in self.vectors:
            POINTS = []
            for point in shape[0]:
                POINTS.append(allignVect(point, self.ihat, self.jhat, self.origin))

            if len(shape[0]) > 2:
                pygame.gfxdraw.filled_polygon(surface, POINTS, shape[1])
            elif len(shape[0]) == 2:
                pygame.draw.line(surface, shape[1], POINTS[0], POINTS[1], 1)
            elif len(shape[0]) == 1:
                pygame.draw.circle(surface, shape[1], POINTS[0], 5)

    def paste(self, layer):
        self.ihat = addVect(self.ihat, layer.ihat)
        self.jhat = addVect(self.jhat, layer.jhat)
        print(addVect(self.ihat, layer.ihat))

def main():
    #create different shapes [[(point1), (point2), (point3)], (R, G, B)]
    point = shape([(0, 0)], (100, 0, 0))
    square = shape([(1.5, 1.5), (1.5, -1.5), (-1.5, -1.5), (-1.5, 1.5)], (250, 0, 0))
    triangle = shape([(-0.433, 0), (0.433, -0.5), (0.433, 0.5)], (100, 200, 100))
    diamond1 = shape([(-1, 0), (0, -0.5), (1, 0),(0, 0.5)], (150, 20, 20))
    diamond2 = shape([(-1.2, 0), (0, -0.7), (1.2, 0),(0, 0.7)], (100, 30, 50))
    diamond3 = shape([(-1.3, 0), (0, -0.8), (1.3, 0),(0, 0.8)], (60, 40, 70))
    diamond4 = shape([(-1.4, 0), (0, -0.9), (1.4, 0),(0, 0.9)], (30, 10, 60))

##    #TESTING LAYER PASTE
##    layer0 = layer((20, 0), (0, 20), (surfaceW/2, surfaceH/2), [])
##    layer1 = layer((20, 0), (0, 20), (surfaceW/2, surfaceH/2), [])
##
##    layer0.vectors.append(point.place((3, 3), 0))
##    layer0.vectors.append(point.place((0, 0), 0))
##    layer0.gridLines((100, 0, 0))
##    layer1.gridLines((0, 100, 0))
    
    #cool red-purple gradient art shapes and layers
    layer1 = layer((40, 0), (0, 40), (surfaceW/2, surfaceH/2), [])
    layer2 = layer((60, 0), (0, 60), (surfaceW/2, surfaceH/2), [])
    layer3 = layer((80, 0), (0, 80), (surfaceW/2, surfaceH/2), [])
    layer4 = layer((100, 0), (0, 100), (surfaceW/2, surfaceH/2), [])
    layer0 = layer((20, 0), (0, 20), (surfaceW/2, surfaceH/2), [])

    layer0.vectors.append(square.place((0, 0), 0))
    layer0.vectors.append(square.place((0, 0), math.pi/4))
    layer0.vectors.append(point.place((0, 0),0))
    #layer0.gridLines((250, 0, 0))

    diamond1.circlePlace(layer1, (0, 0), 1, 4)
    layer1.gridLines((150, 20, 20))
    diamond2.circlePlace(layer2, (0, 0), 2, 8)
    layer2.gridLines((100, 30, 50)) 
    diamond3.circlePlace(layer3, (0, 0), 3, 12)
    layer3.gridLines((60, 40, 70)) 
    diamond4.circlePlace(layer4, (0, 0), 4, 16)
    layer4.gridLines((30, 10, 60))
    
    loop = True
    clock= 0
    
    while loop:
        clock += 1/fps

        surface.fill((255, 255, 255))

        #Matrix transformations

##        #TEST LAYER PASTE
##        #layer1.paste(layer0)
##        layer0.spin(clock, 0.01)
##        layer1.origin = allignVect(layer1.origin, layer0.ihat, layer0.jhat, (winW, winH))

        #cool red-purple gradient art transformations
        layer0.sinGrow(clock, 0.005)
        layer0.spin(clock, 0.01)
        layer1.sinGrow(clock, 0.01)#0.01
        layer1.spin(clock, 0.015)
        layer2.sinGrow(clock, 0.015)#0.015
        layer2.spin(clock, 0.02)
        layer3.sinGrow(clock, 0.02)#0.02
        layer3.spin(clock, 0.025)
        layer4.sinGrow(clock, 0.025)#0.025
        layer4.spin(clock, 0.03)
        
        for l in layers:
            l.draw()

        #let the mouse control where the camera is.
        cameraPos = addVect(scaleVect(-1, pygame.mouse.get_pos()), (0, 0))
        win.blit(surface, cameraPos)
        
        pygame.time.Clock().tick(fps)
        pygame.display.update()       

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False
                

    pygame.quit()
    

if __name__ == "__main__":
    main()
