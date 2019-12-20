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
        # below this these are dependent variables and dont need to be included in __eq__
        # they will match by virtue of pos and vel matching
        self.KinE=0
        self.PotE=0
        self.TotE=0
        self.update_energy()
        #self.PotE = abs(self.px)+abs(self.py)+abs(self.pz)
        #self.KinE = abs(self.vx)+abs(self.vy)+abs(self.vz)
        #self.TotE = self.PotE * self.KinE
        
    def compare_pos(self, coord1, coord2):
        '''
        if coord1 == coord2:
            return 0
        elif coord2 > coord1: # this method is 2.7542108456293742e-05 per iteration. lel
            return 1
        else:
            return -1
        '''
        if coord2 > coord1: # this method is 2.7542108456293742e-05 per iteration. lel
            return 1
        elif coord1 == coord2:
            return 0
        else:
            return -1
            
            
        #else: # this method has speed 3.8243851549625396e-05 per iteration loop with 4 objects
        #    # check if coordinate 2 is behind coordinate 1, if so, -1, else 1
        #    relation = int(coord2<coord1)
        #    return (-1)**(relation)
    
    def apply_gravity(self, body_object, algo=1):
        # i assume we will do ACTUAL math at some point.   
        # if algo == 1: ##2 if we need to change the algo re-open this later
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
        return f"massive_body(pos={self.px,self.py,self.pz}, vel={self.vx,self.vy,self.vz}, type='{self.type}')"
        
    def __eq__(self,other):
        position_equality = (self.px == other.px) & (self.py == other.py) &(self.pz == other.pz)
        velocity_equality = (self.vx == other.vx) & (self.vy == other.vy) &(self.vz == other.vz)
        type_equality = self.type == other.type
        return (position_equality & velocity_equality & type_equality)
        
    def __hash__(self):
        return hash((self.px,self.py,self.pz,self.vx,self.vy,self.vz,self.type))
             
             
             
             
if __name__=="__main__":
    obj1 = massive_body()
    obj2 = massive_body(pos = (0,1,0))
    obj3 = massive_body(pos = (-14,12,17))
             
    logger.debug(f' obj1 is obj2: {obj1 is obj2}, obj1 == obj2: {obj1 == obj2}, and hashes: {hash(obj1) == hash(obj2)}')
    
    obj2.py = 0
    logger.debug(f'set obj2 to same position (and vel) as obj1')
    logger.debug(f' obj1 is obj2: {obj1 is obj2}, obj1 == obj2: {obj1 == obj2}, and hashes: {hash(obj1) == hash(obj2)}')
             
    obj2.py = 1
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
            