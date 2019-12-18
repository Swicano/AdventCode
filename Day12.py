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






if __name__ == "__main__":
    
    
    inputfile = 'c:\\users\gfirest\Box Sync\Other shit\Github\AdventCode\Day12input.txt' #12082 after 1000 steps
    ''' for testing
    inputfile = 'c:\\users\gfirest\Box Sync\Other shit\Github\AdventCode\Day12inputtest1.txt' #179 after 10 steps
    inputfile = 'c:\\users\gfirest\Box Sync\Other shit\Github\AdventCode\Day12inputtest2.txt' #1940 after 100 steps
    '''
     
    system = []
    with open(inputfile) as fi:
        for line in fi.readlines():
            coordsrough = line.split(',') #gives us len 3 dict with some extra crap
            coords = tuple([ int(val.strip('<xyz=> \n')) for val in coordsrough])
            # cleaned up that rough dict, and formatted it
            system.append(cs.massive_body(pos = coords))
         
    for primary in system:
        logger.debug(primary)

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
    