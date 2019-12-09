# oh hey we're building a tree then counting the ... branches?
# the interesting thing is that the data is not ordered,
#  shuold i import all the data then build the tree?
#   no, that seems too easy. buld it as I read it.

# the input is a lot of lines, so we will save it as a file and import it
inputfile = 'c:\\users\gfirest\Box Sync\Other shit\Github\AdventCode\Day6input.txt'     # real input
#inputfile = 'c:\\users\gfirest\Box Sync\Other shit\Github\AdventCode\Day6inputtest.txt' #42 is answer
#inputfile = 'c:\\users\gfirest\Box Sync\Other shit\Github\AdventCode\Day6inputtestscr1.txt' #42 is answer, still
#inputfile = 'c:\\users\gfirest\Box Sync\Other shit\Github\AdventCode\Day6inputtestpt2.txt' #54 is total, 4 transfers

# general structure of building the tree: each line is a parent-child link
#   assume the current tree is a set of trees (multiple roots), search each
#   tree to see if the new parent is already inside it, if so, add that child
#   if not: make a new tree, with the parent as a root.
#   That requires a new function of merging the trees, where we iterate through the multiple roots
#   and then merge any roots that exist as children in other trees.

#   option two: load each pair, save the child as a list with a pointer to it's parent
#   and save the parent with a null pointer. as we update it, if the child already exists, just update the pointer
#   this should be fine, since no child has multiple parents...

#  lets do it this way, but lazily, implement our linked list as just 2 lists
#    one that holds the data, one that holds the location of next()


lazylinkedData = []
lazylinkedNext = []

with open(inputfile, 'r') as f:
    for line in f.readlines():
        par,child = line.strip().split(')')
        link = -1
        
        if par not in lazylinkedData:
            lazylinkedData.append(par)
            lazylinkedNext.append(-1)
            
        link = lazylinkedData.index(par)
  
        if child not in lazylinkedData:
            lazylinkedData.append(child)
            lazylinkedNext.append(-1)
        lazylinkedNext[lazylinkedData.index(child)] = link

# now we have our lazy linked list. next we just iterate through each item in 
# the list, and count the distance to com

total = 0
for start in lazylinkedData:
    next = lazylinkedData.index(start)
    guess = ''
    count = 0
    while next > -0.5:
        guess = guess + lazylinkedData[next]
        next = lazylinkedNext[next]
        count +=1
    print(count)
    total += count -1
print(total)

#For Part 2, we need to know the distance between two objects, based on the map made above
# we can probably do this the easy way, put objects from the start to com in a set, 
# the same for the destination object to com, then just take the symmetric difference
# NOTE: this is cheaty, because it skips their crossover orbit, but compensates by including 
# the objects themselves (in terms of the challenge specifics, the number will be right, 
# but the actual path wont be...

obj1 = 'YOU'
orbits1 = set()
next = lazylinkedData.index(obj1)
while next > -0.5:
    orbits1.add(lazylinkedData[next])
    next = lazylinkedNext[next]
obj2 = 'SAN'
orbits2 = set()
next = lazylinkedData.index(obj2)
while next > -0.5:
    orbits2.add(lazylinkedData[next])
    next = lazylinkedNext[next]

path = len(orbits1 ^ orbits2)-2












