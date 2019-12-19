#Day 12

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

import celestialmechs as cs
import copy ##2





if __name__ == "__main__":
    
    
    inputfile = 'c:\\users\gfirest\Box Sync\Other shit\Github\AdventCode\Day12input.txt' #12082 after 1000 steps
    ''' for testing
    inputfile = 'c:\\users\gfirest\Box Sync\Other shit\Github\AdventCode\Day12inputtest1.txt' #179 after 10 steps
    inputfile = 'c:\\users\gfirest\Box Sync\Other shit\Github\AdventCode\Day12inputtest2.txt' #1940 after 100 steps
    '''
     
    system = []
    with open(inputfile) as fi:
        for line in fi.readlines():
            #convert line into a len 3 list with some extra crap
            coordsrough = line.split(',') 
            # clean up that rough list, and formatted it into a tuple(x,y,z)
            coords = tuple([ int(val.strip('<xyz=> \n')) for val in coordsrough])
            system.append(cs.massive_body(pos = coords))
         
    for primary in system:
        logger.debug(primary)
        
    system0 = copy.deepcopy(system)##2  need a copy to compare against
    
    # now that we have set up our simulation, we can begin doing time steps
    totalsteps = 1000
    report_inc = 100    
    for i in range(1,totalsteps+1):
        
        for primary in system:
            # connect each system pairwise:
            for secondary in system:
                primary.apply_gravity(secondary)
        
        for primary in system:
            primary.apply_velocity()
        
        for primary in system:    
            primary.update_energy()
            
        if not(i%report_inc):
            logger.debug(f"after step {i} :")
            for primary in system:
                logger.debug(primary)
    
    totenerg = sum([ obj.TotE for obj in system])
    
    #Part2: at what step does the universe repeat itself?
    # two ideas: 1: just shove a hash of the system at each time-step into a giant as dict
    #            2: IF the universe repeats itself, then it must be on a cycle, and every point repeats itself
    #              (not sure if thats true), therefore: we just save the FIRST time step, and compare all future
    #              steps to that.
    # out of laziness lets start with 2. (new lines marked with '##2' at end
    