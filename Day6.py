# oh hey we're building a tree then counting the ... branches?
# the interesting thing is that the data is not ordered,
#  shuold i import all the data then build the tree?
#   no, that seems too easy. buld it as I read it.

# the input is a lot of lines, so we will save it as a file and import it
inputfile = 'c:\\users\gfirest\Box Sync\Other shit\Github\AdventCode\Day6input.txt'

# general structure of building the tree: each line is a parent-child link
#   assume the current tree is a set of trees (multiple roots), search each
#   tree to see if the new parent is already inside it, if so, add that child
#   if not: make a new tree, with the parent as a root.
#   That requires a new function of merging the trees, where we iterate through the multiple roots
#   and then merge any roots that exist as children in other trees.

#   option two: load each pair, save the child as a list with a pointer to it's parent
#   and save the parent with a null pointer. as we update it, if the child already exists, just update the pointer
#   this should be fine, since no child has multiple parents...

#  lets do it this way, but lazily, implement our linked list as just a list
#  where the first value is a list of positions, and the rest oare values at that position
#  [ [ list of next's], datalist]
#
#    so a lazy list of 1 item would be  [[-1], 'first']
#    lets add something that points to 'first'
#                                       [[-1,0],'first','pnt_to_frst']
# now lets add another item that doesn't point anywhere yet
#                                       [[-1,0,-1],'first','pnt_to_frst','second']
# and something that points at it
#                                       [[-1,0,-1,2],'first','pnt_to_frst','second', 'pnt->scnd']
# if we then update first to point at second, we would change the -1 to 2
# we can follow this new list [[-1,0,-1,2],'first','pnt_to_frst','second', 'pnt->scnd'], which doesn't really have a head
#  by starting with a location, lets say 1, for the location of 

lazylinked = [[None],None]

with open(inputfile, 'r') as f:
    for line in f.readlines():
        par,child = line.strip().split(')')
        #   print ( f"{child} orbits {par} directly")
    

















