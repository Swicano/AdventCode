#Day 7 buils on the opcode computer we've been building, by chaining them, 
# so we start with a copy of the most recent from Day5:

# so we start with an incode, a phase sequence, and a signal to be amplified.
# inputs alternate between getting a phase angle and getting the old output, so
# we just need to make phase setting list that gets popped back to front, but have
# the output function place the output second from the end?
#    visually:
#  prev_output = out0                      # input to first amplifier
#  Phase_list = [ p5, p4, p3, p2, p1]
#  pretend_output(prev_output, Phase_list):
#     temp = phase_list.pop()
#     phase_list.append(prev_output)
#     phase_list.appent(temp)
#     return phase_list

# phase list  = [ p5, p4, p3, p2, out0, p1]
# after running the program once, the phase list has the phase popped off, and the old output (new input)
# it runs, and outputs a new output (out1 aka in2) onto the list
# phase list  = [ p5, p4, p3, out1, p2]

# since I rewrote print and input, I might as well use this as an excuse to learn
# some more about logging
# because of something(maybe to do with Pyzo, my IDE, basicConfig doesn't seem to work
# this is not unexected based on basicConfig doing nothing if a root logger has 
#  handlers already configured.
import logging
# we need a logger, a formatter, and a handler
logger = logging.getLogger(__name__)
logger.propagate = False # this is set to false to avoid double messages, not necesarrily the best idea...
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler = logging.StreamHandler()
# now we setup each of these to log at the DEBUG level (for now)
logger.setLevel(logging.WARNING)
handler.setLevel(logging.WARNING)
# finally we bind them together
handler.setFormatter(formatter)
logger.addHandler(handler)

logger.debug('this is a test log debug message')


incode = [3,8,1001,8,10,8,105,1,0,0,21,34,59,68,89,102,183,264,345,426,99999,3,9,102,5,9,9,1001,9,5,9,4,9,99,3,9,101,3,9,9,1002,9,5,9,101,5,9,9,1002,9,3,9,1001,9,5,9,4,9,99,3,9,101,5,9,9,4,9,99,3,9,102,4,9,9,101,3,9,9,102,5,9,9,101,4,9,9,4,9,99,3,9,1002,9,5,9,1001,9,2,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,99,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,99,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,99,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,99]

incodetest1 = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5] # phase 9,8,7,6,5, thrust 139629729
incodetest2 = [3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4, 53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10] # phase 9,7,8,5,6, thrust 18216
#incode = incodetest2
   
   
# FUCK I just learned that itertools.permutations exists.....
def make_permutations(list_of_inputs):
    perms = []
    if len(list_of_inputs) == 1:
        perms = [list_of_inputs]
    else:
        for x in list_of_inputs: # we take one out, pass it down, get back a list of lists
            subset = list_of_inputs.copy()
            subset.remove(x)
            subperms = make_permutations(subset)
            # then for each sublist we get, we append the one we took out
            # then combine all these lists together
            for order in subperms:
                order.insert(0,x)
                perms.append(order)
    return perms
            
'''


def print(output):
    Phaselist.insert(-1,output)
    
def input(wasted):
    return Phaselist.pop()
 
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
            logger.error('invalid opcode')
    return incode
'''
'''
phaseorderlist = make_permutations(list(range(0,5)))
thrustlist = []

for Phaselist in phaseorderlist:
    print(0)
    for i in range(0,5):
        program(incode)
    thrustlist.append(Phaselist)    
maxthrust = max(thrustlist)
phaseorderlist = make_permutations(list(range(0,5)))
maxphase = phaseorderlist[thrustlist.index(maxthrust)]
'''

# Day 7 part 2: I might want to rewrite this as a class, since it appears we want
# to be able to run each an indeterminate amound of times, and for indeterminate length per call

