# hull painting robot.
# a 2d  turing maching type thing. it reads the data of the square it is on ( initially 0,0, rotation North (0) )
# computes based on that input (0 or 1), and outputs a new  value to the square (0 or 1), 
#  and rotates its' heading (0 for left, 1 for right 90 degrees)
#  then it takes a step, and repeat.

import logging
# we need a logger, a formatter, and a handler
logger = logging.getLogger(__name__)
logger.propagate = False # this is set to false to avoid double messages, not necesarrily the best idea...
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler = logging.StreamHandler()
# now we setup each of these to log at the DEBUG level (for now)
logger.setLevel(logging.DEBUG)
handler.setLevel(logging.DEBUG)
# finally we bind them together
handler.setFormatter(formatter)
logger.addHandler(handler)


import computer			
# im thinking, you give it an input location, and color, and it returns a 'new color for that location' and the next position, keeps track of orientation internally.
class hull_painter:
    __init__(self, incode, x_loc=0, y_loc=0, orientation=0, startcolor=0 ):
        self.x = x_loc
        self.y = y_loc
        self.orient = orientation # 0 = up, 1 = right, 2 = down, 3 = left (clockwise)
        self.computer = computer.opcomputer(incode)
        self.incolor = startcolor
        self.outcolor = 0
        self.done =0

    def paint_step(self, in_color, inposx, inposy):
        
        self.incolor = in_color
        # not sure if these should be errors or not
        if self.x != inposx:
            logger.warning('inposx doesnt match internal position')
        if self.y != inposy:
            logger.warning('inposx doesnt match internal position')
        
        # first we run it until we get a output color
        while not (self.computer.out_wait_flag or self.done):
            self.computer.load_inqueue(self.incolor)
            # assume loading once is enough
            self.computer.run_until()
            if self.computer.done_flag:
                self.done = 1
                break
            
        if self.done:
            break
            
        self.outcolor = self.computer.read_output()
        
        # then run it again to get a rotation and thus step
        while not (self.computer.out_wait_flag or self.done):
            self.computer.load_inqueue(self.incolor)
            # assume loading once is enough
            self.computer.run_until()
            if self.computer.done_flag:
                raise Exception('Halted mid-run')
        
        # get a 0 for 'turn left' or 1 for 'turn right'
        rot_indic = self.computer.read_output()
        #adjust the orientation
        if rot_indic:
            self.orient = (self.orient +1)%4
        else:
            self.orient = (self.orient -1)%4
        #take a step into direction of orientation
        # if 0, y+=1, 2: y-=1, 1: x+=1, 3: -=1
        if self.orient in {0,2}:
            self.y = self.y + 1 - self.orient
        if self.orient in {1,3}:
            self.x = self.x + 2 - self.orient
            
        return self.outcolor, self.x, self.y
        

# ok lets try to use it.
                
                