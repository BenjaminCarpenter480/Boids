


import queue
# import boids_gen
import pygame as pg
from OpenGL.GL import *
import numpy as np
from numpy.linalg import norm

PATH="/tmp/boids"

# DOMAIN = boids_gen.DOMAIN



class BoidImage():
    def __init__(self):
        
        self.vertices = np.array([
            -0.5,-0.5, 0,  1, 0, 0, #X,Y,Z (Norm -1,1), R,G,B 
            0.5, -0.5, 0,  0, 1, 0,
            0.0, 0.5,  0,  0, 0, 1], dtype=np.float32) 
    
        self.vertex_count = 3
        ######Send off the data to the GPU######
        self.vao = glGenVertexArrays(1) #
        glBindVertexArray(self.vao)
        self.vbo = glGenBuffers(1) #Determine the actual buffer of interest 
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo) #Let teh GPU know the specific buffer of interest
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW) #Send the data to the GPU, and what to do with it 
        #Allocate mem on the graphics card
        glEnableVertexAttribArray(0) #Enable the first attribute location
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0)) #Tell the GPU how the attributes are formatted in the vbo
        #Attribute in the buffer -here 0 is position- , Points in attribute, data type, Normalisation by OpenGL, length of each piece of information in the attribute, offset for the first point, e.g. 
        glEnableVertexAttribArray(1) #Enable the second attribute location
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12)) #Tell the GPU how the attributes are formatted in the vbo
        #Attribute in the buffer -here 0 is position- , Points in attribute, data type, Normalisation by OpenGL, length of each piece of information in the attribute, offset for the first point, e.g. 


class Display():


    def __init__(self) -> None:
        pg.init()            #DOMAN, DOMAIN
        pg.display.set_mode((1000, 1000), pg.OPENGL | pg.DOUBLEBUF)
        self.clock = pg.time.Clock()
        glClearColor(0, 0, 0, 1.0)
        self.main_loop() 
        self.pipe = open(PATH, "r")
        self.data = queue.Queue()

    # def update(self, i):
    #     self._update_axis()
    #     while self.data.qsize() == 0:
    #         self.empty_pipe()
    #     data = self.data.get()
    #     for boid in data.split(';')[:-1]:
    #         print(boid)
    #         b=boid[:-1].split(',')
    #         self.ax.quiver(float(b[0]),float(b[1]),float(b[2]),float(b[3]),
    #                     headlength=norm([float(b[2]),float(b[3])]) )
    #     # print("---------LOOPED----------") 
            
            
    # def empty_pipe(self): 
    #     count = 0
    #     while self.pipe.readable() and count < 500:
    #         self.data.put(self.pipe.readline())
    #         count = count +1

    
    
    
    # def _update_axis(self):
    #     self.ax.clear()
    #     self.ax.set_xlim([0.1, DOMAIN])
    #     self.ax.set_ylim([0.1, DOMAIN])
    #     self.ax.set_xbound([0.1, DOMAIN])
    #     self.ax.set_ybound([0.1, DOMAIN])

    def main_loop(self):
        
        self.update()
        running=True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running=False
                
            #refresh screen
            glClear(GL_COLOR_BUFFER_BIT)
            pg.display.flip()
            
            #timing
            self.clock.tick(60)
        # ani = FuncAnimation(self.fig, self.update, blit=False, interval=0.001)
        # plt.show(block=True)
   
if __name__ == "__main__":
    display = Display()
    # display.startup() 