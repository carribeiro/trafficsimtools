"""
Frame Generator

Generates synthetic frames for simulation purposes. Actual payload is not generated. 
Synthetic frames are generated according to a frame distribution table, which tells
the frequency for each frame size. Frames can also have different source/destination 
hashes, which are used for load balancing and other networking simulation scenarios.
"""

import random

FRAMEMIX = 'uniform'

FRAME_DISTRIBUTION_TABLE = {
    'simpleimix': ('count', [(64, 7), (570, 4), (1518, 1)]),
    'imix': ('percentage', [(58, 0.5867), (62, 0.0200), (594, 0.2366), (1518, 0.1567)]),
    'tcpmix': ('percentage', [(90, 0.5867), (92, 0.0200), (594, 0.2366), (1518, 0.1567)]),
    'ipsecmix': ('percentage', [(90, 0.5867), (92, 0.0200), (594, 0.2366), (1418, 0.1567)]),
    'uniform': ('percentage', [(58, 0.1), (220, 0.1), (382, 0.1), (544, 0.1), (706, 0.1), (868, 0.1), (1030, 0.1), (1192, 0.1), (1354, 0.1), (1516, 0.1)]),
}

class FrameClass(object):
    """ Represents the classes of frames, each with a size. Also keeps stats for each frame class """

    def __init__(self, size, weight):
        self.size = size
        self.weight = weight
        self.count = 0
        self.errors = 0
        self.bits = size*8

class Frame(object):
    """ represents a synthetic frame """

    def __init__(self, fclass):
        self.fclass = fclass

    def __repr__(self):
        return "<Frame:%i>" % (self.fclass.size)

def FrameGenerator(framemix=FRAMEMIX, maxframes=0, maxbits=0):

    # create the frame pool from where frame classes are selected
    frame_classes = []
    frame_class_pool = [] 
    disttype, distribution = FRAME_DISTRIBUTION_TABLE[framemix]
    for size, weight in distribution:
        fclass = FrameClass(size, weight)
        frame_classes.append(fclass)
        if disttype == 'count':
            adjustedweight = weight
        else:
            adjustedweight = int(weight * 10000) # 0.01% resolution
        frame_class_pool += [fclass] * adjustedweight

    # frame generator loop
    # TODO: I believe it should be able to return an empty interval after (or before?) each frame;
    #       has implications for the bits_to_go count
    frames_to_go = maxframes
    bits_to_go = maxbits
    loop_forever = (maxframes==0) and (maxbits==0)
    while loop_forever or ((frames_to_go > 0) or (bits_to_go > 0)):
        frame = Frame(random.choice(frame_class_pool))
        frames_to_go -= 1
        bits_to_go -= frame.fclass.bits
        yield frame
