# Virtual eXtensible Local Area Network (VXLAN)
# https://tools.ietf.org/html/draft-mahalingam-dutt-dcops-vxlan-06

# scapy.contrib.description = VXLAN
# scapy.contrib.status = loads

from scapy.packet import *
from scapy.fields import *
from scapy.all import * # Otherwise failing at the UDP reference below

class VXLAN(Packet):
    name = "VXLAN"
    fields_desc = [ FlagsField("flags", 0x08, 8, ['R', 'R', 'R', 'I', 'R', 'R', 'R', 'R']),
                    X3BytesField("reserved1", 0x000000),
                    ThreeBytesField("vni", 0),
                    XByteField("reserved2", 0x00)]

    def mysummary(self):
        return self.sprintf("VXLAN (vni=%VXLAN.vni%)")

bind_layers(UDP, VXLAN, dport=4789)
bind_layers(VXLAN, Ether)

class VXLAN_GPE(Packet):
    name = "VXLAN_GPE"
    fields_desc = [ FlagsField("flags", 0x18, 8, ['R', 'R', 'R', 'I', 'P', 'R', 'R', 'R']),
                    XShortField("reserved1", 0x0000),
                    XByteField("next_proto", 0x03),
                    ThreeBytesField("vni", 0),
                    XByteField("reserved2", 0x00)]

    def mysummary(self):
        return self.sprintf("VXLAN_GPE (vni=%VXLAN_GPE.vni%)")
    
    def guess_payload_class(self, payload):                                                                                           
        if self.next_proto == 0x5:
            # VXLAN_GPE_INT or INT_PLT
            int_type = ord(payload[0])
            if int_type == 1 or int_type == 2:
                return VXLAN_GPE_INT
            elif int_type == 3:
                return VXLAN_GPE_INT_PLT
        else:
            return Packet.guess_payload_class(self, payload)
 
bind_layers(UDP, VXLAN_GPE, dport=4790)
bind_layers(VXLAN_GPE, Ether, next_proto=3)
