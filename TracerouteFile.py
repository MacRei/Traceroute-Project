import re
import sys

def main(dump_filename):
    tcpPackets = {} 
    ttlSummary = {}  
    with open(dump_filename,'r') as f:
        lines = [line.strip() for line in f]
    i = 0
    while i < len(lines):
        line = lines[i]
        if 'proto TCP' in line:
            ts = float(line.split()[0])
            ttl = int(re.search(r'ttl (\d+)', line).group(1))
            pktID = re.search(r'id (\d+)', line).group(1)
            tcpPackets[pktID] = {'timestamp': ts, 'ttl': ttl}
        elif 'proto ICMP' in line:
            tsIcmp = float(line.split()[0])
            if i + 2 < len(lines):
                routerLine = lines[i + 1]
                routerMatch = re.match(r'(\d+\.\d+\.\d+\.\d+) >', routerLine)
                if routerMatch:
                    routerIP = routerMatch.group(1)
                    tcpPayloadLine = lines[i + 2]
                    idMatch = re.search(r'id (\d+)', tcpPayloadLine)
                    if idMatch:
                        pktID = idMatch.group(1)
                        ttl = tcpPackets[pktID]['ttl']
                        rtt = (tsIcmp - tcpPackets[pktID]['timestamp']) * 1000
                        if ttl not in ttlSummary:
                            ttlSummary[ttl] = {'router': routerIP, 'rtt': []}
                        ttlSummary[ttl]['router'] = routerIP
                        ttlSummary[ttl]['rtt'].append(rtt)
            i += 2
        i += 1

    with open('output.txt','w') as out:
        for ttl in sorted(ttlSummary.keys()):
            router = ttlSummary[ttl]['router']
            rtts = ttlSummary[ttl]['rtt']
            while len(rtts) < 3:
                rtts.append(0.0)
            output = f"TTL {ttl}\n{router}\n{rtts[0]:.3f} ms\n{rtts[1]:.3f} ms\n{rtts[2]:.3f} ms\n"
            print(output)
            out.write(output + '\n')

if __name__ == '__main__':
    filename = sys.argv[1] if len(sys.argv) > 1 else 'sampletcpdump.txt'
    main(filename)
