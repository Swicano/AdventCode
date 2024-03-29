import computer
import pytest


class Test_inits:

    def test_init_empty(self):
        with pytest.raises(Exception):
            assert computer.opcomputer() 	
            
    
    @pytest.mark.parametrize(['incode','phasesetting'] ,[([3,5,8],0), ([-2,-2,-4],0), ([-1,5,4],0), 
                                ([3,-5,-2],0), ([0,5,5],0),([x**2 for x in range(15000)],0),
                                (['a','b',1,2,3,4,5,[9**9**3,2,0]],0),([9**9**3,2,0],0)] )	
    def test_incode_size(self, incode, phasesetting):
        comp = computer.opcomputer(incode, phasesetting=phasesetting)
        print(phasesetting)
        assert len(comp.incode) == max(len(incode),10000)
        

class Test_ParamMode:
    
    @pytest.fixture
    def inited_opcomp(self):
        ''' an opcomp with a nonsense code, 0 RB, 0 PC'''
        return computer.opcomputer( [1,2,3,4,5,6,7,8,9,10,11,12,99 ] )
    
    @pytest.fixture
    def inited_opcompRB(self):
        ''' an opcomp with a nonsense code, 3 RB, 0 PC'''
        return computer.opcomputer( [1,2,3,4,5,6,7,8,9,10,11,12,99 ],relative_base=3 )
        
    # check the read parameter function
    
    @pytest.mark.parametrize(['param','expected'],[(999,0),(1,2),(9,10),(-1,0),(13,0),(0,1),(12,99)])
    def test_posread(self,param,expected, inited_opcomp):
        ''' checks that read_param position mode works'''
        assert inited_opcomp.param_read(0, param) == expected
        
    @pytest.mark.parametrize(['param','expected'],[(999,999),(1,1),(9,9),(-1,-1),(13,13),(0,0),(12,12)])
    def test_immread(self,param,expected, inited_opcomp):
        ''' checks that read_param immediate mode works'''
        assert inited_opcomp.param_read(1, param) == expected
        
    @pytest.mark.parametrize(['param','expected'],[(999,0),(1,5),(9,99),(-1,3),(13,0),(0,4),(12,0)])
    def test_relread(self,param,expected, inited_opcompRB):
        ''' check that read_param relative mode works'''
        assert inited_opcompRB.param_read(2, param) == expected
        
    # check the write parameter function
    # I dont like that read and write param dont match...
    
    labels = ['param','expected']
    datas = [(999,0),(1,3),(9,5),(-1,7),(13,3453454566676),(0,'a'),(12,23)]
    
    @pytest.mark.parametrize(labels,datas)
    def test_poswrite(self,param,expected, inited_opcomp):
        ''' checks that write_param position mode works'''
        inited_opcomp.param_write(0, param, expected)
        assert inited_opcomp.param_read(0, inited_opcomp.incode[param]) == expected

    @pytest.mark.parametrize(labels,datas)
    def test_immwrite(self,param,expected, inited_opcomp):
        ''' checks that write_param immediate mode works'''
        inited_opcomp.param_write(1, param, expected)
        assert inited_opcomp.param_read(1, inited_opcomp.incode[param]) == expected
    
    @pytest.mark.parametrize(labels,datas)
    def test_relwrite(self,param,expected, inited_opcomp):
        ''' checks that write_param Relative mode works'''
        inited_opcomp.param_write(2, param, expected)
        assert inited_opcomp.param_read(2, inited_opcomp.incode[param]) == expected
    
    @pytest.mark.parametrize(labels,datas)    
    def test_relwriteRB(self,param,expected, inited_opcompRB):
        ''' checks that write_param immediate mode works'''
        inited_opcompRB.param_write(2, param, expected)
        assert inited_opcompRB.param_read(2, inited_opcompRB.incode[param]) == expected
        
