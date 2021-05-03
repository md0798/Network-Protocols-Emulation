# Network-Protocols-Emulation

1. Go back N :-

Usage description:-

The program takes command line input as follows:- python3 gbnnode.py 1111 2222 5 -p 0.1
The program runs three threads simultaneously, send, receive and data buffer. There is also an additional function for discard packet.

test case:-

python3 gbnnode.py 2222 1111 5 -p 0.1
node> send aaaaaaa
node> [1609020200.238] packet0a sent
[1609020200.238] packet1a sent
[1609020200.238] packet2a sent
[1609020200.238] packet3a sent
[1609020200.238] packet4a sent
[1609020200.248] ACK0 received, window moves to 1
[1609020200.249] ACK0 received, window moves to 1
[1609020200.249] packet5a sent
[1609020200.259] ACK0 received, window moves to 1
[1609020200.264] ACK0 received, window moves to 1
[1609020200.264] ACK0 received, window moves to 1
[1609020200.749] packet1 timeout
[1609020200.749] packet1 a sent
[1609020200.749] packet2 a sent
[1609020200.749] packet3 a sent
[1609020200.749] packet4 a sent
[1609020200.75] packet5 a sent
[1609020200.76] ACK0 received, window moves to 1
[1609020200.76] ACK0 discarded
[1609020200.76] ACK0 received, window moves to 1
[1609020201.25] packet1 timeout
[1609020201.25] packet1 a sent
[1609020201.25] packet2 a sent
[1609020201.25] packet3 a sent
[1609020201.25] packet4 a sent
[1609020201.25] packet5 a sent
[1609020201.261] ACK1 received, window moves to 2
[1609020201.261] ACK2 received, window moves to 3
[1609020201.261] ACK3 received, window moves to 4
[1609020201.261] ACK4 received, window moves to 5
[1609020201.261] ACK5 received, window moves to 6
[1609020201.262] packet6a sent
[1609020201.272] ACK6 received, window moves to 7
[Summary] 1/14 packets dropped, loss rate = 7.143%

python3 gbnnode.py 1111 2222 5 -p 0.1
node> [1609020200.243] packet0a received
[1609020200.243] ACK0 sent, expecting packet1
[1609020200.243] packet1 a discarded
[1609020200.243] packet2a received
[1609020200.254] ACK0 sent, expecting packet 1
[1609020200.254] packet3a received
[1609020200.254] ACK0 sent, expecting packet 1
[1609020200.259] packet4a received
[1609020200.259] ACK0 sent, expecting packet 1
[1609020200.259] packet5a received
[1609020200.259] ACK0 sent, expecting packet 1
[1609020200.754] packet1 a discarded
[1609020200.754] packet2a received
[1609020200.754] ACK0 sent, expecting packet 1
[1609020200.754] packet3a received
[1609020200.755] ACK0 sent, expecting packet 1
[1609020200.755] packet4a received
[1609020200.755] ACK0 sent, expecting packet 1
[1609020200.755] packet5 a discarded
[1609020201.255] packet1a received
[1609020201.255] ACK1 sent, expecting packet2
[1609020201.255] packet2a received
[1609020201.255] ACK2 sent, expecting packet3
[1609020201.255] packet3a received
[1609020201.255] ACK3 sent, expecting packet4
[1609020201.256] packet4a received
[1609020201.256] ACK4 sent, expecting packet5
[1609020201.256] packet5a received
[1609020201.256] ACK5 sent, expecting packet6
[1609020201.267] packet6a received
[1609020201.267] ACK6 sent, expecting packet7
[Summary] 3/17 packets dropped, loss rate = 17.647%



The program keeps going and the loss rate is equal to the packet dropped upon total number of packets sent from the start.


2. DV algorithm :-

Usage description:-

The program takes command line input as follows:- python3 dvnode.py 3333 1111 .5 2222 .2 4444 .5 /  python3 dvnode.py 4444 2222 .8 3333 .5 last
The program uses only one function to send, receive and update the routing table, which finally converges

test case:-

python3 dvnode.py 1111 2222 .1 3333 .5
Routing table received from 2222
Message sent to 2222
Message sent to 3333
[1609020755.0415092] Node 1111 Routing Table
- (0.1) -> Node 2222
- (0.30000000000000004) -> Node 3333; Next hop -> Node 2222
- (0.9) -> Node 4444; Next hop -> Node 2222
Message sent to 2222
Message sent to 3333
Routing table received from 3333
[1609020755.0420613] Node 1111 Routing Table
- (0.1) -> Node 2222
- (0.30000000000000004) -> Node 3333; Next hop -> Node 2222
- (0.9) -> Node 4444; Next hop -> Node 2222
Routing table received from 3333
[1609020755.0426154] Node 1111 Routing Table
- (0.1) -> Node 2222
- (0.30000000000000004) -> Node 3333; Next hop -> Node 2222
- (0.9) -> Node 4444; Next hop -> Node 2222
Routing table received from 2222
[1609020755.0444064] Node 1111 Routing Table
- (0.1) -> Node 2222
- (0.30000000000000004) -> Node 3333; Next hop -> Node 2222
- (0.7999999999999999) -> Node 4444; Next hop -> Node 2222
Message sent to 2222
Message sent to 3333


