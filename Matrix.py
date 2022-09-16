import pygame
import pygame.gfxdraw
import math
import time
import random

pygame.init()
winW, winH = 1200, 750
win = pygame.display.set_mode((winW, winH), flags=pygame.SCALED, vsync=1 )
surface = pygame.Surface((winW, winH))
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
 
#allign vector to an imagindary grid composed of parallelograms with side lenths of ihat and jhat
#also vector is positioned relative to the origin (in this case the center of the screen 350, 350)
def allignVect(vect, ihat, jhat, origin):
    return addVect((vect[0]*ihat[0] + vect[1]*jhat[0], vect[0]*ihat[1] + vect[1]*jhat[1]), origin)


class shape:
    def __init__(self, points, color):
        self.points = points
        self.color = color

    def place(self, pos, angle):
        POINTS = []
        for point in self.points:
            POINTS.append(addVect(rotateVect(angle, point), pos))

        SHAPE = [POINTS, self.color]
        return SHAPE

    def circular(self, layer, center, distance, divide):
        angle = 2*math.pi/divide
        
        for i in range(divide):
            DISTANCE = rotateVect(angle*i, distance)
            layer.vectors.append(self.place(addVect(center, DISTANCE), angle*i))
            #for vector in layer.vectors[-1][0]:
                #vector = addVect(vector, distance)

class layer:
    def __init__(self, ihat, jhat, origin, vectors):
        self.ihat, self.jhat = ihat, jhat
        #the unitX and Y are broken, just keep it square
        self.unitX = self.ihat
        self.unitY = self.jhat
        self.origin = origin
        self.vectors = vectors

    def gridLines(self, color):
        #I just randomly chose 35
        for y in range(-35, 35):
            self.vectors.append([[(-35, y), (35, y)], color])
        for x in range(-35, 35):
            self.vectors.append([[(x, -35), (x, 35)], color])        

    def spin(self, clock, speed):
        self.ihat = rotateVect(speed, self.ihat)
        self.jhat = rotateVect(speed, self.jhat)

    #KEEP SIN GROW SPEED AT VALUES AROUND 0.01
    def sinGrow(self, clock, speed):
        while speed >= 0.1:
            speed /= 10
        self.ihat = scaleVect(1 + math.sin(clock)*speed, self.ihat)
        self.jhat = scaleVect(1 + math.sin(clock)*speed, self.jhat)

    def spinGrow(self, clock, speed):
        self.ihat = scaleVect(1.5 + math.sin(clock), (self.ihat[0]*math.cos(speed) - self.ihat[1]*math.sin(speed), self.ihat[0]*math.sin(speed) + self.ihat[1]*math.cos(speed)))
        self.jhat = scaleVect(1.5 + math.sin(clock), (self.jhat[0]*math.cos(speed) - self.jhat[1]*math.sin(speed), self.jhat[0]*math.sin(speed) + self.jhat[1]*math.cos(speed)))
        
    def draw(self):
        for shape in self.vectors:
            POINTS = []
            for point in shape[0]:
                try: nextPoint = shape[0][shape[0].index(point) + 1]
                except: nextPoint = shape[0][0]
                POINTS.append(allignVect(point, self.ihat, self.jhat, self.origin))

            if len(shape[0]) > 2:
                pygame.gfxdraw.filled_polygon(surface, POINTS, shape[1])
            else:
                pygame.draw.line(surface, shape[1], POINTS[0], POINTS[1], 1)

def main():
    triangle = shape([(0, -0.5), (-0.5, -math.cos(math.pi/6) -0.5), (0.5, -math.cos(math.pi/6) - 0.5)], (100, 200, 100))
    diamond = shape([(0, -1), (-0.4, -1.5), (0, -2), (0.4, -1.5)], (120, 0, 0))
    ihat, jhat = shape([(0, 0), (1, 0)], (255, 0, 0)), shape([(0, 0), (0, 1)], (255, 0, 0))

    layer0 = layer((25, 0), (0, 25), (winW/2, winH/2), [])    
    layer1 = layer((50, 0), (0, 50), (winW/2, winH/2), [])
    layer2 = layer((60, 0), (0, 60), (winW/2, winH/2), [])
    layer3 = layer((70, 0), (0, 70), (winW/2, winH/2), [])

    #layer0.gridLines((0, 100, 0))
    #layer1.gridLines((100, 0 ,0))

    triangle.circular(layer3, (0, 0), (0, -2.1), 15)    
    triangle.circular(layer2, (0, 0), (0, -1.1), 10)
    triangle.circular(layer1, (0, 0), (0, -0.1), 5)
    diamond.circular(layer0, (-10, 0), (0, 0), 10)
    diamond.circular(layer0, (10, 0), (0, 0), 10)
    diamond.circular(layer0, (0, -10), (0, 0), 10)
    diamond.circular(layer0, (0, 10), (0, 0), 10)
    diamond.circular(layer0, (0, 0), (0, -1.5), 20)
    diamond.circular(layer0, (0, 0), (0, -4.5), 30)
    diamond.circular(layer0, (0, 0), (0, -7.5), 40)
    diamond.circular(layer0, (0, 0), (0, -10.5), 50)
    
    loop = True
    clock= 0
    
    while loop:
        clock += 1/fps

        #Matrix transformations
        layer0.sinGrow(clock, 0.005)
        layer0.spin(clock, 0.02)

        layer1.spin(clock, -0.02)
        layer1.sinGrow(clock, 0.005)
        
        layer2.spin(clock, -0.04)
        layer2.sinGrow(clock, 0.005)

        layer3.spin(clock, -0.06)
        layer3.sinGrow(clock, 0.005)

        surface.fill((255, 255, 255))

        layer0.draw()
        layer1.draw()
        layer2.draw()
        layer3.draw()
        
        #pygame.draw.circle(surface, (0, 0, 0), (winW/2, winH/2), 100, 1)
        win.blit(surface, (0, 0))
        pygame.time.Clock().tick(fps)
        pygame.display.update()       

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False
                

    pygame.quit()
    

if __name__ == "__main__":
    main()
