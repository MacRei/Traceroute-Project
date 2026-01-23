# Traceroute-Project
Built a Python program to analyze tcpdump output, correlating TCP and ICMP traffic to map network routes and measure per-hop latency. Applied deep knowledge of TCP/IP and core network protocols (including DNS and DHCP concepts) to diagnose routing behavior and interpret real-world packet data.

<img width="324" height="745" alt="Screenshot 2026-01-23 at 9 24 43 AM" src="https://github.com/user-attachments/assets/4678d167-9542-49c9-90f7-e190e2c446f5" />

This program first takes the traffic network log, opens it and reads it to memory.
As it works through the lines, it searches for "proto TCP", indicating that a TCP packet was sent. It records the TCP packets timestamp, the TTL(Time to live), and ID of the packet.
If it does not find a TCP packet being sent, it looks for "proto ICMP", which usually indicates that a router recieved the packet but the TTL ran out. The program prepares the ICMP response, reads the router's IP address, and finds ID of the TCP packet sent. It can then match the sent packet with the router that replied.
The program calculates the round trip time for the TCP to go to the router and ICMP to come back. It then converts it to miliseconds.
