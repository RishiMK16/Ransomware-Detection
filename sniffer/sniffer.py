import struct
import socket

def extract_frame(data):
    dest_mac,src_mac,proto=struct.unpack('! 6s 6s H',data[:14])#! marks tell thst we are treating this as network traffic, how bytes are flowed in traffic is different from how they are stored
    return get_mac(dest_mac),get_mac(src_mac),get_mac(proto), socket.htons(proto),data[14:]

def get_mac(byte_addr):
    bytes_str=map('{:2x}'.format,byte_addr)
    mac_addr=':'.join(bytes_str).upper()
    return mac_addr

def main():
    conn = socket.socket( socket.AF_INET, socket.SOCK_RAW , socket.ntohs(3))

    while True:
        raw_data, addr=conn.recvfrom(65536)
        dest_mac, src_mac, eth_proto, data= extract_frame(raw_data)
        print("\nEthernet Frame:")
        print("Destination : {} , Source : {} , Protocol : {}".format(dest_mac, src_mac, eth_proto))


main()