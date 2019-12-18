#Day 12 simulates planets

import logging
# we need a logger, a formatter, and a handler
logger = logging.getLogger(__name__)
logger.propagate = False # this is set to false to avoid double messages, not necesarrily the best idea...
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler = logging.StreamHandler()
# now we setup each of these to log at the DEBUG level (for now)
logger.setLevel(logging.WARNING)
handler.setLevel(logging.WARNING)
# finally we bind them together
handler.setFormatter(formatter)
logger.addHandler(handler)


class massive_body:
    ''' a generic holder for something WITH mass floating in space '''
    # keep the type variable in case we add jupiter in or satelites with different mass
    def __init__(self, pos = None, vel = None, type = 'moon'):
        if pos is None:
            self.px=0
            self.py=0
            self.pz=0
        elif len(pos) != 3:
            logger.warning(f"len of input pos tuple {len(pos)}!=3, assuming 0,0,0")
            self.px=0
            self.py=0
            self.pz=0
        else:
            self.px=pos[0]
            self.py=pos[1]
            self.pz=pos[2]
            
        if vel is None:
            self.vx=0
            self.vy=0
            self.vz=0
        elif len(vel) != 3:
            logger.warning(f"len of input vel tuple {len(vel)}!=3, assuming 0,0,0")
            self.vx=0
            self.vy=0
            self.vz=0
        else:
            self.vx=vel[0]
            self.vy=vel[1]
            self.vz=vel[2]
        self.type = type
        self.KinE=0
        self.PotE=0
        self.TotE=0
        self.update_energy()
        #self.PotE = abs(self.px)+abs(self.py)+abs(self.pz)
        #self.KinE = abs(self.vx)+abs(self.vy)+abs(self.vz)
        #self.TotE = self.PotE * self.KinE
        
    def compare_pos( coord1, coord2):
        if coord1 == coord2:
            return 0
        else:
            # check if coordinate 2 is behind coordinate 1, if so, -1, else 1
            relation = int(coord2<coord1)
            return (-1)**(relation)
    
    def apply_gravity(self, body_object, algo=1):
        # i assume we will do ACTUAL math at some point.   
        if algo == 1:
            self.vx = self.vx + self.compare_pos(self.px, body_object.px)
            self.vy = self.vy + self.compare_pos(self.py, body_object.py)
            self.vz = self.vz + self.compare_pos(self.pz, body_object.pz)
             
    def apply_velocity(self):
        self.px += self.vx
        self.py += self.vy
        self.pz += self.vz
        
    def update_energy(self):
        self.PotE = abs(self.px)+abs(self.py)+abs(self.pz)
        self.KinE = abs(self.vx)+abs(self.vy)+abs(self.vz)
        self.TotE = self.PotE * self.KinE
        
    # str is for human readability
    def __str__(self):
        return  f"{self.type}-object at pos({self.px:3},{self.py:3},{self.pz:3}) with vel({self.vx:3},{self.vy:3},{self.vz:3}), PE:{self.PotE:4}   KE:{self.KinE:4}   TotE:{self.TotE:6}"
    
    # repr should be unambiguous. if possible, if should be executable code that creates an identical object    
    def __repr__(self):
        return f"massive_body( pos = {self.px,self.py,self.pz}, vel = {self.vx,self.vy,self.vz}, type = '{self.type}')"
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
            