# day 10 has nothing to do with opcodes thank god
# ive also just realised i done goofed by not naming all the previous days day01, 02, etc


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

inputfile = 'c:\\users\gfirest\Box Sync\Other shit\Github\AdventCode\Day10input.txt'
inputfiletest1 = 'c:\\users\gfirest\Box Sync\Other shit\Github\AdventCode\Day10inputtest1.txt'
inputfiletest2 = 'c:\\users\gfirest\Box Sync\Other shit\Github\AdventCode\Day10inputtest2.txt'
inputfiletest3 = 'c:\\users\gfirest\Box Sync\Other shit\Github\AdventCode\Day10inputtest3.txt'
inputfiletest4 = 'c:\\users\gfirest\Box Sync\Other shit\Github\AdventCode\Day10inputtest4.txt'