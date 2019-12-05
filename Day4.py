inputmin = 387638
inputmax = 919123

# rules : 1) six digits (and are within min and max 
#         2) 2 adjacent digits are the same
#         3) left to right, the numbers never decrease

# this first one might be possible to do without programming?

# 456789 is the only one that violates rule 2

# 388 888 is the starting point

# for a 1 digit number, 
#         sum(n,1,9)(1) = 9
# for a 2 digit number, the number can be written as ( n2, n1 )
#   the total number of valid numbers that satisfy rule 3 are 
#         sum(n2,1,9)(sum(n1,n2,9)(1)) 
#         sum(n2,1,9) (10-n2)/1!  = 45
#         (11-n3)(10-n3)/2!

# general formula for a m-digit number (n_m,n_(m-1), ... , n_1) is 

#   SUM(n = 1,9)[  PRODUCT(b=1,m-1)[(9+b-n)]/( (m-1)! ) ]
# which for a 6 digit number is: 3003

# now we need to take OUT the numbers taht violate rule 2,
# interestingly, it is not an issue in any number longer than 9 digits, so thats nice
# 
# for m=1,   9 -> 0   after applying rule 2
# for m=2,  45 -> 9
# for m=3, 165 -> 45*2  So it seems like its the equivalent of having a 1 digit less number, multiplied by te additional permutations of which digit we 'delete' by forcing it to match the previous digit.
# for m=4, 495 -> 165*3? but thats 495 again, and this is a problem if we go to 5

# lets take it another way, we have from above the number of passwords that are increasing, and can contain doubles
#  what if we find the number of passwords that are STRICTLY increasing, and thus cannot contain doubles
#  and then just subtract them from each other, to get the ones taht increase, and DO have doubles

# repeating the above
# for a 1 digit number, 
#         sum(n,1,9)(1) = 9   this one stays the same,
# for a 2 digit number, the number can be written as ( n2, n1 )
#   the total number of valid numbers that satisfy rule 3 are 
#         sum(n2,1,9)(sum(n1,n2+1,9)(1))  the important part is the n2+1
#         sum(n2,1,9) (9-n2)/1!  = 36
#         (9-n3)(10-n3)/2!

# general formula for a m-digit number (n_m,n_(m-1), ... , n_1) is 

#   SUM(n = 1,9)[  PRODUCT(b=1,m-1)[(10-b-n)]/( (m-1)! ) ]
# which for a 6 digit number is: 84
# and we check that for any number larger than 9, the solution to the above is 0,
# which it is.

#finally, to address the starting and stopping, numbers, we need only to find this value for the upper limit
# for example, 919123, by finding the number for a 6 digit number with the sum from 1-8 (ending at 899999)
#                          Then we are done, because the leagin 9 really messes with it, and 999999 isnt valid

# for example, 256889, by finding the number for a 6 digit number with the sum from 1-1 (ending at 199999)
#                          adding the number for a 5 digit number with the sum from 2-4 (ie. from   22222 to 49999)
#                          adding the number for a 4 digit number with the sum from 5-5 (ie. from    5555 to  5999)
#                          adding the number for a 3 digit number with the sum from 6-7 (ie. from     666 to   799)
#                          adding the number for a 2 digit number with the sum from 8-8 (ie. from      88 to    89)
#                          adding the number for a 1 digit number with the sum from 2-4 (ie. 0)

# then do the same for the lower number and subtract them


# but lets just do it with loop and checks

counter = 0

for i in range(inputmin, inputmax+1):
    isplit = [ int(char) for char in str(i)] # split the number into a list of digits
    if (isplit == sorted(isplit)) & ( len(set(isplit)) < len(isplit)):
        counter += 1
        print(i)
print(counter)

# part 2 ONLY doublets count, not triplets, quads, etc. 
# instead of just cheching that the length of the set is less than the list, 
# we need there to exist an digit 1-9 which has a count() == 2 

counter2 = 0

for i in range(inputmin, inputmax+1):
    isplit = [ int(char) for char in str(i)] # split the number into a list of digits
    if (isplit == sorted(isplit)) & ( 2 in [isplit.count(x) for x in range(1,10)]):
        counter2 += 1
        print(i)
print(counter2)

