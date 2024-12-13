const Cap = require('cap').Cap;
const decoders = require('cap').decoders;
const PROTOCOL = decoders.PROTOCOL;

const cap = new Cap();
const device = Cap.findDevice('192.168.1.100'); // Replace with your IP address
const filter = 'tcp and port 80'; // BPF filter for HTTP traffic
const bufSize = 10 * 1024 * 1024; // Buffer size (10 MB)
const buffer = Buffer.allocUnsafe(bufSize);

// Open a session on the specified device
const linkType = cap.open(device, filter, bufSize, buffer);

console.log(`Listening on device: ${device}`);

cap.setMinBytes && cap.setMinBytes(0); // For performance tuning if needed

cap.on('packet', (nbytes, trunc) => {
  console.log(`Packet received: ${nbytes} bytes, truncated: ${trunc ? 'yes' : 'no'}`);

  if (linkType === 'ETHERNET') {
    const ret = decoders.Ethernet(buffer);

    console.log(`Ethernet: ${JSON.stringify(ret)}`);

    if (ret.info.type === PROTOCOL.ETHERNET.IPV4) {
      const ipv4 = decoders.IPV4(buffer, ret.offset);

      console.log(`IPv4: ${JSON.stringify(ipv4)}`);

      if (ipv4.info.protocol === PROTOCOL.IP.TCP) {
        const tcp = decoders.TCP(buffer, ipv4.offset);
        console.log(`TCP: ${JSON.stringify(tcp)}`);
      }
    }
  }
});
