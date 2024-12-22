from scapy.all import rdpcap, Raw
import pandas as pd
import os


file_path=r"D:\DATASETS\ransomware\Goodware\5ldata.pcapng"
packets = rdpcap(file_path)
data = []
for pkt in packets:
    if 'IP' in pkt:
        payload = None
        if pkt.haslayer(Raw): 
            payload = pkt[Raw].load.hex()
            
            data.append({
                "time_epoch": pkt.time,
                "src_ip": pkt['IP'].src,
                "dst_ip": pkt['IP'].dst,
                "src_port": pkt.sport if pkt.haslayer('TCP') else None,
                "dst_port": pkt.dport if pkt.haslayer('TCP') else None,
                "packet_len": len(pkt),
                "protocol": pkt['IP'].proto,
                "payload": payload
            })
            
df = pd.DataFrame(data)
outpur_path=r"D:\DATASETS\ransomware\Goodware"
output_file = os.path.join( outpur_path, "Goodware_with_payload.csv")
df.to_csv(output_file, index=False)
print(f"Saved CSV: {output_file}")            