class program:
    """creates an opcode-computer object with an input and ouput queue"""
    def __init__(self, incodes, phasesetting=0, program_counter=0, inqueue=None,
                  outqueue = None, done=0, inwaiting=0, outwaiting=0):
        # with this we should be able to recreate the state of a program at any point.
        self.incode = incodes.copy()
        self.phase_setting = phasesetting
        self.PC = program_counter
        if inqueue is None:
            self.in_queue = []   
        else:
            self.in_queue = inqueue
        if outqueue is None:
            self.out_queue = []
        else:
            self.out_queue = outqueue
        self.done_flag = done
        self.in_wait_flag = inwaiting
        self.out_wait_flag = outwaiting
          
    def load_inqueue(self, input):
        """ add an input value to the end of the input queue""" 
        self.in_queue.append(input)
        self.in_wait_flag = 0
    
    def load_phase_setting(self):
        """ add the phase_setting value to the end of the input queue"""
        self.load_inqueue(self.phase_setting)
    
    def run_till(self, inwait=1, outwait=1, done=1):
        """ run computer through code until a flag gets raised"""
        while not((self.in_wait_flag and inwait) or 
                   (self.out_wait_flag and outwait) or 
                   (self.done_flag and done)):
            self.program_step()
    
    def read_out(self):
        """ return a value from the output queue"""
        if not(len(self.out_queue) and self.out_wait_flag):
            return None
        else:
            temp = self.out_queue.pop(0)  
            if not len(self.out_queue):
                self.out_wait_flag = 0
            return temp
        
    def program_step(self):
        """ execute the the opcode at the current program counter, does nothing if waiting on input"""
        opcode = self.incode[self.PC]
        decode = [opcode%100, int(opcode/100)%10, int(opcode/1000)%10,int(opcode/10000)%10]
        par1=0
        par2=0
        par3=0
        if decode[0] == 1:      #opAdd-----------------------
            if decode[1]:           # immediate
                par1 = self.incode[self.PC+1]
            else:
                par1 = self.incode[self.incode[self.PC+1]]
            if decode[2]:           # immediate
                par2 = self.incode[self.PC+2]
            else:
                par2 = self.incode[self.incode[self.PC+2]]
            if decode[3]:           # immediate
                self.incode[self.PC+3] = par1+par2
            else:
                self.incode[self.incode[self.PC+3]] = par1+par2
            self.PC += 4
            
        elif decode[0] == 2:    #opMul-----------------------
            if decode[1]:           # immediate
                par1 = self.incode[self.PC+1]
            else:
                par1 = self.incode[self.incode[self.PC+1]]
            if decode[2]:           # immediate
                par2 = self.incode[self.PC+2]
            else:
                par2 = self.incode[self.incode[self.PC+2]]
            if decode[3]:           # immediate
                self.incode[self.PC+3] = par1*par2
            else:
                self.incode[self.incode[self.PC+3]] = par1*par2
            self.PC += 4
            
        elif decode[0] == 3:    #opSav----------------------- 
            if(self.in_wait_flag or (len(self.in_queue) == 0)):
                self.in_wait_flag = 1
            else:
                par1 = self.in_queue.pop(0)                      
                if decode[1]:           # immediate
                    self.incode[self.PC+1] = par1
                else:
                    self.incode[self.incode[self.PC+1]] = par1
                self.PC += 2
            
        elif decode[0] == 4:    #opPrn------------------------ 
            temp = 0
            if decode[1]:           # immediate
                temp = self.incode[self.PC+1]
            else:
                temp = self.incode[self.incode[self.PC+1]]
            self.out_queue.append(temp)
            self.out_wait_flag = 1
            self.PC += 2
            
        elif decode[0] == 5:    #opJTr------------------------
            if decode[1]:               # immediate
                par1 = self.incode[self.PC+1]
            else:
                par1 = self.incode[self.incode[self.PC+1]]
            if par1:
                if decode[2]:           # immediate
                    self.PC = self.incode[self.PC+2]
                else:
                    self.PC = self.incode[self.incode[self.PC+2]]
            else:
                self.PC += 3
            
        elif decode[0] == 6:    #opJFl------------------------
            if decode[1]:               # immediate
                par1 = self.incode[self.PC+1]
            else:
                par1 = self.incode[self.incode[self.PC+1]]
            if not(par1):
                if decode[2]:           # immediate
                    self.PC = self.incode[self.PC+2]
                else:
                    self.PC = self.incode[self.incode[self.PC+2]]
            else:
                self.PC += 3
                    
        elif decode[0] == 7:    #opLTh------------------------
            if decode[1]:           # immediate
                par1 = self.incode[self.PC+1]
            else:
                par1 = self.incode[self.incode[self.PC+1]]
            if decode[2]:           # immediate
                par2 = self.incode[self.PC+2]
            else:
                par2 = self.incode[self.incode[self.PC+2]]
            out = int(par1 < par2)
            if decode[3]:           # immediate
                self.incode[self.PC+3] = out
            else:
                self.incode[self.incode[self.PC+3]] = out
            self.PC += 4
            
        elif decode[0] == 8:    #opEqu------------------------
            if decode[1]:           # immediate
                par1 = self.incode[self.PC+1]
            else:
                par1 = self.incode[self.incode[self.PC+1]]
            if decode[2]:           # immediate
                par2 = self.incode[self.PC+2]
            else:
                par2 = self.incode[self.incode[self.PC+2]]
            out = int(par1 == par2)
            if decode[3]:           # immediate
                self.incode[self.PC+3] = out
            else:
                self.incode[self.incode[self.PC+3]] = out
            self.PC += 4
            
        elif decode[0] == 99:   #opHlt
            self.done_flag = 1
            
        else:
            raise Exception("invalid opcode") #oh ya i forgot this one
            logger.error('invalid opcode')
        
    def __del__(self):
        pass
        
phaseorderlist = make_permutations(list(range(5,10)))
thrustlist = []

for Phaselist in phaseorderlist:
    amps = []
    for i in range(0,5):
        amps.append(program(incode,Phaselist[i]))
        amps[i].load_phase_setting()
    transfer = 0
    i = 0
    while True:
        if amps[i].done_flag:
            thrustlist.append(transfer)
            break
        amps[i].load_inqueue(transfer)
        amps[i].run_till(outwait=0)
        logger.debug(f"run_till on amps[{i}], ends with flags:{amps[i].in_wait_flag},{amps[i].out_wait_flag},{amps[i].done_flag}")
        # load the output from this into the next amplifier
        transfer = amps[i].read_out()
        i = (i+1)%5
        
maxthrust = max(thrustlist)
phaseorderlist = make_permutations(list(range(5,10)))
maxphase = phaseorderlist[thrustlist.index(maxthrust)]
        

        
        
        
        
        
        
        
        
        
        
        
        
        
        