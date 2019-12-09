#Day 7 buils on the opcode computer we've been building, by chaining them, 
# so we start with a copy of the most recent from Day5:

input = [3,8,1001,8,10,8,105,1,0,0,21,34,59,68,89,102,183,264,345,426,99999,3,9,102,5,9,9,1001,9,5,9,4,9,99,3,9,101,3,9,9,1002,9,5,9,101,5,9,9,1002,9,3,9,1001,9,5,9,4,9,99,3,9,101,5,9,9,4,9,99,3,9,102,4,9,9,101,3,9,9,102,5,9,9,101,4,9,9,4,9,99,3,9,1002,9,5,9,1001,9,2,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,99,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,99,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,99,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,99]

# for automation-convenience I might wrapper over input and output to pull and push from a list.

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

def decorator(f):
    @functools.wraps(f)
    def wrapper(*args, **kwds):
        wait = delay
        last_except = None
        for _ in range(retry_count):
            try:
                result = f(*args, **kwds)
                if result:
                    return result
            except allowed_exceptions as e:
                print('delaying: {}'.format(wait))
                print('allowed: ' + str(type(e)) + str(e))
                last_except = e
                time.sleep(wait)
                wait *= falloff
        if last_except is not None:
            raise type(last_except) from last_except
    return wrapper
    