# current configuration covers Day 9

# add a new opcode mode, relative mode, and a base to refer to. RB, relative base

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

class opcomputer:
    """creates an opcode-computer object with an input and ouput queue"""
    def __init__(self, incodes, phasesetting=0, program_counter=0, inqueue=None,
                  outqueue = None, done=0, inwaiting=0, outwaiting=0, relative_base=0):
        # with this we should be able to recreate the state of a program at any point.
        self.incode = [0 for x in range(0,10000)]
        self.incode[0:len(incodes)] = incodes.copy()
        self.phase_setting = phasesetting
        self.PC = program_counter
        self.RB = relative_base
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
    
    def status(self):
        """reads the current flag situation and responds"""
        # todo
        return None
          
    def load_inqueue(self, input):
        """ add an input value to the end of the input queue""" 
        self.in_queue.append(input)
        self.in_wait_flag = 0
    
    def load_phase_setting(self):
        """ add the phase_setting value to the end of the input queue"""
        self.load_inqueue(self.phase_setting)
    
    def run_until(self, inwait=1, outwait=1, done=1):
        """ run computer through code until a flag gets raised, unless that flag has been set to 0"""
        while not((self.in_wait_flag and inwait) or 
                   (self.out_wait_flag and outwait) or 
                   (self.done_flag and done)):
            self.compute_step()
    
    def read_output(self):
        """ return a value from the output queue"""
        if not(len(self.out_queue) and self.out_wait_flag):
            return None
        else:
            temp = self.out_queue.pop(0)  
            if not len(self.out_queue):
                self.out_wait_flag = 0
            return temp
            
    def param_read(self, mode, param):
        # position mode, where the value =  code[parameter]
        if mode == 0: 
            return self.incode[param]
        elif mode == 1: # immediate mode, where value = parameter
            return param
        elif mode == 2: # relative mode the value = code[rel_base+parameter]
            return self.incode[param+self.RB]
        else:
            return none
            
    def param_write(self, mode, mem_loc, value):
        # position mode, where the value =  code[parameter]
        if mode == 0: 
            self.incode[ self.incode[mem_loc] ] = value
        elif mode == 1: # immediate mode, where value = parameter
            self.incode[mem_loc] = value
        elif mode == 2: # relative mode the value = code[rel_base+parameter]
            self.incode[ self.incode[mem_loc]+self.RB] = value
        else:
            raise Exception("invalid parameter mode") #oh ya i forgot this one
            logger.error('invalid parameter mode')
            
            
    def compute_step(self):
        """ execute the the opcode at the current program counter, does nothing if waiting on input"""
        opcode = self.incode[self.PC]
        decode = [opcode%100, int(opcode/100)%10, int(opcode/1000)%10,int(opcode/10000)%10]
        par1=0
        par2=0
        par3=0
        if decode[0] == 1:      #opAdd-----------------------
            par1 = self.param_read( decode[1], self.incode[self.PC+1] )
            par2 = self.param_read( decode[2], self.incode[self.PC+2] )
            self.param_write( decode[3], self.PC+3, par1+par2)
            self.PC += 4
            
        elif decode[0] == 2:    #opMul-----------------------
            par1 = self.param_read( decode[1], self.incode[self.PC+1] )
            par2 = self.param_read( decode[2], self.incode[self.PC+2] )
            self.param_write( decode[3], self.PC+3, par1*par2)
            self.PC += 4
            
        elif decode[0] == 3:    #opSav----------------------- 
            if(self.in_wait_flag or (len(self.in_queue) == 0)):
                self.in_wait_flag = 1
            else:
                par1 = self.in_queue.pop(0)   
                self.param_write( decode[1], self.PC+1, par1)                   
                self.PC += 2
            
        elif decode[0] == 4:    #opPrn------------------------ 
            temp =  self.param_read( decode[1], self.incode[self.PC+1] )
            self.out_queue.append(temp)
            self.out_wait_flag = 1
            self.PC += 2
            
        elif decode[0] == 5:    #opJTr------------------------
            par1 = self.param_read( decode[1], self.incode[self.PC+1] )
            if par1: # thus we jump
                self.PC = self.param_read( decode[2], self.incode[self.PC+2] )  
            else:
                self.PC += 3
            
        elif decode[0] == 6:    #opJFl------------------------
            par1 = self.param_read( decode[1], self.incode[self.PC+1] )
            if not(par1): # par1 false, thus we jump
                self.PC = self.param_read( decode[2], self.incode[self.PC+2] )  
            else:
                self.PC += 3
                    
        elif decode[0] == 7:    #opLTh------------------------
            par1 = self.param_read( decode[1], self.incode[self.PC+1] )
            par2 = self.param_read( decode[2], self.incode[self.PC+2] )
            self.param_write( decode[3], self.PC+3, int(par1 < par2))
            self.PC += 4
            
        elif decode[0] == 8:    #opEqu------------------------
            par1 = self.param_read( decode[1], self.incode[self.PC+1] )
            par2 = self.param_read( decode[2], self.incode[self.PC+2] )
            self.param_write( decode[3], self.PC+3, int(par1 == par2))
            self.PC += 4
        
        elif decode[0] == 9	:    #opARB------------------------  
            self.RB += self.param_read( decode[1], self.incode[self.PC+1] )
            self.PC += 2
            
        elif decode[0] == 99:   #opHlt
            self.done_flag = 1
            
        else:
            raise Exception("invalid opcode") #oh ya i forgot this one
            logger.error('invalid opcode')
        
    def __del__(self):
        pass