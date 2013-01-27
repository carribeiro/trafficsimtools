"""
Link Aggregation Simulation

Simulates a link group, composed of BUNDLESIZE links, where all links have the same capacity.
We don't simulate errors (yet), but we can do it in the future (perhaps, by combining this
tool with the biterrorsim tool). Also, this tool is unidirectional; for simulation purposes, 
it doesn't make very much of a difference (assuming links are full duplex of course).

Each size of the link has a number of traffic sources. Packets are generated and allocated
to one of the sources. The packet is transmitted over one of the links in the bundle, depending
on the source. This way we can play with different scenarios, such as one where we have a 
strong concentration of traffic over a single source, compared to a scenario where we have
several traffic sources.

Traffic is also distributed between sources using either a "uniform" or a "power" distribution.
In the "uniform distribution" each source has the same amount of traffic, which is really random
but not representative of real world traffic. The "power distribution" concentrates more traffic 
on a few hosts and is more representative of real world traffic distribution.
"""

