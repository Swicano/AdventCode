import logging
# we need a logger, a formatter, and a handler
logger = logging.getLogger(__name__)
logger.propagate = False # this is set to false to avoid double messages, not necesarrily the best idea outside pyzo
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler = logging.StreamHandler()
# now we setup each of these to log at the DEBUG level (for now)
logger.setLevel(logging.DEBUG)
handler.setLevel(logging.DEBUG)
# finally we bind them together
handler.setFormatter(formatter)
logger.addHandler(handler)

logger.debug('this is a test log debug message')

from functools import partial

#real input code is too large again, so we make them all files
inputfiletest = 'c:\\users\gfirest\Box Sync\Other shit\Github\AdventCode\Day8inputtest.txt'
 # equals 2 layers 3 x 2 pixels like this
testlayersize = 3*2
'''
Layer 1: 123
         456

Layer 2: 789
         012'''
#real input code 
inputfile = 'c:\\users\gfirest\Box Sync\Other shit\Github\AdventCode\Day8input.txt'
layersize = 25*6  # 25 wide by 6 tall
layers = []
layersflat = []
bestzeros = 999
bestlayer = []

with open(inputfile) as f:
    for chunk in iter(partial(f.read,layersize),'\n'):
        layers.append([int(num) for num in chunk])
        numzeros = layers[-1].count(0)
        logger.debug(f"number of zeros is {numzeros}")
        if numzeros < bestzeros:
            bestzeros = numzeros
            bestlayer = layers[-1]
        
print(bestlayer.count(1)*bestlayer.count(2))

# for part two, we are flattening the layers to see the "top color" of each
#    2 is transparent, 1 is white, 0 is black

# so we want to reslice it all as ONE layer, where each ELEMENT is a list of the depth (aka each layer)
# we're just rearranging our matrix here
resliced = list(zip(*layers))
compressed = [] 
for pixelslice in resliced:
    # if all the pixels are transparent, nothing needs to be done
    if len(pixelslice)==pixelslice.count(2):
        compressed.append(2)
        continue
    index1 = 999
    index0 = 999
    try:
        index0 = pixelslice.index(0)
    except ValueError:
        pass
    try:
        index1 = pixelslice.index(1)
    except ValueError:
        pass
    compressed.append(int(index1 <index0))

# compressed contains the answer, we just need a way to display it...
answer = [ print(x) for x in (zip(*[iter(compressed)]*25))]
# but this doesnt help superly....

compressed = [] 
for pixelslice in resliced:
    # if all the pixels are transparent, nothing needs to be done
    if len(pixelslice)==pixelslice.count(2):
        compressed.append(2)
        continue
    index1 = 999
    index0 = 999
    try:
        index0 = pixelslice.index(0)
    except ValueError:
        pass
    try:
        index1 = pixelslice.index(1)
    except ValueError:
        pass
    if(index1 <index0):
        compressed.append(u"\u25A0")
    else:
        compressed.append(u"\u25A1")
        
answer = [''.join(x) for x in zip(*[iter(compressed)]*25) ]
for line in answer:
    print(line)