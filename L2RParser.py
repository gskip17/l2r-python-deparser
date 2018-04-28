from scapy.all import sniff
from scapy.all import *
from itertools import cycle
from l2r_parser_defs import *
from pkt_gmlrr import PktGmlrr

import binascii
import sys


class L2RPktParser:

	def __init__(self):	

		'''
			@self.parse_by_dec:
	
			    Function lookup table. Keys on decimal packet ID of data in.
			    (Only 1 packet type supported thus far)
		
			    Register new parsers here, use 1401 as an example.
	
			    For further extension, keep this dict below all parser definitions..
					
		'''
		self.parse_by_dec = {
			1404 : [ "PktGuildMemberListReadResult" , guild_member_list_read_result ]	
		}

		return


	def parse(self, pkt_id, payload, BUFFER, response_bytes):
		'''
		
			Parser logic:
	
				- check if a parser is available for this packet
				- if there is one, write packet to a tmp file (don't need to just helpful for debugging really)
					change parser_def to use KaiTai.from_bytes rather than KaiTai.from_file and pass in bytes instead
				- parse_by_dec based on packet_id if registered, return to main.
		
		'''	
		if self.parser_available(pkt_id) == False:
			print("No Parser Available for Packet Type: ", pkt_id)
			return

		print("Parser found for ", self.parse_by_dec[pkt_id][0])
		
		self.dump_bin("data/tmp", response_bytes)	
		
		result = self.parse_by_dec[pkt_id][1](payload)
			
		return result


	def dump_bin(self, file_name, data):
		
		try:
			with open(file_name, 'wb')  as f: 
				f.write(data)	
		except Exception as e:
			print("Unable to dump binary payload data - ", e)
			sys.exit(0)
		return	


	########
	#
	#   Check that a parser exists for this packet - checks for DECIMAL value
	#

	def parser_available(self, pkt_id):	
		return True if pkt_id in self.parse_by_dec.keys() else False
			



