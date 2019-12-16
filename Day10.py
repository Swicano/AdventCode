# day 10 has nothing to do with opcodes thank god
# ive also just realised i done goofed by not naming all the previous days day01, 02, etc


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

from fractions import Fraction  # needed for part 2
logger.debug('this is a test log debug message')

inputfile = 'c:\\users\gfirest\Box Sync\Other shit\Github\AdventCode\Day10input.txt'
#  5, 8  33
inputfiletest1 = 'c:\\users\gfirest\Box Sync\Other shit\Github\AdventCode\Day10inputtest1.txt'
#  1, 2  35
inputfiletest2 = 'c:\\users\gfirest\Box Sync\Other shit\Github\AdventCode\Day10inputtest2.txt'
#  6, 3  41
inputfiletest3 = 'c:\\users\gfirest\Box Sync\Other shit\Github\AdventCode\Day10inputtest3.txt'
# 11,13 210 # 200th is at 8,2
inputfiletest4 = 'c:\\users\gfirest\Box Sync\Other shit\Github\AdventCode\Day10inputtest4.txt'

#inputfile = inputfiletest4
# key idea, if two asteroids are the same angle from the observation station, they can't be seen
# BUT i dont need them to have the same angle theta, since we get that angle from arctan(a/b)
#           we can just calculate a/b, and if those match, the angle will as well

''' 
is this the best way... we need to
   1) find each of n asteroid locations in the m x m grid O(m^2)?
   2) for each asteroid (O(n)), measure the ratio of the x and y distance to each other asteroid
       O(n-1), add it to set: O(n^2)
   3) find the set with the largest length (O(n))
   
   OPTION2
   1) for each  point test if it is an asteroid (O(m^2)?) if it is:
   2) check the neighbors by adding a vector denoting the distance (we can order it by 
   manhattan distance) if we find a match, remove all multiples of that vector from the 
   pool of vectors to check.
    problem: what if first occurence is already a multiple of a smaller vector? e.g. asteroid at +4,+4 AND +5,+5, but not closer?
   this just seems like the first one but with extra effort.
   lets just do the first
'''
def spot_asteroids(station_loc, asteroid_locs):
    ind = asteroid_locs.index(station_loc)
    coordx,coordy = station_loc
    prelist = asteroid_coords[:ind]
    postlist = asteroid_coords[ind+1:]
    # measure the TOA of each other asteroid to that asteroid, and add it 
    # we use a set so that duplicates are automatically removed.
    topset = {(asty-coordy)/(astx-coordx)  
                for astx,asty in prelist if astx != coordx}
    botset = {(asty-coordy)/(astx-coordx) 
                for astx,asty in postlist if astx != coordx}
    midset = {1 if asty>coordy else -1 
                for astx,asty in prelist+postlist if astx == coordx}
    return topset, midset, botset

def find_nth_asteroid(stationloc, asteroid_coords, angle_list, n, quad=1, rev=False):
    vec = 0
    if angle_list == "inf":
        vec = (0,1)            
    elif angle_list == "-inf":
        vec = (0,-1)
    else:
        angle_list.sort(reverse = rev)
        angle = angle_list[n-1]
        frec = Fraction(angle).limit_denominator(1000)
        # by default the negative sign goes to the numerator (y)
        # quad 1 2 3 4
        #    x + - - + 
        #      -1** int(quad/2)
        #    y - - + + 
        # frec - + - +
        # so   1 -1 -1 1
        denom = frec.denominator*(-1)**(int((quad)/2))
        numer = frec.numerator*(-1)**(int((quad)/2))
        vec = (denom, numer)
    loc = stationloc
    while True:
        loc = (loc[0]+vec[0],loc[1]+vec[1])
        if loc in asteroid_coords:
            return loc
        elif loc[0] > 1000000 or loc[1] > 1000000:
            raise Exception('not found error')

#step one find all the asteroids
asteroid_coords = []
with open(inputfile) as fi:
    logger.debug(f" reading from file {inputfile}")
    asteroid_coords = [ (x,y)
                            for y, line in enumerate(fi.readlines()) 
                                for x,val in enumerate(line) 
                                     if val == '#' ] 


                