class Test_ops:
    ''' test the individual operations'''
    
    # add operation has 3 parameters, so
    # PC: 01 for addition, and 000 up to 222 prefixed on that for imm, pos, or rel.
    #     par3mode par2mode par1mode opadd , par1 , par2, par3
    #       0/1/2   0/1/2    0/1/2    01   , x ,     y  ,  z
    #  easiest to test is immediate mode:
    #     11101, 12, 12, 13 -> 11101, 12, 12, 24
 
    labels = ['in_code','out_loc', 'out_val']
    datas = [([11101,12,12,13], 3, 24),
             ([11101,12,-12,13], 3, 0),
             ([11101,12,12,'a'], 3, 24),
             ([    1,4,5,13,1000,888,23,55,732,34,246,91,-4], 13, 1888),    # 1000 + 888
             ([  101,4,5,13,1000,888,23,55,732,34,246,91,-4], 13,  892),    #    4 + 888
             ([  201,4,5,13,1000,888,23,55,732,34,246,91,-4], 13,  943),    #   55 + 888
             ([ 1001,4,5,13,1000,888,23,55,732,34,246,91,-4], 13, 1005),    # 1000 + 5
             ([ 1101,4,5,13,1000,888,23,55,732,34,246,91,-4], 13,    9),    #    4 + 5
             ([ 1201,4,5,13,1000,888,23,55,732,34,246,91,-4], 13,   60),    #   55 + 5
             ([ 2001,4,5,13,1000,888,23,55,732,34,246,91,-4], 13, 1732),    # 1000 + 732
             ([ 2101,4,5,13,1000,888,23,55,732,34,246,91,-4], 13,  736),    #    4 + 732
             ([ 2201,4,5,13,1000,888,23,55,732,34,246,91,-4], 13,  787),    #   55 + 732
             ([10001,4,5,13,1000,888,23,55,732,34,246,91,-4],  3, 1888),    # 1000 + 888
             ([10101,4,5,13,1000,888,23,55,732,34,246,91,-4],  3,  892),    #    4 + 888
             ([10201,4,5,13,1000,888,23,55,732,34,246,91,-4],  3,  943),    #   55 + 888
             ([11001,4,5,13,1000,888,23,55,732,34,246,91,-4],  3, 1005),    # 1000 +   5
             ([11101,4,5,13,1000,888,23,55,732,34,246,91,-4],  3,    9),    #    4 +   5
             ([11201,4,5,13,1000,888,23,55,732,34,246,91,-4],  3,   60),    #   55 +   5
             ([12001,4,5,13,1000,888,23,55,732,34,246,91,-4],  3, 1732),    # 1000 + 732
             ([12101,4,5,13,1000,888,23,55,732,34,246,91,-4],  3,  736),    #    4 + 732
             ([12201,4,5,13,1000,888,23,55,732,34,246,91,-4],  3,  787),    #   55 + 732
             ([20001,4,5,13,1000,888,23,55,732,34,246,91,-4], 16, 1888),    # 1000 + 888
             ([20101,4,5,13,1000,888,23,55,732,34,246,91,-4], 16,  892),    #    4 + 888
             ([20201,4,5,13,1000,888,23,55,732,34,246,91,-4], 16,  943),    #   55 + 888
             ([21001,4,5,13,1000,888,23,55,732,34,246,91,-4], 16, 1005),    # 1000 +   5
             ([21101,4,5,13,1000,888,23,55,732,34,246,91,-4], 16,    9),    #    4 +   5
             ([21201,4,5,13,1000,888,23,55,732,34,246,91,-4], 16,   60),    #   55 +   5
             ([22001,4,5,13,1000,888,23,55,732,34,246,91,-4], 16, 1732),    # 1000 + 732
             ([22101,4,5,13,1000,888,23,55,732,34,246,91,-4], 16,  736),    #    4 + 732
             ([22201,4,5,13,1000,888,23,55,732,34,246,91,-4], 16,  787)     #   55 + 732
               ]
    
    @pytest.mark.parametrize(labels,datas)
    def test_opAdd(self,in_code, out_loc, out_val):
        comp = computer.opcomputer( in_code )
        comp.RB = 3
        comp.compute_step()
        assert comp.incode[out_loc] == out_val
        assert comp.PC == 4
        
    # test multiply
    labels = ['in_code','out_loc', 'out_val']
    datas = [([11102,12,12,13], 3, 12*12),
             ([11102,12,-12,13], 3, -12*12),
             ([11102,12,12,'a'], 3, 12*12),
             ([    2,4,5,13,1000,888,23,55,732,34,246,91,-4], 13, 1000 * 888),    # 1000 + 888
             ([  102,4,5,13,1000,888,23,55,732,34,246,91,-4], 13,    4 * 888),    #    4 + 888
             ([  202,4,5,13,1000,888,23,55,732,34,246,91,-4], 13,   55 * 888),    #   55 + 888
             ([ 1002,4,5,13,1000,888,23,55,732,34,246,91,-4], 13, 1000 *   5),    # 1000 + 5
             ([ 1102,4,5,13,1000,888,23,55,732,34,246,91,-4], 13,    4 *   5),    #    4 + 5
             ([ 1202,4,5,13,1000,888,23,55,732,34,246,91,-4], 13,   55 *   5),    #   55 + 5
             ([ 2002,4,5,13,1000,888,23,55,732,34,246,91,-4], 13, 1000 * 732),    # 1000 + 732
             ([ 2102,4,5,13,1000,888,23,55,732,34,246,91,-4], 13,    4 * 732),    #    4 + 732
             ([ 2202,4,5,13,1000,888,23,55,732,34,246,91,-4], 13,   55 * 732),    #   55 + 732
             ([10002,4,5,13,1000,888,23,55,732,34,246,91,-4],  3, 1000 * 888),    # 1000 + 888
             ([10102,4,5,13,1000,888,23,55,732,34,246,91,-4],  3,    4 * 888),    #    4 + 888
             ([10202,4,5,13,1000,888,23,55,732,34,246,91,-4],  3,   55 * 888),    #   55 + 888
             ([11002,4,5,13,1000,888,23,55,732,34,246,91,-4],  3, 1000 *   5),    # 1000 +   5
             ([11102,4,5,13,1000,888,23,55,732,34,246,91,-4],  3,    4 *   5),    #    4 +   5
             ([11202,4,5,13,1000,888,23,55,732,34,246,91,-4],  3,   55 *   5),    #   55 +   5
             ([12002,4,5,13,1000,888,23,55,732,34,246,91,-4],  3, 1000 * 732),    # 1000 + 732
             ([12102,4,5,13,1000,888,23,55,732,34,246,91,-4],  3,    4 * 732),    #    4 + 732
             ([12202,4,5,13,1000,888,23,55,732,34,246,91,-4],  3,   55 * 732),    #   55 + 732
             ([20002,4,5,13,1000,888,23,55,732,34,246,91,-4], 16, 1000 * 888),    # 1000 + 888
             ([20102,4,5,13,1000,888,23,55,732,34,246,91,-4], 16,    4 * 888),    #    4 + 888
             ([20202,4,5,13,1000,888,23,55,732,34,246,91,-4], 16,   55 * 888),    #   55 + 888
             ([21002,4,5,13,1000,888,23,55,732,34,246,91,-4], 16, 1000 *   5),    # 1000 +   5
             ([21102,4,5,13,1000,888,23,55,732,34,246,91,-4], 16,    4 *   5),    #    4 +   5
             ([21202,4,5,13,1000,888,23,55,732,34,246,91,-4], 16,   55 *   5),    #   55 +   5
             ([22002,4,5,13,1000,888,23,55,732,34,246,91,-4], 16, 1000 * 732),    # 1000 + 732
             ([22102,4,5,13,1000,888,23,55,732,34,246,91,-4], 16,    4 * 732),    #    4 + 732
             ([22202,4,5,13,1000,888,23,55,732,34,246,91,-4], 16,   55 * 732)     #   55 + 732
               ]
    
    @pytest.mark.parametrize(labels,datas)
    def test_opMul(self,in_code, out_loc, out_val):
        comp = computer.opcomputer( in_code )		
        comp.RB = 3
        comp.compute_step()
        assert comp.incode[out_loc] == out_val
        assert comp.PC == 4
    
    
    # Test save
    labels = ['in_code','sav_loc', 'sav_val']
    datas = [([    3,4,5,13,1000,888,23,55,732,34,246,91,-4],  4, 1643216813216),  
             ([  103,4,5,13,1000,888,23,55,732,34,246,91,-4],  1,    4 * 888),     
             ([  103,4,5,13,1000,888,23,55,732,34,246,91,-4],  1,    []),
             ([  103,4,5,13,1000,888,23,55,732,34,246,91,-4],  1,   'b'),        
             ([  203,4,5,13,1000,888,23,55,732,34,246,91,-4],  7,   55 * 888),    
               ]
    
    @pytest.mark.parametrize(labels,datas)
    def test_opSav(self,in_code, sav_loc, sav_val):
        comp = computer.opcomputer( in_code )
        comp.RB = 3
        comp.load_inqueue(sav_val)
        comp.compute_step()
        assert comp.incode[sav_loc] == sav_val
        assert comp.PC == 2
        
    
    # Test print
    labels = ['in_code', 'prn_val']
    datas = [([    4,4,5,13,1000,888,23,55,732,34,246,91,-4], 1000),  
             ([  104,4,5,13,1000,888,23,55,732,34,246,91,-4],  4),           
             ([  204,4,5,13,1000,888,23,55,732,34,246,91,-4],  55),   
               ]
    
    @pytest.mark.parametrize(labels,datas)
    def test_opPrn(self,in_code, prn_val):
        comp = computer.opcomputer( in_code )
        comp.RB = 3
        comp.compute_step()
        assert comp.out_wait_flag == 1
        assert comp.read_output() == prn_val
        assert comp.PC == 2
        assert comp.out_wait_flag == 0
   
   
    # Test jump ops
    labels = ['in_code', 'expected_PC']
    datas = [([    5,4,5,13,1000,888,23,55,732,34,246,91,-4], 888),    # read pos 4, true, PC= 888
             ([  105,4,5,13,1000,888,23,55,732,34,246,91,-4], 888),    # read 4,     true, PC= 888
             ([  205,4,5,13,1000,888,23,55,732,34,246,91,-4], 888),    # read pos 7, true, PC= 888
             ([ 1005,4,5,13,1000,888,23,55,732,34,246,91,-4],   5),    # read pos 4, true, PC= 5
             ([ 1105,4,5,13,1000,888,23,55,732,34,246,91,-4],   5),    # read 4,     true, PC= 5 
             ([ 1205,4,5,13,1000,888,23,55,732,34,246,91,-4],   5),    # read pos 7, true, PC= 5
             ([ 2005,4,5,13,1000,888,23,55,732,34,246,91,-4], 732),    # read pos 4, true, PC= 732
             ([ 2105,4,5,13,1000,888,23,55,732,34,246,91,-4], 732),    # read 4,     true, PC= 732
             ([ 2205,4,5,13,1000,888,23,55,732,34,246,91,-4], 732),    # read pos 7, true, PC= 732
             ([    6,4,5,13,1000,888,23,55,732,34,246,91,-4],   3),    # read pos 4, true, PC= 3
             ([  106,4,5,13,1000,888,23,55,732,34,246,91,-4],   3),    # read 4,     true, PC= 3
             ([  206,4,5,13,1000,888,23,55,732,34,246,91,-4],   3),    # read pos 7, true, PC= 3
             ([ 1006,4,5,13,1000,888,23,55,732,34,246,91,-4],   3),    # read pos 4, true, PC= 3
             ([ 1106,4,5,13,1000,888,23,55,732,34,246,91,-4],   3),    # read 4,     true, PC= 3
             ([ 1206,4,5,13,1000,888,23,55,732,34,246,91,-4],   3),    # read pos 7, true, PC= 3
             ([ 2006,4,5,13,1000,888,23,55,732,34,246,91,-4],   3),    # read pos 4, true, PC= 3
             ([ 2106,4,5,13,1000,888,23,55,732,34,246,91,-4],   3),    # read 4      true, PC= 3
             ([ 2206,4,5,13,1000,888,23,55,732,34,246,91,-4],   3),    # read pos 7, true, PC= 3
             ([    6,4,5,13,   0,888,23,55,732,34,246,91,-4], 888),    # read pos 4, false, PC= 888
             ([  106,0,5,13,1000,888,23,55,732,34,246,91,-4], 888),    # read 4,     false, PC= 888
             ([  206,4,5,13,1000,888,23, 0,732,34,246,91,-4], 888),    # read pos 7, false, PC= 888
             ([ 1006,4,5,13,   0,888,23,55,732,34,246,91,-4],   5),    # read pos 4, false, PC= 5
             ([ 1106,0,5,13,1000,888,23,55,732,34,246,91,-4],   5),    # read 4,     false, PC= 5 
             ([ 1206,4,5,13,1000,888,23, 0,732,34,246,91,-4],   5),    # read pos 7, false, PC= 5
             ([ 2006,4,5,13,   0,888,23,55,732,34,246,91,-4], 732),    # read pos 4, false, PC= 732
             ([ 2106,0,5,13,1000,888,23,55,732,34,246,91,-4], 732),    # read 4,     false, PC= 732
             ([ 2206,4,5,13,1000,888,23, 0,732,34,246,91,-4], 732),    # read pos 7, false, PC= 732
             ([    5,4,5,13,   0,888,23,55,732,34,246,91,-4],   3),    # read pos 4, false, PC= 3
             ([  105,0,5,13,1000,888,23,55,732,34,246,91,-4],   3),    # read 4,     false, PC= 3
             ([  205,4,5,13,1000,888,23, 0,732,34,246,91,-4],   3),    # read pos 7, false, PC= 3
             ([ 1005,4,5,13,   0,888,23,55,732,34,246,91,-4],   3),    # read pos 4, false, PC= 3
             ([ 1105,0,5,13,1000,888,23,55,732,34,246,91,-4],   3),    # read 4      false, PC= 3
             ([ 1205,4,5,13,1000,888,23, 0,732,34,246,91,-4],   3),    # read pos 7, false, PC= 3
             ([ 2005,4,5,13,   0,888,23,55,732,34,246,91,-4],   3),    # read pos 4, false, PC= 3
             ([ 2105,0,5,13,1000,888,23,55,732,34,246,91,-4],   3),    # read 4      false, PC= 3
             ([ 2205,4,5,13,1000,888,23, 0,732,34,246,91,-4],   3),    # read pos 7, false, PC= 3

               ]
    
    @pytest.mark.parametrize(labels,datas)
    def test_opJTrJfl(self, in_code, expected_PC ):
        comp = computer.opcomputer( in_code )
        comp.RB = 3
        comp.compute_step()
        assert comp.PC == expected_PC
        
    # test comparison ops
    labels = ['in_code', 'sav_loc','sav_val']
    datas = [([    7,4,5,13,1000,888,23,55,732,34,246,91,-4], 13, 1000 < 888),    # 1000 + 888
             ([  107,4,5,13,1000,888,23,55,732,34,246,91,-4], 13,    4 < 888),    #    4 + 888
             ([  207,4,5,13,1000,888,23,55,732,34,246,91,-4], 13,   55 < 888),    #   55 + 888
             ([ 1007,4,5,13,1000,888,23,55,732,34,246,91,-4], 13, 1000 <   5),    # 1000 + 5
             ([ 1107,4,5,13,1000,888,23,55,732,34,246,91,-4], 13,    4 <   5),    #    4 + 5
             ([ 1207,4,5,13,1000,888,23,55,732,34,246,91,-4], 13,   55 <   5),    #   55 + 5
             ([ 2007,4,5,13,1000,888,23,55,732,34,246,91,-4], 13, 1000 < 732),    # 1000 + 732
             ([ 2107,4,5,13,1000,888,23,55,732,34,246,91,-4], 13,    4 < 732),    #    4 + 732
             ([ 2207,4,5,13,1000,888,23,55,732,34,246,91,-4], 13,   55 < 732),    #   55 + 732
             ([10007,4,5,13,1000,888,23,55,732,34,246,91,-4],  3, 1000 < 888),    # 1000 + 888
             ([10107,4,5,13,1000,888,23,55,732,34,246,91,-4],  3,    4 < 888),    #    4 + 888
             ([10207,4,5,13,1000,888,23,55,732,34,246,91,-4],  3,   55 < 888),    #   55 + 888
             ([11007,4,5,13,1000,888,23,55,732,34,246,91,-4],  3, 1000 <   5),    # 1000 +   5
             ([11107,4,5,13,1000,888,23,55,732,34,246,91,-4],  3,    4 <   5),    #    4 +   5
             ([11207,4,5,13,1000,888,23,55,732,34,246,91,-4],  3,   55 <   5),    #   55 +   5
             ([12007,4,5,13,1000,888,23,55,732,34,246,91,-4],  3, 1000 < 732),    # 1000 + 732
             ([12107,4,5,13,1000,888,23,55,732,34,246,91,-4],  3,    4 < 732),    #    4 + 732
             ([12207,4,5,13,1000,888,23,55,732,34,246,91,-4],  3,   55 < 732),    #   55 + 732
             ([20007,4,5,13,1000,888,23,55,732,34,246,91,-4], 16, 1000 < 888),    # 1000 + 888
             ([20107,4,5,13,1000,888,23,55,732,34,246,91,-4], 16,    4 < 888),    #    4 + 888
             ([20207,4,5,13,1000,888,23,55,732,34,246,91,-4], 16,   55 < 888),    #   55 + 888
             ([21007,4,5,13,1000,888,23,55,732,34,246,91,-4], 16, 1000 <   5),    # 1000 +   5
             ([21107,4,5,13,1000,888,23,55,732,34,246,91,-4], 16,    4 <   5),    #    4 +   5
             ([21207,4,5,13,1000,888,23,55,732,34,246,91,-4], 16,   55 <   5),    #   55 +   5
             ([22007,4,5,13,1000,888,23,55,732,34,246,91,-4], 16, 1000 < 732),    # 1000 + 732
             ([22107,4,5,13,1000,888,23,55,732,34,246,91,-4], 16,    4 < 732),    #    4 + 732
             ([22207,4,5,13,1000,888,23,55,732,34,246,91,-4], 16,   55 < 732),
             ([    8,4,5,13,1000,888,23,55,732,34,246,91,-4], 13, 1000 == 888),    # 1000 + 888
             ([  108,4,5,13,1000,888,23,55,732,34,246,91,-4], 13,    4 == 888),    #    4 + 888
             ([  208,4,5,13,1000,888,23,55,732,34,246,91,-4], 13,   55 == 888),    #   55 + 888
             ([ 1008,4,5,13,1000,888,23,55,732,34,246,91,-4], 13, 1000 ==   5),    # 1000 + 5
             ([ 1108,4,5,13,1000,888,23,55,732,34,246,91,-4], 13,    4 ==   5),    #    4 + 5
             ([ 1208,4,5,13,1000,888,23,55,732,34,246,91,-4], 13,   55 ==   5),    #   55 + 5
             ([ 2008,4,5,13,1000,888,23,55,732,34,246,91,-4], 13, 1000 == 732),    # 1000 + 732
             ([ 2108,4,5,13,1000,888,23,55,732,34,246,91,-4], 13,    4 == 732),    #    4 + 732
             ([ 2208,4,5,13,1000,888,23,55,732,34,246,91,-4], 13,   55 == 732),    #   55 + 732
             ([10008,4,5,13,1000,888,23,55,732,34,246,91,-4],  3, 1000 == 888),    # 1000 + 888
             ([10108,4,5,13,1000,888,23,55,732,34,246,91,-4],  3,    4 == 888),    #    4 + 888
             ([10208,4,5,13,1000,888,23,55,732,34,246,91,-4],  3,   55 == 888),    #   55 + 888
             ([11008,4,5,13,1000,888,23,55,732,34,246,91,-4],  3, 1000 ==   5),    # 1000 +   5
             ([11108,4,5,13,1000,888,23,55,732,34,246,91,-4],  3,    4 ==   5),    #    4 +   5
             ([11208,4,5,13,1000,888,23,55,732,34,246,91,-4],  3,   55 ==   5),    #   55 +   5
             ([12008,4,5,13,1000,888,23,55,732,34,246,91,-4],  3, 1000 == 732),    # 1000 + 732
             ([12108,4,5,13,1000,888,23,55,732,34,246,91,-4],  3,    4 == 732),    #    4 + 732
             ([12208,4,5,13,1000,888,23,55,732,34,246,91,-4],  3,   55 == 732),    #   55 + 732
             ([20008,4,5,13,1000,888,23,55,732,34,246,91,-4], 16, 1000 == 888),    # 1000 + 888
             ([20108,4,5,13,1000,888,23,55,732,34,246,91,-4], 16,    4 == 888),    #    4 + 888
             ([20208,4,5,13,1000,888,23,55,732,34,246,91,-4], 16,   55 == 888),    #   55 + 888
             ([21008,4,5,13,1000,888,23,55,732,34,246,91,-4], 16, 1000 ==   5),    # 1000 +   5
             ([21108,4,5,13,1000,888,23,55,732,34,246,91,-4], 16,    4 ==   5),    #    4 +   5
             ([21208,4,5,13,1000,888,23,55,732,34,246,91,-4], 16,   55 ==   5),    #   55 +   5
             ([22008,4,5,13,1000,888,23,55,732,34,246,91,-4], 16, 1000 == 732),    # 1000 + 732
             ([22108,4,5,13,1000,888,23,55,732,34,246,91,-4], 16,    4 == 732),    #    4 + 732
             ([22208,4,5,13,1000,888,23,55,732,34,246,91,-4], 16,   55 == 732)
            ]   
    
    @pytest.mark.parametrize(labels,datas)
    def test_opLthEqu(self, in_code, sav_loc, sav_val ):
        comp = computer.opcomputer( in_code )
        comp.RB = 3
        comp.compute_step()
        assert comp.incode[sav_loc] == sav_val
        assert comp.PC == 4
        
    # test the adjust relative base
    labels = ['in_code', 'expectedRB']
    datas = [([    9,4,5,13,1000,888,23,55,732,34,246,91,-4], 1003),  
             ([  109,4,5,13,1000,888,23,55,732,34,246,91,-4],  7),           
             ([  209,4,5,13,1000,888,23,55,732,34,246,91,-4],  58),   
               ]
    
    @pytest.mark.parametrize(labels,datas)
    def test_opARB(self,in_code, expectedRB):
        comp = computer.opcomputer( in_code )
        comp.RB = 3
        comp.compute_step()
        assert comp.RB ==  expectedRB
        assert comp.PC == 2
    
    # test the halt op

# content of test_sample.py
#def func(x):
#    return x + 1


#def test_answer():
#    assert func(4) == 5