python3 dvnode.py 2222 1111 .1 3333 .2 4444 .8
Routing table received from 4444
Message sent to 1111
Message sent to 3333
Message sent to 4444
[1609020755.0413053] Node 2222 Routing Table
- (0.1) -> Node 1111
- (0.2) -> Node 3333
- (0.8) -> Node 4444
Routing table received from 1111
[1609020755.0425398] Node 2222 Routing Table
- (0.1) -> Node 1111
- (0.2) -> Node 3333
- (0.8) -> Node 4444
Routing table received from 1111
[1609020755.0439813] Node 2222 Routing Table
- (0.1) -> Node 1111
- (0.2) -> Node 3333
- (0.8) -> Node 4444
Routing table received from 4444
[1609020755.0440786] Node 2222 Routing Table
- (0.1) -> Node 1111
- (0.2) -> Node 3333
- (0.8) -> Node 4444
Routing table received from 3333
[1609020755.0441632] Node 2222 Routing Table
- (0.1) -> Node 1111
- (0.2) -> Node 3333
- (0.7) -> Node 4444; Next hop -> Node 3333
Message sent to 1111
Message sent to 3333
Message sent to 4444
Routing table received from 4444
[1609020755.0447633] Node 2222 Routing Table
- (0.1) -> Node 1111
- (0.2) -> Node 3333
- (0.7) -> Node 4444; Next hop -> Node 3333
Routing table received from 3333
[1609020755.0452664] Node 2222 Routing Table
- (0.1) -> Node 1111
- (0.2) -> Node 3333
- (0.7) -> Node 4444; Next hop -> Node 3333
Routing table received from 4444
[1609020755.0453935] Node 2222 Routing Table
- (0.1) -> Node 1111
- (0.2) -> Node 3333
- (0.7) -> Node 4444; Next hop -> Node 3333
Routing table received from 1111
[1609020755.045484] Node 2222 Routing Table
- (0.1) -> Node 1111
- (0.2) -> Node 3333
- (0.7) -> Node 4444; Next hop -> Node 3333



python3 dvnode.py 3333 1111 .5 2222 .2 4444 .5
Routing table received from 4444
Message sent to 1111
Message sent to 2222
Message sent to 4444
[1609020755.0422869] Node 3333 Routing Table
- (0.5) -> Node 1111
- (0.2) -> Node 2222
- (0.5) -> Node 4444
Routing table received from 2222
[1609020755.0424263] Node 3333 Routing Table
- (0.30000000000000004) -> Node 1111; Next hop -> Node 2222
- (0.2) -> Node 2222
- (0.5) -> Node 4444
Message sent to 1111
Message sent to 2222
Message sent to 4444
Routing table received from 1111
[1609020755.043066] Node 3333 Routing Table
- (0.30000000000000004) -> Node 1111; Next hop -> Node 2222
- (0.2) -> Node 2222
- (0.5) -> Node 4444
Routing table received from 1111
[1609020755.0431755] Node 3333 Routing Table
- (0.30000000000000004) -> Node 1111; Next hop -> Node 2222
- (0.2) -> Node 2222
- (0.5) -> Node 4444
Routing table received from 4444
[1609020755.0432932] Node 3333 Routing Table
- (0.30000000000000004) -> Node 1111; Next hop -> Node 2222
- (0.2) -> Node 2222
- (0.5) -> Node 4444
Routing table received from 4444
[1609020755.0433848] Node 3333 Routing Table
- (0.30000000000000004) -> Node 1111; Next hop -> Node 2222
- (0.2) -> Node 2222
- (0.5) -> Node 4444
Routing table received from 4444
[1609020755.0437832] Node 3333 Routing Table
- (0.30000000000000004) -> Node 1111; Next hop -> Node 2222
- (0.2) -> Node 2222
- (0.5) -> Node 4444
Routing table received from 2222
[1609020755.0449533] Node 3333 Routing Table
- (0.30000000000000004) -> Node 1111; Next hop -> Node 2222
- (0.2) -> Node 2222
- (0.5) -> Node 4444
Routing table received from 1111
[1609020755.0450516] Node 3333 Routing Table
- (0.30000000000000004) -> Node 1111; Next hop -> Node 2222
- (0.2) -> Node 2222
- (0.5) -> Node 4444
 

python3 dvnode.py 4444 2222 .8 3333 .5 last
Message sent to 2222
Message sent to 3333
Routing table received from 2222
[1609020755.0416822] Node 4444 Routing Table
- (0.8) -> Node 2222
- (0.5) -> Node 3333
- (0.9) -> Node 1111; Next hop -> Node 2222
Message sent to 2222
Message sent to 3333
Routing table received from 3333
[1609020755.0427516] Node 4444 Routing Table
- (0.7) -> Node 2222; Next hop -> Node 3333
- (0.5) -> Node 3333
- (0.9) -> Node 1111; Next hop -> Node 2222
Message sent to 2222
Message sent to 3333
Routing table received from 3333
[1609020755.043516] Node 4444 Routing Table
- (0.7) -> Node 2222; Next hop -> Node 3333
- (0.5) -> Node 3333
- (0.8) -> Node 1111; Next hop -> Node 3333
Message sent to 2222
Message sent to 3333
Routing table received from 2222
[1609020755.0447907] Node 4444 Routing Table
- (0.7) -> Node 2222; Next hop -> Node 3333
- (0.5) -> Node 3333
- (0.8) -> Node 1111; Next hop -> Node 3333