# step 2 for each asteroid...
asteroids_spotted = []
max_spotted = 0
for i in range(0, len(asteroid_coords)):
    # to handle that pesky asymptote at 180 degrees
    # we just split them in 3 groups, one extra to deal with infinities.
    topset,midset,botset = spot_asteroids(asteroid_coords[i], asteroid_coords)
    
    num_spotted =  len(topset)+len(botset)+len(midset)
    max_spotted = max(max_spotted, num_spotted)
    asteroids_spotted.append(num_spotted)
    

        
                
        
# and step 3 is pretty easy
print(max_spotted)
print(asteroid_coords[asteroids_spotted.index(max_spotted)])

'''
Part2, we want to know, if we start counting from straight upwards, going clockwise
what is the 200th asteroid we count (if there are under 200 immediately visible, we remove
those asteroids, revealing previously hidden asteroids, and keep counting.
   ''' 
#add in part 2 code
station = asteroid_coords[asteroids_spotted.index(max_spotted)]
topset, midset, botset = spot_asteroids(station, asteroid_coords)
remain = 200 # the 200th asteroid is what we're looking for.
while max_spotted < remain:
    pass
    # figure this out later (not necessary for my puzzle solution)
    # but we need to remove all spotted asteroids from asteroid_coords, and generate a new
    # spot_asteroids 
target_loc = ()
while remain:
    # in order to stay right of vertical, we need to split the topset
    toplistpos = [ x for x in topset if x>=0] # quadrant 1
    toplistneg = list(topset -set(toplistpos) )       # quadrant 2
    botlistpos = [ x for x in botset if x>=0]      # quadrant 3
    botlistneg =  list(botset -set(botlistpos))        # quadrant 4
    logger.debug(f"len: top, mid, bot are {len(topset)},{len(midset)},{len(botset)} and the split len are top pos:{len(toplistpos)},top neg:{len(toplistneg)}, bot pos:{len(botlistpos)}, bot neg:{len(botlistneg)}")
        #step one, check if 1 is in midset (vertical inf degrees)
    if 1 in midset:
        midset.remove(1)
        if remain > 1:
            remain -= 1
        else:
            target_loc = find_nth_asteroid( station, asteroid_coords,  "inf", 1)
            remain = 0
            logger.debug(f"found target at {target_loc} inside midset up")
            continue #break?
    # then check quadrant 1
    if len(toplistneg) < remain:
        remain -= len(toplistneg)
    else:
        target_loc = find_nth_asteroid( station, asteroid_coords,  toplistneg, remain, quad = 1, rev = False)
        remain = 0
        logger.debug(f"found target at {target_loc} inside quad1")
        continue
    # then check quadrant 4
    if len(botlistpos) < remain:
        remain -= len(botlistpos)
    else:
        target_loc = find_nth_asteroid( station, asteroid_coords, botlistpos, remain,  quad = 4, rev = False)
        remain = 0
        logger.debug(f"found target at {target_loc} inside quad4")
        continue
    #check if -1 is in midset (vertical inf degrees)
    if -1 in midset:
        midset.remove(-1)
        if remain > 1:
            remain -= 1
        else:
            target_loc = find_nth_asteroid( station, asteroid_coords,  "inf", -1)
            remain = 0
            logger.debug(f"found target at {target_loc} inside midset down")
            continue #break?
    # then check quadrant 3
    if len(botlistneg) < remain:
        remain -= len(botlistneg)
    else:
        target_loc = find_nth_asteroid( station, asteroid_coords, botlistneg, remain, quad = 3)
        remain = 0
        logger.debug(f"found target at {target_loc} inside quad3")
        continue
    # then check quadrant 2
    if len(toplistpos) < remain:
        remain -= len(toplistpos)
    else:
        target_loc = find_nth_asteroid( station, asteroid_coords, toplistpos, remain, quad = 2)
        remain = 0
        logger.debug(f"found target at {target_loc} inside quad2")
        continue
print(target_loc)
