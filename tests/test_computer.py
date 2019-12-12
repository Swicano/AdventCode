import computer
import pytest


class Test_inits:
    
    @pytest.mark.parametrize('incode, num2, expected',[(3,5,8),
                  (-2,-2,-4), (-1,5,4), (3,-5,-2), (0,5,5)])	
                  
    def test_init_empty(self):
        with pytest.raises(Exception):
            assert computer.opcomputer() 	
    
    def test_incode_size

# content of test_sample.py
#def func(x):
#    return x + 1


#def test_answer():
#    assert func(4) == 5