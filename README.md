trafficsimtools
===============

Tools to simulate traffic patterns in IP & Ethernet networks.

This toolbox is being created to help understand the behavior of traffic under some circumstances. 
Two immediate applications are:

1) Bit error rate simulation. This tool started after a work discussion on the correlation between frame size
and error distribution. My guess was that smaller packets would be less affected (as a percentage) than bigger
packets. A tool was developed to help understand this question, using a "Monte Carlo" style simulation.

2) Load sharing simulation. Many network professionals believe that link aggregation or channel bonding can
give them n times the performance of a single link, which isn't really true. This tool helps investigate the
behavior of load sharing algorithms under several traffic loads, and allows to simulate the effect of having
a high concentration of traffic between a limited set of hosts.

Importante note: I'm not a mathemathician, so I knew I couldn't even start to try some mathemathical 
proof regarding these situations. On the other hand I have formal CS education and thus understand 
that dealing with random number generation is far from trivial. Because of this I tried to keep
myself limited to simpler implementations.
