# Day 5 is updating the OpCode computer from Day2 with new instructions and immediate mode
# Copy in relevant lines from Day2

incode = [3,225,1,225,6,6,1100,1,238,225,104,0,1101,81,30,225,1102,9,63,225,1001,92,45,224,101,-83,224,224,4,224,102,8,223,223,101,2,224,224,1,224,223,223,1102,41,38,225,1002,165,73,224,101,-2920,224,224,4,224,102,8,223,223,101,4,224,224,1,223,224,223,1101,18,14,224,1001,224,-32,224,4,224,1002,223,8,223,101,3,224,224,1,224,223,223,1101,67,38,225,1102,54,62,224,1001,224,-3348,224,4,224,1002,223,8,223,1001,224,1,224,1,224,223,223,1,161,169,224,101,-62,224,224,4,224,1002,223,8,223,101,1,224,224,1,223,224,223,2,14,18,224,1001,224,-1890,224,4,224,1002,223,8,223,101,3,224,224,1,223,224,223,1101,20,25,225,1102,40,11,225,1102,42,58,225,101,76,217,224,101,-153,224,224,4,224,102,8,223,223,1001,224,5,224,1,224,223,223,102,11,43,224,1001,224,-451,224,4,224,1002,223,8,223,101,6,224,224,1,223,224,223,1102,77,23,225,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,8,226,677,224,1002,223,2,223,1006,224,329,1001,223,1,223,7,226,226,224,102,2,223,223,1006,224,344,101,1,223,223,108,677,677,224,1002,223,2,223,1006,224,359,101,1,223,223,1107,226,677,224,1002,223,2,223,1005,224,374,101,1,223,223,1008,677,226,224,1002,223,2,223,1005,224,389,101,1,223,223,1007,677,226,224,1002,223,2,223,1005,224,404,1001,223,1,223,1107,677,226,224,1002,223,2,223,1005,224,419,1001,223,1,223,108,677,226,224,102,2,223,223,1006,224,434,1001,223,1,223,7,226,677,224,102,2,223,223,1005,224,449,1001,223,1,223,107,226,226,224,102,2,223,223,1006,224,464,101,1,223,223,107,677,226,224,102,2,223,223,1006,224,479,101,1,223,223,1007,677,677,224,1002,223,2,223,1006,224,494,1001,223,1,223,1008,226,226,224,1002,223,2,223,1006,224,509,101,1,223,223,7,677,226,224,1002,223,2,223,1006,224,524,1001,223,1,223,1007,226,226,224,102,2,223,223,1006,224,539,101,1,223,223,8,677,226,224,1002,223,2,223,1006,224,554,101,1,223,223,1008,677,677,224,102,2,223,223,1006,224,569,101,1,223,223,1108,677,226,224,102,2,223,223,1005,224,584,101,1,223,223,107,677,677,224,102,2,223,223,1006,224,599,1001,223,1,223,1108,677,677,224,1002,223,2,223,1006,224,614,1001,223,1,223,1107,677,677,224,1002,223,2,223,1005,224,629,1001,223,1,223,108,226,226,224,1002,223,2,223,1005,224,644,101,1,223,223,8,226,226,224,1002,223,2,223,1005,224,659,101,1,223,223,1108,226,677,224,1002,223,2,223,1006,224,674,101,1,223,223,4,223,99,226]

#def program(input):
#    PC = 0
#    while True:
#        if input[PC] ==1:
#            input[ input[PC+3] ] = input[ input[PC+1] ] + input[ input[PC+2] ]
#            PC=PC+4
#        elif input[PC] ==2:
#            input[ input[PC+3] ] = input[ input[PC+1] ] * input[ input[PC+2] ]
#            PC=PC+4
#        elif input[PC] == 99:
#            break
#        else:
#            raise Exception("invalid opcode") #oh ya i forgot this one
#    #print( input[0])
#    return input
    
