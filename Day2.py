import math

input = [1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,1,9,19,1,19,5,23,2,6,23,27,1,6,27,31,2,31,9,35,1,35,6,39,1,10,39,43,2,9,43,47,1,5,47,51,2,51,6,55,1,5,55,59,2,13,59,63,1,63,5,67,2,67,13,71,1,71,9,75,1,75,6,79,2,79,6,83,1,83,5,87,2,87,9,91,2,9,91,95,1,5,95,99,2,99,13,103,1,103,5,107,1,2,107,111,1,111,5,0,99,2,14,0,0]

testinput1=[1,0,0,0,99]             #2,0,0,0,99
testinput2=[2,3,0,3,99]             #2,3,0,6,99
testinput3=[2,4,4,5,99,0]           #2,4,4,5,99,9801
testinput4=[1,1,1,4,99,5,6,0,99]    #30,1,1,4,2,5,6,0,99

# reset to 1202 state
input[1]=12
input[2]=2

# uncomment if you want to use a test input instead
input[:] = testinput4

#code for part 1
#for i in range(0,len(input),4):
#    if input[i] ==1:
#        input[ input[i+3] ] = input[ input[i+1] ] + input[ input[i+2] ]
#    elif input[i] ==2:
#        input[ input[i+3] ] = input[ input[i+1] ] * input[ input[i+2] ]
#    elif input[i] == 99:
#        break
#        
#print( input[0])



#code for part 2: it is clear that there might be opcode parameter length fuckery at some point
# so a quick rewrite of the loop above is in order, and make it a function

def program(input):
    PC = 0
    while True:
        if input[PC] ==1:
            input[ input[PC+3] ] = input[ input[PC+1] ] + input[ input[PC+2] ]
            PC=PC+4
        elif input[PC] ==2:
            input[ input[PC+3] ] = input[ input[PC+1] ] * input[ input[PC+2] ]
            PC=PC+4
        elif input[PC] == 99:
            break
        else:
            raise Exception("invalid opcode") #oh ya i forgot this one
    #print( input[0])
    return input

# now we put that inside a big old double loop to solve what input[1] and [2]
# give an output value of 19690720

for i in range(0,100):
    for j in range(0,100):
        inputcopy = list()
        inputcopy[:] = input
        inputcopy[1]=i
        inputcopy[2]=j
        try:
            final = program(inputcopy)
        if final[0] == 19690720:
            print( [i,j])
            break
        

        