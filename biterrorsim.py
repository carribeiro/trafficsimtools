BER = 10**-6
FRAMEMIX = 'uniform'
TOTALTIMESEC = 3000
MSPERTICK = 1
TXBPS = 100000
BITSPERTICK = int(TXBPS / (1000 / MSPERTICK))
TOTALTICKS = int(TOTALTIMESEC * (1000 / MSPERTICK))
ERRORCHANCEPERTICK = BITSPERTICK * BER
NOREPORTS = 20

FRAME_SIZE_DISTRIBUTION = {
    'simpleimix': [(64, 7), (570, 4), (1518, 1)],
    'imix': [(58, 0.5867), (62, 0.0200), (594, 0.2366), (1518, 0.1567)],
    'tcpmix': [(90, 0.5867), (92, 0.0200), (594, 0.2366), (1518, 0.1567)],
    'ipsecmix': [(90, 0.5867), (92, 0.0200), (594, 0.2366), (1418, 0.1567)],
    'uniform': [(58, 0.1), (220, 0.1), (382, 0.1), (544, 0.1), (706, 0.1), (868, 0.1), (1030, 0.1), (1192, 0.1), (1354, 0.1), (1516, 0.1)],
}

class Frame(object):
    pass

class FrameSizeStats(object):
    """ Keeps frame stats per framesize """
    pass

import random

# global status
frames = []
totalerrors = 0

# create the stats per frame size (depends on FRAMEMIX)
framesizestats = []
framepool = []
for i, entry in enumerate(FRAME_SIZE_DISTRIBUTION[FRAMEMIX]):
    size, weight = entry
    fsstat = FrameSizeStats()
    fsstat.size = size
    fsstat.weight = weight
    fsstat.count = 0
    fsstat.errors = 0
    framesizestats.append(fsstat)
    # inserts frames in the framepool for selection according to the adjusted weight
    # this way we can select frames with a very simple "random.choice()" call 
    adjustedweight = int(weight * 10000) # 0.01% resolution
    framepool += [fsstat] * adjustedweight

# time loop, where each tick represents MSPERTICK miliseconds
# TODO: investigate a different way to implement this loop. this implementation
#       has a problem because we leave unused time at the end of the last tick
#       for every packet. a better implementation generates packets in sequence 
#       and increases time depending on the packet size. it should perform better 
#       too (with less iterations)
print("Error chance per ticket", ERRORCHANCEPERTICK)
print("Bits per tick", BITSPERTICK)
lefttotransmit = 0
for tick in range(TOTALTICKS):
    # if not transmitting a frame, generate a new one
    if lefttotransmit <= 0:
        # selects frame size
        fsstat = random.choice(framepool)
        fsstat.count += 1
        frame = Frame()
        frame.sizestats = fsstat
        frame.errors = 0
        frames.append(frame)
        lefttotransmit = frame.sizestats.size*8 # counted in bits
    # check if an error occurs in this tick
    # TODO: should check if lefttotransmit is a fraction of bitspertick 
    #       and adjust error chance accordingly 
    if random.random() < ERRORCHANCEPERTICK:
        frame.errors += 1
        frame.sizestats.errors += 1
        totalerrors += 1
    # transmit bits
    lefttotransmit -= BITSPERTICK * 8 
    # report progress
    if (tick % (TOTALTICKS / NOREPORTS)) == 0:
        print("%i ticks, %i frames, %i errors" % (tick, len(frames), totalerrors))
# prints histogram
for fsstat in framesizestats:
    # TODO: scaling does not work (yet), needs to make a first pass to check 
    #       the biggest percentage & scale accordingly
    framesizepercentage = int(100*fsstat.count/len(frames)) # scales up to 25
    print("%4i: %s (%i frames, %i errors, %6.2f %%)" % (fsstat.size,"*"*framesizepercentage, fsstat.count, fsstat.errors, (fsstat.errors*100.0)/(fsstat.count)))