# list of Opcodes:
#   01: 3 params: p1+p2 -> p3                           opAdd
#   02: 3 params: p1*p2 -> p3                           opMul
#   03: 1 params: input -> p1                           opSav
#   04: 1 params: p1 -> output                          opPrn
#   05: 2 params: if(p1)  p2 -> PC                      opJTr
#   06: 2 params: if(!p1) p2 -> PC                      opJFl
#   07: 3 params: if(p1 < p2)  1 -> p3, else 0 -> p3    opLTh
#   08: 3 params: if(p1 == p2) 1 -> p3, else 0 -> p3    opEqu
#   99: 0 params: halt
#   
#

def program(incode):
    PC = 0
    while True:
        opcode = incode[PC]
        decode = [opcode%100, int(opcode/100)%10, int(opcode/1000)%10,int(opcode/10000)%10]
        par1=0
        par2=0
        par3=0
        
        if decode[0] == 1:      #opAdd-----------------------
            if decode[1]:           # immediate
                par1 = incode[PC+1]
            else:
                par1 = incode[incode[PC+1]]
            if decode[2]:           # immediate
                par2 = incode[PC+2]
            else:
                par2 = incode[incode[PC+2]]
            if decode[3]:           # immediate
                incode[PC+3] = par1+par2
            else:
                incode[incode[PC+3]] = par1+par2
            PC += 4
            
        elif decode[0] == 2:    #opMul-----------------------
            if decode[1]:           # immediate
                par1 = incode[PC+1]
            else:
                par1 = incode[incode[PC+1]]
            if decode[2]:           # immediate
                par2 = incode[PC+2]
            else:
                par2 = incode[incode[PC+2]]
            if decode[3]:           # immediate
                incode[PC+3] = par1*par2
            else:
                incode[incode[PC+3]] = par1*par2
            PC += 4
            
        elif decode[0] == 3:    #opSav-----------------------
            par1 = int(input('System ID to test: '))
            if decode[1]:           # immediate
                incode[PC+1] = par1
            else:
                incode[incode[PC+1]] = par1
            PC += 2
            
        elif decode[0] == 4:    #opPrn------------------------
            if decode[1]:           # immediate
                print(incode[PC+1])
            else:
                print(incode[incode[PC+1]])
            PC += 2
            
        elif decode[0] == 5:    #opJTr------------------------
            if decode[1]:               # immediate
                par1 = incode[PC+1]
            else:
                par1 = incode[incode[PC+1]]
            if par1:
                if decode[2]:           # immediate
                    PC = incode[PC+2]
                else:
                    PC = incode[incode[PC+2]]
            else:
                PC += 3
            
        elif decode[0] == 6:    #opJFl------------------------
            if decode[1]:               # immediate
                par1 = incode[PC+1]
            else:
                par1 = incode[incode[PC+1]]
            if not(par1):
                if decode[2]:           # immediate
                    PC = incode[PC+2]
                else:
                    PC = incode[incode[PC+2]]
            else:
                PC += 3
                    
        elif decode[0] == 7:    #opLTh------------------------
            if decode[1]:           # immediate
                par1 = incode[PC+1]
            else:
                par1 = incode[incode[PC+1]]
            if decode[2]:           # immediate
                par2 = incode[PC+2]
            else:
                par2 = incode[incode[PC+2]]
            out = int(par1 < par2)
            if decode[3]:           # immediate
                incode[PC+3] = out
            else:
                incode[incode[PC+3]] = out
            PC += 4
            
        elif decode[0] == 8:    #opEqu------------------------
            if decode[1]:           # immediate
                par1 = incode[PC+1]
            else:
                par1 = incode[incode[PC+1]]
            if decode[2]:           # immediate
                par2 = incode[PC+2]
            else:
                par2 = incode[incode[PC+2]]
            out = int(par1 == par2)
            if decode[3]:           # immediate
                incode[PC+3] = out
            else:
                incode[incode[PC+3]] = out
            PC += 4
            
        elif decode[0] == 99:   #opHlt
            break
            
        else:
            raise Exception("invalid opcode") #oh ya i forgot this one
    return incode
    
program(incode) #5346030 for 1

# part two adds several more opcodes, which is fine, we just extend them