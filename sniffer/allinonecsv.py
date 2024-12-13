from scapy.all import rdpcap, Raw
import pandas as pd
import os

dataset_path = "D:/DATASETS/ransomware/PCAP_data"
check = ".pcap"
families = os.listdir(dataset_path)

for i in range(len(families)):
    ransomware_family = families[i]
    family_path = os.path.join(dataset_path, ransomware_family)  
    print(family_path)
    samples = os.listdir(family_path)
    for j in range(len(samples)):
        x = samples[j]
        file_path = os.path.join(family_path, x)  
        if os.path.isfile(file_path) and x.endswith(check):  # Check if it's a file and ends with ".pcap"
            print(f"Processing file: {file_path}")
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
            output_file = os.path.join(family_path, f"{ransomware_family}_with_payload.csv")
            df.to_csv(output_file, index=False)
            print(f"Saved CSV: {output_file}")

