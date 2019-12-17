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
    def __init__(self, incode, x_loc=0, y_loc=0, orientation=0, startcolor=0 ):
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
            logger.warning('inposy doesnt match internal position')
        
        # first we run it until we get a output color
        while not (self.computer.out_wait_flag or self.done):
            self.computer.load_inqueue(self.incolor)
            # assume loading once is enough
            self.computer.run_until()
            if self.computer.in_wait_flag:
                logger.debug('input waiting')
            if self.computer.done_flag:
                self.done = 1
                break
            
        if self.done:
            return self.done,None, None,None
            
        self.outcolor = self.computer.read_output()

        
        # then run it again to get a rotation and thus step
        while not (self.computer.out_wait_flag or self.done):
            self.computer.load_inqueue(self.incolor)
            # assume loading once is enough
            self.computer.run_until()
            if self.computer.done_flag:
                raise Exception('Halted mid-run')
            if self.computer.in_wait_flag:
                logger.debug('input waiting')
        
        # get a 0 for 'turn left' or 1 for 'turn right'
        rot_indic = self.computer.read_output()
        #adjust the orientation
        if rot_indic:
            self.orient = (self.orient +1)%4
        else:
            self.orient = (self.orient -1)%4
        #logger.debug(f"orientation is {self.orient}")
        
        #take a step into direction of new orientation
        # if 0, y+=1, 2: y-=1, 1: x+=1, 3: -=1
        if self.orient in {0,2}:
            self.y = self.y + 1 - self.orient
        elif self.orient in {1,3}:
            self.x = self.x + 2 - self.orient
        else:
            logger.warning('orientation is not a cardinal direction')
        logger.debug(self.x)
        return self.done, self.outcolor, self.x, self.y
        

# ok lets try to use it.

if __name__ == "__main__":

    #load in incode from file
    inputcode = []
    inputfile = 'c:\\users\gfirest\Box Sync\Other shit\Github\AdventCode\Day11input.txt'
    inputfile = 'c:\\users\gfirest\Box Sync\Other shit\Github\AdventCode\Day11inputtest1.txt'
    with open(inputfile) as fi:
        logger.debug(f" reading from file {inputfile}")
        instring = fi.read()
        inputcode = [ int(code) for code in instring.split(',')] 
    
    #initialize a hullpainter
    # and a hull
    painter = hull_painter(inputcode)
    spots = set()
    hull = {(0,0):0}
    lastx = 0
    lasty = 0
    done = 0
    steps = 0
    newspot = 1
    # assume at least one step
    currcolor = hull.get((lastx,lasty),0)
    done, newcolor, newx, newy = painter.paint_step(currcolor, lastx, lasty)
    while not done:
        hull[(lastx,lasty)] = newcolor
        spots.add((lastx,lasty))
        steps+=1
        lastx = newx
        lasty = newy
        currcolor = hull.get((lastx,lasty),0)
        done, newcolor, newx, newy = painter.paint_step(currcolor, lastx, lasty)
        if (newx,newy) not in hull:
            newspot+=1
                
                
                
                
                
                
                
                
                
                