#Day 12

import celestialmechs as cs






if __name__ == "__main__":
    
    
     inputfile = 'c:\\users\gfirest\Box Sync\Other shit\Github\AdventCode\Day12input.txt'
     inputfile = 'c:\\users\gfirest\Box Sync\Other shit\Github\AdventCode\Day12inputtest1.txt'
     
     system = []
     with open(inputfile) as fi:
         for line in fi.readlines():
             coordsrough = line.split(',') #gives us len 3 dict with some extra crap
             coords = tuple([ int(val.strip('<xyz=> \n')) for val in coordsrough])
             # cleaned up that rough dict, and formatted it
             system.append(cs.massive_body(pos = coords))
         
    # now that we have set up our simulation, we can begin doing time steps
    
    totalsteps = 11
    report_inc = 1
    
    for i in range(0,totalsteps):
        
        # apply gravity:
        for primary in system:
            for secondary in system